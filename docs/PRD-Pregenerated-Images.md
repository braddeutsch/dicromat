# Product Requirements Document: Pre-Generated Image System
## Dicrhomat - Static Image Asset Generation

### Version
1.0

### Date
December 2025

---

## 1. Overview

This document outlines the transition from on-the-fly programmatic image generation to a pre-generated static image asset system. The system will generate 100 test images offline and serve them as static assets, replacing the current dynamic generation approach.

### Context

The current implementation (as defined in ADR-001) uses programmatic image generation with seeded randomization to create unique images per session. This PRD proposes an alternative approach using pre-generated images to improve performance and reduce server-side computational load.

---

## 2. Motivation

### Problems with Current Approach

1. **Server Load**: Each image request triggers CPU-intensive image generation (Pillow + NumPy operations)
2. **Latency**: 2-second generation time per image adds delay to user experience
3. **Scalability**: Under high concurrent load, image generation becomes a bottleneck
4. **Resource Costs**: Requires computational resources on every request

### Benefits of Pre-Generated Approach

1. **Performance**: Static file serving is near-instantaneous (<100ms vs 2s)
2. **Scalability**: Can leverage CDN for global distribution
3. **Cost Reduction**: Minimal server computation, standard static file hosting
4. **Reliability**: Eliminates risk of generation failures during tests
5. **Simplified Architecture**: Removes image generation service from critical path

### Trade-offs

| Aspect | On-the-Fly Generation | Pre-Generated Images |
|--------|----------------------|---------------------|
| Performance | ~2s per image | <100ms per image |
| Test Security | Unique per session | Shared pool (100 images) |
| Flexibility | Algorithm changes instant | Requires regeneration |
| Storage | 0 bytes | ~5-10 MB (100 images) |
| Server Load | High CPU | Negligible |
| Scalability | Limited by CPU | High (CDN-ready) |

---

## 3. Requirements

### 3.1 Functional Requirements

**FR-1: Image Generation Script**
- Create a standalone Python script to generate 100 test images
- Each image must follow existing Ishihara-style specifications
- Output images to a dedicated asset directory
- Generate metadata file describing each image

**FR-2: Image Distribution**
- 30 images for Protanopia detection (image numbers 0-29)
- 30 images for Deuteranopia detection (image numbers 30-59)
- 30 images for Tritanopia detection (image numbers 60-89)
- 10 control images (image numbers 90-99)

**FR-3: Metadata Schema**
- For each image, store:
  - Image filename
  - Correct answer (0-99)
  - Dichromism type (protanopia, deuteranopia, tritanopia, control)
  - Difficulty level (easy, medium, hard)
  - Generation timestamp
  - Image hash (for integrity verification)

**FR-4: Image Serving**
- Serve images as static assets via Flask static file serving
- Support standard HTTP caching headers
- Maintain same API endpoint structure for backward compatibility

**FR-5: Test Session Image Selection**
- Each test session randomly selects 10 images from the pool:
  - 3 protanopia images (from images 0-29)
  - 3 deuteranopia images (from images 30-59)
  - 3 tritanopia images (from images 60-89)
  - 1 control image (from images 90-99)
- Selection is seeded by session_id for reproducibility
- Same session always receives same images

### 3.2 Non-Functional Requirements

**NFR-1: Performance**
- Image serving response time < 100ms (p95)
- Generation script completes in < 5 minutes for all 100 images
- Supports 1000+ concurrent users without degradation

**NFR-2: Quality**
- All images must be valid 400x400px PNG files
- File size < 150KB per image
- Images must pass visual quality validation

**NFR-3: Maintainability**
- Generation script well-documented for future regeneration
- Easy to adjust number of images or distribution
- Metadata format versioned and documented

---

## 4. Technical Design

### 4.1 Image Generation Script

**Location**: `backend/scripts/generate_images.py`

**Command-line Interface**:
```bash
python backend/scripts/generate_images.py \
  --output-dir backend/static/test_images \
  --count 100 \
  --format png \
  --seed <random-seed>
```

