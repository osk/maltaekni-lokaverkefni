from generate_pairs import generate_pairs_from_file


def test_generate_pairs_1():
    sentence = generate_pairs_from_file("tests/test_data/1.json")

    assert len(sentence) == 1
    assert (
        sentence[0]["sentence"]
        == "Árið 1980 deildi hann verðlaununum með Walter Gilbert ( f. 1932 ) og Paul Berg ( f. 1926 ) ."  # noqa
    )
    assert sentence[0]["pairs"][0]["a"]["name"] == "Walter Gilbert"
    assert sentence[0]["pairs"][0]["b"]["name"] == "Paul Berg"


def test_generate_pairs_2():
    sentence = generate_pairs_from_file("tests/test_data/2.json")

    assert len(sentence[0]["pairs"]) == 15
    # fragile
    assert sentence[0]["pairs"][14]["a"]["name"] == "Elínu Ólafsdóttur"
    assert sentence[0]["pairs"][14]["b"]["name"] == "Jóni Hjaltalín Ólafssyni"


def test_generate_pairs_3():
    sentence = generate_pairs_from_file("tests/test_data/3.json")
    assert len(sentence) == 0
