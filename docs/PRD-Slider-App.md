# Product Requirements Document: Colorblind Test Image Parameter Explorer

## Overview

### Project Name
Slider App - Interactive Parameter Space Explorer for Dichromacy Research

### Version
1.0

### Date
December 2025

---

## 1. Executive Summary

The Slider App is a specialized research tool designed to help identify colorblind test images that are easily distinguishable for individuals with deuteranomaly/protanomaly (red-green color vision deficiencies) but difficult for individuals with normal trichromatic vision. The application provides real-time interactive controls to explore the parameter space of test image generation, enabling systematic discovery of optimal color combinations and image properties.

### Key Features
- Real-time single image generation with interactive sliders
- RGB controls for foreground and background colors
- Grayscale noise parameters (offset and variance)
- Circle size and variance controls
- Luminance matching utilities
- Optional dichromat simulation preview
- Parameter logging and session recording
- Export successful parameter combinations
- Quick A/B testing workflow

---

## 2. Product Vision

### Mission Statement
To provide an interactive research tool for discovering optimal colorblind test parameters that exploit the perceptual differences between dichromatic and trichromatic vision, enabling personalized assessment and understanding of color vision deficiencies.

### Target Audience

**Primary Users:**
- Parents/guardians testing children with color vision deficiencies
- Researchers studying color perception differences
- Individuals with mild deuteranomaly/protanomaly exploring their vision
- Vision scientists conducting parameter optimization

**Secondary Users:**
- Educational institutions teaching about color vision
- Developers creating accessible color schemes
- Optometrists exploring patient-specific test parameters

### User Needs
- Fast, interactive parameter adjustment with immediate visual feedback
- Systematic exploration of color/noise/pattern parameter space
- Easy logging of successful parameter combinations
- Side-by-side comparison of parameters
- Scientific accuracy in luminance calculations
- Reproducible results for validation
- Simple workflow for two-person testing (normal vs. dichromat)

---

## 3. Success Metrics

### Key Performance Indicators (KPIs)

**Technical Metrics:**
- Image generation latency < 100ms per slider change
- Smooth interaction at 30+ fps
- Accurate luminance matching (|Y_fg - Y_bg| < 0.01)
- Parameter combinations saved per session > 5

**User Experience Metrics:**
- Time to find first successful candidate < 15 minutes
- Successful parameter discovery rate > 70% per session
- User satisfaction with slider responsiveness > 4.5/5.0

**Research Metrics:**
- Reproducibility of successful parameters across sessions
- Correlation with established dichromat simulation models
- Discovery of novel parameter combinations

---

## 4. Scope

### In Scope
- Single-page React application with real-time rendering
- Backend API for image generation (Flask)
- Interactive sliders for all key parameters:
  - Foreground RGB (R, G, B: 0-255)
  - Background RGB (R, G, B: 0-255)
  - Circle mean size (6-40 px)
  - Circle size variance (0-60%)
  - Grayscale noise offset (-0.08 to +0.08)
  - Grayscale noise variance (0-0.25)
  - Pattern density (10-60%)
- Real-time luminance (Y) calculation and display
- Luminance matching helper (auto-adjust to match Y values)
- Parameter preset saving and loading
- Session logging with timestamps
- Export parameter sets as JSON/CSV
- Optional dichromat simulation toggle
- Reset to defaults functionality

### Out of Scope (Version 1.0)
- Multi-image batch generation
- Automated parameter optimization/search algorithms
- User authentication or cloud storage
- Sharing results online
- Mobile application (desktop/tablet only)
- Advanced color space visualizations (LAB, XYZ)
- Statistical analysis dashboards
- Integration with medical records

### Future Considerations (Post-v1.0)
- Automated search using CMA-ES or gradient descent
- Built-in A/B testing workflow with timer
- Heatmaps showing explored parameter space
- Machine learning-based parameter suggestions
- Multiple dichromat simulation models (Machado, Brettel, Viénot)
- Advanced analytics and result visualization
- Collaborative testing mode (remote)
- Integration with eye-tracking devices

---

## 5. User Stories

### Core User Stories

**US-001: Adjust Image Parameters**
- As a researcher, I want to adjust RGB values with sliders so that I can explore color combinations in real-time
- Acceptance Criteria:
  - All parameter sliders respond within 100ms
  - Image updates immediately as sliders move
  - Current parameter values displayed numerically
  - Sliders have appropriate ranges and step sizes

