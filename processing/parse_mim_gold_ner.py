"""
Data processing for the three MIM-GOLD datasets used in the project:

* MIM-GOLD21.05 (in `base_files`)
* MIM-GOLD-NER 2.0 (in `ner_files`)
* MIM-GOLD-EL (in `el_files`)

Does a four pass parsing:

1. Parse the NER files along with the base files to create a list of entities
   with references to the base files.
2. Group the entities by label, including all references to the entity in all
   files.
3. Match each entry in the EL files with the NER files and fix the JSON files up
   a bit to make them easier to work with.
4. "De-dupe" the processed EL files by consolidating all matches with the same
    label and entity into one entry. Also flags for any entries that have
    multiple matches with different labels. (TODO Is this a thing?)

Along the way we save interesting results as JSON files.
"""

import json
from utils import save_file
from conll import (
    parse_conll_bio,
    consolidate_conll_bio_labels,
)

ner_files = [
    ("adjudications", "../data/MIM-GOLD-2_0/adjudications.txt"),
    ("blog", "../data/MIM-GOLD-2_0/blog.txt"),
    ("books", "../data/MIM-GOLD-2_0/books.txt"),
    ("emails", "../data/MIM-GOLD-2_0/emails.txt"),
    ("fbl", "../data/MIM-GOLD-2_0/fbl.txt"),
    ("laws", "../data/MIM-GOLD-2_0/laws.txt"),
    ("mbl", "../data/MIM-GOLD-2_0/mbl.txt"),
    ("radio_tv_news", "../data/MIM-GOLD-2_0/radio_tv_news.txt"),
    ("school_essays", "../data/MIM-GOLD-2_0/school_essays.txt"),
    ("scienceweb", "../data/MIM-GOLD-2_0/scienceweb.txt"),
    ("webmedia", "../data/MIM-GOLD-2_0/webmedia.txt"),
    ("websites", "../data/MIM-GOLD-2_0/websites.txt"),
    ("written-to-be-spoken", "../data/MIM-GOLD-2_0/written-to-be-spoken.txt"),
]

base_files = [
    ("adjudications", "../data/MIM-GOLD21.05/data/adjucations.tsv"),
    ("blog", "../data/MIM-GOLD21.05/data/blog.tsv"),
    ("books", "../data/MIM-GOLD21.05/data/books.tsv"),
    ("emails", "../data/MIM-GOLD21.05/data/emails.tsv"),
    ("fbl", "../data/MIM-GOLD21.05/data/fbl.tsv"),
    ("laws", "../data/MIM-GOLD21.05/data/laws.tsv"),
    ("mbl", "../data/MIM-GOLD21.05/data/mbl.tsv"),
    ("radio_tv_news", "../data/MIM-GOLD21.05/data/radio-tv-news.tsv"),
    ("school_essays", "../data/MIM-GOLD21.05/data/school-essays.tsv"),
    ("scienceweb", "../data/MIM-GOLD21.05/data/scienceweb.tsv"),
    ("webmedia", "../data/MIM-GOLD21.05/data/webmedia.tsv"),
    ("websites", "../data/MIM-GOLD21.05/data/websites.tsv"),
    ("written-to-be-spoken", "../data/MIM-GOLD21.05/data/written-to-be-spoken.tsv"),
]

el_files = [
    ("adjudications", "../data/MIM-GOLD-EL/adjudications_release_candidates.json"),
    ("blog", "../data/MIM-GOLD-EL/blog_release_candidates.json"),
    ("books", "../data/MIM-GOLD-EL/books_release_candidates.json"),
    ("emails", "../data/MIM-GOLD-EL/emails_release_candidates.json"),
    ("fbl", "../data/MIM-GOLD-EL/fbl_release_candidates.json"),
    ("laws", "../data/MIM-GOLD-EL/laws_release_candidates.json"),
    ("mbl", "../data/MIM-GOLD-EL/mbl_release_candidates.json"),
    ("radio_tv_news", "../data/MIM-GOLD-EL/radio_tv_news_release_candidates.json"),
    ("school_essays", "../data/MIM-GOLD-EL/school_essays_release_candidates.json"),
    ("scienceweb", "../data/MIM-GOLD-EL/scienceweb_release_candidates.json"),
    ("webmedia", "../data/MIM-GOLD-EL/webmedia_release_candidates.json"),
    ("websites", "../data/MIM-GOLD-EL/websites_release_candidates.json"),
    (
        "written-to-be-spoken",
        "../data/MIM-GOLD-EL/written-to-be-spoken_release_candidates.json",
    ),
]


