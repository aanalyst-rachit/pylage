from pylage.ENGINE.styling.collector import StyleCollector


def test_style_collector_deduplicates_identical_css():
    collector = StyleCollector()
    collector.add(".x{color:red}")
    collector.add(".x{color:red}")
    collector.add(".y{color:blue}")

    rendered = collector.render()

    assert rendered.count("<style>") == 2
    assert rendered.count(".x{color:red}") == 1
    assert rendered.count(".y{color:blue}") == 1


def test_style_collector_ignores_empty_css():
    collector = StyleCollector()
    collector.add("")
    collector.add(".x{color:red}")
    collector.add("")

    assert len(collector) == 1
    assert collector.render() == "<style>.x{color:red}</style>"
