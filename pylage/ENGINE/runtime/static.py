from __future__ import annotations

import gzip
import mimetypes
from pathlib import Path

_COMPRESSIBLE_TYPES = {
    "text/css",
    "text/html",
    "text/javascript",
    "application/javascript",
    "application/json",
    "application/xml",
    "image/svg+xml",
}


def content_type_for(path: Path) -> str:
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def _accepts_gzip(accept_encoding: str) -> bool:
    for item in accept_encoding.split(","):
        parts = [part.strip() for part in item.split(";")]
        if not parts:
            continue

        encoding = parts[0].lower()
        if encoding != "gzip":
            continue

        quality = 1.0
        for parameter in parts[1:]:
            if "=" not in parameter:
                continue
            name, value = parameter.split("=", 1)
            if name.strip().lower() != "q":
                continue
            try:
                quality = float(value.strip())
            except ValueError:
                quality = 0.0
            break

        return quality > 0.0

    return False


def prepare_static_response(
    content: bytes,
    content_type: str,
    *,
    accept_encoding: str = "",
    cache_control: str = "public, max-age=3600",
) -> tuple[bytes, dict[str, str]]:
    headers = {
        "Content-Type": content_type,
        "Cache-Control": cache_control,
    }

    media_type = content_type.split(";", 1)[0].strip().lower()

    if (
        _accepts_gzip(accept_encoding)
        and media_type in _COMPRESSIBLE_TYPES
        and len(content) >= 256
    ):
        compressed = gzip.compress(content)
        if len(compressed) < len(content):
            content = compressed
            headers["Content-Encoding"] = "gzip"
            headers["Vary"] = "Accept-Encoding"

    headers["Content-Length"] = str(len(content))
    return content, headers
