# Product Requirements Document: Test Design
## Dicrhomat - Scientific Methodology and Test Configuration

### Version
1.0

### Date
December 2025

---

## 1. Overview

This document defines the scientific basis, methodology, and specific configurations for the Dicrhomat dichromism detection test. It ensures the test is grounded in color vision science and provides reliable screening for protanopia, deuteranopia, and tritanopia.

---

## 2. Scientific Background

### 2.1 Color Vision Fundamentals

**Normal Color Vision (Trichromacy):**
- Three types of cone cells in the retina
- S-cones: Sensitive to short wavelengths (blue, ~420-440nm peak)
- M-cones: Sensitive to medium wavelengths (green, ~530-540nm peak)
- L-cones: Sensitive to long wavelengths (red, ~560-580nm peak)
- Brain combines signals to perceive full color spectrum

**Dichromacy (Two-Color Vision):**
- One cone type absent or non-functional
- Results in reduced color discrimination in specific ranges
- Affects approximately 8% of males, <1% of females (for red-green types)

### 2.2 Types of Dichromism

**Protanopia (Red-Blind):**
- Missing or non-functional L-cones (red-sensitive)
- Difficulty distinguishing red from green
- Reds appear darker than to normal vision
- Affects ~1% of males
- Confusion colors: Red/green, blue/purple, yellow/orange

**Deuteranopia (Green-Blind):**
- Missing or non-functional M-cones (green-sensitive)
- Difficulty distinguishing red from green
- Most common form of dichromacy
- Affects ~1% of males
- Confusion colors: Red/green, blue/purple (similar to protanopia but different severity)

**Tritanopia (Blue-Blind):**
- Missing or non-functional S-cones (blue-sensitive)
- Difficulty distinguishing blue from yellow
- Much rarer (<0.01% of population)
- Confusion colors: Blue/green, yellow/violet, blue/gray

### 2.3 Ishihara Test Principle

The Dicrhomat test is inspired by the Ishihara color test (published 1917), which uses:
- **Pseudoisochromatic plates**: Images composed of colored dots
- **Figure-ground separation**: Number formed by dots of one color set, background by another
- **Luminance matching**: Dots have similar brightness (luminance) but different hues
- **Color confusion**: Colors chosen to be confusable for specific dichromacy types

**Key Principle**: If two colors have similar luminance but different hues, a person with dichromacy may not be able to distinguish them if the hues fall within their confusion range.

---

## 3. Test Objectives

### 3.1 Primary Objectives

1. **Screen for dichromism**: Identify individuals likely to have protanopia, deuteranopia, or tritanopia
2. **Type identification**: Determine which specific type of dichromism is present
3. **Confidence assessment**: Provide confidence level in the diagnosis

### 3.2 Secondary Objectives

1. **Consistency**: Produce reliable, repeatable results
2. **Sensitivity**: Minimize false negatives (correctly identify dichromats)
3. **Specificity**: Minimize false positives (correctly identify normal vision)

### 3.3 Non-Objectives

- **Medical diagnosis**: This is a screening tool, not a medical diagnostic test
- **Anomalous trichromacy detection**: Does not distinguish between dichromacy and milder color deficiencies
- **Severity grading**: Does not measure degree of color deficiency
- **Legal certification**: Not intended for occupational health or legal purposes

---

## 4. Test Structure

### 4.1 Overview

- **Total Images**: 10
- **Protanopia Tests**: 3 images (30%)
- **Deuteranopia Tests**: 3 images (30%)
- **Tritanopia Tests**: 3 images (30%)
- **Control Test**: 1 image (10%)

### 4.2 Image Distribution

| Image # | Type | Target Number | Purpose |
|---------|------|---------------|---------|
| 1 | Protanopia | Random | Red-green confusion test |
| 2 | Deuteranopia | Random | Red-green confusion test |
| 3 | Tritanopia | Random | Blue-yellow confusion test |
| 4 | Protanopia | Random | Red-green confusion test |
| 5 | Deuteranopia | Random | Red-green confusion test |
| 6 | Tritanopia | Random | Blue-yellow confusion test |
| 7 | Protanopia | Random | Red-green confusion test |
| 8 | Deuteranopia | Random | Red-green confusion test |
| 9 | Tritanopia | Random | Blue-yellow confusion test |
| 10 | Control | Random | Baseline test (high contrast) |

