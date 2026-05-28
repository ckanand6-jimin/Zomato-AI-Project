# UI/UX Design Prompt: Zomato AI Restaurant Recommendation System

> **For:** Google Stitch, Figma, or any design tool  
> **Purpose:** Generate high-fidelity frontend designs for the restaurant recommendation web application

---

## Project Overview

**Zomato AI Restaurant Recommender** is a preference-driven restaurant discovery platform that combines structured restaurant data filtering with LLM-powered ranking and personalized explanations. The UI should feel modern, intuitive, and Zomato-inspired—guiding users through preferences to AI-ranked results.

---

## Design Principles

1. **Preference-First Flow:** Users articulate preferences first; system surfaces grounded, explained recommendations.
2. **Transparent AI:** Every recommendation includes an AI-generated explanation tied to stated preferences.
3. **Progressive Disclosure:** Show only relevant information per stage; avoid overwhelming users.
4. **Zomato-Inspired Aesthetic:** Clean cards, readable typography, warm restaurant imagery, intuitive navigation.
5. **Trust & Grounding:** Emphasize that all recommendations come from real dataset entries (no hallucinations).
6. **Accessibility:** WCAG 2.1 AA compliant; sufficient contrast, keyboard navigation, screen reader support.

---

## User Journey & Screens

### Screen 1: Hero / Landing Page

**Purpose:** Introduce the application and establish context.

**Layout:**
- Header: Logo (Zomato-inspired icon) + Brand name "Zomato AI Recommender"
- Hero section with:
  - Headline: "Discover restaurants that match your taste"
  - Subheadline: "AI-powered recommendations grounded in real data, personalized for you"
  - Call-to-action button: "Find Restaurants" (prominent, contrasting color)
- Optional: Brief feature callouts (3–4 bullet points):
  - "Real restaurant data"
  - "AI-powered explanations"
  - "Personalized to your preferences"
  - "Instant results"

**Visual Style:**
- Warm, inviting color palette (oranges, warm reds for primary; neutral grays for secondary)
- Restaurant-themed imagery or illustration (food, dining, discovery)
- Large, readable typography (hero headline: 48–56px)

---

### Screen 2: Preference Form

**Purpose:** Collect user preferences via an intuitive, progressive form.

**Layout:**
- Full-width form container (max-width: 600px, centered)
- Clear heading: "Tell us your preferences"
- Subheading: "We'll find the best matches for you"

**Form Fields & Components:**

#### 2.1 Location (Required)
- **Component:** Dropdown / Combobox
- **Label:** "Location *" (with asterisk for required)
- **Placeholder:** "Select a city..."
- **Options:** Dynamically populated from repository (Delhi, Bangalore, Mumbai, etc.)
- **Visual:** Icon (📍 location pin) left of field
- **Validation:** Show error if empty on submit

#### 2.2 Budget (Required)
- **Component:** Radio button group (horizontal layout)
- **Label:** "Budget Tier *"
- **Options:**
  - ◯ Low (₹0–500)
  - ◯ Medium (₹501–1,500) [default selected]
  - ◯ High (₹1,500+)
- **Visual:** Each option shows budget range and subtle icon (coin, wallet, etc.)
- **Interaction:** Smooth transition on selection

#### 2.3 Cuisine (Optional)
- **Component:** Text input with suggestions / tag input
- **Label:** "Cuisine preference"
- **Placeholder:** "e.g. Italian, Chinese (comma-separated)"
- **Behavior:**
  - User types cuisine name
  - Optional autocomplete dropdown shows matching cuisines from dataset
  - User can enter multiple cuisines (comma-separated)
  - Entered cuisines appear as dismissible tags below input
- **Visual:** 🍽️ Fork/knife icon left of field

#### 2.4 Minimum Rating (Optional)
- **Component:** Slider
- **Label:** "Minimum Rating"
- **Range:** 0.0 to 5.0 stars
- **Default:** 3.5
- **Step:** 0.1
- **Display:**
  - Current value shown as "★ 3.5" near slider
  - Visual star rating indicator above/below slider
  - Color gradient (low ratings: light yellow → high ratings: bright gold/orange)

#### 2.5 Additional Preferences (Optional)
- **Component:** Textarea
- **Label:** "Additional preferences"
- **Placeholder:** "e.g. family-friendly, quick service, vegetarian options, romantic ambiance"
- **Max length:** 200 characters (show counter: "50/200")
- **Visual:** 💭 Chat/thought icon left of field