def append_base_file(parsed, base_content):
    """Finds and appends information from the base file to the parsed file. Makes
    use of the fact that two files are structured the exact same way."""
    for entity in parsed:
        base_info = []
        for line in entity["lines"]:
            # line is not zero indexed
            target_line = base_content[line - 1]
            base_info.append(target_line)
        entity["base_info"] = base_info
    return parsed


def restructure_el_file(el_file):
    """
    Restructures the EL file to be a bit easier to work with. The original file
    is a list of objects with an index key, drop that and just index the actual objects.
    """
    fixed = []
    for index in el_file:
        fixed.append(el_file[index])
    return fixed


def parse_file(file, category, base_file):
    """Parse the NER file, consolidate the labels, and append the base file info."""
    with open(file, "rb") as input_file:
        content = input_file.read().decode("utf8")
    with open(base_file, "rb") as input_file:
        base_content = input_file.read().decode("utf8").splitlines()
    parsed = parse_conll_bio(content, category)
    consolidated = consolidate_conll_bio_labels(parsed)
    consolidated_with_base = append_base_file(consolidated, base_content)

    return consolidated_with_base


def parse_files(ner_files, base_files):
    """Parse all NER files along with the base files and return the result"""
    results = []
    for category, file in ner_files:
        print("Parsing", category)
        base_file = [item[1] for item in base_files if item[0] == category]
        results.extend(parse_file(file, category, base_file[0]))

    return results


def group_entites_by_label(list_of_entities):
    """Group parsed NER list by entities."""
    groups = {}
    for item in list_of_entities:
        entity = item["entity"]
        if entity not in groups:
            groups[entity] = []
        groups[entity].append(item)

    return groups


def transform_el_predicition_to_json(prediction):
    """
    Transforms an EL prediction to a JSON object.
    Format is some almost JSON string, e.g.
    "[[{'text': 'Héraðsdómar Íslands >> is', 'score': tensor(-0.0588)}]]"
    """
    fixed_apostrophe = (
        prediction.replace("'text'", '"text"')
        .replace("'score'", '"score"')
        .replace('"text": \'', '"text": "')
        .replace('\', "score"', '", "score"')
    )
    replace_tensor = fixed_apostrophe.replace("tensor(", "").replace(")}", "}")  # lazy

    # horrible late night hack to escape inner quotes
    y = []
    for i in replace_tensor.split('"text": "'):
        x = []
        for j in i.split('", "score"'):
            x.append(j.replace('"', '\\"'))
        y.append('", "score"'.join(x))
    escape_quotes = '"text": "'.join(y)

    try:
        parsed = json.loads(escape_quotes)[0]
    except json.decoder.JSONDecodeError:
        raise Exception("Error parsing", replace_tensor, "original", prediction)

    for item in parsed:
        split = item["text"].split(" >> ")
        item["text"] = {"value": split[0], "lang": split[1]}

    return parsed


def match_el_with_ner_all(el_files, ner_all):
    """Match the EL data with the NER data."""
    results = []
    for category, file in el_files:
        print("Matching", category)
        with open(file, "rb") as input_file:
            el_content = json.load(input_file)
        el_content = restructure_el_file(el_content)
        for entry in el_content:
            # Find the NER matches
            matches = [ner_all[item] for item in ner_all if item == entry["name"]]
            entry["matches"] = matches

            # Make unlabelled a true boolean
            entry["unlabelled"] = True if entry["unlabelled"] == "True" else False

            entry["prediction"] = transform_el_predicition_to_json(entry["prediction"])
            results.append(entry)

    return results


def dedupe_el(el_data):
    """Remove duplicate NER entries."""
    for entry in el_data:
        deduped = []
        for match in entry["matches"]:

            matches = next(
                (
                    item
                    for item in deduped
                    if item["label"] == match["label"]
                    and item["entity"] == match["entity"]
                ),
                None,
            )

            if not matches:
                deduped.append(match[0])
        if len(deduped) > 1:
            print("More than one label for", entry["name"], deduped)
        entry["matches"] = deduped
    return el_data


if __name__ == "__main__":
    result = parse_files(ner_files, base_files)
    save_file(result, "../data/output/mim_gold_ner_all_raw.json")

    grouped = group_entites_by_label(result)
    save_file(grouped, "../data/output/mim_gold_ner_all_grouped.json")

    el_result = match_el_with_ner_all(el_files, grouped)

    # This is a big file, around 300MB
    # save_file(el_result, "../data/output/mim_gold_el_with_ner_all.json")

    el_deduped = dedupe_el(el_result)
    save_file(el_result, "../data/output/mim_gold_el_with_ner_deduped.json")
