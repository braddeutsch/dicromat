# Product Requirements Document: Frontend System
## Dicrhomat - React User Interface

### Version
1.0

### Date
December 2025

---

## 1. Overview

The frontend provides an intuitive, accessible web interface for users to complete the dichromism color blindness test. Built with React, it manages test flow, displays images, collects responses, and presents results in a clear, user-friendly manner.

---

## 2. Technical Architecture

### Stack
- **Framework**: React 18+
- **Build Tool**: Vite or Create React App
- **Routing**: React Router 6+
- **State Management**: React Context API or Zustand
- **HTTP Client**: Axios or Fetch API
- **Styling**: CSS Modules or Styled Components
- **UI Components**: Custom components (no heavy UI library for v1.0)
- **TypeScript**: Preferred for type safety

### Project Structure
```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── App.tsx              # Main app component
│   ├── index.tsx            # Entry point
│   ├── routes/
│   │   └── AppRoutes.tsx    # Route definitions
│   ├── pages/
│   │   ├── WelcomePage.tsx  # Landing/instructions
│   │   ├── TestPage.tsx     # Test interface
│   │   └── ResultsPage.tsx  # Results display
│   ├── components/
│   │   ├── TestImage.tsx    # Image display
│   │   ├── AnswerInput.tsx  # Number input
│   │   ├── ProgressBar.tsx  # Progress indicator
│   │   ├── ResultsChart.tsx # Results visualization
│   │   └── Button.tsx       # Reusable button
│   ├── context/
│   │   └── TestContext.tsx  # Global test state
│   ├── services/
│   │   └── api.ts           # API client
│   ├── types/
│   │   └── index.ts         # TypeScript types
│   ├── styles/
│   │   ├── global.css       # Global styles
│   │   └── variables.css    # CSS variables
│   └── utils/
│       └── helpers.ts       # Utility functions
├── package.json
└── vite.config.ts / tsconfig.json
```

---

## 3. Application Routes

### 3.1 Route Definitions

| Route | Component | Description | Auth Required |
|-------|-----------|-------------|---------------|
| `/` | WelcomePage | Landing page with instructions | No |
| `/test/:sessionId` | TestPage | Test interface | Session ID |
| `/results/:sessionId` | ResultsPage | Results display | Completed session |
| `*` | NotFound | 404 page | No |

### 3.2 Navigation Flow

```
WelcomePage
    ↓ (Start Test button clicked)
    ↓ (API: POST /api/test/start)
    ↓
TestPage (image 1/10)
    ↓ (Submit answer)
    ↓ (API: POST /api/test/{sessionId}/answer)
    ↓
TestPage (image 2/10)
    ...
    ↓
TestPage (image 10/10)
    ↓ (Submit final answer)
    ↓ (API: POST /api/test/{sessionId}/answer)
    ↓ (Auto-redirect)
    ↓
ResultsPage
    ↓ (API: GET /api/test/{sessionId}/results)
```

---

## 4. Page Specifications

### 4.1 WelcomePage

**Purpose**: Introduce the test, provide instructions, and collect optional metadata

**Layout:**
```
+------------------------------------------+
|  DICROMAT                                |
|  Color Vision Test                       |
+------------------------------------------+
|                                          |
|  [Icon/Illustration]                     |
|                                          |
|  What is this test?                      |
|  This test screens for dichromism, a     |
|  type of color blindness affecting...    |
|                                          |
|  Instructions:                           |
|  • You will see 10 images with numbers   |
|  • Enter the number you see (0-99)       |
|  • If you don't see a number, select     |
|    "No number visible"                   |
|  • Test takes approximately 3-5 minutes  |
|                                          |
|  [Optional: Demographics form]           |
|                                          |
|  [Start Test Button]                     |
|                                          |
|  Disclaimer: This is a screening tool... |
+------------------------------------------+
```

**Components:**
- Header with app name
- Informational text sections
- Optional metadata form (collapsible)
  - Age range dropdown
  - Gender dropdown
  - Previous diagnosis checkbox
- Start button (primary CTA)
- Disclaimer text (small, gray)

**State:**
- Form data (age_range, gender, previous_diagnosis)
- Loading state during API call

