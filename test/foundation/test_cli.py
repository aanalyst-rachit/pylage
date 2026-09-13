from pathlib import Path

import pytest

from pylage import cli
from pylage.ENGINE.core.component import Component


def test_cli_resolves_get_app(tmp_path):
    app_file = tmp_path / 'app.py'
    app_file.write_text(
        'import pylage as pl\n\n'
        'def get_app():\n'
        '    return pl.column(pl.heading("CLI Test"))\n',
        encoding='utf-8',
    )

    app = cli._resolve_app(app_file)

    assert isinstance(app, Component)


def test_cli_resolves_module_app(tmp_path):
    app_file = tmp_path / 'app.py'
    app_file.write_text(
        'import pylage as pl\n\n'
        'app = pl.column(pl.heading("Module App"))\n',
        encoding='utf-8',
    )

    app = cli._resolve_app(app_file)

    assert isinstance(app, Component)


def test_cli_rejects_invalid_app(tmp_path):
    app_file = tmp_path / 'app.py'
    app_file.write_text(
        'app = "not a component"\n',
        encoding='utf-8',
    )

    with pytest.raises(TypeError, match='must define get_app'):
        cli._resolve_app(app_file)


def test_cli_parser():
    parser = cli.build_parser()

    args = parser.parse_args(
        [
            'run',
            'app.py',
            '--host',
            '0.0.0.0',
            '--port',
            '9000',
            '--no-browser',
        ]
    )

    assert args.command == 'run'
    assert args.app == Path('app.py')
    assert args.host == '0.0.0.0'
    assert args.port == 9000
    assert args.no_browser is True
    assert args.no_reload is False


def test_cli_parser_no_reload():
    parser = cli.build_parser()

    args = parser.parse_args(
        [
            'run',
            'app.py',
            '--no-reload',
        ]
    )

    assert args.no_reload is True


def test_cli_main_starts_runtime_and_watcher(monkeypatch, tmp_path):
    app_file = tmp_path / 'app.py'
    app_file.write_text(
        'import pylage as pl\n\n'
        'def get_app():\n'
        '    return pl.column(pl.heading("CLI Runtime Test"))\n',
        encoding='utf-8',
    )

    initial_app = cli._resolve_app(app_file)
    reloaded_app = cli._resolve_app(app_file)
    resolved_apps = iter([initial_app, reloaded_app])

    captured = {
        'runtime': None,
        'watcher': None,
        'opened_url': None,
        'reload_app': None,
    }

    class FakeRuntime:
        def __init__(self, app, *, host, port):
            captured['runtime'] = self
            self.app = app
            self.host = host
            self.port = port
            self.url = 'http://127.0.0.1:9100'
            self.running = True

        def start(self):
            self.running = False

        def reload_app(self, app):
            captured['reload_app'] = app
            self.app = app

        def stop(self):
            self.running = False

    class FakeWatcher:
        def __init__(self, path, callback, error_callback=None):
            captured['watcher'] = self
            self.path = path
            self.callback = callback
            self.error_callback = error_callback
            self.started = False
            self.stopped = False

        def start(self):
            self.started = True
            self.callback()

        def stop(self):
            self.stopped = True

    def fake_resolve(_path):
        return next(resolved_apps)

    monkeypatch.setattr(cli, '_resolve_app', fake_resolve)
    monkeypatch.setattr(cli, 'Runtime', FakeRuntime)
    monkeypatch.setattr(cli, 'FileWatcher', FakeWatcher)
    monkeypatch.setattr(
        cli.webbrowser,
        'open',
        lambda url: captured.update(opened_url=url),
    )

    result = cli.main(
        [
            'run',
            str(app_file),
            '--host',
            '0.0.0.0',
            '--port',
            '9100',
        ]
    )

    assert result == 0
    assert captured['runtime'].app is reloaded_app
    assert captured['runtime'].host == '0.0.0.0'
    assert captured['runtime'].port == 9100
    assert captured['opened_url'] == 'http://127.0.0.1:9100'
    assert captured['watcher'].path == app_file.resolve()
    assert captured['watcher'].started is True
    assert captured['watcher'].stopped is True
    assert captured['reload_app'] is reloaded_app


def test_cli_main_no_browser_and_no_reload(monkeypatch, tmp_path):
    app_file = tmp_path / 'app.py'
    app_file.write_text(
        'import pylage as pl\n\n'
        'app = pl.column(pl.heading("CLI Flags Test"))\n',
        encoding='utf-8',
    )

    class FakeRuntime:
        def __init__(self, app, *, host, port):
            self.url = 'http://127.0.0.1:9200'
            self.running = True

        def start(self):
            self.running = False

        def stop(self):
            self.running = False

    def fail_browser(_url):
        raise AssertionError('browser should not be opened')

    def fail_watcher(*_args):
        raise AssertionError('watcher should not be created')

    monkeypatch.setattr(cli, 'Runtime', FakeRuntime)
    monkeypatch.setattr(cli, 'FileWatcher', fail_watcher)
    monkeypatch.setattr(cli.webbrowser, 'open', fail_browser)

    result = cli.main(
        [
            'run',
            str(app_file),
            '--no-browser',
            '--no-reload',
        ]
    )

    assert result == 0