**Rationale for Distribution:**
- Equal weighting for each dichromism type
- Interleaved order prevents pattern recognition
- Control at end to validate test completion
- 3 samples per type provides statistical confidence

### 4.3 Number Selection

**Available Numbers Per Type:**
- **Protanopia**: 12, 29, 42, 57, 74
- **Deuteranopia**: 8, 15, 35, 63, 88
- **Tritanopia**: 5, 26, 45, 69, 96
- **Control**: 3, 6, 9 (single digits for easy recognition)

**Selection Criteria:**
- Two-digit numbers (easier to embed in dot pattern)
- No repeated digits within same test session
- Avoid similar-looking numbers (68 vs 88, 15 vs 18)
- Random selection from pool for each session

---

## 5. Color Specifications

### 5.1 Color Science Principles

**Luminance Matching:**
- Foreground and background dots must have similar luminance (brightness)
- Prevents detection based on brightness alone
- Calculated using: L = 0.2126*R + 0.7152*G + 0.0722*B (Rec. 709)

**Hue Separation:**
- Colors must be sufficiently separated in hue for normal vision
- Colors must be confusable for target dichromacy type
- Use color confusion lines in CIE color space

### 5.2 Protanopia Test Colors

**Objective**: Distinguish reds from greens (protanopes cannot)

**Background Dots (appear red to normal vision):**
- Base: RGB(210, 80, 80)
- Variations: ±20 in R, ±10 in G/B (randomized per dot)
- Luminance target: ~110

**Foreground Dots (number, appear green to normal vision):**
- Base: RGB(80, 200, 80)
- Variations: ±10 in R/B, ±20 in G (randomized per dot)
- Luminance target: ~110

**To Normal Vision**: Clear red vs green distinction
**To Protanope**: Similar appearance (both appear brownish/grayish), difficult to distinguish

### 5.3 Deuteranopia Test Colors

**Objective**: Distinguish reds from greens (deuteranopes cannot)

**Background Dots (appear green to normal vision):**
- Base: RGB(90, 190, 90)
- Variations: ±10 in R/B, ±20 in G (randomized per dot)
- Luminance target: ~105

**Foreground Dots (number, appear red/orange to normal vision):**
- Base: RGB(200, 90, 70)
- Variations: ±20 in R, ±10 in G/B (randomized per dot)
- Luminance target: ~105

**To Normal Vision**: Clear green vs red/orange distinction
**To Deuteranope**: Similar appearance, difficult to distinguish

### 5.4 Tritanopia Test Colors

**Objective**: Distinguish blues from yellows (tritanopes cannot)

**Background Dots (appear blue to normal vision):**
- Base: RGB(100, 100, 220)
- Variations: ±10 in R/G, ±20 in B (randomized per dot)
- Luminance target: ~100

**Foreground Dots (number, appear yellow to normal vision):**
- Base: RGB(220, 220, 90)
- Variations: ±20 in R/G, ±10 in B (randomized per dot)
- Luminance target: ~100

**To Normal Vision**: Clear blue vs yellow distinction
**To Tritanope**: Similar appearance, difficult to distinguish

### 5.5 Control Test Colors

**Objective**: Easy for all vision types (validates attention and honesty)

**Background Dots (appear light gray):**
- Base: RGB(200, 200, 200)
- Variations: ±15 in all channels (randomized per dot)
- Luminance: ~195

**Foreground Dots (number, appear black):**
- Base: RGB(40, 40, 40)
- Variations: ±10 in all channels (randomized per dot)
- Luminance: ~40

**High Contrast**: 4.9:1 ratio, easily visible to all

---

## 6. Image Generation Specifications

### 6.1 Image Properties

- **Dimensions**: 400 x 400 pixels
- **Format**: PNG (lossless)
- **Color Depth**: 24-bit RGB
- **Background**: White or transparent circle mask
- **Shape**: Circular (resembles traditional Ishihara plates)

