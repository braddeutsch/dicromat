"""API routes for the Slider App - Parameter Explorer."""

from flask import request, jsonify
from . import api_bp
from services.slider_image_generator import SliderImageGenerator
from utils.luminance import calculate_luminance, match_luminance


def validate_rgb(rgb: list, name: str) -> tuple:
    """Validate RGB array and return error response if invalid."""
    if not isinstance(rgb, list) or len(rgb) != 3:
        return None, f'{name} must be an array of 3 integers'
    if not all(isinstance(v, int) and 0 <= v <= 255 for v in rgb):
        return None, f'{name} values must be integers between 0 and 255'
    return rgb, None


@api_bp.route('/slider/generate', methods=['POST'])
def generate_slider_image():
    """Generate a test image with specified parameters."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    
    fg_rgb, err = validate_rgb(data.get('fg_rgb', [150, 120, 140]), 'fg_rgb')
    if err:
        return jsonify({'error': err}), 400
    
    bg_rgb, err = validate_rgb(data.get('bg_rgb', [145, 145, 145]), 'bg_rgb')
    if err:
        return jsonify({'error': err}), 400
    
    circle_mean_size = data.get('circle_mean_size', 20)
    if not isinstance(circle_mean_size, (int, float)) or not 6 <= circle_mean_size <= 40:
        return jsonify({'error': 'circle_mean_size must be between 6 and 40'}), 400
    
    circle_size_variance = data.get('circle_size_variance', 0.30)
    if not isinstance(circle_size_variance, (int, float)) or not 0 <= circle_size_variance <= 0.60:
        return jsonify({'error': 'circle_size_variance must be between 0 and 0.60'}), 400
    
    noise_offset = data.get('noise_offset', 0.0)
    if not isinstance(noise_offset, (int, float)) or not -0.08 <= noise_offset <= 0.08:
        return jsonify({'error': 'noise_offset must be between -0.08 and 0.08'}), 400
    
    noise_variance = data.get('noise_variance', 0.08)
    if not isinstance(noise_variance, (int, float)) or not 0 <= noise_variance <= 0.25:
        return jsonify({'error': 'noise_variance must be between 0 and 0.25'}), 400
    
    pattern_density = data.get('pattern_density', 0.25)
    if not isinstance(pattern_density, (int, float)) or not 0.10 <= pattern_density <= 0.60:
        return jsonify({'error': 'pattern_density must be between 0.10 and 0.60'}), 400
    
    simulate_dichromat = data.get('simulate_dichromat', False)
    dichromat_type = data.get('dichromat_type', 'deuteranopia')
    if dichromat_type not in ('deuteranopia', 'protanopia', 'tritanopia'):
        return jsonify({'error': 'dichromat_type must be deuteranopia, protanopia, or tritanopia'}), 400
    
    seed = data.get('seed')
    
    try:
        generator = SliderImageGenerator()
        result = generator.generate(
            fg_rgb=fg_rgb,
            bg_rgb=bg_rgb,
            circle_mean_size=circle_mean_size,
            circle_size_variance=circle_size_variance,
            noise_offset=noise_offset,
            noise_variance=noise_variance,
            pattern_density=pattern_density,
            simulate_dichromat=simulate_dichromat,
            dichromat_type=dichromat_type,
            seed=seed
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Image generation failed: {str(e)}'}), 500


@api_bp.route('/slider/luminance', methods=['POST'])
def calculate_luminance_endpoint():
    """Calculate luminance for given RGB values."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    
    rgb, err = validate_rgb(data.get('rgb', [128, 128, 128]), 'rgb')
    if err:
        return jsonify({'error': err}), 400
    
    luminance = calculate_luminance(*rgb)
    return jsonify({'luminance': round(luminance, 4)})


@api_bp.route('/slider/match-luminance', methods=['POST'])
def match_luminance_endpoint():
    """Calculate foreground G value to match background luminance."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    
    fg_rgb, err = validate_rgb(data.get('fg_rgb', [150, 120, 140]), 'fg_rgb')
    if err:
        return jsonify({'error': err}), 400
    
    bg_rgb, err = validate_rgb(data.get('bg_rgb', [145, 145, 145]), 'bg_rgb')
    if err:
        return jsonify({'error': err}), 400
    
    try:
        matched_fg = match_luminance(tuple(fg_rgb), tuple(bg_rgb))
        fg_luminance = calculate_luminance(*matched_fg)
        bg_luminance = calculate_luminance(*bg_rgb)
        
        return jsonify({
            'matched_fg_rgb': list(matched_fg),
            'luminance_fg': round(fg_luminance, 4),
            'luminance_bg': round(bg_luminance, 4),
            'luminance_delta': round(abs(fg_luminance - bg_luminance), 4)
        })
    except Exception as e:
        return jsonify({'error': f'Luminance matching failed: {str(e)}'}), 500


@api_bp.route('/slider/presets', methods=['GET'])
def get_presets():
    """Get recommended parameter presets."""
    presets = [
        {
            'name': 'Neutral Baseline',
            'description': 'Recommended starting point for exploration',
            'params': {
                'fg_rgb': [150, 120, 140],
                'bg_rgb': [145, 145, 145],
                'circle_mean_size': 20,
                'circle_size_variance': 0.30,
                'noise_offset': 0.0,
                'noise_variance': 0.08,
                'pattern_density': 0.25
            }
        },
        {
            'name': 'R-High G-Low',
            'description': 'High red, low green - targets deutans',
            'params': {
                'fg_rgb': [175, 115, 145],
                'bg_rgb': [145, 145, 145],
                'circle_mean_size': 18,
                'circle_size_variance': 0.35,
                'noise_offset': 0.0,
                'noise_variance': 0.12,
                'pattern_density': 0.22
            }
        },
        {
            'name': 'R-Low G-High',
            'description': 'Low red, high green - alternative deutan target',
            'params': {
                'fg_rgb': [125, 165, 145],
                'bg_rgb': [145, 145, 145],
                'circle_mean_size': 22,
                'circle_size_variance': 0.25,
                'noise_offset': 0.0,
                'noise_variance': 0.10,
                'pattern_density': 0.28
            }
        },
        {
            'name': 'High Noise Challenge',
            'description': 'Higher noise for harder detection',
            'params': {
                'fg_rgb': [165, 125, 140],
                'bg_rgb': [145, 145, 145],
                'circle_mean_size': 16,
                'circle_size_variance': 0.40,
                'noise_offset': 0.0,
                'noise_variance': 0.18,
                'pattern_density': 0.20
            }
        }
    ]
    return jsonify({'presets': presets})
