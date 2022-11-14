from parse_mim_gold_ner import transform_el_predicition_to_json


def test_transform_el_predicition_to_json_single():
    input = """[[{'text': 'Héraðsdómar Íslands >> is', 'score': tensor(-0.0588)}]]"""
    transformed = transform_el_predicition_to_json(input)

    assert transformed == [
        {"text": {"value": "Héraðsdómar Íslands", "lang": "is"}, "score": -0.0588}
    ]


def test_transform_el_predicition_to_json_fail():
    input = """
    [[
      {\'text\': "Llista d\'universitats d\'Espanya >> ca", \'score\': tensor(-1.3115)}
    ]]"""
    transformed = transform_el_predicition_to_json(input)

    assert transformed == [
        {
            "text": {"value": "Llista d'universitats d'Espanya", "lang": "ca"},
            "score": -1.3115,
        }
    ]


def test_transform_el_predicition_to_json_fail2():
    input = """
    [[
      {'text': 'LÎle de l'épouvante >> fr', 'score': tensor(-1.3322)},
      {'text': 'Lisola del sole >> it', 'score': tensor(-1.6885)},
      {'text': 'LÎle de l'étrange >> fr', 'score': tensor(-1.7623)},
      {'text': 'LÎle de la mort >> fr', 'score': tensor(-1.9195)},
      {'text': 'LÎle de lOubli >> fr', 'score': tensor(-3.1787)}
    ]]
    """
    transformed = transform_el_predicition_to_json(input)

    assert transformed == [
        {"text": {"value": "LÎle de l'épouvante", "lang": "fr"}, "score": -1.3322},
        {"text": {"value": "Lisola del sole", "lang": "it"}, "score": -1.6885},
        {"text": {"value": "LÎle de l'étrange", "lang": "fr"}, "score": -1.7623},
        {"text": {"value": "LÎle de la mort", "lang": "fr"}, "score": -1.9195},
        {"text": {"value": "LÎle de lOubli", "lang": "fr"}, "score": -3.1787},
    ]


def test_transform_el_predicition_to_json_multi():
    input = """
    [[
      {'text': 'Héraðsdómar Íslands >> is', 'score': tensor(-0.0588)},
      {'text': 'Héraðsdómur Reykjavíkur >> is', 'score': tensor(-0.6082)},
      {'text': 'Höfuðborgarsvæðið >> is', 'score': tensor(-0.9610)},
      {'text': 'Héraðsdómur >> is', 'score': tensor(-1.0113)},
      {'text': 'Héraðsvötn >> is', 'score': tensor(-1.0859)}]]
      """
    transformed = transform_el_predicition_to_json(input)

    assert transformed == [
        {"text": {"value": "Héraðsdómar Íslands", "lang": "is"}, "score": -0.0588},
        {"text": {"value": "Héraðsdómur Reykjavíkur", "lang": "is"}, "score": -0.6082},
        {"text": {"value": "Höfuðborgarsvæðið", "lang": "is"}, "score": -0.9610},
        {"text": {"value": "Héraðsdómur", "lang": "is"}, "score": -1.0113},
        {"text": {"value": "Héraðsvötn", "lang": "is"}, "score": -1.0859},
    ]


def test_transform_el_predicition_to_json_fail3():
    input = """
    [[
      {'text': \"Phoenix (système d'arcade) >> fr\", 'score': tensor(-1.9563)},
      {'text': 'Arizonas \"Coyotes\" >> lv', 'score': tensor(-2.2037)}
    ]]
    """

    transformed = transform_el_predicition_to_json(input)

    assert transformed == [
        {
            "text": {"value": "Phoenix (système d'arcade)", "lang": "fr"},
            "score": -1.9563,
        },
        {"text": {"value": 'Arizonas "Coyotes"', "lang": "lv"}, "score": -2.2037},
    ]