### 6.2 Dot Pattern

**Dot Count**: 800-1200 dots per image (randomized)

**Dot Sizes**:
- Small: 10-15px diameter (40% of dots)
- Medium: 15-20px diameter (40% of dots)
- Large: 20-25px diameter (20% of dots)
- Randomized size per dot

**Dot Placement**:
- Random positions within circular boundary (radius 190px, centered at 200, 200)
- Minimum spacing: 5px between dot centers (prevent overlap)
- Poisson disk sampling or rejection sampling for distribution
- Uniform density across circle

**Foreground vs Background Ratio**:
- Foreground dots (number): ~15-20% of total dots
- Background dots: ~80-85% of total dots

### 6.3 Number Rendering

**Font Rendering Approach**:
1. Render target number using bold sans-serif font (e.g., Arial Bold, 180px)
2. Rasterize to binary mask (black and white)
3. Scale and center within circle
4. Use mask to determine which dots are foreground vs background

**Alternative Bitmap Approach**:
- Predefine bitmap patterns for each number (0-99)
- Use bitmap as mask for dot color assignment

**Number Placement**:
- Centered in circle
- Sufficient size to be readable (~150px tall)
- Clear edges with dot density

### 6.4 Randomization

**Seed-Based Generation**:
- Seed: Hash(session_id + image_number)
- Ensures same session gets same images (prevents cheating on reload)
- Different sessions get different images (prevents sharing answers)

**Randomized Elements**:
- Exact dot positions
- Dot sizes
- Color variations (within specified ranges)
- Dot count (within range)

**Non-Randomized Elements**:
- Target number for each image_number
- Base colors
- Overall image structure

### 6.5 Quality Assurance

**Validation Checks**:
- Verify luminance similarity (background vs foreground within ±10%)
- Verify dot count within range
- Verify number is visible to normal vision (contrast check)
- Verify no rendering artifacts

---

## 7. Scoring Methodology

### 7.1 Answer Recording

For each image, record:
- Correct answer (generated number)
- User answer (number 0-99 or null)
- Dichromism type tested
- Timestamp

### 7.2 Correctness Determination

**Exact Match**:
- User answer === Correct answer → Correct
- User answer !== Correct answer → Incorrect
- User answer === null (no number seen) → Incorrect (unless expected for that dichromacy)

**No Partial Credit**: Must match exactly

### 7.3 Analysis Algorithm

**Step 1: Group by Type**

Count errors for each type:
- Protanopia errors: Incorrect answers on protanopia images (max 3)
- Deuteranopia errors: Incorrect answers on deuteranopia images (max 3)
- Tritanopia errors: Incorrect answers on tritanopia images (max 3)
- Control errors: Incorrect answers on control image (max 1)

**Step 2: Validate Test**

If control image is incorrect:
- Flag test as unreliable
- Suggest retaking test
- Do not proceed with analysis

**Step 3: Calculate Error Rates**

- Protanopia error rate = (protanopia errors) / 3
- Deuteranopia error rate = (deuteranopia errors) / 3
- Tritanopia error rate = (tritanopia errors) / 3

**Step 4: Determine Result**

```
IF control incorrect:
  → Unreliable test

ELSE IF all error rates ≤ 0.33 (0-1 error per type):
  → Normal color vision

ELSE IF protanopia error rate ≥ 0.67 AND deuteranopia error rate < 0.67 AND tritanopia error rate < 0.67:
  → Protanopia suspected (High confidence if 100%, Medium if 67%)

ELSE IF deuteranopia error rate ≥ 0.67 AND protanopia error rate < 0.67 AND tritanopia error rate < 0.67:
  → Deuteranopia suspected (High confidence if 100%, Medium if 67%)

ELSE IF tritanopia error rate ≥ 0.67 AND protanopia error rate < 0.67 AND deuteranopia error rate < 0.67:
  → Tritanopia suspected (High confidence if 100%, Medium if 67%)

ELSE IF multiple error rates ≥ 0.67:
  → Multiple deficiencies suspected OR unreliable test (Low confidence)

ELSE:
  → Inconclusive (Mixed pattern, recommend professional testing)
```

