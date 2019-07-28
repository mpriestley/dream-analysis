# dream-analysis

Quantitative analysis of dreams using a LIWC dictionary.

# User Guide
At the moment, the analysis script doesn't have a user interface. You need to go into the code to adapt it :)

Specify the file name of the dream diary you want to analyse.
```
with open ('my_dreams.txt', "r") as myfile:
```
This should be a txt file where each dream begins with a date (format "dd/mm/yy" or "mm/dd/yy"). Specify the appropriate date format by uncommenting it in the script later on.
```
# american date
# mm,dd,yy = date.split('/')
```
To plot the temporal development of a specific word category, change the "colname" variable:
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