#### Form Actions
- **Primary Button:** "Find Restaurants" (large, prominent color)
  - Disabled until location + budget are selected
  - Shows loading spinner on click
- **Secondary Button:** "Reset" (outline style, less prominent)
  - Clears all fields and resets to defaults

**Responsive Behavior:**
- Desktop (≥768px): Single-column form, all fields visible at once
- Mobile (<768px): Form fields stack vertically; full viewport width with padding
- Buttons: Full width on mobile; auto width on desktop

**Visual Refinements:**
- Subtle background color change on form container (off-white or light gray)
- Rounded corners (8–12px) on input fields
- Clear visual hierarchy: headings → labels → inputs
- Consistent spacing between elements (16px standard unit)

---

### Screen 3: Loading State

**Purpose:** Provide visual feedback during recommendation generation.

**Layout:**
- Overlay or dedicated screen
- Centered content:
  - Large animated spinner (restaurant-themed: rotating fork/knife, animated plates, etc.)
  - Text: "Generating personalized recommendations..."
  - Subtext: "Filtering restaurants and consulting AI (usually 2–8 seconds)"

**Animation:**
- Smooth, continuous rotation of spinner
- Optional: Pulsing restaurant icon or animated food illustration
- Estimated time indicator (optional): "⏱️ ~5 seconds"

**Accessibility:**
- aria-live region announces "Loading recommendations" to screen readers
- Spinner labeled for screen readers (not purely decorative)

---

### Screen 4: Results Page

**Purpose:** Display AI-ranked restaurant recommendations with explanations.

**Layout:**
- Header section:
  - Back button or "New Search" link (top-left)
  - Brief result summary: "Showing 5 recommendations for [Location] • [Budget] • [Cuisine]"
- Optional Summary section:
  - AI-generated summary paragraph (if available) in a highlighted callout box
  - Italic text, slightly larger font (16–18px)
  - Example: "We found 5 highly-rated restaurants in Delhi that match your medium budget and Italian cuisine preference. All of these are known for consistent quality and great value."
- Results cards (main content):
  - Vertical stack (mobile) or grid (desktop: 1–2 columns depending on space)
- Empty state / error handling (if no results)

#### 4.1 Result Card Layout (for each recommendation)

Each card displays one restaurant with detailed information:

**Card Header:**
- Rank badge (top-left corner): `#1`, `#2`, etc. in a small circle (orange/primary color)
- Restaurant name (large, bold): "Trattoria Example"
- Rating badge (top-right): ⭐ 4.5 (with star icon + numeric rating)

**Card Body:**
- **Cuisine:** "Italian, Pizza" (secondary text, smaller font)
- **Location:** 📍 "Connaught Place, New Delhi" (tertiary text)
- **Cost:** "₹1,200 for two" or "₹1,200–1,500 per person"
- **Budget tier:** "Medium budget" (small label/badge)
- **Explanation section:**
  - Heading: "Why we picked this"
  - Indented paragraph (light background color or left border accent):
    > "Trattoria Example is an excellent match for your Italian cuisine preference and medium budget. Located in Connaught Place, it's highly rated (4.5★) and known for authentic pasta and intimate ambiance."
  - Text is left-aligned, readable (14–16px), with good line-height

**Card Footer (Optional):**
- Action buttons:
  - "View Details" (outline button, opens extended info modal if available)
  - "Save" / Heart icon (bookmark/wishlist interaction)
  - "More info" link (could link to external source or map)

**Visual Style:**
- White or off-white background
- Subtle shadow (elevation: 2–4px)
- Rounded corners (8–12px)
- Hover effect: Slight scale (1.02x), shadow increase, cursor pointer
- Clear spacing between cards (12–16px gap)
- Left accent border (4–6px) in primary orange color for emphasis

**Responsive Behavior:**
- Desktop (≥768px): 2-column grid, cards side-by-side
- Tablet (480–768px): 2-column grid or 1-column depending on content length
- Mobile (<480px): Full-width single-column stack

#### 4.2 Empty State (No Matches)

**Layout:**
- Centered illustration or icon (large restaurant icon with X or empty symbol)
- Heading: "No restaurants match your criteria"
- Message: "We couldn't find restaurants matching all your preferences. Try relaxing your filters."