### 7.4 Confidence Levels

| Confidence | Criteria | Interpretation |
|------------|----------|----------------|
| High | 100% error rate for one type, 0% for others | Very likely to have specific dichromacy |
| Medium | 67% error rate for one type, ≤33% for others | Likely to have specific dichromacy |
| Low | Mixed error patterns, control passed | Unclear, may have partial deficiency |
| None | Control failed | Test invalid |

### 7.5 Edge Cases

**All Answers Correct**:
- Result: Normal color vision
- Confidence: High

**All Answers Incorrect (including control)**:
- Result: Unreliable test
- Reason: Likely inattention, misunderstanding, or random guessing
- Action: Suggest retaking test

**Random Pattern (e.g., 1 error in each type + control correct)**:
- Result: Inconclusive
- Reason: No clear pattern
- Action: Recommend professional testing

---

## 8. Result Interpretation

### 8.1 Result Categories

**Normal Color Vision:**
- **Display**: "Your color vision appears normal"
- **Explanation**: "You correctly identified the numbers in images designed to test for color blindness. This suggests you have normal color perception."
- **Icon**: Green checkmark
- **Recommendations**: None

**Protanopia Suspected:**
- **Display**: "Possible Protanopia (Red Color Blindness)"
- **Explanation**: "You had difficulty seeing numbers in images designed to detect protanopia. Protanopia is a type of red-green color blindness where red cones are absent or non-functional. People with protanopia may have difficulty distinguishing reds from greens, and reds may appear darker."
- **Icon**: Red/orange alert
- **Recommendations**: "Consider consulting an optometrist or ophthalmologist for comprehensive color vision testing."

**Deuteranopia Suspected:**
- **Display**: "Possible Deuteranopia (Green Color Blindness)"
- **Explanation**: "You had difficulty seeing numbers in images designed to detect deuteranopia. Deuteranopia is the most common type of red-green color blindness where green cones are absent or non-functional. People with deuteranopia may have difficulty distinguishing reds from greens."
- **Icon**: Green/orange alert
- **Recommendations**: "Consider consulting an optometrist or ophthalmologist for comprehensive color vision testing."

**Tritanopia Suspected:**
- **Display**: "Possible Tritanopia (Blue Color Blindness)"
- **Explanation**: "You had difficulty seeing numbers in images designed to detect tritanopia. Tritanopia is a rare type of color blindness where blue cones are absent or non-functional. People with tritanopia may have difficulty distinguishing blues from yellows."
- **Icon**: Blue/yellow alert
- **Recommendations**: "Tritanopia is rare. Please consult an optometrist or ophthalmologist for comprehensive color vision testing to confirm."

**Inconclusive:**
- **Display**: "Inconclusive Results"
- **Explanation**: "Your test results show a mixed pattern that doesn't clearly indicate normal color vision or a specific type of color blindness."
- **Icon**: Gray question mark
- **Recommendations**: "We recommend consulting an eye care professional for a comprehensive color vision assessment. This screening test has limitations and may not capture all types of color vision deficiencies."

**Unreliable Test:**
- **Display**: "Test Results Unreliable"
- **Explanation**: "The control image, which should be visible to all vision types, was answered incorrectly. This may indicate the test was not completed under proper conditions."
- **Icon**: Yellow warning
- **Recommendations**: "Please retake the test in good lighting conditions, ensuring you view each image carefully. If problems persist, consult an eye care professional."

### 8.2 Disclaimers

**Standard Disclaimer (shown on all results):**
"This is a screening tool and not a medical diagnostic test. For a comprehensive evaluation of your color vision, please consult a qualified eye care professional. Results may be affected by screen calibration, lighting conditions, and viewing distance."

---

## 9. Validation and Testing

### 9.1 Algorithm Validation

**Validation Dataset**:
- Test with known dichromats (if available)
- Test with individuals with normal color vision
- Compare results to established Ishihara test results

**Metrics**:
- **Sensitivity**: Percentage of actual dichromats correctly identified
- **Specificity**: Percentage of normal vision individuals correctly identified
- **Positive Predictive Value**: Percentage of positive results that are true positives
- **Negative Predictive Value**: Percentage of negative results that are true negatives

