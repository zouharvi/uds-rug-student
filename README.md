Notes and code for the Multichannel Management final project.
The task is to automatically classify interview sentences to an [ontology](https://raw.githubusercontent.com/zouharvi/multichannel-management/main/meta/codebook_redesign/codebook.pdf), focusing on the top levels:

- interesting / not interesting
- interesting: roles / communication
- roles: government / media / citizen
- communication: effective / ineffective

See [src/misc/ontology.py](src/misc/ontology.py) for specific coding.

## Architecture

Pre-trained language models are hoped to do most of the work.
The interviews are in Dutch and as such, there are two solutions:
- Translate them into English and use BERT & RoBERTa
- Use Dutch versions of the models, such as [BERTje](https://github.com/wietsedv/bertje)

This is followed up by a simple classification layer and the whole pipeline fine-tuned.

## Data

TODO