**Options**:
- `--output-dir`: Directory for generated images (default: `backend/static/test_images`)
- `--count`: Number of images to generate (default: 100)
- `--format`: Image format (png, jpeg; default: png)
- `--seed`: Random seed for reproducibility (default: current timestamp)
- `--metadata-file`: Metadata output path (default: `backend/static/test_images/metadata.json`)

**Implementation Outline**:
```python
#!/usr/bin/env python3
"""
Generate pre-computed test images for Dicrhomat application.
"""

import argparse
import json
import hashlib
from pathlib import Path
from datetime import datetime
from services.image_generator import ImageGenerator

def main():
    parser = argparse.ArgumentParser(description='Generate test images')
    parser.add_argument('--output-dir', default='backend/static/test_images')
    parser.add_argument('--count', type=int, default=100)
    parser.add_argument('--format', default='png', choices=['png', 'jpeg'])
    parser.add_argument('--seed', default=None)
    args = parser.parse_args()

    # Initialize generator
    generator = ImageGenerator(seed_salt=args.seed or str(datetime.now()))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        'version': '1.0',
        'generated_at': datetime.utcnow().isoformat(),
        'total_images': args.count,
        'seed': args.seed,
        'images': []
    }

    # Generate images by type
    for i in range(args.count):
        # Determine type and answer
        if i < 30:
            dichromism_type = 'protanopia'
            correct_answer = generator.get_random_answer(i, range(10, 90))
        elif i < 60:
            dichromism_type = 'deuteranopia'
            correct_answer = generator.get_random_answer(i, range(10, 90))
        elif i < 90:
            dichromism_type = 'tritanopia'
            correct_answer = generator.get_random_answer(i, range(10, 90))
        else:
            dichromism_type = 'control'
            correct_answer = generator.get_random_answer(i, range(10, 90))

        # Generate image
        image_bytes = generator.generate_test_image(
            session_id='pregenerated',
            image_number=i,
            dichromism_type=dichromism_type,
            correct_answer=correct_answer
        )

        # Save image
        filename = f'image_{i:03d}.{args.format}'
        filepath = output_dir / filename
        filepath.write_bytes(image_bytes)

        # Calculate hash
        image_hash = hashlib.sha256(image_bytes).hexdigest()

        # Store metadata
        metadata['images'].append({
            'id': i,
            'filename': filename,
            'correct_answer': correct_answer,
            'dichromism_type': dichromism_type,
            'difficulty': 'medium',  # Could be parameterized
            'sha256': image_hash
        })

        print(f'Generated {filename} ({dichromism_type}, answer: {correct_answer})')

    # Write metadata
    metadata_path = output_dir / 'metadata.json'
    metadata_path.write_text(json.dumps(metadata, indent=2))

    print(f'\nSuccessfully generated {args.count} images')
    print(f'Output directory: {output_dir}')
    print(f'Metadata file: {metadata_path}')

if __name__ == '__main__':
    main()
```

### 4.2 Metadata File Format

**Location**: `backend/static/test_images/metadata.json`

**Schema**:
```json
{
  "version": "1.0",
  "generated_at": "2025-12-07T10:00:00Z",
  "total_images": 100,
  "seed": "random-seed-value",
  "images": [
    {
      "id": 0,
      "filename": "image_000.png",
      "correct_answer": 42,
      "dichromism_type": "protanopia",
      "difficulty": "medium",
      "sha256": "abc123..."
    },
    ...
  ]
}
```

### 4.3 Directory Structure

```
backend/
├── static/
│   └── test_images/
│       ├── metadata.json          # Image metadata
│       ├── image_000.png          # Protanopia images (0-29)
│       ├── image_001.png
│       ├── ...
│       ├── image_029.png
│       ├── image_030.png          # Deuteranopia images (30-59)
│       ├── ...
│       ├── image_059.png
│       ├── image_060.png          # Tritanopia images (60-89)
│       ├── ...
│       ├── image_089.png
│       ├── image_090.png          # Control images (90-99)
│       ├── ...
│       └── image_099.png
└── scripts/
    └── generate_images.py         # Generation script
```

