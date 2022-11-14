"""
Pair generator from the EL dataset matched with the NER dataset via
`parse_mim_gold_ner`. Uses the JSON generated in `mim_golg_el_with_ner_deduped`.

An entity is:

* `name`, name of the entity
* `label`, label of the entity from the defined list from NER dataset
* `index`, from the EL data so the entity can be back referenced
* `base_info`, array of CoNLL strings with PoS tagging and lemma
* `wiki`, the correct *Icelandic* wiki entry or None (`correct_wiki` from EL dataset)
* `predictions`, array of *Icelandic* predictions from the the EL dataset, empty if
  `wiki` is defined

A pair is:

* `a`, one entity in the pair
* `b`, other entity in the pair, or None if the sentence only contains one entity
* `sentence`, the sentence where `a` and `b` appear
* `id`, object that defines an unique key for the sentence from the EL dataset,
  (section, sentence_id), e.g.
  { "id": "adjudications-0", "section": "adjudications", "sentence_id": 0 }

No semantic meaning in which name is in `a` or `b` if both are defined.
"""

import json
import itertools

from utils import save_file


def clean_sentence(sentence):
    return sentence.replace("[START] ", "").replace(" [END]", "").strip()


def generate_id(item):
    return {
        "id": item["section"] + "-" + str(item["sentence_id"]),
        "section": item["section"],
        "sentence_id": item["sentence_id"],
    }


def generate_pair_entity(item):
    # if we get this something is wrong in our generated data
    if len(item["matches"]) == 0:
        return None
    name = item["name"]
    index = item["index"]
    first_match = item["matches"][0]
    label = first_match["label"]
    base_info = first_match["base_info"]
    wiki_split = item["correct_wiki"].split(" >> ")
    wiki = ""
    predictions = []

    if len(wiki_split) == 2 and wiki_split[1] == "is":
        wiki = wiki_split[0]

    predictions = list(filter(lambda i: i["text"]["lang"] == "is", item["prediction"]))

    return {
        "name": name,
        "label": label,
        "index": index,
        "base_info": base_info,
        "wiki": wiki,
        "predictions": predictions,
    }


def generate_pairs(data):
    """
    Generates one or more pairs from the given data.
    """
    assert len(data) >= 1

    # Guards for data consistency
    prime_sentence = None
    prime_id = None

    # List of all candidates we generate pairs from
    candidates = []

    for item in data:
        sentence = clean_sentence(item["sentence"])
        id = generate_id(item)

        if prime_id is None:
            prime_id = id
            prime_sentence = sentence
        else:
            if prime_id["id"] != id["id"] or prime_sentence != sentence:
                # TODO Should raise
                print(
                    "items mismatch", id["id"], prime_id["id"], sentence, prime_sentence
                )

        candidate = generate_pair_entity(item)

        if candidate:
            candidates.append(candidate)
        else:
            # TODO Should raise
            print("candidate has no matches", prime_id["id"])

    pairs = []

    # Generates (N*(N-1))/2 pairs or 1 if a single candidate
    if len(candidates) == 0:
        return []
    elif len(candidates) > 1:
        combinations = list(itertools.combinations(candidates, 2))
    else:
        combinations = [candidates]

    for candidate_pair in combinations:
        pairs.append(
            {
                "sentence": prime_sentence,
                "id": prime_id,
                "a": candidate_pair[0],
                "b": candidate_pair[1] if len(candidate_pair) > 1 else None,
            }
        )

    return pairs


def collect_data_and_generate_pairs(data):
    """Collect all data for each sentence, then generate pairs from them."""
    pairs = []

    last = None
    collected = []
    # TODO make more pythonic
    for item in data:
        # Key for sentence, one or more datum
        current = (item["section"], item["sentence_id"])

        # Assumes all sentences are located one after another, which could be wrong.
        # This should be a two-pass process:
        # 1) collect *all* sentences
        # 2) generate pairs from them
        if last == current or last is None:
            collected.append(item)
        else:
            pairs = pairs + generate_pairs(collected)
            collected = [item]

        last = current
    # Generate the last pair
    pairs = pairs + generate_pairs(collected)

    return pairs


def generate_pairs_from_file(file, max=None):
    with open(file, "rb") as input_file:
        data = json.load(input_file)

    if max is not None:
        data = data[:max]

    pairs = collect_data_and_generate_pairs(data)

    return pairs


if __name__ == "__main__":
    file = "../data/output/mim_gold_el_with_ner_deduped.json"

    pairs = generate_pairs_from_file(file)

    save_file(pairs, "../data/output/pairs/pairs.json")

    # save a csv for debug/glancing data
    csv_data = "sentence_id;a_name;a_label;b_name;b_label\n"

    for pair in pairs:
        id = pair["id"]["id"]
        sentence = pair["sentence"]
        a_name = pair["a"]["name"]
        a_label = pair["a"]["label"]
        b_name = pair["b"]["name"] if pair["b"] else ""
        b_label = pair["b"]["label"] if pair["b"] else ""
        csv_data += "{0};{1};{2};{3};{4};{5}\n".format(
            id, a_name, a_label, b_name, b_label, sentence
        )

    with open("../data/output/pairs/pairs.csv", "w", encoding="utf-8") as output_file:
        output_file.write(csv_data)