**US-002: Match Luminance**
- As a user, I want to match foreground and background luminance so that I can isolate chromatic differences
- Acceptance Criteria:
  - Luminance (Y) calculated and displayed for FG and BG
  - "Match Luminance" button auto-adjusts to minimize Y difference
  - Visual indicator when luminance is matched (|ΔY| < 0.01)
  - Formula uses proper sRGB linearization

**US-003: Save Successful Parameters**
- As a tester, I want to save parameter combinations that work so that I can review and refine them later
- Acceptance Criteria:
  - "Save Parameters" button with optional note/tag
  - Timestamp recorded automatically
  - List of saved parameters displayed
  - Export saved parameters as JSON or CSV

**US-004: Preview Dichromat View**
- As a user, I want to preview how the image looks to a dichromat so that I can verify chromatic differences
- Acceptance Criteria:
  - Toggle to enable deuteranopia/protanopia simulation
  - Side-by-side or toggle view comparison
  - Simulation uses established algorithm (e.g., Machado et al.)
  - Clear labeling of normal vs. simulated view

**US-005: Reset and Start Fresh**
- As a user, I want to reset all parameters to defaults so that I can start a new exploration session
- Acceptance Criteria:
  - "Reset" button returns all sliders to default values
  - Confirmation dialog prevents accidental resets
  - Default parameters follow recommended starting points
  - Session log remains intact (not cleared)

**US-006: Quick Testing Workflow**
- As a parent testing with my child, I want a simple workflow to test whether they can see the pattern
- Acceptance Criteria:
  - Adjustable parameters generate new image instantly
  - Simple yes/no response recording for both testers
  - Response time tracking (optional)
  - Quick navigation to next parameter variation

---

## 6. Technical Requirements

### 6.1 Frontend (React)

**Component Structure:**
```
SliderApp/
├── ImageDisplay (canvas or img with real-time rendering)
├── ParameterControls
│   ├── ColorSliders (FG/BG RGB)
│   ├── NoiseSliders (offset, variance)
│   ├── PatternSliders (circle size, variance, density)
│   └── LuminanceDisplay (calculated Y values)
├── ActionButtons (Save, Reset, Match Luminance)
├── SavedParametersList
├── DichromatSimulation (optional toggle)
└── SessionLog
```

**State Management:**
- Use React hooks (useState, useEffect) for parameter state
- Debounced image generation requests (optional, if needed)
- Local storage for saved parameters (persistent across sessions)

**Performance:**
- Image generation via API or client-side Canvas rendering
- Optimize for smooth slider interaction (throttle if necessary)
- Lazy loading for saved parameters list

### 6.2 Backend (Flask)

**New Endpoint: `/api/slider/generate`**

**Request:**
```json
{
  "fg_rgb": [150, 120, 140],
  "bg_rgb": [140, 150, 140],
  "circle_mean_size": 20,
  "circle_size_variance": 0.3,
  "noise_offset": 0.0,
  "noise_variance": 0.1,
  "pattern_density": 0.25,
  "simulate_dichromat": false,
  "dichromat_type": "deuteranopia"
}
```

**Response:**
```json
{
  "image_base64": "iVBORw0KGgoAAAANS...",
  "luminance_fg": 0.4521,
  "luminance_bg": 0.4518,
  "luminance_delta": 0.0003
}
```

**Image Generation Algorithm:**
1. Convert sRGB (0-255) to linear RGB (0-1)
2. Calculate luminance using: Y = 0.2126*R + 0.7152*G + 0.0722*B
3. Generate circle pattern (random positions, sizes)
4. Apply grayscale noise (Gaussian or uniform)
5. Optional: Apply dichromat simulation transform
6. Return base64-encoded PNG

**Dichromat Simulation (Optional):**
- Implement Machado et al. (2009) transformation matrices
- Support deuteranopia and protanopia
- Apply to linearized RGB before converting back

### 6.3 Database Schema (Optional for v1.0)

```sql
CREATE TABLE parameter_sessions (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    timestamp DATETIME,
    fg_r INTEGER,
    fg_g INTEGER,
    fg_b INTEGER,
    bg_r INTEGER,
    bg_g INTEGER,
    bg_b INTEGER,
    circle_mean_size REAL,
    circle_size_variance REAL,
    noise_offset REAL,
    noise_variance REAL,
    pattern_density REAL,
    notes TEXT,
    tester_normal_response TEXT,  -- 'yes', 'no', 'maybe'
    tester_dichromat_response TEXT,
    response_time_normal REAL,
    response_time_dichromat REAL
);
```

