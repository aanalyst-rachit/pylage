from __future__ import annotations

from typing import Any

import msgpack

from pylage.ENGINE.core.protocol import (
    EventMessage,
    EventMessageResponse,
    ThemeUpdateMessage,
    TreeAddMessage,
    TreeClearMessage,
    TreeMoveMessage,
    TreeRemoveMessage,
    TreeReplaceMessage,
    TreeSetChildrenMessage,
    UpdateMessage,
)

_MESSAGE_TYPES = {
    'event': EventMessage,
    'response': EventMessageResponse,
    'update': UpdateMessage,
    'theme_update': ThemeUpdateMessage,
    'tree_add': TreeAddMessage,
    'tree_move': TreeMoveMessage,
    'tree_replace': TreeReplaceMessage,
    'tree_set_children': TreeSetChildrenMessage,
    'tree_clear': TreeClearMessage,
    'tree_remove': TreeRemoveMessage,
}


def encode_message(message: Any) -> bytes:
    to_dict = getattr(message, 'to_dict', None)
    if not callable(to_dict):
        raise TypeError('Message must provide to_dict().')
    return msgpack.packb(to_dict(), use_bin_type=True)


def decode_message(data: bytes | bytearray | memoryview) -> Any:
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError('Binary protocol data must be bytes-like.')

    decoded = msgpack.unpackb(data, raw=False)
    if not isinstance(decoded, dict):
        raise ValueError('Binary protocol message must decode to a dictionary.')

    message_type = decoded.get('type')
    message_class = _MESSAGE_TYPES.get(message_type)
    if message_class is None:
        raise ValueError(f'Unknown protocol message type: {message_type!r}.')

    return message_class.from_dict(decoded)


def encode_dict(data: dict[str, Any]) -> bytes:
    if not isinstance(data, dict):
        raise TypeError('Protocol data must be a dictionary.')
    return msgpack.packb(data, use_bin_type=True)


def decode_dict(data: bytes | bytearray | memoryview) -> dict[str, Any]:
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError('Binary protocol data must be bytes-like.')

    decoded = msgpack.unpackb(data, raw=False)
    if not isinstance(decoded, dict):
        raise ValueError('Binary protocol message must decode to a dictionary.')
    return decoded
