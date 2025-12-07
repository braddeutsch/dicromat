from datetime import datetime, timedelta, timezone
from pathlib import Path
from flask import request, jsonify, Response, current_app, send_from_directory
from . import api_bp
from models import db
from models.test_session import TestSession
from models.answer import Answer
from services.image_generator import ImageGenerator
from services.results_analyzer import ResultsAnalyzer
from services.image_selector import ImageSelector


def error_response(code: str, message: str, status: int, details=None):
    return jsonify({
        'error': {
            'code': code,
            'message': message,
            'details': details
        }
    }), status


def get_session_or_error(session_id: str):
    session = db.session.get(TestSession, session_id)
    if not session:
        return None, error_response('SESSION_NOT_FOUND', 'The requested session does not exist', 404)

    expiry_hours = current_app.config.get('SESSION_EXPIRY_HOURS', 24)
    created_at = session.created_at.replace(tzinfo=timezone.utc) if session.created_at.tzinfo is None else session.created_at
    if datetime.now(timezone.utc) - created_at > timedelta(hours=expiry_hours):
        return None, error_response('SESSION_EXPIRED', 'Session has expired', 410)

    return session, None


def get_image_selector():
    """Get ImageSelector instance with metadata."""
    # Determine metadata path relative to backend directory
    backend_dir = Path(__file__).parent.parent
    metadata_path = backend_dir / 'static' / 'test_images' / 'metadata.json'

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Metadata file not found at {metadata_path}. "
            "Please run: python backend/scripts/generate_images.py"
        )

    return ImageSelector(str(metadata_path))


