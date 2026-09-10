from __future__ import annotations

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.renderers.html import render_document


PYODIDE_VERSION = "0.29.3"
PYLAGE_WHEEL = "pylage-1.0.2-py3-none-any.whl"


def inject_playground_bridge(document: str, wheel_url: str | None = None) -> str:
    if wheel_url is None:
        wheel_url = f"/dist/{PYLAGE_WHEEL}"

    bridge = f"""
<script src="https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.js"></script>
<script>
(() => {{
    const wheelUrl = {wheel_url!r};
    const editorId = "pylage-playground-editor";
    const runId = "pylage-playground-run";
    const previewId = "pylage-playground-preview";
    const statusId = "pylage-playground-status";

    let pyodide = null;
    let loading = null;

    function status(message) {{
        const element = document.getElementById(statusId);
        if (element) {{
            element.textContent = message;
        }}
    }}

    async function getPyodide() {{
        if (pyodide) {{
            return pyodide;
        }}

        if (!loading) {{
            loading = (async () => {{
                status("Loading Pyodide...");

                pyodide = await loadPyodide();

                status("Installing PyLage...");

                await pyodide.loadPackage("micropip");

                await pyodide.runPythonAsync(
                    `import micropip
await micropip.install(${{JSON.stringify(wheelUrl)}}, deps=False)`
                );

                status("Ready");

                return pyodide;
            }})();
        }}

        return loading;
    }}

    async function execute(source) {{
        const runtime = await getPyodide();
        const sourceLiteral = JSON.stringify(source);

        const code = `
import ast
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render

_source = ${{sourceLiteral}}
_tree = ast.parse(_source, mode="exec")

if not _tree.body:
    raise ValueError("Playground code is empty")

_last = _tree.body[-1]

if isinstance(_last, ast.Expr):
    _tree.body[-1] = ast.Assign(
        targets=[
            ast.Name(
                id="__pylage_result",
                ctx=ast.Store(),
            )
        ],
        value=_last.value,
    )
    ast.fix_missing_locations(_tree)

_exec = compile(
    _tree,
    "<pylage-playground>",
    "exec",
)

exec(_exec, globals(), globals())

_result = globals().get("__pylage_result")

if not isinstance(_result, Component):
    raise TypeError(
        "Playground code must finish with a "
        "PyLage Component expression"
    )

render(_result)
`;

        return await runtime.runPythonAsync(code);
    }}

    async function run() {{
        const editor = document.getElementById(editorId);
        const preview = document.getElementById(previewId);

        if (!editor || !preview) {{
            return;
        }}

        const source = editor.value;
        const button = document.getElementById(runId);

        if (button) {{
            button.disabled = true;
        }}

        try {{
            status("Running Python...");

            const html = await execute(source);

            preview.innerHTML = html;

            status("Preview updated");
        }} catch (error) {{
            status("Error: " + error);
            console.error(error);
        }} finally {{
            if (button) {{
                button.disabled = false;
            }}
        }}
    }}

    window.addEventListener("DOMContentLoaded", () => {{
        const button = document.getElementById(runId);
        const docs = document.getElementById("pylage-playground-docs");
        const github = document.getElementById("pylage-playground-github");
        const install = document.getElementById("pylage-playground-install");

        if (docs) {{
            docs.addEventListener("click", () => {{
                window.location.href = "https://aanalyst-rachit.github.io/pylage/";
            }});
        }}

        if (github) {{
            github.addEventListener("click", () => {{
                window.location.href = "https://github.com/aanalyst-rachit/pylage";
            }});
        }}

        if (install) {{
            install.addEventListener("click", async () => {{
                try {{
                    await navigator.clipboard.writeText("pip install pylage");
                    status("Install command copied");
                }} catch (error) {{
                    status("Copy failed: pip install pylage");
                    console.error(error);
                }}
            }});
        }}

        if (button) {{
            button.addEventListener("click", run);
        }}

        getPyodide().catch(error => {{
            status("Error: " + error);
            console.error(error);
        }});
    }});
}})();
</script>
"""

    return document.replace("</body>", bridge + "</body>")


def build_playground_document(
    component: Component,
    title: str = "PyLage Playground",
    wheel_url: str | None = None,
) -> str:
    document = render_document(component, title=title)
    return inject_playground_bridge(document, wheel_url=wheel_url)
