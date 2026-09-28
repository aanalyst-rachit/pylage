<div class="pylage-hero">
  <div class="hero-badge">PYLAGE 1.0.8</div>
  <h1>Build reactive web apps.<br><span>Stay in Python.</span></h1>
  <p class="hero-lead">A Python-first, server-driven UI framework for fast interactive applications with reactive state, routing, components, and browser synchronization.</p>
  <div class="hero-actions">
    <a class="hero-button hero-button-primary" href="helper/installation/">Get started</a>
    <a class="hero-button hero-button-secondary" href="https://aanalyst-rachit.github.io/pylage/playground/">Open Playground</a>
  </div>
  <div class="hero-meta">
    <span>Python 3.10+</span>
    <span>Server-driven</span>
    <span>No frontend build system</span>
  </div>
</div>

<div class="code-showcase">
  <div class="code-showcase-copy">
    <span class="section-kicker">A small API surface</span>
    <h2>From Python to UI in minutes.</h2>
    <p>Compose familiar Python functions into interactive interfaces. State, events, layout, and rendering stay in one application.</p>
  </div>

```python
import pylage as pl

count = pl.state(0)

def increment():
    count.set(count.value + 1)

app = pl.column(
    pl.heading("Hello PyLage"),
    pl.text(count),
    pl.button("Increment", on_click=increment),
)

pl.run(app)
```
</div>

## Everything you need to build

<div class="feature-grid">
  <div class="feature-card">
    <div class="feature-icon">01</div>
    <h3>Reactive state</h3>
    <p>Keep application state in Python and update the browser as state changes.</p>
    <a href="api/state/">Explore state →</a>
  </div>

  <div class="feature-card">
    <div class="feature-icon">02</div>
    <h3>Composable UI</h3>
    <p>Build interfaces from layouts, primitives, forms, data views, and interactive components.</p>
    <a href="api/components/">Browse components →</a>
  </div>

  <div class="feature-card">
    <div class="feature-icon">03</div>
    <h3>Routing</h3>
    <p>Organize multi-page applications with Python-first routing and navigation.</p>
    <a href="api/routing/">Read routing docs →</a>
  </div>

  <div class="feature-card">
    <div class="feature-icon">04</div>
    <h3>Theming</h3>
    <p>Control appearance with the PyLage styling system instead of a separate frontend stack.</p>
    <a href="api/styling/">Explore styling →</a>
  </div>

  <div class="feature-card">
    <div class="feature-icon">05</div>
    <h3>Server-driven runtime</h3>
    <p>Keep application behavior on the server while synchronizing interactive browser state.</p>
    <a href="api/runtime/">Understand the runtime →</a>
  </div>

  <div class="feature-card">
    <div class="feature-icon">06</div>
    <h3>Production ready</h3>
    <p>Move from a local prototype to deployment with the same Python application model.</p>
    <a href="deployment/">Deploy PyLage →</a>
  </div>
</div>

<div class="split-section">
  <div>
    <span class="section-kicker">Designed for Python developers</span>
    <h2>One stack. One language.</h2>
  </div>
  <div>
    <p>PyLage is designed around the idea that application logic and interface composition should not require separate frontend and backend projects.</p>
    <div class="inline-links">
      <a href="first_app/">Build your first app →</a>
      <a href="api/">Explore the API →</a>
    </div>
  </div>
</div>

<div class="quick-start">
  <div>
    <span class="section-kicker">Quick start</span>
    <h2>Install PyLage and start building.</h2>
    <p>Requires Python 3.10 or newer.</p>
  </div>

```bash
pip install pylage
```
</div>

## Explore PyLage

<div class="link-grid">
  <a href="first_app/" class="link-card"><strong>First App</strong><span>Build a complete application from scratch.</span></a>
  <a href="component/button/" class="link-card"><strong>Components</strong><span>Explore the UI component library.</span></a>
  <a href="benchmark/" class="link-card"><strong>Benchmarks</strong><span>See the framework performance work.</span></a>
  <a href="helper/framework_comparison/" class="link-card"><strong>Architecture</strong><span>Understand the design and framework model.</span></a>
</div>

<div class="home-footer">
  <strong>PyLage 1.0.7</strong>
  <span>Python-first reactive UI.</span>
  <a href="https://github.com/aanalyst-rachit/pylage">GitHub</a>
  <a href="https://pypi.org/project/pylage/">PyPI</a>
</div>