---

## 7. Parameter Specifications

### 7.1 Slider Ranges and Defaults

| Parameter | Range | Default | Step | Unit |
|-----------|-------|---------|------|------|
| Foreground R | 0-255 | 150 | 1 | integer |
| Foreground G | 0-255 | 120 | 1 | integer |
| Foreground B | 0-255 | 140 | 1 | integer |
| Background R | 0-255 | 140 | 1 | integer |
| Background G | 0-255 | 150 | 1 | integer |
| Background B | 0-255 | 140 | 1 | integer |
| Circle Mean Size | 6-40 | 20 | 0.5 | pixels |
| Circle Size Variance | 0-60 | 30 | 1 | % |
| Noise Offset | -0.08 to +0.08 | 0.0 | 0.01 | normalized |
| Noise Variance | 0-0.25 | 0.08 | 0.01 | normalized |
| Pattern Density | 10-60 | 25 | 1 | % |

### 7.2 Luminance Calculation

**sRGB to Linear RGB Conversion:**
```
For each channel c in {R, G, B}:
  s = c / 255.0
  if s <= 0.04045:
    linear = s / 12.92
  else:
    linear = ((s + 0.055) / 1.055) ^ 2.4
```

**Luminance (Y) Calculation:**
```
Y = 0.2126 * R_linear + 0.7152 * G_linear + 0.0722 * B_linear
```

**Luminance Matching:**
- Target: |Y_fg - Y_bg| < 0.01
- Strategy: Fix R and B, solve for G to match Y
- Formula: G_linear = (Y_target - 0.2126*R_linear - 0.0722*B_linear) / 0.7152
- Then convert back to sRGB

---

## 8. User Interface Mockup

### Layout (Desktop)

