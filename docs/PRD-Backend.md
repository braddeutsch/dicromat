# Product Requirements Document: Backend System
## Dicrhomat - Flask API and Image Generation

### Version
1.0

### Date
December 2025

---

## 1. Overview

The backend system provides RESTful API endpoints for test session management, dynamic image generation, answer recording, and results analysis. Built on Flask with SQLAlchemy ORM, it serves as the data layer and computation engine for the Dicrhomat application.

---

## 2. Technical Architecture

### Stack
- **Framework**: Flask 3.0+
- **ORM**: SQLAlchemy 2.0+
- **Database**: PostgreSQL 14+ (production) / SQLite 3+ (development)
- **Image Processing**: Pillow (PIL) 10.0+
- **Numerical Computing**: NumPy 1.24+
- **API Documentation**: Flask-RESTX or OpenAPI/Swagger
- **CORS**: Flask-CORS

### Project Structure
```
backend/
├── app.py                  # Flask application entry point
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── models/
│   ├── __init__.py
│   ├── test_session.py    # TestSession model
│   └── answer.py          # Answer model
├── routes/
│   ├── __init__.py
│   └── test_routes.py     # API endpoints
├── services/
│   ├── __init__.py
│   ├── image_generator.py # Image generation logic
│   └── results_analyzer.py # Results analysis
├── utils/
│   ├── __init__.py
│   └── helpers.py         # Utility functions
└── tests/
    ├── test_api.py
    ├── test_image_gen.py
    └── test_analysis.py
```

---

## 3. Database Schema

### 3.1 TestSession Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique session identifier |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Session creation time |
| completed_at | TIMESTAMP | NULL | Session completion time |
| user_agent | VARCHAR(500) | NULL | Browser user agent |
| ip_address | VARCHAR(45) | NULL | User IP (optional, privacy consideration) |
| metadata | JSONB | NULL | Optional user demographics |

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `created_at` for cleanup queries

### 3.2 Answer Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique answer identifier |
| session_id | UUID | FOREIGN KEY (test_session.id), NOT NULL | Reference to test session |
| image_number | INTEGER | NOT NULL, CHECK (1-10) | Which image (1-10) |
| correct_answer | INTEGER | NOT NULL, CHECK (0-99) | Correct number in image |
| user_answer | INTEGER | NULL, CHECK (0-99 or NULL) | User's response (NULL = "no number seen") |
| dichromism_type | VARCHAR(20) | NOT NULL | Target type: protanopia, deuteranopia, tritanopia |
| answered_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When answer was submitted |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `(session_id, image_number)`
- FOREIGN KEY on `session_id`

**Constraints:**
- Each session must have exactly 10 answers (enforced at application level)
- Answers must be submitted in order (image_number sequential)

---

## 4. API Endpoints

### 4.1 POST /api/test/start

**Description:** Initialize a new test session

**Request Body:**
```json
{
  "metadata": {
    "age_range": "25-34",
    "gender": "prefer_not_to_say",
    "previous_diagnosis": false
  }
}
```
All fields optional.

