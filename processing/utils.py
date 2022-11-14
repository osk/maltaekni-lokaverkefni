import json


def save_file(data, file):
    """Save the data to an indented JSON file with UTF-8 strings."""
    json_str = json.dumps(data, indent=4, ensure_ascii=False)

    with open(file, "w", encoding="utf-8") as output_file:
        output_file.write(json_str)