**Suggestions Box:**
- Bulleted list of actionable suggestions:
  - "Lower your minimum rating (highest available: 4.2)"
  - "Try a different cuisine"
  - "Change your budget tier"
  - "Search in a nearby city"

**Call-to-Action:**
- "Modify Preferences" button (secondary color)
- "Start Over" link

#### 4.3 Error State (LLM or System Failure)

**Layout:**
- Warning banner at top of results section
- Icon: ⚠️
- Text: "The AI recommendation step encountered an issue, so we're showing the top-rated matches based on your filters instead."
- Results still display using fallback rankings (no explanations, or generic explanations)

---

### Screen 5: Results Metadata / Details Panel

**Purpose:** Show technical details for transparency and debugging.

**Location:** Collapsible expander at bottom of results page

**Content (expandable):**
- **Filters Applied:** "Location, Minimum Rating, Cuisine, Budget"
- **Candidates Considered:** "18 restaurants matched your preferences"
- **AI Fallback Used:** "No" or "Yes" (if LLM failed)
- **Search Timestamp:** "Generated 2 minutes ago"

**Visual:**
- Subtle border (1px), light background
- Small text (12–14px)
- Tab-like icon or chevron icon for expand/collapse

---

## Color Palette

**Primary Colors:**
- **Primary Orange:** `#FF6B35` or `#E8651E` (CTA buttons, accents, rank badges, left card borders)
- **Warm Red:** `#D63230` (hover states, alerts)

**Neutral Colors:**
- **Dark Text:** `#2C3E50` or `#1A1A1A` (headings, body text)
- **Light Text:** `#7F8C8D` (secondary info, placeholders)
- **Off-White Background:** `#F8F9FA` or `#FAFAFA`
- **White:** `#FFFFFF` (card backgrounds, input fields)
- **Light Gray:** `#E8E8E8` (borders, dividers)

**Semantic Colors:**
- **Success:** `#27AE60` (green, for positive feedback)
- **Warning:** `#F39C12` (orange/yellow, for cautions)
- **Error:** `#E74C3C` (red, for errors)
- **Info:** `#3498DB` (blue, for informational messages)

**Star Rating Color:**
- **Filled Star:** `#FFB700` or `#FFC107` (gold)
- **Empty Star:** `#E0E0E0` (light gray)

---

## Typography

**Font Family:**
- **Primary:** Inter, Roboto, or similar modern sans-serif (for web, use system fonts or Google Fonts)
- **Fallback:** -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui

**Font Sizes & Hierarchy:**
| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Page Heading (Hero) | 48–56px | 700 (Bold) | Primary Orange or Dark Text |
| Section Heading | 28–32px | 700 (Bold) | Dark Text |
| Card Title (Restaurant Name) | 20–24px | 600 (Semibold) | Dark Text |
| Body Text | 14–16px | 400 (Regular) | Dark Text |
| Secondary Text (Cuisine, Location) | 12–14px | 500 (Medium) | Light Text |
| Label (Form, Badges) | 12–13px | 600 (Semibold) | Dark Text / Inverted on colored background |
| Small Text (Metadata, Expanders) | 11–12px | 400 (Regular) | Light Text |

**Line Height:**
- Headings: 1.2–1.3
- Body text: 1.5–1.6
- Form labels: 1.4

---

## Spacing & Layout Grid

**Base Unit:** 8px (use 8px, 16px, 24px, 32px, etc.)

**Container Widths:**
- **Mobile:** Full width with 16px padding on each side
- **Tablet:** 90% width, max 600px
- **Desktop:** 1200px max-width, centered

**Common Spacings:**
- Form field gap: 16px
- Card gap: 16px–20px
- Section gap: 32px–40px
- Button padding: 12px 24px
- Input padding: 12px 16px

---

## Interactive Elements & States

### Button States (Primary CTA: "Find Restaurants")

| State | Background | Text Color | Cursor | Notes |
|-------|-----------|-----------|--------|-------|
| **Default** | Primary Orange | White | pointer | Fully opaque |
| **Hover** | Warm Red | White | pointer | Slight scale (1.02x), shadow increase |
| **Active (Pressed)** | Darker Red | White | pointer | Scale (0.98x), reduced shadow |
| **Disabled** | Light Gray | Medium Gray | not-allowed | Opacity 0.6, no hover effects |
| **Loading** | Primary Orange | White | wait | Spinner icon inside button, text hidden |

### Form Input States