**Response (201 Created):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-12-07T10:30:00Z",
  "total_images": 10
}
```

**Error Responses:**
- `500 Internal Server Error`: Database or system error

**Business Logic:**
1. Generate new UUID for session
2. Store session in database with timestamp
3. Return session_id to client

---

### 4.2 GET /api/test/{session_id}/image/{image_number}

**Description:** Retrieve generated test image

**Path Parameters:**
- `session_id` (UUID): Session identifier
- `image_number` (integer): Image number 1-10

**Query Parameters:**
- `format` (optional): Image format (png, jpeg); default: png

**Response (200 OK):**
- Content-Type: image/png or image/jpeg
- Binary image data

**Response Headers:**
```
Content-Type: image/png
Cache-Control: private, max-age=3600
X-Correct-Answer: [ENCRYPTED_VALUE]
X-Dichromism-Type: protanopia
```

**Error Responses:**
- `404 Not Found`: Session ID doesn't exist
- `400 Bad Request`: Invalid image_number (must be 1-10)
- `410 Gone`: Session expired
- `500 Internal Server Error`: Image generation failed

**Business Logic:**
1. Validate session exists and is active
2. Determine which test configuration to use based on image_number
3. Generate image programmatically using image_generator service
4. Embed correct answer in response header (encrypted/hashed)
5. Return image binary data

**Caching Strategy:**
- Images are generated fresh each session (prevents memorization)
- Client-side caching allowed for session duration
- Server-side caching NOT implemented (dynamic generation)

---

### 4.3 POST /api/test/{session_id}/answer

**Description:** Submit user's answer for an image

**Path Parameters:**
- `session_id` (UUID): Session identifier

**Request Body:**
```json
{
  "image_number": 3,
  "user_answer": 42,
  "time_taken_ms": 3500
}
```

Fields:
- `image_number` (required, integer 1-10)
- `user_answer` (optional, integer 0-99 or null): User's answer, null if no number seen
- `time_taken_ms` (optional, integer): Time spent on image

**Response (201 Created):**
```json
{
  "success": true,
  "image_number": 3,
  "next_image": 4,
  "is_complete": false
}
```

If test is complete (image 10 submitted):
```json
{
  "success": true,
  "image_number": 10,
  "next_image": null,
  "is_complete": true,
  "results_available": true
}
```

**Error Responses:**
- `404 Not Found`: Session ID doesn't exist
- `400 Bad Request`: Invalid image_number or duplicate submission
- `409 Conflict`: Image already answered
- `500 Internal Server Error`: Database error

**Business Logic:**
1. Validate session exists
2. Verify image_number hasn't been answered yet
3. Retrieve correct answer from image generation configuration
4. Store answer record in database
5. If image 10, mark session as completed
6. Return next image number or completion status

---

### 4.4 GET /api/test/{session_id}/results

**Description:** Retrieve analyzed test results

**Path Parameters:**
- `session_id` (UUID): Session identifier

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "completed_at": "2025-12-07T10:35:23Z",
  "total_correct": 7,
  "total_images": 10,
  "analysis": {
    "color_vision_status": "deficient",
    "suspected_type": "deuteranopia",
    "confidence": "high",
    "details": {
      "protanopia_errors": 1,
      "deuteranopia_errors": 2,
      "tritanopia_errors": 0,
      "normal_errors": 0
    }
  },
  "interpretation": "Results suggest deuteranopia (green color blindness). You had difficulty seeing numbers in 2 of 3 images designed to detect this condition.",
  "recommendations": "Consider consulting an eye care professional for comprehensive color vision testing.",
  "answers": [
    {
      "image_number": 1,
      "correct_answer": 42,
      "user_answer": 42,
      "is_correct": true,
      "dichromism_type": "protanopia"
    },
    ...
  ]
}
```

**Error Responses:**
- `404 Not Found`: Session ID doesn't exist
- `409 Conflict`: Test not yet completed
- `500 Internal Server Error`: Analysis error

**Business Logic:**
1. Validate session exists and is complete (10 answers submitted)
2. Retrieve all answers for session
3. Analyze pattern of errors using results_analyzer service
4. Calculate confidence scores for each dichromism type
5. Generate human-readable interpretation
6. Return comprehensive results

---

## 5. Image Generation Service

### 5.1 Requirements

**Functional Requirements:**
- Generate 400x400px images with circular boundaries
- Create randomized dot patterns (500-1000 dots per image)
- Embed target number (0-99) using color differentiation
- Support three dichromism types: protanopia, deuteranopia, tritanopia
- Ensure numbers are visible to normal color vision
- Ensure numbers are invisible/difficult for target dichromism type

**Non-Functional Requirements:**
- Generation time < 2 seconds per image
- Consistent difficulty across images
- Randomization prevents memorization
- Reproducible for same session+image_number (seeded randomization)

### 5.2 Algorithm

**High-Level Process:**
1. Initialize random seed based on session_id + image_number
2. Generate random dot positions within circular boundary
3. Assign dot sizes (random within range: 10-25px diameter)
4. Define number shape using font rasterization or bitmap
5. Apply color palette based on dichromism type and number position
6. Render image using Pillow

**Color Palette Strategy:**

For **Protanopia** (red-blind) detection:
- Background dots: Red (e.g., RGB 255, 100, 100)
- Number dots: Green (e.g., RGB 100, 255, 100)
- To normal vision: Distinct colors
- To protanope: Similar luminance, difficult to distinguish