**Interactions:**
1. User reads instructions
2. (Optional) User fills out metadata form
3. User clicks "Start Test"
4. Loading indicator appears
5. API call: POST /api/test/start with metadata
6. On success: Navigate to /test/{sessionId}
7. On error: Show error message

**Acceptance Criteria:**
- [ ] Clear, readable instructions
- [ ] Metadata form is optional (can be skipped)
- [ ] Start button disabled during API call
- [ ] Loading state visible during API call
- [ ] Error handling for failed API call
- [ ] Mobile-responsive layout

---

### 4.2 TestPage

**Purpose**: Display test images, collect user responses, manage test flow

**Layout:**
```
+------------------------------------------+
|  DICROMAT                     [3 / 10]   |
+------------------------------------------+
|                                          |
|  +------------------------------------+  |
|  |                                    |  |
|  |        [Test Image Display]        |  |
|  |                                    |  |
|  |           400 x 400 px             |  |
|  |                                    |  |
|  +------------------------------------+  |
|                                          |
|  What number do you see?                 |
|                                          |
|  [Number Input: ___]                     |
|                                          |
|  [ ] I don't see a number                |
|                                          |
|  [Submit Answer Button]                  |
|                                          |
|  Progress: [===========----------] 30%   |
+------------------------------------------+
```

**Components:**

**TestImage Component:**
- Displays image from API: GET /api/test/{sessionId}/image/{imageNumber}
- Fixed size: 400x400px (scaled for mobile)
- Centered on page
- Loading skeleton while image loads
- Alt text: "Color blindness test plate {number}"

**AnswerInput Component:**
- Number input field (0-99)
- Large, clear font
- Autofocus on load
- Validation: integer only, range 0-99
- "I don't see a number" checkbox (mutually exclusive with number input)
- Error state if validation fails

**ProgressBar Component:**
- Visual bar showing completion (10%, 20%, ..., 100%)
- Text: "3 / 10" (current/total)
- Color: Primary brand color

**Submit Button:**
- Primary button style
- Disabled states:
  - No input provided (number or checkbox)
  - During API submission
  - Invalid number
- Loading spinner during submission

**State:**
- sessionId (from route params)
- currentImageNumber (1-10)
- userAnswer (number or null)
- isNoNumberVisible (boolean)
- isSubmitting (boolean)
- imageLoading (boolean)
- error (string | null)

**Interactions:**
1. Component mounts
2. Fetch image: GET /api/test/{sessionId}/image/{currentImageNumber}
3. Display image once loaded
4. User examines image
5. User enters number OR checks "no number" checkbox
6. User clicks "Submit Answer"
7. Validate input
8. API call: POST /api/test/{sessionId}/answer
9. On success:
   - If currentImageNumber < 10: Load next image (increment currentImageNumber)
   - If currentImageNumber === 10: Navigate to /results/{sessionId}
10. On error: Show error message, allow retry

**Edge Cases:**
- Session not found: Redirect to home with error message
- Network error during image load: Show retry button
- Network error during answer submission: Show retry button
- User navigates back: Prevent (or warn about losing progress)
- User refreshes page: Preserve state if possible, otherwise restart

**Acceptance Criteria:**
- [ ] Images load reliably and display correctly
- [ ] Number input validation works
- [ ] Checkbox exclusivity with number input
- [ ] Submit button disabled when invalid
- [ ] Progress updates after each answer
- [ ] Auto-advances to next image
- [ ] Auto-redirects to results after image 10
- [ ] Loading states for image and submission
- [ ] Error handling for all API failures
- [ ] Keyboard navigation support (Enter to submit)
- [ ] Mobile-responsive (image scales appropriately)

---

### 4.3 ResultsPage

**Purpose**: Display comprehensive test results and interpretation