**Targets** (minimum acceptable):
- Sensitivity: ≥ 80%
- Specificity: ≥ 90%

### 9.2 Image Quality Testing

- Generate 100 sample images per type
- Manually review for clarity, contrast, readability
- Verify colors are confusable for target dichromacy (simulate using color blindness filters)

### 9.3 Usability Testing

- Test with 10+ users
- Observe test completion
- Gather feedback on clarity, difficulty, interpretation
- Measure average time per image

### 9.4 Display Variability Testing

- Test on different monitors (LCD, OLED, etc.)
- Test with different brightness settings
- Test with color temperature variations
- Document any significant differences

---

## 10. Limitations

### 10.1 Known Limitations

1. **Display Dependence**: Results depend on screen calibration and color accuracy
2. **Lighting Conditions**: Ambient lighting can affect color perception
3. **Anomalous Trichromacy**: May not detect partial color deficiencies (protanomaly, deuteranomaly, tritanomaly)
4. **Monochromatism**: Does not test for complete color blindness
5. **Severity Grading**: Cannot measure degree of color deficiency
6. **Small Sample Size**: 10 images may not capture all variations
7. **Learning Effects**: Repeated testing may improve scores due to memorization
8. **Attention**: Requires focused attention; distraction can affect results

### 10.2 Mitigations

- Provide clear instructions for viewing conditions (good lighting, proper distance)
- Include disclaimer about screen dependence
- Recommend professional testing for definitive diagnosis
- Randomize images per session to reduce memorization
- Include control image to detect inattention

---

## 11. Ethical Considerations

### 11.1 Privacy

- Minimal data collection
- Anonymous testing option
- Clear privacy policy
- No sharing of results without consent

### 11.2 Non-Discrimination

- Results should not be used for discriminatory purposes
- Emphasize that color blindness is a variation, not a disability for most activities
- Avoid stigmatizing language

### 11.3 Medical Disclaimer

- Clearly state this is NOT a medical diagnosis
- Encourage professional consultation
- Do not provide medical advice

---

## 12. Future Enhancements

### 12.1 Scientific Improvements

- **Adaptive Testing**: Adjust difficulty based on earlier responses
- **Expanded Battery**: More images per type for higher confidence
- **Anomalous Trichromacy Detection**: Add tests for partial color deficiencies
- **Severity Grading**: Quantify degree of deficiency
- **Additional Types**: Test for rare color vision deficiencies

### 12.2 Methodological Improvements

- **Calibration Check**: Include a calibration image to verify display quality
- **Eye Tracking**: Measure viewing patterns (research purposes)
- **Response Time Analysis**: Use reaction time as additional metric
- **Multiple Sessions**: Track consistency across sessions

---

## 13. References and Standards

### 13.1 Scientific References

1. Ishihara, S. (1917). "Tests for Color Blindness"
2. Birch, J. (1997). "Efficiency of the Ishihara test for identifying red-green colour deficiency"
3. Neitz, J., & Neitz, M. (2011). "The genetics of normal and defective color vision"
4. CIE (Commission Internationale de l'Éclairage) standards for color spaces

### 13.2 Color Standards

- sRGB color space (IEC 61966-2-1)
- Rec. 709 luminance calculation
- CIE 1931 color space for color confusion lines

---

## 14. Acceptance Criteria

- [ ] Image generation algorithm produces valid Ishihara-style images
- [ ] Color specifications match target confusion lines for each dichromacy type
- [ ] Luminance matching within ±10% for foreground/background
- [ ] Numbers are clearly visible to normal color vision
- [ ] Numbers are difficult/invisible to target dichromacy type (validated)
- [ ] Scoring algorithm correctly categorizes test results
- [ ] Result interpretations are clear, accurate, and helpful
- [ ] Disclaimers are prominent and appropriate
- [ ] Validation testing shows ≥80% sensitivity and ≥90% specificity
- [ ] Usability testing shows positive user feedback
- [ ] All limitations documented and communicated to users

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-07 | Initial | First draft |