@api_bp.route('/test/start', methods=['POST'])
def start_test():
    try:
        data = request.get_json(silent=True) or {}
        metadata = data.get('metadata')

        if metadata and len(str(metadata)) > 1024:
            return error_response('VALIDATION_ERROR', 'Metadata too large (max 1KB)', 400)

        # Create session first to get session_id
        session = TestSession(
            user_agent=request.headers.get('User-Agent'),
            metadata_json=metadata
        )

        # Generate image mapping using ImageSelector
        try:
            selector = get_image_selector()
            # Get mapping of test image numbers (1-10) to pregenerated image IDs (0-99)
            image_mapping = selector.get_session_image_mapping(session.id)
            # Convert keys to strings for JSON storage
            session.image_mapping = {str(k): v for k, v in image_mapping.items()}
        except FileNotFoundError as e:
            # Fall back to None if images haven't been generated yet
            # This allows backward compatibility with on-the-fly generation
            current_app.logger.warning(f"Pregenerated images not found: {e}")
            session.image_mapping = None

        db.session.add(session)
        db.session.commit()

        return jsonify(session.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return error_response('DATABASE_ERROR', 'Failed to create session', 500, str(e))


@api_bp.route('/test/<session_id>/image/<int:image_number>', methods=['GET'])
def get_image(session_id: str, image_number: int):
    session, err = get_session_or_error(session_id)
    if err:
        return err

    if image_number < 1 or image_number > 10:
        return error_response('INVALID_IMAGE_NUMBER', 'Image number must be between 1 and 10', 400)

    try:
        # Check if session has pregenerated image mapping
        if session.image_mapping:
            # Use pregenerated images
            selector = get_image_selector()

            # Get the pregenerated image ID for this test image number
            image_id = session.image_mapping.get(str(image_number))
            if image_id is None:
                return error_response('IMAGE_MAPPING_ERROR', 'Image mapping not found for this image number', 500)

            # Get image metadata
            image_info = selector.get_image_info(image_id)
            if not image_info:
                return error_response('IMAGE_NOT_FOUND', f'Pregenerated image {image_id} not found', 500)

            # Serve static image file
            backend_dir = Path(__file__).parent.parent
            static_dir = backend_dir / 'static' / 'test_images'

            response = send_from_directory(
                str(static_dir),
                image_info['filename'],
                mimetype='image/png'
            )

            # Set cache headers and metadata headers
            response.headers['Cache-Control'] = 'private, max-age=3600'
            response.headers['ETag'] = image_info['sha256'][:16]  # Use first 16 chars of hash as ETag
            response.headers['X-Dichromism-Type'] = image_info['dichromism_type']
            response.headers['X-Image-ID'] = str(image_id)

            return response

        else:
            # Fall back to on-the-fly generation for backward compatibility
            current_app.logger.info(f"Using on-the-fly generation for session {session_id}")

            generator = ImageGenerator(current_app.config.get('RANDOM_SEED_SALT', 'dicrhomat-salt'))
            config = generator.get_test_config(session_id, image_number)
            image_bytes = generator.generate_test_image(
                session_id,
                image_number,
                config['dichromism_type'],
                config['correct_answer']
            )

            response = Response(image_bytes, mimetype='image/png')
            response.headers['Cache-Control'] = 'private, max-age=3600'
            response.headers['X-Dichromism-Type'] = config['dichromism_type']

            return response

    except Exception as e:
        return error_response('IMAGE_GENERATION_FAILED', 'Failed to serve image', 500, str(e))


@api_bp.route('/test/<session_id>/answer', methods=['POST'])
def submit_answer(session_id: str):
    session, err = get_session_or_error(session_id)
    if err:
        return err

    data = request.get_json()
    if not data:
        return error_response('VALIDATION_ERROR', 'Request body required', 400)

    image_number = data.get('image_number')
    user_answer = data.get('user_answer')

    if image_number is None or not isinstance(image_number, int) or image_number < 1 or image_number > 10:
        return error_response('INVALID_IMAGE_NUMBER', 'Image number must be integer between 1 and 10', 400)

    if user_answer is not None:
        if not isinstance(user_answer, int) or user_answer < 0 or user_answer > 99:
            return error_response('VALIDATION_ERROR', 'User answer must be integer 0-99 or null', 400)

    existing = Answer.query.filter_by(session_id=session_id, image_number=image_number).first()
    if existing:
        return error_response('ANSWER_ALREADY_EXISTS', 'This image has already been answered', 409)

    try:
        # Get correct answer and dichromism type
        if session.image_mapping:
            # Use pregenerated image metadata
            selector = get_image_selector()

            # Get the pregenerated image ID
            image_id = session.image_mapping.get(str(image_number))
            if image_id is None:
                return error_response('IMAGE_MAPPING_ERROR', 'Image mapping not found for this image number', 500)

            # Get image metadata
            image_info = selector.get_image_info(image_id)
            if not image_info:
                return error_response('IMAGE_NOT_FOUND', f'Pregenerated image {image_id} not found', 500)

            correct_answer = image_info['correct_answer']
            dichromism_type = image_info['dichromism_type']

        else:
            # Fall back to on-the-fly generation for backward compatibility
            generator = ImageGenerator(current_app.config.get('RANDOM_SEED_SALT', 'dicrhomat-salt'))
            config = generator.get_test_config(session_id, image_number)
            correct_answer = config['correct_answer']
            dichromism_type = config['dichromism_type']

        answer = Answer(
            session_id=session_id,
            image_number=image_number,
            correct_answer=correct_answer,
            user_answer=user_answer,
            dichromism_type=dichromism_type
        )

        db.session.add(answer)

        is_complete = False
        if image_number == 10:
            session.completed_at = datetime.now(timezone.utc)
            is_complete = True

        db.session.commit()

        return jsonify({
            'success': True,
            'image_number': image_number,
            'next_image': None if image_number == 10 else image_number + 1,
            'is_complete': is_complete,
            'results_available': is_complete
        }), 201

    except Exception as e:
        db.session.rollback()
        return error_response('DATABASE_ERROR', 'Failed to save answer', 500, str(e))


@api_bp.route('/test/<session_id>/results', methods=['GET'])
def get_results(session_id: str):
    session, err = get_session_or_error(session_id)
    if err:
        return err
    
    answers = Answer.query.filter_by(session_id=session_id).order_by(Answer.image_number).all()
    
    if len(answers) < 10:
        return error_response('TEST_INCOMPLETE', 'Test not yet completed', 409)
    
    try:
        analyzer = ResultsAnalyzer()
        analysis = analyzer.analyze_session(answers)
        
        total_correct = sum(1 for a in answers if a.user_answer == a.correct_answer)
        
        return jsonify({
            'session_id': session_id,
            'completed_at': session.completed_at.isoformat() + 'Z' if session.completed_at else None,
            'total_correct': total_correct,
            'total_images': 10,
            'analysis': {
                'color_vision_status': analysis['color_vision_status'],
                'suspected_type': analysis['suspected_type'],
                'confidence': analysis['confidence'],
                'details': analysis['details']
            },
            'interpretation': analysis['interpretation'],
            'recommendations': analysis['recommendations'],
            'answers': [a.to_dict() for a in answers]
        })
    
    except Exception as e:
        return error_response('DATABASE_ERROR', 'Failed to analyze results', 500, str(e))
