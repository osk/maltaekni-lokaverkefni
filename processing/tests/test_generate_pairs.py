from generate_pairs import generate_pairs_from_file


def test_generate_pairs_1():
    pairs = generate_pairs_from_file("tests/test_data/1.json")
    print(pairs)
    assert len(pairs) == 1
    assert (
        pairs[0]["sentence"]
        == "Árið 1980 deildi hann verðlaununum með Walter Gilbert ( f. 1932 ) og Paul Berg ( f. 1926 ) ."  # noqa
    )
    assert pairs[0]["a"]["name"] == "Walter Gilbert"
    assert pairs[0]["b"]["name"] == "Paul Berg"


def test_generate_pairs_2():
    pairs = generate_pairs_from_file("tests/test_data/2.json")
    assert len(pairs) == 15
    # fragile
    assert pairs[14]["a"]["name"] == "Elínu Ólafsdóttur"
    assert pairs[14]["b"]["name"] == "Jóni Hjaltalín Ólafssyni"


def test_generate_pairs_3():
    pairs = generate_pairs_from_file("tests/test_data/3.json")
    assert len(pairs) == 1
    assert pairs[0]["a"]["name"] == "Héraðsdóms Reykjavíkur"
    assert pairs[0]["b"] is None