**Layout:**
```
+------------------------------------------+
|  DICROMAT - Your Results                 |
+------------------------------------------+
|                                          |
|  [Icon: Checkmark or Alert]              |
|                                          |
|  Your Color Vision: DEFICIENT            |
|  Suspected Type: Deuteranopia            |
|  Confidence: High                        |
|                                          |
|  +------------------------------------+  |
|  | What does this mean?               |  |
|  |                                    |  |
|  | You had difficulty seeing numbers  |  |
|  | in 2 of 3 images designed to       |  |
|  | detect deuteranopia (green color   |  |
|  | blindness)...                      |  |
|  +------------------------------------+  |
|                                          |
|  Your Answers:                           |
|  +------------------------------------+  |
|  | Image 1: ✓ Correct (42)            |  |
|  | Image 2: ✗ Incorrect (Your: 24)    |  |
|  | Image 3: ✓ Correct (29)            |  |
|  | ...                                |  |
|  +------------------------------------+  |
|                                          |
|  [Chart/Visualization]                   |
|                                          |
|  Recommendations:                        |
|  • Consult an eye care professional...   |
|                                          |
|  [Take Test Again] [Download Results]    |
+------------------------------------------+
```

**Components:**

**ResultsSummary Component:**
- Status badge (Normal / Deficient / Inconclusive)
- Color-coded: Green (normal), Red (deficient), Gray (inconclusive)
- Suspected dichromism type (if applicable)
- Confidence level

**ResultsInterpretation Component:**
- Plain-language explanation of results
- What the condition means
- How it affects daily life (brief)

**AnswersList Component:**
- Table or list of all 10 answers
- Columns: Image number, Correct answer, User answer, Status (✓/✗)
- Visual indicators (checkmark/x icons)
- Color-coded rows (green/red) or neutral
- Possibly grouped by dichromism type

**ResultsChart Component (Optional v1.0):**
- Bar chart showing error rates by type
- X-axis: Protanopia, Deuteranopia, Tritanopia
- Y-axis: Percentage incorrect
- Simple SVG or canvas visualization

**Recommendations Component:**
- Bullet-point list
- Medical disclaimer
- Link to resources (optional)

**State:**
- sessionId (from route params)
- results (full results object from API)
- loading (boolean)
- error (string | null)

**Interactions:**
1. Component mounts
2. Fetch results: GET /api/test/{sessionId}/results
3. Display loading state
4. On success: Render results
5. On error: Show error message
6. User can click "Take Test Again" → Navigate to /
7. (Optional) User can download/print results

**Edge Cases:**
- Session not found: Redirect to home with error
- Test not completed: Redirect to test page or show error
- Network error: Show retry button

**Acceptance Criteria:**
- [ ] Results load and display correctly
- [ ] All result data is shown (summary, interpretation, answers)
- [ ] Visual design clearly distinguishes normal/deficient results
- [ ] Interpretation is clear and jargon-free
- [ ] Recommendations are actionable
- [ ] "Take Test Again" button works
- [ ] Loading state during API call
- [ ] Error handling for API failures
- [ ] Mobile-responsive layout
- [ ] (Optional) Download/print functionality

---

## 5. State Management

### 5.1 Global State (Context API)

**TestContext:**
```typescript
interface TestContextType {
  sessionId: string | null;
  currentImageNumber: number;
  totalImages: number;
  answers: Answer[];
  isTestComplete: boolean;
  startTest: (metadata?: Metadata) => Promise<void>;
  submitAnswer: (imageNumber: number, answer: number | null) => Promise<void>;
  resetTest: () => void;
}
```

**Context Provider:**
- Wraps entire app
- Manages session lifecycle
- Handles API calls for start and submit
- Stores answers array
- Provides reset function

**Benefits:**
- Centralized test state
- Prevents prop drilling
- Easy access from any component
- Simplifies state synchronization

---

## 6. API Service

### 6.1 API Client Module

**File:** `src/services/api.ts`

