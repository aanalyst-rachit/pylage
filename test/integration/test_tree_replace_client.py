from pylage.ENGINE.runtime.client import CLIENT_RUNTIME


def test_tree_replace_client_uses_renderer_html_when_available():
    runtime = CLIENT_RUNTIME

    assert "message.new_component" in runtime
    assert "CSS.escape(message.old_component_id)" in runtime
    assert 'typeof item.html !== "string"' in runtime
    assert "createRenderedNodes(item)" in runtime
    assert "template.innerHTML = item.html.trim()" in runtime


def test_tree_replace_client_supports_multiple_rendered_nodes():
    runtime = CLIENT_RUNTIME

    assert "const nodes = Array.from(" in runtime
    assert "template.content.childNodes" in runtime
    assert "if (Array.isArray(replacementNodes))" in runtime
    assert "parent.insertBefore(" in runtime
    assert "oldComponent.remove()" in runtime


def test_tree_replace_client_falls_back_to_raw_tree_creation():
    runtime = CLIENT_RUNTIME

    assert "document.createElement" in runtime
    assert "item.tag || \"div\"" in runtime
    assert "item.props" in runtime
    assert "item.children" in runtime


def test_tree_replace_client_supports_nested_fallback_tree():
    runtime = CLIENT_RUNTIME

    assert "const children = item.children || [];" in runtime
    assert "children.forEach(function (child)" in runtime
    assert "createTreeNode(child)" in runtime
    assert "element.appendChild(childNode)" in runtime


def test_tree_replace_client_keeps_renderer_root_identity():
    runtime = CLIENT_RUNTIME

    assert (
        'node.getAttribute("data-pylage-id") === item.id'
        in runtime
    )
    assert "rootElement = node" in runtime


def test_tree_replace_client_scans_events_after_dynamic_replacement():
    runtime = CLIENT_RUNTIME

    assert "scanAndBindEvents(parent)" in runtime
