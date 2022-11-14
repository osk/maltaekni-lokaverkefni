# Parsing and data manipulation

Python project to parse and manipulate data.

```bash
# install
poetry install

# lint
poetry run flake8

# test
poetry run pytest

# test watch
poetry run ptw

# test & collect coverage
poetry run coverage run -m pytest

# coverage report
poetry run coverage report -m
```

To generate data, run in order:

```bash
python parse_mim_gold_ner
python generate_pairs
```