### 4.4 API Changes

**Modified Endpoint**: `GET /api/test/{session_id}/image/{image_number}`

**Current Behavior**: Generates image on-the-fly

**New Behavior**:
1. Determine which pre-generated image to serve based on session selection
2. Serve static image file from `backend/static/test_images/`
3. Return metadata from in-memory metadata cache

**Implementation Changes**:

**Before** (`backend/routes/test_routes.py`):
```python
@api_bp.route('/test/<session_id>/image/<int:image_number>', methods=['GET'])
def get_image(session_id: str, image_number: int):
    # Validate session
    generator = ImageGenerator(...)
    config = generator.get_test_config(session_id, image_number)

    # Generate image on-the-fly
    image_bytes = generator.generate_test_image(...)

    return Response(image_bytes, mimetype='image/png')
```

**After**:
```python
@api_bp.route('/test/<session_id>/image/<int:image_number>', methods=['GET'])
def get_image(session_id: str, image_number: int):
    # Validate session
    session = get_session_or_404(session_id)

    # Get pre-selected image for this session and image number
    image_mapping = get_session_image_mapping(session_id)
    pregenerated_image_id = image_mapping[image_number]

    # Load metadata
    metadata = load_image_metadata()
    image_info = metadata['images'][pregenerated_image_id]

    # Serve static file
    return send_from_directory(
        'static/test_images',
        image_info['filename'],
        mimetype='image/png',
        max_age=3600,
        etag=image_info['sha256']
    )
```

### 4.5 Image Selection Service

**New Service**: `backend/services/image_selector.py`

**Purpose**: Deterministically map session_id to a set of 10 images from the pool of 100

```python
import random
import json
from pathlib import Path
from typing import Dict, List

class ImageSelector:
    def __init__(self, metadata_path: str):
        """Initialize with metadata file."""
        self.metadata = json.loads(Path(metadata_path).read_text())

        # Organize images by type
        self.protanopia_images = [
            img for img in self.metadata['images']
            if img['dichromism_type'] == 'protanopia'
        ]
        self.deuteranopia_images = [
            img for img in self.metadata['images']
            if img['dichromism_type'] == 'deuteranopia'
        ]
        self.tritanopia_images = [
            img for img in self.metadata['images']
            if img['dichromism_type'] == 'tritanopia'
        ]
        self.control_images = [
            img for img in self.metadata['images']
            if img['dichromism_type'] == 'control'
        ]

    def get_session_images(self, session_id: str) -> Dict[int, int]:
        """
        Get mapping of test image_number (1-10) to pregenerated image_id.

        Returns:
            {1: 5, 2: 12, 3: 7, ...}  # image_number -> pregenerated_image_id
        """
        # Seed random with session_id for reproducibility
        rng = random.Random(session_id)

        # Select images
        selected_protanopia = rng.sample(self.protanopia_images, 3)
        selected_deuteranopia = rng.sample(self.deuteranopia_images, 3)
        selected_tritanopia = rng.sample(self.tritanopia_images, 3)
        selected_control = rng.sample(self.control_images, 1)

        # Map to test image numbers (1-10)
        mapping = {}
        mapping[1] = selected_protanopia[0]['id']
        mapping[2] = selected_protanopia[1]['id']
        mapping[3] = selected_protanopia[2]['id']
        mapping[4] = selected_deuteranopia[0]['id']
        mapping[5] = selected_deuteranopia[1]['id']
        mapping[6] = selected_deuteranopia[2]['id']
        mapping[7] = selected_tritanopia[0]['id']
        mapping[8] = selected_tritanopia[1]['id']
        mapping[9] = selected_tritanopia[2]['id']
        mapping[10] = selected_control[0]['id']

        return mapping

    def get_image_info(self, image_id: int) -> dict:
        """Get metadata for a specific image."""
        return self.metadata['images'][image_id]
```

### 4.6 Session Data Model Changes

**Modified**: `backend/models/test_session.py`

