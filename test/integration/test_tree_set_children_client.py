from pylage.ENGINE.runtime.client import CLIENT_RUNTIME


def test_tree_set_children_client_replaces_existing_children():
    runtime = CLIENT_RUNTIME

    assert "tree_set_children" in runtime
    assert "message.children" in runtime
    assert "while (parent.firstChild)" in runtime
    assert "parent.removeChild(" in runtime
    assert "insertTreeNodes(" in runtime


def test_tree_set_children_client_preserves_new_child_order():
    runtime = CLIENT_RUNTIME

    assert "message.children.forEach" in runtime
    assert "insertTreeNodes(" in runtime
    assert "parent.appendChild(node)" in runtime


def test_tree_set_children_client_builds_nested_fallback_subtrees():
    runtime = CLIENT_RUNTIME

    assert "function createTreeNode(item)" in runtime
    assert "const children = item.children || [];" in runtime
    assert "children.forEach(function (child)" in runtime
    assert "createTreeNode(child)" in runtime
    assert "element.appendChild(childNode)" in runtime


def test_tree_set_children_client_supports_deep_nested_subtrees():
    runtime = CLIENT_RUNTIME

    # Recursive construction must continue for arbitrary nested children.
    assert runtime.count("createTreeNode(child)") >= 1
    assert runtime.count("element.appendChild(childNode)") >= 1


def test_tree_set_children_client_prefers_renderer_html():
    runtime = CLIENT_RUNTIME

    assert 'typeof item.html !== "string"' in runtime
    assert "createRenderedNodes(item)" in runtime
    assert "template.innerHTML = item.html.trim()" in runtime


def test_tree_set_children_client_supports_multiple_top_level_nodes():
    runtime = CLIENT_RUNTIME

    assert "if (Array.isArray(nodes))" in runtime or "if (Array.isArray(childNodes))" in runtime
    assert "nodes.forEach(function (node)" in runtime
    assert "parent.appendChild(node)" in runtime
