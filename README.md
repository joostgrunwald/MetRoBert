# MetRoBert

MetRobert is an automatic metaphor identification model in Dutch and English.
The principles are ment to show that the model can be easily adjusted for use in any other language.
A tutorial in using this for other languages will follow.

## File system

This directory exists of two parts, one for creating the input that is used for the model and one that contains the model itself.
See the bottom of this readme for more detailed lists of functionality.

## Bagging

For bagging an sh script is included. Please use this script and adjust the bagging index as needed.
Bagging takes quite some time so please leave bagging until you are satisfied with the model.

## Ponyland

If you are running this model as a member of the Radbour University you will most likely be using Ponyland.
Our model is currently stored at /vol/tensusers4/jgrunwald/MetRobert*run2.
The verb model will take approximatly 3 * 5 minutes to fully train and approximatly 3 _ 1 minute to test.
The allpos model will take approximatly 12 _ 5 minutes to fully train and approximatly 3 \_ 2 minutes to test.

## Requirements

```
python==3.8
pytorch
transformers
nltk
scipy
numpy
tqdm
colorama
```

### Data Parsers

```
pasmaparser_cov_melbert_allpos -> This parser creates the dev (covid data) input for the model for all POS tags.
pasmaparser_melBERT_allpos -> This parser creates the train/test input for the model for all POS tags.
pasmaparser_melbert_ww -> This parser creates the train/test input for the model for only verbs.
pasmaparser_zn and pasmaparser_ww -> These parsers create train/test input for our old model, pos tags ZN and VERB.
```