For **Deuteranopia** (green-blind) detection:
- Background dots: Green (e.g., RGB 100, 255, 100)
- Number dots: Red (e.g., RGB 255, 100, 100)
- To normal vision: Distinct colors
- To deuteranope: Similar luminance, difficult to distinguish

For **Tritanopia** (blue-blind) detection:
- Background dots: Blue (e.g., RGB 100, 100, 255)
- Number dots: Yellow (e.g., RGB 255, 255, 100)
- To normal vision: Distinct colors
- To tritanope: Similar luminance, difficult to distinguish

**Color Variations:**
- Add random hue/saturation/luminance variations (±10%) to avoid obvious patterns
- Ensure overall luminance similarity between foreground/background

### 5.3 Test Configuration

**10 Images Distribution:**
- Images 1-3: Protanopia detection (numbers: random from 12, 29, 42, 57, 74)
- Images 4-6: Deuteranopia detection (numbers: random from 8, 15, 35, 63, 88)
- Images 7-9: Tritanopia detection (numbers: random from 5, 26, 45, 69, 96)
- Image 10: Control image (normal color contrast, detects random guessing)

**Difficulty Levels:**
- All images at similar difficulty (moderate)
- Control image should be easy for all vision types

### 5.4 Implementation Interface

```python
class ImageGenerator:
    def generate_test_image(
        self,
        session_id: str,
        image_number: int,
        dichromism_type: str,
        correct_answer: int
    ) -> bytes:
        """
        Generate a test image for dichromism detection.

        Args:
            session_id: Unique session identifier for seeding
            image_number: Image number 1-10
            dichromism_type: 'protanopia', 'deuteranopia', or 'tritanopia'
            correct_answer: Number to embed in image (0-99)

        Returns:
            PNG image as bytes
        """
        pass
```

---

## 6. Results Analysis Service

### 6.1 Analysis Algorithm

**Inputs:**
- List of 10 Answer records for a session

**Processing:**
1. Group answers by dichromism_type
2. Calculate error rate for each type:
   - Protanopia error rate = (incorrect protanopia answers) / (total protanopia images)
   - Deuteranopia error rate = (incorrect deuteranopia answers) / (total deuteranopia images)
   - Tritanopia error rate = (incorrect tritanopia answers) / (total tritanopia images)
3. Check control image (image 10) correctness
4. Apply decision rules

**Decision Rules:**

If control image is incorrect:
- Flag: "Unreliable test - control image failed"

Otherwise:
- **Normal color vision**: All error rates ≤ 33% (max 1 error per type)
- **Protanopia suspected**: Protanopia error rate ≥ 67% (2+ errors), others < 67%
- **Deuteranopia suspected**: Deuteranopia error rate ≥ 67% (2+ errors), others < 67%
- **Tritanopia suspected**: Tritanopia error rate ≥ 67% (2+ errors), others < 67%
- **Multiple types suspected**: Multiple error rates ≥ 67%
- **Inconclusive**: Mixed pattern not fitting above

**Confidence Levels:**
- **High**: 100% error rate for one type, 0% for others
- **Medium**: 67-100% error rate for one type, <67% for others
- **Low**: Mixed error patterns, control passed
- **None**: Unreliable test

### 6.2 Implementation Interface

```python
class ResultsAnalyzer:
    def analyze_session(self, session_id: str) -> dict:
        """
        Analyze test results and determine dichromism type.

        Args:
            session_id: Session to analyze

        Returns:
            {
                'color_vision_status': 'normal' | 'deficient' | 'inconclusive',
                'suspected_type': str | None,
                'confidence': 'none' | 'low' | 'medium' | 'high',
                'details': {...},
                'interpretation': str,
                'recommendations': str
            }
        """
        pass
```

---

## 7. Configuration Management

### 7.1 Environment Variables

```bash
# Flask
FLASK_ENV=development|production
SECRET_KEY=<random-secret-key>

# Database
DATABASE_URL=postgresql://user:pass@localhost/dicrhomat
# or
DATABASE_URL=sqlite:///dicrhomat.db

# CORS
CORS_ORIGINS=http://localhost:3000,https://dicrhomat.example.com

# Session
SESSION_EXPIRY_HOURS=24

# Image Generation
IMAGE_SIZE=400
IMAGE_FORMAT=PNG
RANDOM_SEED_SALT=<random-salt>
```