```typescript
interface StartTestResponse {
  session_id: string;
  created_at: string;
  total_images: number;
}

interface SubmitAnswerResponse {
  success: boolean;
  image_number: number;
  next_image: number | null;
  is_complete: boolean;
}

interface Results {
  session_id: string;
  completed_at: string;
  total_correct: number;
  total_images: number;
  analysis: {
    color_vision_status: string;
    suspected_type: string | null;
    confidence: string;
    details: {
      protanopia_errors: number;
      deuteranopia_errors: number;
      tritanopia_errors: number;
      normal_errors: number;
    };
  };
  interpretation: string;
  recommendations: string;
  answers: Answer[];
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async startTest(metadata?: Metadata): Promise<StartTestResponse> {
    // POST /api/test/start
  }

  async getImage(sessionId: string, imageNumber: number): Promise<string> {
    // GET /api/test/{sessionId}/image/{imageNumber}
    // Returns image URL or blob
  }

  async submitAnswer(
    sessionId: string,
    imageNumber: number,
    answer: number | null
  ): Promise<SubmitAnswerResponse> {
    // POST /api/test/{sessionId}/answer
  }

  async getResults(sessionId: string): Promise<Results> {
    // GET /api/test/{sessionId}/results
  }
}

export const api = new ApiService(import.meta.env.VITE_API_BASE_URL);
```

### 6.2 Error Handling

**Custom Error Types:**
```typescript
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string
  ) {
    super(message);
  }
}
```

**Error Handling Strategy:**
- Network errors: Show "Connection error, please try again"
- 404 errors: Redirect to home with "Session not found"
- 500 errors: Show "Server error, please try again later"
- Validation errors: Show specific field error

---

## 7. Styling and Design

### 7.1 Design Principles

- **Simplicity**: Minimal distractions during test
- **Accessibility**: High contrast, large fonts, keyboard navigation
- **Responsiveness**: Works on desktop and tablet (not phone for v1.0)
- **Consistency**: Uniform button styles, spacing, colors

### 7.2 Color Palette

```css
:root {
  --primary: #2563eb;      /* Blue for buttons */
  --primary-hover: #1d4ed8;
  --success: #16a34a;      /* Green for correct */
  --error: #dc2626;        /* Red for incorrect */
  --warning: #f59e0b;      /* Orange for warnings */
  --neutral-100: #f3f4f6;  /* Light background */
  --neutral-900: #111827;  /* Text */
  --white: #ffffff;
}
```

### 7.3 Typography

- **Headings**: Sans-serif (e.g., Inter, Roboto)
  - H1: 32px, bold
  - H2: 24px, semibold
  - H3: 20px, medium
- **Body**: 16px, regular
- **Small**: 14px (disclaimers, captions)
- **Number Input**: 24px, bold (easy to read)

### 7.4 Component Styles

**Button:**
- Primary: Blue background, white text, rounded, 44px height (touch-friendly)
- Secondary: White background, blue border/text
- Disabled: Gray, reduced opacity, no pointer

**Input:**
- Border: 2px solid gray
- Focus: Blue border, box-shadow
- Error: Red border
- Padding: 12px

**Card:**
- White background
- Box-shadow for depth
- Rounded corners (8px)
- Padding: 24px

### 7.5 Responsive Breakpoints

- **Desktop**: ≥ 1024px (default layout)
- **Tablet**: 768px - 1023px (slightly adjusted spacing)
- **Not supported (v1.0)**: < 768px (show message: "Please use desktop or tablet")

---

## 8. Accessibility (a11y)

### 8.1 Requirements

- **Semantic HTML**: Use proper heading hierarchy, button elements, form labels
- **Keyboard Navigation**: All interactive elements accessible via Tab, Enter, Space
- **Focus Indicators**: Visible focus outlines (do not remove)
- **Alt Text**: Descriptive alt text for images (though test images may be decorative)
- **ARIA Labels**: Where needed (e.g., progress bar)
- **Color Contrast**: WCAG AA compliance (4.5:1 for text)
- **Screen Reader**: Test with screen reader (though visual test inherently requires sight)

### 8.2 Specific Considerations

- Test images: Alt text may spoil the answer, use generic description
- Number input: Clear label "What number do you see?"
- Error messages: Use aria-live regions for dynamic updates
- Progress: Use aria-valuenow, aria-valuemin, aria-valuemax

---

## 9. Performance Optimization

### 9.1 Requirements

- **Initial Load**: < 2 seconds on 3G
- **Image Load**: < 2 seconds per image
- **Route Transitions**: Instant (no lag)
- **Bundle Size**: < 500KB (gzipped)

