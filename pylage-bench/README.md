# PyLage Benchmark

This benchmark measures browser-observable interaction latency and startup time for
PyLage, NiceGUI, Streamlit, and Reflex using two small application scenarios:

- Counter: click a button and wait until the displayed counter value increments.
- Form: submit a unique name/email pair and wait until the new submitted row appears.

## Protocol

Each framework is measured independently:

1. Start a fresh server process.
2. Wait until the HTTP endpoint is ready.
3. Launch a fresh Playwright browser page.
4. Measure startup from page navigation until the benchmark UI is ready.
5. Run 20 warmup interactions.
6. Run 50 measured interactions.
7. Measure each interaction from the user action until the expected UI state is visible.
8. Save the raw samples plus startup, mean, P50, and P95.
9. Stop the complete server process group.

The benchmark does not use artificial fixed sleeps as the interaction completion
condition.

## Scenarios

### Counter

Completion is detected by observing the displayed counter value change from `N`
to `N+1`.

### Form

Completion is detected by observing the newly submitted unique row:

`UserN | userN@example.com`

This avoids using a persistent status message such as `Saved` as the completion
signal.

## Final Counter Results

| Framework | Startup (ms) | P50 (ms) | P95 (ms) | Mean (ms) | N |
|---|---:|---:|---:|---:|---:|
| PyLage | 409.48 | 60.61 | 74.33 | 61.36 | 50 |
| NiceGUI | 1015.95 | 79.99 | 96.51 | 81.66 | 50 |
| Reflex | 709.79 | 61.18 | 68.06 | 61.28 | 50 |
| Streamlit | 3329.76 | 255.36 | 316.59 | 259.90 | 50 |

## Final Form Results

| Framework | Startup (ms) | P50 (ms) | P95 (ms) | Mean (ms) | N |
|---|---:|---:|---:|---:|---:|
| PyLage | 597.09 | 116.42 | 129.34 | 115.21 | 50 |
| NiceGUI | 1049.05 | 143.04 | 175.01 | 142.95 | 50 |
| Reflex | 722.71 | 85.41 | 108.14 | 87.48 | 50 |
| Streamlit | 3232.20 | 563.77 | 639.92 | 542.94 | 50 |

## Framework Run Modes

- PyLage: local Python application server.
- NiceGUI: local Python application server.
- Streamlit: `streamlit run` in headless mode.
- Reflex: `reflex run --env preview`.

The exact commands are defined in the benchmark runners.

## Reports and Raw Data

- `REPORT.md` — final counter report.
- `REPORT_FORM.md` — final form report.
- `results/*.json` — raw benchmark summaries and measured samples.
- `logs/` — framework startup/runtime logs.

## Reproduction

From the repository root:

```bash
python pylage-bench/measure/run_bench.py --framework all --samples 50 --warmup 20
python pylage-bench/measure/run_form_bench.py --framework all --samples 50 --warmup 20
python pylage-bench/measure/make_report.py
