# ADR-001: Programmatic Image Generation for Test Plates

## Status
Accepted

## Date
2025-12-07

## Context

The Dicromat application requires Ishihara-style test images to detect three types of dichromism (protanopia, deuteranopia, and tritanopia). We needed to decide between two primary approaches for providing these test images to users:

1. **Pre-generated static images**: Create a fixed set of test images during development and serve the same images to all users
2. **Programmatic generation**: Generate test images dynamically for each test session using server-side code

### Key Considerations

**User Security & Test Validity:**
- Pre-generated images could be memorized or shared online, compromising test integrity
- Users could potentially cheat by looking up answers to known images
- Test results need to be reliable for users making important decisions about their color vision

**Technical Requirements:**
- Need 10 test images per session (3 for protanopia, 3 for deuteranopia, 3 for tritanopia, 1 control)
- Images must be scientifically valid and consistent with Ishihara methodology
- Target image generation time: < 2 seconds per image
- Support for 100 concurrent users

**Storage & Scalability:**
- Each image is approximately 400x400px PNG (~50-100KB)
- Static approach: Minimal storage, simple CDN distribution
- Dynamic approach: No image storage needed, but requires CPU resources

**Development Complexity:**
- Static: Simple implementation, requires manual creation or one-time generation
- Dynamic: Complex algorithm development, requires Pillow, NumPy, and careful color science

## Decision

We will implement **programmatic image generation** using Python's Pillow library and NumPy for color calculations. Each test session will receive uniquely generated images based on a seeded random number generator (using session_id + image_number as seed).

### Implementation Details

- **Technology**: Pillow (PIL) 10.0+ for image rendering, NumPy 1.24+ for color calculations
- **Algorithm**: Dot-pattern based generation with randomized dot positions, sizes, and subtle color variations
- **Seeding**: Deterministic randomization using `hash(session_id + image_number)` for reproducibility
- **Color Palettes**: Scientifically validated color pairs for each dichromism type
- **Performance Target**: < 2 seconds per image generation
- **Caching**: Session-scoped only (images cached in browser for session duration)

### Rationale

1. **Prevents Memorization**: Each session receives unique images, preventing answer sharing and memorization
2. **Test Integrity**: Users cannot look up answers online since images are unique
3. **Reproducibility**: Seeded randomization allows regeneration of same image if needed for debugging
4. **Flexibility**: Can easily adjust difficulty, add new test types, or refine algorithms without redistributing assets
5. **Research Value**: Enables future A/B testing and adaptive difficulty algorithms
6. **Storage Efficiency**: Zero storage cost for image assets (only code)

## Consequences

### Positive

- **Enhanced Security**: Test results are more reliable due to inability to cheat
- **Future Flexibility**: Can implement adaptive testing, difficulty adjustments, or new test types with code changes only
- **No Image Asset Management**: No need to version control, CDN-distribute, or manage large image libraries
- **Research Opportunities**: Can log generation parameters for analysis and improvement
- **Customization Potential**: Future ability to generate personalized test variations
- **Cost Efficiency**: Eliminates CDN storage costs for images

### Negative

- **Increased CPU Load**: Each image request requires computational resources
  - *Mitigation*: Optimize algorithm, implement session-scoped caching, monitor performance metrics
- **Latency Risk**: Image generation adds delay to user experience
  - *Mitigation*: Performance target of < 2s, prefetch next image while user answers current one
- **Algorithm Complexity**: Requires careful implementation to ensure scientific validity
  - *Mitigation*: Validate against published Ishihara standards, implement comprehensive testing, consider expert review
- **Server Dependency**: Image generation tied to backend availability (cannot use pure CDN)
  - *Mitigation*: Ensure backend reliability, implement health checks, consider horizontal scaling if needed
- **Testing Complexity**: Need to validate color accuracy and dichromism detection effectiveness
  - *Mitigation*: Implement automated tests for color palettes, manual testing with color-blind volunteers (if possible)

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Image generation exceeds 2s target | Medium | High | Profile and optimize code, use vectorized NumPy operations, consider Cython for hot paths |
| Generated images not scientifically valid | Medium | High | Validate against published standards, conduct user testing, iterate based on feedback |
| Server overload with concurrent users | Low | Medium | Implement rate limiting, monitor CPU usage, horizontal scaling if needed |
| Algorithm produces inconsistent difficulty | Medium | Medium | Extensive testing, standardize parameters, log and analyze user results |

## Alternatives Considered

### 1. Pre-Generated Static Images
**Pros**: Simple, fast delivery via CDN, zero compute cost
**Cons**: Can be memorized/shared, no flexibility, test integrity compromised
**Decision**: Rejected due to security concerns

### 2. Hybrid Approach (Limited Pool with Randomization)
Generate a pool of 100-200 images and randomly select from pool per session
**Pros**: Balanced performance/security, reduces computation
**Cons**: Still vulnerable to memorization over time, storage costs, pool management complexity
**Decision**: Rejected - doesn't fully solve memorization issue

### 3. Client-Side Generation (JavaScript)
**Pros**: Zero server load, instant generation
**Cons**: Vulnerable to inspection/tampering, requires shipping algorithm to client, harder to validate results
**Decision**: Rejected due to security and validation concerns

### 4. Pre-Generated with Watermarking/Encryption
**Pros**: Fast delivery, some tamper protection
**Cons**: Still memorizable, encryption overhead, complex key management
**Decision**: Rejected - overly complex without full benefit

## Implementation Notes

### Color Palette Examples (from PRD-Backend.md)

**Protanopia Detection:**
- Background dots: Red (RGB 255, 100, 100)
- Number dots: Green (RGB 100, 255, 100)
- Variation: ±10% hue/saturation/luminance

**Deuteranopia Detection:**
- Background dots: Green (RGB 100, 255, 100)
- Number dots: Red (RGB 255, 100, 100)
- Variation: ±10% hue/saturation/luminance

**Tritanopia Detection:**
- Background dots: Blue (RGB 100, 100, 255)
- Number dots: Yellow (RGB 255, 255, 100)
- Variation: ±10% hue/saturation/luminance

### Test Configuration Distribution
- Images 1-3: Protanopia detection (numbers from: 12, 29, 42, 57, 74)
- Images 4-6: Deuteranopia detection (numbers from: 8, 15, 35, 63, 88)
- Images 7-9: Tritanopia detection (numbers from: 5, 26, 45, 69, 96)
- Image 10: Control image (high contrast for all vision types)

## Success Metrics

- Image generation time: < 2s (target), < 5s (maximum) at 95th percentile
- User completion rate: > 85% (indicates acceptable performance)
- Test reliability: Consistent results for same user across multiple tests
- Server performance: < 70% CPU usage under normal load (100 concurrent users)

## References

- PRD-Backend.md, Section 5: Image Generation Service
- PRD-Technical-Specs.md, Section 8: Performance Requirements
- Original Ishihara methodology and color science principles
- Pillow documentation: https://pillow.readthedocs.io/
- NumPy documentation: https://numpy.org/doc/

## Reviewers

- [ ] Technical Lead
- [ ] Backend Developer
- [ ] Product Owner
- [ ] Scientific Advisor (color vision expert, if available)

## Related ADRs

- None (first ADR)
- Future ADR: Caching strategy for generated images
- Future ADR: Horizontal scaling approach for image generation

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-07 | Initial | First draft based on PRDs |
