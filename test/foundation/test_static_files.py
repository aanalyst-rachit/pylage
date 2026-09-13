import gzip
from pathlib import Path
from urllib.request import Request, urlopen

from pylage.ENGINE.runtime.server import LocalServer
from pylage.ENGINE.runtime.static import content_type_for, prepare_static_response


def test_content_type_for_common_static_files():
    assert content_type_for(Path("styles.css")) == "text/css"
    assert content_type_for(Path("app.js")) in {"text/javascript", "application/javascript"}
    assert content_type_for(Path("icon.svg")) == "image/svg+xml"
    assert content_type_for(Path("data.unknown")) == "application/octet-stream"


def test_prepare_static_response_sets_cache_and_length_headers():
    content = b"body { margin: 0; }"

    body, headers = prepare_static_response(
        content,
        "text/css",
        cache_control="public, max-age=3600",
    )

    assert body == content
    assert headers["Content-Type"] == "text/css"
    assert headers["Cache-Control"] == "public, max-age=3600"
    assert headers["Content-Length"] == str(len(content))
    assert "Content-Encoding" not in headers


def test_prepare_static_response_gzips_compressible_content():
    content = (b"body { margin: 0; padding: 0; }\n" * 100)

    body, headers = prepare_static_response(
        content,
        "text/css",
        accept_encoding="gzip",
    )

    assert headers["Content-Encoding"] == "gzip"
    assert headers["Vary"] == "Accept-Encoding"
    assert headers["Content-Length"] == str(len(body))
    assert gzip.decompress(body) == content


def test_prepare_static_response_respects_gzip_quality_zero():
    content = (b"body { margin: 0; }\n" * 100)

    body, headers = prepare_static_response(
        content,
        "text/css",
        accept_encoding="gzip; q=0",
    )

    assert body == content
    assert "Content-Encoding" not in headers
    assert "Vary" not in headers
    assert headers["Content-Length"] == str(len(content))


def test_local_server_serves_static_file_with_headers(tmp_path: Path):
    index = tmp_path / "index.html"
    index.write_text("<html>index</html>", encoding="utf-8")
    css = tmp_path / "styles.css"
    css.write_text("body { margin: 0; }", encoding="utf-8")

    server = LocalServer(tmp_path)
    server.start()

    try:
        with urlopen(server.url + "styles.css") as response:
            body = response.read()

            assert response.status == 200
            assert response.headers["Content-Type"].split(";", 1)[0] == "text/css"
            assert response.headers["Cache-Control"] == "public, max-age=3600"
            assert response.headers["Content-Length"] == str(len(body))
            assert body == css.read_bytes()

        with urlopen(server.url) as response:
            assert response.headers["Cache-Control"] == "no-cache"
    finally:
        server.stop()


def test_local_server_gzip_static_response(tmp_path: Path):
    content = (b"body { margin: 0; padding: 0; }\n" * 100)
    (tmp_path / "styles.css").write_bytes(content)

    server = LocalServer(tmp_path)
    server.start()

    try:
        request = Request(
            server.url + "styles.css",
            headers={"Accept-Encoding": "gzip"},
        )

        with urlopen(request) as response:
            body = response.read()

            assert response.status == 200
            assert response.headers["Content-Encoding"] == "gzip"
            assert response.headers["Vary"] == "Accept-Encoding"
            assert response.headers["Content-Length"] == str(len(body))
            assert gzip.decompress(body) == content
    finally:
        server.stop()
