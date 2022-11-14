# Parsing

Notes on parsing the data required for this project.

## Parsing MIM-GOLD data

See [`processing` folder and comments in files](./../processing/).

Input data is saved in [`data/`](../data/) and is checked in to make it easier to generate output data.

Output is saved in [`data/output`](../data/output/). Each file is large (>10MB) so it's not checked into git.

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