| State | Border | Background | Text Color | Icon | Notes |
|-------|--------|-----------|-----------|------|-------|
| **Default** | Light Gray | White | Dark | Primary | 1px border |
| **Focus** | Primary Orange | White | Dark | Primary | 2px border, subtle glow shadow |
| **Hover** | Medium Gray | White | Dark | Primary | Slight background change |
| **Error** | Error Red | Light Red | Dark | Error | 2px border, error icon |
| **Disabled** | Light Gray | Off-White | Light Gray | Light Gray | Opacity 0.6 |

### Card Interactions

- **Hover:** Scale 1.02x, shadow increases, subtle lift animation (100–150ms)
- **Click/Focus:** Outline (2–3px) in Primary Orange (for keyboard navigation)
- **Transition:** All transitions 200–300ms ease-out

---

## Responsive Design Breakpoints

```
Mobile:       0–480px   (portrait phones)
Tablet Small: 481–768px (landscape phones, small tablets)
Tablet:       769–1024px (standard tablets)
Desktop:      1025px+   (laptops, desktops)
```

**Key Responsive Changes:**
- Form: Single column on mobile; full layout on tablet+
- Results grid: 1 column on mobile; 2 columns on tablet+
- Header: Hamburger menu on mobile; full nav on desktop
- Spacing: 12–16px on mobile; 16–24px on tablet+

---

## Accessibility Requirements

1. **Contrast:** All text ≥ 4.5:1 for normal text; ≥ 3:1 for large text (WCAG AA)
2. **Keyboard Navigation:**
   - Tab order: Logical left-to-right, top-to-bottom
   - Focus indicators: Visible (2–3px outline, 2–4px offset)
   - Form: Enter/Return submits; Tab moves between fields
3. **Screen Reader Support:**
   - All images have descriptive alt text
   - Form labels explicitly associated with inputs (`<label for="...">`)
   - Icon-only buttons have aria-labels (e.g., "Close search")
   - Loading state and results updates announced (aria-live regions)
4. **Color Independence:** Never convey information by color alone (use icons, text, patterns)
5. **Font Size:** Min 14px body text; scalable to 200% without loss of functionality

---

## Animations & Transitions

**Timing:**
- Fast interactions (hover, focus): 100–150ms
- Medium interactions (card expand, form submit): 200–300ms
- Longer flows (page transitions, loading): 300–500ms
- Easing: `ease-out` for most interactions (feels snappy)

**Key Animations:**
- Form input focus: Subtle glow + border color change (150ms)
- Button click: Scale down (50ms) then scale back (50ms) + color change
- Card hover: Scale + shadow increase (200ms)
- Loading spinner: Continuous 360° rotation (2s, linear, infinite)
- Results appear: Fade-in + slight slide-up (300ms, staggered if multiple cards)

---

## Mobile-Specific Considerations

1. **Touch Targets:** All buttons/interactive elements ≥ 48px × 48px
2. **Input Fields:** Use appropriate input types (email, tel, etc.) to trigger mobile keyboards
3. **Viewport:** `<meta name="viewport" content="width=device-width, initial-scale=1">`
4. **Safe Area:** Account for notches / bottom navigation on modern phones
5. **Gestures:** Support swipe gestures for card navigation if desired (optional)

---

## Desktop Enhancements (Optional)

1. **Advanced Filters:** Collapsible filter sidebar with more granular options
2. **Map Integration:** Show restaurants on an interactive map alongside cards
3. **Favorites/Wishlist:** Save recommendations for later viewing
4. **Comparison View:** Side-by-side comparison of 2–3 restaurants
5. **Sorting:** Allow users to sort results by rating, cost, or custom weight

---

## Design Tokens / CSS Variables (Example)

```css
/* Colors */
--color-primary: #FF6B35;
--color-primary-dark: #E8651E;
--color-primary-light: #FFE8D9;
--color-text-dark: #2C3E50;
--color-text-light: #7F8C8D;
--color-bg-white: #FFFFFF;
--color-bg-light: #F8F9FA;
--color-border: #E8E8E8;
--color-success: #27AE60;
--color-warning: #F39C12;
--color-error: #E74C3C;

/* Typography */
--font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-size-base: 16px;
--font-size-lg: 20px;
--font-size-xl: 28px;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

/* Spacing */
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;

/* Shadows */
--shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.08);
--shadow-md: 0 4px 8px rgba(0, 0, 0, 0.12);
--shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.15);

/* Border Radius */
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;

/* Transitions */
--transition-fast: 150ms ease-out;
--transition-normal: 300ms ease-out;
```

