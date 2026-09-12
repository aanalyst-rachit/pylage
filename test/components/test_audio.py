from pylage.ENGINE import Audio
from pylage.ENGINE.core.renderer import render


def test_audio_creates_audio_component():
    audio = Audio()

    assert audio.type == "Audio"


def test_audio_renders_as_audio():
    audio = Audio(
        src="song.mp3",
        controls=True,
    )

    html = render(audio)

    assert "<audio" in html
    assert 'src="song.mp3"' in html
    assert "controls" in html
    assert "</audio>" in html


def test_audio_supports_props():
    audio = Audio(
        src="track.mp3",
        class_name="player",
        title="Music",
        controls=True,
    )

    html = render(audio)

    assert 'src="track.mp3"' in html
    assert 'class="player"' in html
    assert 'title="Music"' in html
    assert "controls" in html
import pytest

def test_audio_rejects_dangerous_src_scheme():
    with pytest.raises(ValueError, match="unsafe URL scheme"):
        render(Audio(src="javascript:alert(1)"))

def test_audio_rejects_dangerous_src_with_leading_control_whitespace():
    with pytest.raises(ValueError, match="unsafe URL scheme"):
        render(Audio(src=chr(9) + chr(10) + "javascript:alert(1)"))

def test_audio_allows_safe_src_urls():
    for src in ("song.mp3", "/assets/song.mp3", "//cdn.example/song.mp3", "https://example.com/song.mp3"):
        html = render(Audio(src=src))
        assert ("src=\"" + src + "\"") in html
