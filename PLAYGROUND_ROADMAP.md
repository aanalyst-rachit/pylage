# PyLage Playground Roadmap

## Goal
Create a modern PyLage landing page with a live Python-to-UI playground.

## V1 Steps
1. Landing Page — modern hero + product positioning. **Complete**
2. Playground UI — code editor on left, live preview on right. **Complete**
3. Browser Runtime — prototype PyLage execution with Pyodide where feasible.
4. Demo Components — reactive examples using current V1 APIs.
5. Error/Loading UX — clean execution states and useful errors.
6. Mobile/Responsive — usable on desktop and mobile.
7. Docs Integration — keep existing MkDocs docs intact and link them from landing page.
8. Test + Deploy — verify locally, then deploy through GitHub Pages.

## Step 2 Verification
- Landing page and playground runtime manually verified in the browser.
- Python editor uses the existing PyLage textarea and State APIs.
- Run action updates the preview through the existing Component.set_children() mutation API.
- Focused Step 2 integration tests: 3 passed.

## Rule
V2 is NOT a prerequisite. Build the first working playground on the current V1 architecture; use V2 later for enhancements.