```
┌─────────────────────────────────────────────────────────────┐
│  Slider App - Parameter Explorer                     [?][X] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐  ┌──────────────────────────────┐ │
│  │                      │  │  Foreground RGB              │ │
│  │                      │  │  R: [====|====] 150          │ │
│  │   Generated Image    │  │  G: [==|======] 120          │ │
│  │    (400x400px)       │  │  B: [===|=====] 140          │ │
│  │                      │  │  Y: 0.4521                   │ │
│  │                      │  │                              │ │
│  │                      │  │  Background RGB              │ │
│  │                      │  │  R: [===|=====] 140          │ │
│  └──────────────────────┘  │  G: [====|====] 150          │ │
│                            │  B: [===|=====] 140          │ │
│  Normal View / Dichromat   │  Y: 0.4518  ΔY: 0.0003 ✓     │ │
│  [Toggle Simulation]       │                              │ │
│                            │  [Match Luminance]           │ │
│                            │                              │ │
│  ┌──────────────────────┐  │  Circle Parameters           │ │
│  │ Saved Parameters     │  │  Mean Size: [==|==] 20 px    │ │
│  │                      │  │  Variance: [===|==] 30%      │ │
│  │ 1. R165,G110,B140... │  │                              │ │
│  │ 2. R180,G95,B135...  │  │  Noise Parameters            │ │
│  │ 3. R155,G125,B142... │  │  Offset: [====|====] 0.00    │ │
│  │                      │  │  Variance: [==|===] 0.08     │ │
│  │ [Export CSV]         │  │                              │ │
│  └──────────────────────┘  │  Pattern Density             │ │
│                            │  Density: [==|====] 25%      │ │
│  [Save Parameters]         │                              │ │
│  [Reset to Defaults]       │  [Apply Changes]             │ │
│                            └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. Implementation Guidelines

### 9.1 Recommended Color Search Strategy

**Starting Point (Mid-gray neutral):**
- Background: RGB = (145, 145, 145)
- Calculate Y_base = 0.18 (approximately)

**Foreground Sweep:**
- Increase R by 10-40 while decreasing G by 10-40
- Maintain Y ≈ Y_base using luminance formula
- Example candidates:
  - (165, 125, 145) → Y ≈ 0.18
  - (175, 115, 145) → Y ≈ 0.18
  - (155, 135, 145) → Y ≈ 0.18

**Testing Protocol:**
1. Generate image with candidate FG/BG
2. Dichromat viewer attempts to identify pattern
3. Normal viewer attempts to identify pattern
4. If dichromat sees easily AND normal does not → Save parameters
5. If dichromat struggles → increase chromatic contrast (larger R/G shift)
6. If normal sees easily → increase noise variance or circle variance

### 9.2 Noise Tuning

- Start with noise_variance = 0.08 (moderate masking)
- If normal viewer detects pattern easily → increase to 0.12-0.18
- If dichromat viewer struggles → decrease to 0.05-0.08
- Keep noise_offset near 0 to avoid luminance cues

### 9.3 Pattern Tuning

- Smaller circles (10-20px) → harder for everyone
- Larger circles (25-35px) → easier for everyone
- Higher variance (40-50%) → better camouflage for normals
- Lower density (15-20%) → harder pattern recognition

---

## 10. Assumptions and Constraints

### Assumptions
- Users have calibrated displays (standard sRGB consumer monitors)
- Testing occurs in consistent lighting conditions
- Users understand the two-person testing workflow
- Dichromat has mild deuteranomaly or protanomaly (not total dichromacy)
- Users have basic understanding of color theory (RGB, luminance)

### Constraints
- Desktop/tablet only (minimum 1280x800 resolution)
- Modern browser with HTML5 Canvas support
- Image generation limited to 500x500px (performance)
- Single session per browser (no multi-user collaboration)
- No automated optimization in v1.0 (manual exploration only)

### Dependencies
- Python 3.9+ with Pillow and NumPy
- Flask framework for backend
- React 18+ for frontend
- Optional: Machado transformation matrices for dichromat simulation

---

## 11. Risks and Mitigations

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|---------|---------------------|
| Display calibration affects results | High | High | Include calibration check; recommend sRGB mode |
| Slider interaction too slow | Medium | High | Optimize rendering; use Canvas; debounce requests |
| Luminance matching fails edge cases | Medium | Medium | Add manual override; validate formula edge cases |
| Users don't understand luminance concept | Medium | Medium | Add tooltips; provide preset "matched" examples |
| Parameter space too large to explore | High | Medium | Provide guided starting points; suggest sweep patterns |
| Dichromat simulation inaccurate | Medium | High | Use validated transformation; label as "approximate" |

---

## 12. Testing Strategy

### 12.1 Unit Testing
- Luminance calculation accuracy (compare to reference values)
- sRGB linearization edge cases (very dark, very bright)
- Parameter validation (range checking)

### 12.2 Integration Testing
- Image generation API endpoint
- Parameter saving/loading
- Dichromat simulation toggle

### 12.3 User Acceptance Testing
- Test with actual dichromat and normal viewer pairs
- Validate that successful parameters are reproducible
- Confirm slider responsiveness on target hardware
- Verify export functionality (JSON/CSV)

### 12.4 Performance Testing
- Measure image generation latency under various parameters
- Test slider smoothness (frame rate)
- Verify memory usage during extended sessions

---

## 13. Open Questions

1. Should we implement a guided wizard for first-time users?
2. What dichromat simulation algorithm should we use (Machado, Brettel, Viénot)?
3. Should we allow custom image sizes or fix at 500x500px?
4. Do we need a "quick test" mode that randomizes nearby parameters?
5. Should saved parameters include screenshots of generated images?
6. How many saved parameter sets should we support per session?
7. Should we implement undo/redo for parameter changes?
8. Do we need keyboard shortcuts for power users?
9. Should we add a heatmap overlay showing explored parameter space?
10. Is there value in integrating a countdown timer for timed testing?

---

## 14. Success Criteria

The Slider App v1.0 will be considered successful if:

1. Users can generate and view a test image within 5 seconds of loading the app
2. All sliders respond smoothly with < 100ms latency
3. Luminance matching achieves |ΔY| < 0.01 accuracy
4. At least 5 parameter combinations can be saved and exported per session
5. The app enables discovery of at least one "successful" parameter set (dichromat sees, normal doesn't) within 30 minutes of exploration
6. User feedback rates the slider responsiveness as "smooth" or better
7. No critical bugs in core slider/image generation workflow

---

## 15. Approval

This PRD should be reviewed and approved by:
- [ ] Product Owner
- [ ] Technical Lead (Backend)
- [ ] Technical Lead (Frontend)
- [ ] Vision Science Advisor
- [ ] UX Designer

---

## 16. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-07 | Initial | First draft based on new_app_plan.txt |

---

## Appendix A: Recommended Parameter Presets

### Preset 1: Neutral Start (Recommended Default)
```json
{
  "name": "Neutral Baseline",
  "fg_rgb": [150, 120, 140],
  "bg_rgb": [145, 145, 145],
  "circle_mean_size": 20,
  "circle_size_variance": 30,
  "noise_offset": 0.0,
  "noise_variance": 0.08,
  "pattern_density": 25
}
```

### Preset 2: High R, Low G (Deutan Target)
```json
{
  "name": "R-High G-Low",
  "fg_rgb": [175, 115, 145],
  "bg_rgb": [145, 145, 145],
  "circle_mean_size": 18,
  "circle_size_variance": 35,
  "noise_offset": 0.0,
  "noise_variance": 0.12,
  "pattern_density": 22
}
```

### Preset 3: Low R, High G (Deutan Target Alt)
```json
{
  "name": "R-Low G-High",
  "fg_rgb": [125, 165, 145],
  "bg_rgb": [145, 145, 145],
  "circle_mean_size": 22,
  "circle_size_variance": 25,
  "noise_offset": 0.0,
  "noise_variance": 0.10,
  "pattern_density": 28
}
```

### Preset 4: High Noise (Hard Mode)
```json
{
  "name": "High Noise Challenge",
  "fg_rgb": [165, 125, 140],
  "bg_rgb": [145, 145, 145],
  "circle_mean_size": 16,
  "circle_size_variance": 40,
  "noise_offset": 0.0,
  "noise_variance": 0.18,
  "pattern_density": 20
}
```

---

## Appendix B: Reference Formulas

### B.1 Luminance Matching Solver

Given:
- Target luminance: Y_target
- Fixed values: R_fg, B_fg

Solve for G_fg:

```python
def solve_g_for_luminance(r_srgb, b_srgb, y_target):
    # Convert R and B to linear
    r_lin = srgb_to_linear(r_srgb / 255.0)
    b_lin = srgb_to_linear(b_srgb / 255.0)

    # Solve for G_linear
    g_lin = (y_target - 0.2126 * r_lin - 0.0722 * b_lin) / 0.7152

    # Clamp and convert back to sRGB
    g_lin = max(0.0, min(1.0, g_lin))
    g_srgb = linear_to_srgb(g_lin)

    return int(g_srgb * 255)

