# English/German Spellchecker

In this project, tweets in both German and English were classified by their langauge and checked for spelling errors. Spelling corrections are offered within one Damerau-Levenstein disntance away. The most misspelled words in each respective language were listed along side their corrections.
<br/>
<br/>

##  Results
<br/>
<br/>

```python

output:
[('kinda', 2290, ['kind', 'linda']),
 ('bc', 712, ['be', 'by', 'b']),
 ('gonna', 492, ['donna', 'gonne', 'gona']),
 ('lol', 395, ['vol', 'lo', 'pol']),
 ('omg', 377, ['om', 'og']),
 ('wanna', 330, ['anna', 'canna', 'hanna']),
 ('rn', 297, ['in', 'an', 'on']),
 ('tbh', 284, ['th', 'tch']),
 ('idk', 261, ['id', 'ink', 'ilk']),
 ('ppl', 217, ['pol', 'pal'])]

```
<br/>

Here are the most misspelled words in English, along with their respective misspell count and the possible terms for replacement.

<br/>
<br/>


```python

output:
[('nen', 424, ['ren', 'nn']),
 ('nochmal', 294, ['nochmals']),
 ('nem', 233, ['dem', 'neu', 'nm']),
 ('erstmal', 216, ['erstmals']),
 ('lol', 214, ['hol', 'mol', 'aol']),
 ('daß', 180, ['saß', 'maß', 'dax']),
 ('gibts', 164, ['gibt', 'gifts']),
 ('nich', 151, ['nicht', 'noch', 'sich']),
 ('zb', 147, ['zu', 'ob', 'tb']),
 ('vllt', 146, [])]

```
<br/>

Here are the most misspelled words in English, along with their respective misspell count and the possible terms for replacement.

<br/>
<br/>


## Prerequisites
In addtion to string and regex, you will need the nltk library

```bash

pip install nltk

```

<br/>
<br/>

## Cleaning the data
<br/>
<br/>
Raw data from tweets in two different langauges had a lot to filter. Websites, hashtags, numbers, punctuation, and @ tags were removed from the text. These replacements were done consectively rather than a single regular experession to avoid group overlapping and for simplicity.

<br/>
<br/>

```python
    data_index[tweet] = re.sub('https?[^\s]+', ' ' , data_index[tweet])
    data_index[tweet] = re.sub('[@#][^\s]+', ' ' , data_index[tweet])
    data_index[tweet] = re.sub(r'[0-9][^\s]+', ' ' , data_index[tweet])
    data_index[tweet] = re.sub(r'\w+\.[^\s]+', ' ' , data_index[tweet])
    data_index[tweet] = re.sub(r'[^a-zäöüß\s]', ' ', data_index[tweet])
    data_index[tweet] = re.sub(r'[^\w\s]', ' ' , data_index[tweet])

```

<br/>
<br/>

## Running the Code
<br/>
<br/>
This can be run directly in the notebook.
However you may require jupyter-notebook as well.


```bash
sudo apt-get install jupyter-notebook
```
<br/>
<br/>

## The processing
<br/>
<br/>
The data was tokenized and normalized using NLTK libraries. Filtering and cleaning of the data was done through regular expressions, and string libraries.

```python

import re 
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer as wnl

```
<br/>
<br/>

## Text classification
<br/>
<br/>
To classify between languages, the NLTK stop word list and character lists were used to intitally distinguish between them. For further refinement, dictionaries were generated of terms that occured most frequently in the previously classified texts. These were run again against to more accurately label each tweet. As a fall back if the tally for words occuring in either language could not determin which language the tweet was in, the stop word list and character screening was used.


<br/>
<br/>

## Misspells
<br/>
<br/>
Once terms were normalized using a lemmatizer, the misspellings were ran against lexicons within each respective langauges. In the prelimiary run, there were many acronyms and text speech being assessed as misspelled terms. Many of these were addeed to a separete dictionary. In addition, contractions were replaced in not include them in the results as they are acceptable. However, the choice to allow for much of the accepted internet acronym were removed. Adding them to the acceptable lexicons was also probable, as that would have caught the unintentional misspellings as opposed to intentional use of non-dictionary standard terms. 
<br/>
<br/>
As a second measure for tweets, especially ones in German, misspelled words were also run against the opposite language lexicons to caputre terms that might have been intentially used but not specially a part of that language. This may have contributed to some missed corrections. It is one of the problems with a raw text.

<br/>
<br/>

## Spelling Corrections
<br/>
<br/>
To identify which terms were most likely to replace the misspelled words, an edited distance (Damerau-Levenstein) algorithm was implemented with a limit of a distance of 1. In this algorythm, All possible combinations within one l measure of distance from subtraction, addition, deletion, and substitution were compiled into a dictionary. This dictionary was then run against the lexicons in their respective langauge. This eliminated all non-valid terms. The remaining list is then presented within the results as probable replacements.
<br/>
<br/>

```python

chunks = [(term[:i], term[i:])for i in range(len(term) + 1)]
    for chunk1, chunk2 in chunks:
        if chunk2:
            #subtraction
            possible[chunk1+chunk2[1:]] = 1
            for char in alphabet:
                #substitution
                possible[chunk1+char+chunk2[1:]] = 1
        if len(chunk2) > 1:
            #transposition
            possible[chunk1+chunk2[1]+chunk2[0]+chunk2[2:]] = 1
        for char in alphabet:
            #addition
            possible[chunk1+char+chunk2] = 1
```

<br/>
<br/>

## Expansion
<br/>
<br/>
Further extensions of this project could include giving spell corrections weights related to the surrounding context to have more sensible replacements. An additional expansion could be an increasing the potential edited distance if a potential solution could not be found, similar to a back-off algorithm. Potentially, more lexicon sources may also be usefull in refining both language classification and spelling corrections.
<br/>
<br/>

## The Data

The data was given from twitter. It was collected and distributed via the University of Stuttgart. German and English lexicons were also contributed from University of Stuttgart files.
<br/>
<br/>
<br/>
<br/>

## Authors


* **King De Lany** - *Initial work* - [DelanyK](https://github.com/DelanyK)



## Acknowledgments

*This project was from the Information Retrieval and Text mining course and the University of Stuttgart. Parterns that contributed ideas, [RenouB](https://github.com/RenouB) and [Amirasweilem](https://github.com/amirasweilem)