### 7.2 Configuration Classes

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_EXPIRY_HOURS = 24

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
```

---

## 8. Error Handling

### 8.1 Standard Error Response Format

```json
{
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "The requested session does not exist",
    "details": null
  }
}
```

### 8.2 Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| SESSION_NOT_FOUND | 404 | Session ID doesn't exist |
| SESSION_EXPIRED | 410 | Session older than 24 hours |
| INVALID_IMAGE_NUMBER | 400 | Image number not 1-10 |
| ANSWER_ALREADY_EXISTS | 409 | Image already answered |
| TEST_INCOMPLETE | 409 | Test not finished, results unavailable |
| IMAGE_GENERATION_FAILED | 500 | Error generating image |
| DATABASE_ERROR | 500 | Database operation failed |
| VALIDATION_ERROR | 400 | Request validation failed |

---

## 9. Testing Requirements

### 9.1 Unit Tests

- **Models**: CRUD operations, constraints, relationships
- **Image Generator**: Color palettes, randomization, number embedding
- **Results Analyzer**: Decision rules, edge cases, confidence calculation
- **API Endpoints**: Request/response validation, error handling

### 9.2 Integration Tests

- **API Workflow**: Complete test flow from start to results
- **Database**: Transaction handling, concurrent sessions
- **Image Generation**: Performance, consistency

### 9.3 Performance Tests

- Image generation under load (target: <2s per image, 100 concurrent users)
- Database query performance (target: <100ms for all queries)
- API endpoint response times (target: <500ms excluding image generation)

### 9.4 Test Coverage

- Minimum 80% code coverage
- 100% coverage for results analysis logic
- All error paths tested

---

## 10. Security Considerations

### 10.1 Input Validation

- Validate all UUIDs format
- Sanitize image_number (must be integer 1-10)
- Validate user_answer range (0-99 or null)
- Limit metadata JSON size (max 1KB)

### 10.2 Rate Limiting

- Maximum 5 new sessions per IP per hour
- Maximum 1 request per second per session
- Prevent brute-force answer attempts

### 10.3 Data Privacy

- IP addresses optional (consider GDPR)
- No PII collection without consent
- Session data retention policy (delete after 30 days)
- Secure database connections (SSL)

### 10.4 CORS Configuration

- Whitelist specific origins (no wildcard in production)
- Allow methods: GET, POST, OPTIONS
- Allow headers: Content-Type, Authorization

---

## 11. Deployment Requirements

### 11.1 Infrastructure

- Python 3.9+ runtime
- PostgreSQL 14+ database
- Minimum 512MB RAM
- Minimum 1 vCPU

### 11.2 Dependencies

See `requirements.txt`:
```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
psycopg2-binary==2.9.9
Pillow==10.1.0
numpy==1.24.3
python-dotenv==1.0.0
```

### 11.3 Database Migrations

- Use Alembic for schema migrations
- Initial migration creates test_session and answer tables
- Migration rollback plan required

---

## 12. Monitoring and Logging

### 12.1 Logging

- Log levels: DEBUG (dev), INFO (prod)
- Log all API requests (method, path, status, duration)
- Log image generation time
- Log database errors with stack traces

### 12.2 Metrics

- Track: sessions created, tests completed, completion rate
- Track: average test duration
- Track: API response times (p50, p95, p99)
- Track: image generation times

### 12.3 Alerts

- Alert on: Error rate > 5%
- Alert on: Image generation time > 5s
- Alert on: Database connection failures

---

## 13. API Documentation

### 13.1 OpenAPI/Swagger

- Generate OpenAPI 3.0 specification
- Interactive API documentation at `/api/docs`
- Include example requests/responses
- Document all error codes

---

## 14. Acceptance Criteria

- [ ] All API endpoints implemented and tested
- [ ] Database schema created with migrations
- [ ] Image generation produces valid Ishihara-style images
- [ ] Results analysis correctly identifies dichromism types
- [ ] Unit test coverage ≥ 80%
- [ ] Integration tests pass for complete workflow
- [ ] API documentation generated
- [ ] Error handling for all edge cases
- [ ] CORS configured for frontend origin
- [ ] Environment-based configuration working
- [ ] Logging implemented
- [ ] Session expiry mechanism working

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-07 | Initial | First draft |
