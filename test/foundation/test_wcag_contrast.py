from __future__ import annotations

import pytest

from pylage.UI.tokens import (
    COLORS,
    contrast_ratio,
    meets_wcag_contrast,
    theme_contrast_results,
    validate_wcag_contrast,
)


def test_black_and_white_have_maximum_wcag_contrast():
    assert contrast_ratio('#000000', '#ffffff') == pytest.approx(21.0)


def test_contrast_ratio_is_symmetric():
    forward = contrast_ratio('#123456', '#ffffff')
    reverse = contrast_ratio('#ffffff', '#123456')

    assert forward == pytest.approx(reverse)


def test_identical_colors_have_ratio_one():
    assert contrast_ratio('#336699', '#336699') == pytest.approx(1.0)


def test_short_hex_colors_are_supported():
    assert contrast_ratio('#000', '#fff') == pytest.approx(21.0)


def test_invalid_hex_color_raises_value_error():
    with pytest.raises(ValueError):
        contrast_ratio('not-a-color', '#ffffff')


def test_non_string_color_raises_type_error():
    with pytest.raises(TypeError):
        contrast_ratio(None, '#ffffff')


def test_wcag_aa_normal_text_threshold():
    assert meets_wcag_contrast(
        '#000000',
        '#ffffff',
        level='AA',
    )

    assert not meets_wcag_contrast(
        '#777777',
        '#ffffff',
        level='AA',
    )


def test_wcag_aa_large_text_threshold():
    assert meets_wcag_contrast(
        '#777777',
        '#ffffff',
        level='AA',
        large_text=True,
    )


def test_wcag_aaa_normal_text_threshold():
    assert meets_wcag_contrast(
        '#000000',
        '#ffffff',
        level='AAA',
    )

    assert not meets_wcag_contrast(
        '#777777',
        '#ffffff',
        level='AAA',
    )


def test_wcag_aaa_large_text_threshold():
    assert meets_wcag_contrast(
        '#000000',
        '#ffffff',
        level='AAA',
        large_text=True,
    )


def test_invalid_wcag_level_raises_value_error():
    with pytest.raises(ValueError):
        meets_wcag_contrast(
            '#000000',
            '#ffffff',
            level='A',
        )


def test_default_theme_returns_numeric_contrast_results():
    results = theme_contrast_results()

    assert results
    assert all(isinstance(value, float) for value in results.values())
    assert all(value >= 1.0 for value in results.values())


def test_default_theme_passes_wcag_validation():
    assert validate_wcag_contrast()


def test_default_theme_contrast_pairs_are_numeric():
    results = theme_contrast_results(COLORS)

    expected = {
        'text_on_background',
        'text_on_surface',
        'muted_text_on_background',
        'primary_contrast',
        'secondary_contrast',
    }

    assert expected == set(results)


def test_failing_custom_theme_returns_false():
    colors = dict(COLORS)
    colors['text'] = '#ffffff'
    colors['background'] = '#ffffff'

    assert not validate_wcag_contrast(colors)
