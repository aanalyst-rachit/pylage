import json

import pytest

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
from pylage.ENGINE.core.protocol_codec import decode_message, encode_message


@pytest.mark.parametrize(
    'message',
    [
        EventMessage('abc123', 'click', {'value': 'hello'}),
        EventMessageResponse.success({'value': 42}),
        EventMessageResponse.failure('boom'),
        UpdateMessage('heading-1', {'text': 'Hello'}, ['hidden'], {'text': {'kind': 'string'}}),
        ThemeUpdateMessage('body{margin:0}'),
        TreeAddMessage('root', [{'id': 'child', 'type': 'heading'}], 0),
        TreeMoveMessage('child', 'old-root', 'new-root'),
        TreeReplaceMessage('root', 'old', {'id': 'new', 'type': 'button'}, 2),
        TreeSetChildrenMessage('root', [{'id': 'a'}, {'id': 'b'}]),
        TreeClearMessage('root', ['a', 'b']),
        TreeRemoveMessage('root', ['a', 'b']),
    ],
)
def test_binary_protocol_round_trip(message):
    encoded = encode_message(message)

    assert isinstance(encoded, bytes)
    assert encoded

    decoded = decode_message(encoded)

    assert decoded == message


def test_binary_protocol_preserves_changed_props_only():
    message = UpdateMessage(
        'component-1',
        {'text': 'changed'},
        ['class_name'],
        {'text': {'kind': 'string'}},
    )

    decoded = decode_message(encode_message(message))

    assert decoded.props == {'text': 'changed'}
    assert decoded.remove_props == ['class_name']
    assert decoded.prop_meta == {'text': {'kind': 'string'}}


def test_binary_update_is_smaller_than_compact_json():
    message = UpdateMessage(
        'component-123456',
        {
            'text': 'A reasonably long changed value',
            'disabled': True,
            'aria-label': 'Save changes',
        },
        ['old-class'],
        {
            'text': {'kind': 'string'},
            'disabled': {'kind': 'boolean'},
        },
    )

    json_payload = json.dumps(message.to_dict(), separators=(',', ':')).encode()
    binary_payload = encode_message(message)

    assert len(binary_payload) < len(json_payload)
