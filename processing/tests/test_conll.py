from conll import (
    parse_conll_bio,
    parse_conll_bio_line,
    parse_conll_bio_marked_label,
    consolidate_conll_bio_labels,
)
from pytest import raises


def test_parse_conll_bio_marked_label_type():
    (marker, label) = parse_conll_bio_marked_label("B-Miscellaneous")
    assert marker == "B"
    assert label == "Miscellaneous"


def test_parse_conll_bio_marked_label_empty_str():
    result = parse_conll_bio_marked_label("")
    assert result is None


def test_parse_conll_bio_marked_label_type_outside():
    (marker, label) = parse_conll_bio_marked_label("O")
    assert marker == "O"
    assert label is None


def test_parse_conll_bio_marked_label_empty_label():
    (marker, label) = parse_conll_bio_marked_label("X-")
    assert label == ""


def test_parse_conll_bio_marked_label_invalid_marked_label():
    with raises(Exception):
        parse_conll_bio_marked_label("B-Miscellaneous-Invalid")


def test_parse_conll_bio_marked_label_not_start_letter():
    with raises(Exception):
        parse_conll_bio_marked_label("1-Foo")


def test_parse_conll_bio_valid():
    parsed = parse_conll_bio("Fossavatnsgangan	B-Miscellaneous", "Foo")
    print(parsed)
    assert parsed[0] == {
        "entity": "Fossavatnsgangan",
        "label": "Miscellaneous",
        "marker": "B",
        "line": 1,
        "category": "Foo",
    }


def test_parse_conll_bio_line_empty():
    result = parse_conll_bio_line("", 1)
    assert result is None


def test_parse_conll_bio():
    str = """Litla	B-Miscellaneous
ferðafélagið	I-Miscellaneous
er	O"""
    parsed = parse_conll_bio(str, "foo")
    assert parsed == [
        {
            "entity": "Litla",
            "label": "Miscellaneous",
            "marker": "B",
            "line": 1,
            "category": "foo",
        },
        {
            "entity": "ferðafélagið",
            "label": "Miscellaneous",
            "marker": "I",
            "line": 2,
            "category": "foo",
        },
        {
            "entity": "er",
            "label": None,
            "marker": "O",
            "line": 3,
            "category": "foo",
        },
    ]


def test_consolidate_conll_bio_labels():
    str = """Litla	B-Miscellaneous
ferðafélagið	I-Miscellaneous
er	O"""
    parsed = parse_conll_bio(str, "foo")
    consolidated = consolidate_conll_bio_labels(parsed)
    assert consolidated == [
        {
            "entity": "Litla ferðafélagið",
            "label": "Miscellaneous",
            "lines": [1, 2],
            "category": "foo",
        }
    ]


def test_consolidate_conll_bio_labels_invalid_solo_i():
    parsed = parse_conll_bio("Foo	I-Bar")
    with raises(Exception):
        consolidate_conll_bio_labels(parsed)


def test_consolidate_conll_bio_labels_invalid_i_follows_b():
    parsed = parse_conll_bio("Foo	B-Bar\nFee	I-Foo")
    with raises(Exception):
        consolidate_conll_bio_labels(parsed)


def test_consolidate_conll_bio_labels_invalid_unknown_marker():
    parsed = parse_conll_bio("Foo	X-Bar")
    with raises(Exception):
        consolidate_conll_bio_labels(parsed)