---

## Component Library / Reusable Elements

**Core Components:**
1. **Button** – Primary, Secondary, Tertiary variants; loading state; disabled state
2. **Input Field** – Text, email, tel, number; with label, placeholder, error message
3. **Select / Dropdown** – Single select, multi-select; searchable
4. **Radio Group** – Horizontal/vertical layout; optional icons
5. **Slider** – Range input; visual value display
6. **Card** – Standard container with shadow; hover effects
7. **Badge** – Labels, tags, status indicators
8. **Alert / Banner** – Info, success, warning, error variants
9. **Modal / Dialog** – Centered overlay for confirmations, details
10. **Spinner / Loading** – Animated loading indicator
11. **Toast / Notification** – Transient success/error messages (optional)
12. **Expander / Accordion** – Collapse/expand sections

---

## Additional Notes for Designer

1. **Brand Consistency:** Maintain Zomato brand aesthetic (warm, inviting, food-focused) while adding modern AI/tech elements.
2. **Restaurant Imagery:** Use placeholder restaurant images or illustrations. Consider subtle food photography as background texture.
3. **Icons:** Use a consistent icon set (e.g., Feather Icons, Material Design Icons). Keep stroke weight consistent.
4. **Dark Mode:** Consider providing a dark mode variant for evening/nighttime browsing.
5. **Internationalization:** Design with space for longer text labels (e.g., German, French translations).
6. **Progressive Enhancement:** Ensure basic functionality works without JavaScript; enhance with smooth animations when JS is available.
7. **Performance:** Optimize images; lazy-load restaurant cards if list is long.
8. **Testing:** Create interactive prototypes for user testing before development. Test on real mobile devices.

---

## File Structure / Deliverables

```
Design Assets/
├── Wireframes/
│   ├── 01-landing-page.fig
│   ├── 02-preference-form.fig
│   ├── 03-loading-state.fig
│   ├── 04-results-page.fig
│   ├── 05-empty-state.fig
│   └── 06-error-state.fig
├── High-Fidelity Mockups/
│   ├── Desktop/
│   │   ├── landing-page.fig
│   │   ├── results-page.fig
│   │   └── ...
│   └── Mobile/
│       ├── landing-page.fig
│       ├── results-page.fig
│       └── ...
├── Component Library/
│   ├── buttons.fig
│   ├── inputs.fig
│   ├── cards.fig
│   ├── badges.fig
│   └── ...
├── Style Guide/
│   ├── colors.fig
│   ├── typography.fig
│   ├── spacing.fig
│   └── interactions.fig
└── Prototypes/
    ├── interactive-prototype.fig (Figma prototype link)
    └── user-flows.fig
```

---

## Design Handoff Checklist

- [ ] All screens designed in desktop + mobile variants
- [ ] Interactive prototype with working transitions and states
- [ ] Component library exported with clear naming conventions
- [ ] Color palette and typography specs documented
- [ ] Accessibility guidelines verified (contrast, keyboard nav, alt text)
- [ ] Responsive breakpoints tested
- [ ] Animation specs detailed (timing, easing, etc.)
- [ ] Hover/focus/active states shown for all interactive elements
- [ ] Error/loading/empty states designed
- [ ] Design tokens exported (CSS variables or design system format)
- [ ] Design rationale documented
- [ ] Developer handoff complete (Figma specs, assets, code snippets if applicable)

---

## References & Inspiration

- **Zomato App:** https://www.zomato.com (reference for restaurant card design, ratings, location display)
- **Design Systems:** Material Design (Google), iOS Human Interface Guidelines (Apple), Ant Design
- **Figma Community:** Search for restaurant app templates, preference form designs
- **Accessibility:** WebAIM, WCAG 2.1 Guidelines, Inclusive Components

---

## Questions for Clarification (To Designer)

1. Should we integrate Google Maps for restaurant location display?
2. Do you want restaurant images in the cards, or just text-based information?
3. Should there be a saved preferences / favorites feature?
4. Is a dark mode variant in scope for this phase?
5. Should the app support multiple languages? If so, which ones?
6. Do you want animations (entrance effects, micro-interactions) or minimal animations for performance?
7. Should there be a "suggest similar" or "refine search" option after viewing results?

---

**End of Design Prompt**