**New Field**: Store image selection mapping in session

```python
class TestSession(db.Model):
    __tablename__ = 'test_session'

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    metadata = db.Column(db.JSON, nullable=True)

    # NEW: Store image mapping
    image_mapping = db.Column(db.JSON, nullable=False)
    # Format: {"1": 5, "2": 12, ...}  # Keys are strings in JSON
```

**Migration Required**: Add `image_mapping` column to existing sessions table

---

## 5. Implementation Plan

### Phase 1: Script Development (Week 1)

**Tasks**:
- [ ] Create `backend/scripts/generate_images.py`
- [ ] Reuse existing `ImageGenerator` class
- [ ] Implement metadata generation
- [ ] Add command-line argument parsing
- [ ] Test script locally with 10 images

**Deliverables**:
- Working generation script
- Sample metadata.json
- Documentation on running the script

### Phase 2: Image Generation (Week 1)

**Tasks**:
- [ ] Run script to generate 100 production images
- [ ] Validate all images visually (spot check 20%)
- [ ] Verify metadata integrity
- [ ] Check file sizes and quality
- [ ] Commit images to git or store in asset repository

**Deliverables**:
- 100 production-quality test images
- Complete metadata.json
- Validation report

### Phase 3: Backend Integration (Week 2)

**Tasks**:
- [ ] Create `ImageSelector` service
- [ ] Add `image_mapping` field to `TestSession` model
- [ ] Update `/test/start` endpoint to generate image mapping
- [ ] Update `/test/{session_id}/image/{image_number}` to serve static images
- [ ] Update `Answer` model logic to use metadata for correct answers
- [ ] Remove or deprecate dynamic `ImageGenerator` usage in request path

**Deliverables**:
- Modified API endpoints
- Updated database schema
- Migration scripts

### Phase 4: Testing (Week 2)

**Tasks**:
- [ ] Unit tests for `ImageSelector`
- [ ] Integration tests for image serving
- [ ] Load tests (1000 concurrent users)
- [ ] Verify session reproducibility
- [ ] Test cache headers and CDN compatibility

**Deliverables**:
- Test suite passing
- Performance benchmark results
- Load testing report

### Phase 5: Deployment (Week 3)

**Tasks**:
- [ ] Deploy images to static hosting or CDN
- [ ] Run database migration
- [ ] Deploy updated backend code
- [ ] Monitor performance and error rates
- [ ] Validate end-to-end test flow

**Deliverables**:
- Production deployment
- Monitoring dashboard
- Rollback plan documented

---

## 6. Testing Requirements

### 6.1 Script Testing

- **Test 1**: Script generates exactly 100 images
- **Test 2**: Metadata contains all required fields
- **Test 3**: All images are valid PNG files
- **Test 4**: File sizes are reasonable (<150KB)
- **Test 5**: Same seed produces identical images
- **Test 6**: Different seeds produce different images

### 6.2 API Testing

- **Test 7**: Session creation includes image mapping
- **Test 8**: Same session_id always returns same images
- **Test 9**: Different sessions receive different image combinations
- **Test 10**: Image serving returns correct HTTP status codes
- **Test 11**: Cache headers are set correctly
- **Test 12**: Results analysis works with pre-generated images

### 6.3 Performance Testing

- **Test 13**: Image serving <100ms response time (p95)
- **Test 14**: 1000 concurrent users supported
- **Test 15**: CDN integration works correctly

---

## 7. Security Considerations

### 7.1 Image Pool Size

**Risk**: With only 100 images, users could potentially memorize answers

**Mitigation**:
- 100 images provides 30C3 × 30C3 × 30C3 × 10C1 = 234,256,200 unique test combinations
- Probability of same test in two sessions: extremely low
- Can increase pool to 200 or 500 images if needed

### 7.2 Metadata Exposure

**Risk**: Metadata file exposes correct answers

**Mitigation**:
- Do not serve `metadata.json` as static file
- Load metadata server-side only
- Include in `.gitignore` if answers should remain private
- Or encrypt answers in metadata file

