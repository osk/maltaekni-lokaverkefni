# Final project for the course "Introduction to NLP" at the University of Iceland

The goal of this project is to work with the [MÍM-GOLD-EL](https://repository.clarin.is/repository/xmlui/handle/20.500.12537/168) dataset and create a crowd-sourcing tool that can be used to annotate the relations in the dataset.

## Entity and relation types

First question to answer is what are the possible entity and relation types. We have an open list for the MÍM-GOLD-EL but we'd like to curate a list of possible types to present to people annotating the data.

More in [entity and relation types notes](./notes/entity-relation-types.md).

## Parsing data

See [./notes/parsing.md] and code in [`processing/`](./processing/).

## UX and UI

See [./notes/ux-ui.md](./notes/ux-ui.md).

## Prior art / references

### How I'm gathering data

Starting from some recommended articles/datasets do a cursory search for related work. Save papers in Zotero, add links below.

### Datasets / papers / resources that might help

[wikineural: Data and evaluation code for the paper WikiNEuRal: Combined Neural and Knowledge-based Silver Data Creation for Multilingual NER (EMNLP 2021).](https://github.com/Babelscape/wikineural)
[via](https://github.com/davidsbatista/NER-datasets/blob/master/README.md#en)

***

[wikiann: a multilingual named entity recognition dataset consisting of Wikipedia articles annotated with LOC (location), PER (person), and ORG (organisation) tags in the IOB2 format](https://huggingface.co/datasets/wikiann)
[via](https://github.com/davidsbatista/NER-datasets/blob/master/README.md#en)

Has Icelandic data with these three tags: LOC, PER, ORG, e.g. [is validation set](https://huggingface.co/datasets/wikiann/viewer/is/validation).

***

Paper: [Integrating Probabilistic Extraction Models and Data Mining to Discover Relations and Patterns in Text](https://aclanthology.org/N06-1038/)

***

PhD thesis: [Large-Scale Semantic Relationship Extraction for Information Discovery](https://www.davidsbatista.net/assets/documents/publications/dsbatista-phd-thesis-2016.pdf) by [David Soares Batista](https://www.davidsbatista.net/)

## TODO

* [x] Func that generates marking pairs on parsed and processed data
* [ ] List of relations to offer
* [ ] Sketches for UX
* [ ] Prototype of UI

`TODO` used in code and other places.

### Datasets / papers

* [WikiANN](https://huggingface.co/datasets/wikiann) has Icelandic NER data, it can be downloaded from [`https://s3.amazonaws.com/datasets.huggingface.co/wikiann/1.1.0/panx_dataset.zip`](https://s3.amazonaws.com/datasets.huggingface.co/wikiann/1.1.0/panx_dataset.zip).
* [Datasets of Annotated Semantic Relationships](https://github.com/davidsbatista/Annotated-Semantic-Relationships-Datasets)
* [Named entity recognition](https://github.com/sebastianruder/NLP-progress/blob/master/english/named_entity_recognition.md)
* [NER-datasets](https://github.com/davidsbatista/NER-datasets/blob/master/README.md#en)

### Data bugs

* [ ] Bugs in MIM-GOLD-2_0 NER file `mbl.txt`
  * On line 16741, `Bruce	I-Organization` should be `Bruce	B-Organization`
  * On line 16741, `Enschede	I-Organization` should be `Enschede	B-Organization`
  * On line 26827, `20	I-Time` should be `20	B-Time`
  * On line 29029, `Lisa	I-Person` should be `Lisa	B-Person`
  * On line 100344, `Gunnar	I-Person` should be `Gunnar	B-Person`
  * On line 100454, `kl.	I-Time` should be `kl.	B-Time`
  * On line 100505, `kl.	I-Time` should be `kl.	B-Time`
  * On line 100655, `Kristín	I-Person` should be `Kristín	B-Person`
  * On line 100696, `kl.	I-Time` should be `kl.	B-Time`
  * On line 100719, `Bergur	I-Person` should be `Bergur	I-Person`
  * On line 100752, `kl.	I-Time` should be `kl.	B-Time`
  * On line 102047, `kl.	I-Time` should be `kl.	B-Time`
  * On line 102286, `kl.	I-Time` should be `kl.	B-Time`
  * On line 125452, `Byggðasafns	I-Organization` should be `Byggðasafns	B-Organization`
  * On line 160949, `Sp	I-Organization` should be `Sp	B-Organization`
  * On line 222465, `Jón	I-Person` should be `Jón	B-Person`
  * On line 230829, `Jón	I-Person` should be `Jón	B-Person`
  * On line 249105, `GEOFFREY	I-Person` should be `GEOFFREY	B-Person`
* [ ] Bugs in MIM-GOLD-2_0 NER file `websites.txt`
  * On line `5496`, `-10.	I-Date` should be `-10.	B-Date` (also -10 is sus)

* [ ] Bugs in `books_release_candidates.json`
  * Items `4194` and `4212` should be `Brit. Mus.` not `Brit . Mus .`
  * Item `4890` should be `Film Aap S.A.` not `Film Aap S.A .`
  * Item `4908` should be `Elder-Dalrymple Productions Ltd.` not `Elder-Dalrymple Productions Ltd .`
  * Item `5283` should be `E.B. Lewis` not `E.B . Lewis`
  * Line 125236 should be `"prediction": "[[{'text': 'LÎle de l'épouvante >> fr', 'score': tensor(-1.3322)}, {'text': 'Lisola del sole >> it', 'score': tensor(-1.6885)}, {'text': 'LÎle de l'étrange >> fr', 'score': tensor(-1.7623)}, {'text': 'LÎle de la mort >> fr', 'score': tensor(-1.9195)}, {'text': 'LÎle de lOubli >> fr', 'score': tensor(-3.1787)}]]",`
* [ ] Bugs in `mbl_release_candidates.json`
  * Item `57` should be `Ásdís Björg Pálmadóttir` not `Ásdís Pálmadóttir` (??)
  