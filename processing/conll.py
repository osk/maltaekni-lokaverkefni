import re

"""
CoNLL parser for MIM-GOLD-*.

Nomenclature:

For the input:
"Litla	B-Miscellaneous
ferðafélagið	I-Miscellaneous
er	O"

* "Litla ferðafélagið" is the entity
  * "Litla" is the Beginning (B) of the label
  * "ferðafélagið" is the Inside (I) of the label
  * B and I we call "markers"
  * "B-Miscellaneous" we call the "marked label"
* "Miscellaneous" is the label of the entity
* "er" is an Outside (think it stands for that) (O) label

(This might be wrong, but it is what I think it is.)
"""


def parse_conll_bio_marked_label(str):
    """
    Return marked label, marker, and label of string.
    E.g. "B-Miscellaneous" -> ("B", "Miscellaneous")
    Does not validate the input, it only parses the string according to the
    expected format.
    Raises an exception if the input is not valid.
    Returns None if not a marked label.
    """
    if str == "":
        return None

    split = str.split("-")
    if len(split) > 2:
        raise Exception("marked label has more than one dash: " + str)

    if not re.match(r"^[A-Z]$", split[0]):
        raise Exception("marked label does not start with a capital letter: " + str)

    marker = split[0]
    label = split[1] if len(split) > 1 else None

    return (marker, label)


def parse_conll_bio_line(line, line_number, category=None):
    """
    Parse a single line, expecting the input to be a line with a single tab that
    separates the entity from the label.
    Returns a verbose dictionary with the parsed data along with passed metadata
    about line number and category.
    """
    split = line.split("\t")
    if len(split) != 2:
        return None

    entity, marked_label = split
    marker, label = parse_conll_bio_marked_label(marked_label)
    return {
        "entity": entity,
        "label": label,
        "marker": marker,
        "line": line_number,
        "category": category,
    }


def parse_conll_bio(str, category=None):
    """Parse the whole file."""
    lines = str.split("\n")
    results = []
    line_number = 1
    for line in lines:
        results.append(parse_conll_bio_line(line, line_number, category))
        line_number += 1
    return results


def consolidate_conll_bio_labels(parsed):
    """
    Consolidate the parsed CoNLL BIO entity/labels into a list of entities with
    full labels.
    Does some validation.
    """
    entities = []
    entity = None
    for line in parsed:
        if line is None:
            if entity is not None:
                entities.append(entity)
                entity = None
            continue
        if line["marker"] == "B":
            if entity is not None:
                entities.append(entity)
                entity = None
            entity = {
                "label": line["label"],
                "entity": line["entity"],
                "lines": [line["line"]],
                "category": line["category"],
            }
        elif line["marker"] == "I":
            if entity is None:
                raise Exception(
                    "I marker without B marker in "
                    + line["category"]
                    + " on line "
                    + str(line["line"])
                )
            if entity["label"] != line["label"]:
                raise Exception(
                    "I marker with different label than B marker in "
                    + line["category"]
                    + " on line "
                    + str(line["line"])
                )
            entity["entity"] += " " + line["entity"]
            entity["lines"].append(line["line"])
        elif line["marker"] == "O":
            if entity is not None:
                entities.append(entity)
                entity = None
        else:
            raise Exception("Unknown marker: " + line["marker"])
    return entities