### 9.2 Strategies

- **Code Splitting**: Lazy load routes
- **Image Optimization**: Use appropriate format (WebP with PNG fallback)
- **Caching**: Cache images in browser (service worker optional)
- **Minification**: Production build minified
- **CDN**: Serve static assets from CDN (production)

---

## 10. Testing Requirements

### 10.1 Unit Tests

- **Components**: Render tests, interaction tests
- **Utils**: Validation functions
- **API Service**: Mock API calls

**Tools**: Vitest or Jest + React Testing Library

### 10.2 Integration Tests

- **User Flows**: Full test completion flow
- **API Integration**: Mock backend responses

### 10.3 E2E Tests (Optional v1.0)

- **Critical Path**: Start test → Complete 10 images → View results
- **Tools**: Playwright or Cypress

### 10.4 Manual Testing

- Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- Test on different screen sizes
- Test with keyboard only
- Test with screen reader (basic)

### 10.5 Coverage

- Minimum 70% code coverage
- 100% coverage for critical paths (test flow)

---

## 11. Environment Configuration

### 11.1 Environment Variables

```bash
# .env.development
VITE_API_BASE_URL=http://localhost:5000

# .env.production
VITE_API_BASE_URL=https://api.dicrhomat.example.com
```

### 11.2 Build Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint src --ext .ts,.tsx"
  }
}
```

---

## 12. Error States and Edge Cases

### 12.1 Network Errors

- **Image Load Failure**: Show placeholder with "Retry" button
- **API Call Failure**: Show error message with "Try Again" button
- **Timeout**: Show timeout message, allow retry

### 12.2 User Errors

- **Invalid Input**: Highlight field, show validation message
- **Empty Submission**: Disable button, show tooltip
- **Premature Navigation**: Warn about losing progress (or auto-save state)

### 12.3 System Errors

- **Session Expired**: Redirect to home, show message "Session expired, please start a new test"
- **Server Error (500)**: Show friendly error, suggest trying again later

---

## 13. User Experience Enhancements

### 13.1 Loading States

- Skeleton loaders for images
- Spinner for button submissions
- Progress indicators for multi-step flows

### 13.2 Feedback

- Success messages (subtle, non-intrusive)
- Error messages (clear, actionable)
- Tooltips for guidance

### 13.3 Animations (Subtle)

- Fade-in for page transitions
- Smooth progress bar animation
- Button hover/active states

### 13.4 Instructions

- Clear, concise copy
- Visual examples (optional)
- "What to expect" section

---

## 14. Analytics (Optional v1.0)

### 14.1 Events to Track

- Test started
- Test completed
- Test abandoned (at which image)
- Average time per image
- Results viewed

### 14.2 Tools

- Google Analytics or Plausible (privacy-focused)
- No PII tracking

---

## 15. Deployment

### 15.1 Build Process

1. Run `npm run build`
2. Output in `dist/` folder
3. Deploy to static hosting (Netlify, Vercel, S3 + CloudFront)

### 15.2 Environment Setup

- Configure environment variables for API base URL
- Set up CORS on backend for frontend domain

### 15.3 CI/CD (Optional v1.0)

- Automated builds on Git push
- Run tests before deployment
- Deploy to staging/production environments

---

## 16. Acceptance Criteria

- [ ] All pages implemented (Welcome, Test, Results)
- [ ] Test flow works end-to-end
- [ ] All API integrations functional
- [ ] State management working correctly
- [ ] Responsive design for desktop and tablet
- [ ] Accessibility features implemented (keyboard navigation, focus management)
- [ ] Error handling for all failure scenarios
- [ ] Loading states for all async operations
- [ ] Unit tests passing with ≥70% coverage
- [ ] Manual testing completed on target browsers
- [ ] Performance benchmarks met (load times, bundle size)
- [ ] Production build successfully deploys

---

## 17. Future Enhancements (Post-v1.0)

- Mobile support (smaller screens)
- User accounts and result history
- Share results functionality
- Multiple languages
- Dark mode
- Advanced analytics dashboard
- Adaptive test difficulty
- Educational content section
- Comparison with previous tests

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-07 | Initial | First draft |