def srgb_to_linear(s):
    if s <= 0.04045:
        return s / 12.92
    else:
        return ((s + 0.055) / 1.055) ** 2.4

def linear_to_srgb(lin):
    if lin <= 0.0031308:
        return lin * 12.92
    else:
        return 1.055 * (lin ** (1/2.4)) - 0.055
```

### B.2 Dichromat Simulation (Machado et al. 2009)

**Deuteranopia Matrix (simplified):**
```
[0.625,  0.375,  0.0  ]
[0.7,    0.3,    0.0  ]
[0.0,    0.03,   0.97 ]
```

**Protanopia Matrix (simplified):**
```
[0.567,  0.433,  0.0  ]
[0.558,  0.442,  0.0  ]
[0.0,    0.242,  0.758]
```

Apply to linear RGB:
```python
import numpy as np

def simulate_deuteranopia(rgb_linear):
    transform = np.array([
        [0.625, 0.375, 0.0],
        [0.7,   0.3,   0.0],
        [0.0,   0.03,  0.97]
    ])
    return np.dot(transform, rgb_linear)
```

---

## Appendix C: File Structure

```
slider_app/
├── slider_app.py              # Main Flask app entry point
├── config.py                  # Configuration (if reusing existing)
├── routes_slider.py           # API routes for slider app
├── image_generator_slider.py # Image generation logic
├── utils/
│   ├── luminance.py          # Luminance calculation utilities
│   └── dichromat_sim.py      # Dichromat simulation (optional)
└── static/
    └── slider_frontend/       # React app build output
        └── index.html
```

**Frontend:**
```
frontend/slider_app/
├── src/
│   ├── App.js                # Main app component
│   ├── components/
│   │   ├── ImageDisplay.js
│   │   ├── ColorSliders.js
│   │   ├── NoiseSliders.js
│   │   ├── PatternSliders.js
│   │   ├── LuminanceDisplay.js
│   │   ├── SavedParameters.js
│   │   └── DichromatToggle.js
│   ├── hooks/
│   │   └── useImageGenerator.js
│   └── utils/
│       └── luminance.js      # Client-side luminance calc
└── package.json
```
