# Description of tool
This script runs quantitative analysis of an individual's dream diary.
* **Quantifies the contents of the diary** using a LIWC dictionary. This gives the frequency of words related to over 70 categories (e.g. cognitive processes, positive/negative emotions, social interactions, sensory experiences).
* **Compares these scores to those derived from the general population**. This makes the scores meaningful by showing which aspects of an individual's dream life are statistically different from the baselines found by researchers.
* **Graphically plots changes in the content of dreams over time**. This can be used to explore the temporal development of specific themes (e.g. changes in emotional valence over several months/years)
* **Plots a network of named entities** (people, places), where nodes represent names and links represent the occurrence of these entities together in the same dream.

I suggest having a corpus of at least 100 diary entries to work with (the repository includes an example dream diary).
The functionality could be adapted to work on a normal diary, by adding the LIWC population baselines for expressive writing.



# User Guide
At the moment, the analysis script doesn't have a user interface.<br/>
You need to go inside the script **"main.py"** to adapt it & run.<br/>

I've marked all the bits you need to change with a #TODO tag.<br/>
First, specify the file name of the dream diary you want to analyse.
```
with open ('my_dreams.txt', "r") as myfile:
```
This should be a txt file where each dream begins with a date (format "dd/mm/yy" or "mm/dd/yy").<br/>
Specify the appropriate date format by uncommenting it in the script later on.
```
# american date
# mm,dd,yy = date.split('/')
```
To plot the temporal development of a specific word category, you can change the "colname" variable:
```
colname = 'affect' # other options:''function','pronoun', 'ppron','i','we','you','shehe',
#                        'they','ipron', 'article','prep', 'auxverb', 'adverb',
#                        'conj','negate','verb','adj','compare','interrog','number',
#                        'quant','affect','posemo','negemo','anx','anger','sad',
#                        'social','family','friend','female','male','cogproc',
#                        'insight','cause','discrep','tentat','certain','differ',
#                        'percept','see','hear','feel','bio','body','health','sexual',
#                        'ingest','drives','affiliation','achieve','power','reward',
#                        'risk','focuspast','focuspresent','focusfuture','relativ',
#                        'motion','space','time','work','leisure','home','money',
#                        'relig','death','informal','swear','netspeak','assent',
#                        'nonflu','filler'
```
When plotting the network of names, you can adjust the thresholds to make the plot look visually interpretable. Otherwise there might be too many nodes or connections to make sense of. You can choose to select names that occur in at least a few dreams, and require that the links between names exceed a certain threshold of mutual occurrence (this is a normalised and transformed value).
```
# select names that occur in more than 3 dreams
select_names = dict((k, v) for k, v in name_freq.items() if v > 3) # change the "v > x" bit with your desired x
```
```
# threshold on how often they co-occur
am_edgelist = am_edgelist[am_edgelist['Weight'] > float(0.3)] # change the float value, must be between 0 and 1
```
# Dependencies
Python libraries: re, datetime, pandas, numpy, networkx, plt, nltk

# Acknowledgements
SDDb dream baselines taken from [Bulkeley, K., & Graves, M. (2018). Using the LIWC program to study dreams. Dreaming, 28(1), 43](https://www.researchgate.net/publication/323646665_Using_the_LIWC_program_to_study_dreams).

LIWC dictionary developed by [Pennebaker, J.W., Boyd, R.L., Jordan, K., & Blackburn, K. (2015). The development and psychometric properties of LIWC2015. Austin, TX: University of Texas at Austin](https://repositories.lib.utexas.edu/bitstream/handle/2152/31333/LIWC2015_LanguageManual.pdf).

LIWC dictionary reader functions came from [Sean Rife's psyLex project](https://github.com/seanrife/psyLex).

Merri's dream diary sourced from [DreamBank repository](http://www.dreambank.net/).