### 7.3 Image Integrity

**Risk**: Images could be tampered with

**Mitigation**:
- Store SHA-256 hashes in metadata
- Verify hash on application startup
- Use read-only filesystem in production

---

## 8. Migration Strategy

### 8.1 Backward Compatibility

**Option A: Big Bang**
- Deploy all changes at once
- All new sessions use pre-generated images
- In-flight sessions may break

**Option B: Gradual Migration**
- Support both systems simultaneously
- Flag in session determines which system to use
- Migrate over time, deprecate old system

**Recommendation**: Option B (Gradual Migration)

### 8.2 Rollback Plan

If pre-generated system fails:
1. Re-enable dynamic generation code path
2. Update session creation to skip image mapping
3. Serve images dynamically for new sessions
4. Monitor and investigate issues

---

## 9. Documentation Requirements

### 9.1 User Documentation

- No user-facing changes (API remains same)

### 9.2 Developer Documentation

- **README**: How to regenerate images
- **Script Usage**: Command-line options for `generate_images.py`
- **Architecture Decision Record**: Document why we switched approaches
- **Migration Guide**: For deploying this change

### 9.3 Operations Documentation

- **Deployment Guide**: How to deploy images and code changes
- **Monitoring**: What metrics to track
- **Troubleshooting**: Common issues and solutions

---

## 10. Success Metrics

### 10.1 Performance Improvements

- Image serving latency reduced from ~2000ms to <100ms (95th percentile)
- Server CPU usage reduced by >50% under load
- 99.9% uptime for image serving

### 10.2 Quality Metrics

- Test completion rate remains ≥85%
- Results accuracy comparable to dynamic generation
- Zero image serving errors

### 10.3 Operational Metrics

- Deployment successful with zero downtime
- Rollback not required
- No increase in support tickets

---

## 11. Risks and Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Image quality issues | Low | High | Thorough visual validation before deployment |
| Test memorization | Low | Medium | 100 images provides sufficient variety |
| Storage costs | Low | Low | 100 images ~10MB, negligible cost |
| CDN sync delays | Medium | Low | Pre-warm CDN before deployment |
| Migration bugs | Medium | High | Gradual rollout, comprehensive testing |
| Lost reproducibility | Low | Medium | Session-seeded selection maintains reproducibility |

---

## 12. Future Enhancements

### 12.1 Dynamic Pool Expansion

- Generate 500-1000 images for greater variety
- Periodically refresh image pool (e.g., quarterly)

### 12.2 Difficulty Levels

- Generate images at multiple difficulty levels
- Adaptive testing selects difficulty based on user performance

### 12.3 CDN Optimization

- Distribute images via global CDN (CloudFront, Cloudflare)
- Edge caching for <50ms latency worldwide

### 12.4 Image Versioning

- Support multiple versions of image sets
- A/B test different generation algorithms

---

## 13. Open Questions

1. Should we store images in Git or external storage (S3, CDN)?
2. What is the optimal number of images (100, 200, 500)?
3. Should we encrypt correct answers in metadata.json?
4. Do we need different image sets for different regions/languages?
5. Should we implement image rotation/refresh on a schedule?

---

## 14. Acceptance Criteria

- [ ] Generation script creates 100 valid images with metadata
- [ ] All images pass visual quality inspection
- [ ] `ImageSelector` service correctly maps sessions to images
- [ ] API endpoints serve pre-generated images with <100ms latency
- [ ] Database migration adds `image_mapping` field
- [ ] Same session_id consistently returns same images
- [ ] Test completion flow works end-to-end
- [ ] Results analysis produces correct dichromism detection
- [ ] Performance tests show >90% latency reduction
- [ ] Load tests support 1000+ concurrent users
- [ ] Documentation completed (script usage, deployment guide)
- [ ] Rollback plan tested and documented

---

## 15. Approval

This PRD should be reviewed and approved by:

- [ ] Product Owner
- [ ] Backend Tech Lead
- [ ] DevOps Engineer
- [ ] QA Lead

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-07 | Initial | First draft |
