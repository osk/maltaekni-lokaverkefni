# Parsing

Notes on parsing the data required for this project.

## Parsing MIM-GOLD data

See [`processing` folder and comments in files](./../processing/).

Input data is saved in [`data/`](../data/) and is checked in to make it easier to generate output data.

Output is saved in [`data/output`](../data/output/). Each file is large (>10MB) so it's not checked into git.

What is the final result of the "parsing phase" is in `pairs.json`, a file with 34.387 pairs from 9.322 sentences (does that make sense? shouldn't it be more?). The structure is an array of objects with the sentence, the sentence id and an array of the pairs. Example from the first sentence (not all pairs shown):

```json
[
  {
    "sentence": "Ár 2008 , föstudaginn 6. júní , er á dómþingi Héraðsdóms Reykjavíkur , sem háð er í Dómhúsinu við Lækjartorg af Allani Vagni Magnússyni héraðsdómara , ásamt meðdómsmönnunum Elínu Ólafsdóttur og Jóni Hjaltalín Ólafssyni læknum kveðinn upp dómur í málinu nr. E- 7823/2006",
    "id": {
      "id": "adjudications-6",
      "section": "adjudications",
      "sentence_id": 6
    },
    "pairs": [
      {
        "a": {
          "name": "Héraðsdóms Reykjavíkur",
          "label": "Organization",
          "index": "5"
        },
        "b": {
          "name": "Dómhúsinu",
          "label": "Location",
          "index": "6"
        }
      },
      {
        "a": {
          "name": "Héraðsdóms Reykjavíkur",
          "label": "Organization",
          "index": "5"
        },
        "b": {
          "name": "Lækjartorg",
          "label": "Location",
          "index": "7"
        }
      }
    ]
  }
]
```

Since we're not doing disambiguation, we will get the same entities in multiple sentences and we will be treating them as different entities. This is not ideal, but it's the best we can do for now.

### Creating the pairs

To create the pairs:

```python
cd processing
poetry install
python parse_mim_gold_ner.py
python generate_pairs.py
```

The output is in `data/output/pairs/pairs.json`.

For usage of this data, see [./web.md](./web.md).

### Problems

* Some bugs in the data.
* Names ending in punctuation, e.g. `Villtu vinna milljón?` which is different in CoNLL and EL data (kept in EL, stripped in CoNLL)
* Extra spaces after punctuation in EL data, e.g. `E.B . Lewis`

Stopped trying to clean up by hand after enough cases and commented out errors, see `parse_mim_gold_ner.py`.

## CoNLL format

> `ID FORM LEMMA PLEMMA POS PPOS FEAT PFEAT HEAD PHEAD DEPREL PDEPREL`
>
> * `ID` (index in sentence, starting at 1)
> * `FORM` (word form itself)
> * `LEMMA` (word's lemma or stem)
> * `POS` (part of speech)
> * `FEAT` (list of morphological features separated by |)
> * `HEAD` (index of syntactic parent, 0 for ROOT)
> * `DEPREL` (syntactic relationship between HEAD and this word)
>
> — [What is CoNLL data format?](https://stackoverflow.com/questions/27416164/what-is-conll-data-format)

### In NER context

> Named entity recognition (NER) is the task of tagging entities in text with their corresponding type. Approaches typically use BIO notation, which differentiates the beginning (B) and the inside (I) of entities. O is used for non-entity tokens.
> [Named entity recognition](https://github.com/sebastianruder/NLP-progress/blob/master/english/named_entity_recognition.md)

### Links

* [CoNLL-U Format](https://universaldependencies.org/docs/format.html).
* [CoNLL-X Shared Task: Multi-lingual Dependency Parsing. Data format](https://web.archive.org/web/20160814191537/http://ilk.uvt.nl/conll/#dataformat).
