# takes a dream diary in the form of a text file
# analyses the word content using a Linguistic Inquiry Word Count (LIWC) dictionary
# compares the scores to population baselines
# graphically plots comparisons and changes in dream content over time
# extracts a network of names
#
# created by Maria Priestley, priestleymaria@yahoo.co.uk

from readDict import * # functions to read and count words from the LIWC dictionary
from wordCount import *
from named_entities import * # function to extract named entities
import re # regular expressions
import datetime # dates
import pandas as pd # data frames
import numpy as np # numerical data
import networkx as nx # networks
import matplotlib.pyplot as plt # plot figures

# TODO
# set name of txt file containing the dreams you want to analyse
with open ('merri_dreams.txt', "r") as myfile:
    text=myfile.read().replace('\n', ' ') # each dream must begin with date (either dd/mm/yy, or mm/dd/yy)

# load SDDb dream baselines, originally published in Bulkeley & Graves (2018)
with open ('SDDb_base.txt', "r") as f:
    base=f.readlines()
baselines = []
for line in base:
    splits = line.split()
    baselines.append([splits[0],float(splits[1]),float(splits[2])])
# put baselines into a data frame
df = pd.DataFrame(baselines, columns = ['category','base_mean','base_sd'])

#########################
##### word counts #######
#########################

inDict = (r'LIWC2015_English.dic') # path to the LIWC dictionary
# read the dictionary
dictIn,catList = readDict(inDict)
# run the wordCount function
out = wordCount(text, dictIn, catList)

print("total words: ",out[2])
# category counts
my_means = []
categories = []
for k, v in out[0].items():
    try:
        my_mean = v/out[2]*100 # expressed as percentages
        category = k.split()[0]
        my_means.append([category, float(my_mean)])
        categories.append(category)
    except:
        print("Error in: ",category)
# put them into a data frame
my_df = pd.DataFrame(my_means, columns = ['category','my_mean'])
# join data frames of our means and baselines
data = pd.merge(df, my_df, on='category', how='outer')
# calculate z-scores
data['z_score'] = (data['my_mean'] - data['base_mean'])/data['base_sd']
# get top 10 largest absolute z-scores
top_z = data.iloc[data['z_score'].abs().argsort()[::-1][:10]]
ax = top_z.plot(kind='bar',x='category',y='z_score',title='Top special categories', rot=45)
ax.set_ylabel('Z-score')
ax.axhline(y=0, xmin=-1, xmax=1)
# mark z-scores corresponding to 95% confidence interval
ax.axhline(y=1.96, xmin=-1, xmax=1, color='r', linestyle='--', lw=2)
ax.axhline(y=-1.96, xmin=-1, xmax=1, color='r', linestyle='--', lw=2)
ax.get_legend().remove()
# save plot
fig = ax.get_figure()
fig.savefig("top_z_scores.png", bbox_inches='tight')

##############################
##### temporal patterns ######
##############################

# this section splits the dreams by date, to examine changes in content over time
daily_dreams = [] # daily dream frequencies
dreams_dict = {} # will structure dream texts by day
dates = []
tot_words = [] # word count of each dream
# in the dreams file, the dates are given in a fixed form
# use a regular expression to split at the dates
splits = re.split(r'(\d+/\d+/\d+)', text)
i = 0
# iterate over each split 
while i < (len(splits)-1):
    if re.match(r'(\d+/\d+/\d+)', splits[i]): # if date
        date = splits[i]
        # convert to proper date
        # TODO 
        # uncomment the proper date format here
        # european date
        dd,mm,yy = date.split('/')
        # american date
        # mm,dd,yy = date.split('/')
        # in case of single digits
        if len(dd)<2:
            dd= '0'+dd
        if len(mm)<2:
            mm= '0'+mm
        if len(yy)==2:
            yy= '20'+yy
        date = datetime.date(int(yy), int(mm), int(dd))
        dream_text = splits[i+1]
        # merge dream texts if they occurred on the same day
        if date in dreams_dict:
            dreams_dict[date]= str(dreams_dict[date]) + " " + dream_text
        else:
            dreams_dict[date]=dream_text
        proportions = [] # proportions of categories in each dream
        # now do word counts for each dream
        # Run the wordCount function
        out = wordCount(dream_text, dictIn, catList)
        for k, v in out[0].items():
            proportions.append(float(v/out[2]*100))
        dates.append(date) # this will become our index
        tot_words.append(out[2])
        daily_dreams.append(proportions)
        i+=2 # increment
    else:
        i+=1 # increment

# put them into a data frame
daily_freq = pd.DataFrame(daily_dreams, columns = categories)
daily_freq['date'] = dates
daily_freq['date'] = pd.to_datetime(daily_freq['date'], errors='coerce')
daily_freq['wordcount'] = tot_words
# daily_freq['wordcount'].mean() # average word counts, bear in mind that multiple dreams in the same day get merged into one
# aggregate into quarterly frequencies, gives scores for every 3 months instead of daily
q_freq = daily_freq.set_index('date').resample('Q').mean()
totals = daily_freq.set_index('date').resample('Q').sum()
# the 'total words' column can be checked to make sure that a decent amount of data
# were available for deriving each quarterly estimate
q_freq['total_words'] = totals['wordcount']
q_freq.reset_index(level=0, inplace=True)
# TODO
# you can plot a specific category of interest
# category definitions can be found here: https://repositories.lib.utexas.edu/bitstream/handle/2152/31333/LIWC2015_LanguageManual.pdf
colname = 'affect' # other options:'function','pronoun', 'ppron','i','we','you','shehe',
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
#                        'nonflu','filler']
ax = q_freq.fillna(method='ffill').plot(x='date', y=colname, kind='line',title='"'+colname+'" category frequency over time')
ax.set_ylabel('Percent frequency')
ax.set_xlabel('Date (quarterly)')
# save plot
fig = ax.get_figure()
fig.savefig(colname+"_frequency.png", bbox_inches='tight')

# data frame to store quarterly z-scores for all categories
q_zscore = pd.DataFrame(q_freq['date'].values, columns = ['date'])
for colname, col in q_freq.iteritems():
    if colname in df['category'].values:
        base_mean = df.loc[df['category'] == colname]['base_mean'].astype('float64')
        base_sd = df.loc[df['category'] == colname]['base_sd'].astype('float64')
        q_zscore[colname]=q_freq[colname].apply(lambda x: x-base_mean)/base_sd
# standard deviation of each category over time
# this measures the spread of data, bigger std means that values are more spread out in time
q_sd = pd.DataFrame(q_zscore[df['category'].values].std(axis=0),columns = ['sd'])

# get top 5 categories
# this shows categories with biggest standard deviation in Z-scores
top_qsd = q_sd.iloc[q_sd['sd'].argsort()[::-1][:5]] # first chunk
# next 5 categories
# can rerun this bit again
# top_qsd = q_sd.iloc[q_sd['sd'].argsort()[::-1][5:10]] #second chunk
top_qsd['category'] = top_qsd.index.values
selection = q_zscore[top_qsd['category'].values]
dates = q_zscore['date'].copy()
selection['date']= dates
#plot
ax = selection.set_index('date').ffill().plot(kind='line',title='Top changing categories')
ax.set_ylabel('Z-score')
ax.set_xlabel('Date (quarterly)')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.axhline(y=0,color='black', linestyle='--')
# z scores corresponding to 95% confidence interval
ax.axhline(y=1.96, xmin=-1, xmax=1, color='r', linestyle='--')
ax.axhline(y=-1.96, xmin=-1, xmax=1, color='r', linestyle='--')
# save plot
fig = ax.get_figure()
fig.savefig("top_changing_scores.png", bbox_inches='tight')

#########################
## find named entities ##
#########################
# if error, try importing nltk and run nltk.download()
named_entities = get_named_entities(text)

#########################
## network of names #####
#########################

name_freq = {} # number of dreams in which each name occurs
for dream in dreams_dict:
    matches = [] # names that occur in each dream
    for name in named_entities:
        my_regex = r"\b" + name + r"\b"
        if re.search(my_regex, dreams_dict[dream]):
            matches.append(name)
    for match in matches:
        if match in name_freq:
            name_freq[match]+=1
        else:
            name_freq[match] = 1
# select names that occur in more than 3 dreams
# TODO
# this threshold can be changed
select_names = dict((k, v) for k, v in name_freq.items() if v > 3) # change the "v > x" bit with your desired x

# adjacency matrix to store links between entities
am = pd.DataFrame(np.zeros(shape=(len(select_names),len(select_names))),columns=select_names.keys(), index=select_names.keys())

# fill in the connections
for dream in dreams_dict:
    matches = [] # names that occur in each dream
    for name in select_names.keys():
        my_regex = r"\b" + name + r"\b"
        if re.search(my_regex, dreams_dict[dream]):
            matches.append(name)
    for match in matches:
        # record names that co-occur in the same dream
        for match_2 in matches:
            am.at[match,match_2] += 1
# log transform
log_data = np.log(am)
log_data[np.isneginf(log_data)] = 0
# normalise
am_norm = (log_data-log_data.min())/(log_data.max()-log_data.min())
am_edgelist = am_norm.rename_axis('Source')\
  .reset_index()\
  .melt('Source', value_name='Weight', var_name='Target')\
  .query('Source != Target')\
  .reset_index(drop=True)
# threshold on how often they co-occur
# TODO
# this can be changed
am_edgelist = am_edgelist[am_edgelist['Weight'] > float(0.6)] # change the float value, must be between 0 and 1

G = nx.from_pandas_edgelist(am_edgelist,'Source','Target', edge_attr='Weight')
# largest connected component
Gc = max(nx.connected_component_subgraphs(G), key=len)
weights = [i['Weight'] for i in dict(Gc.edges).values()]
labels = [i for i in dict(Gc.nodes).keys()]
labels = {i:i for i in dict(Gc.nodes).keys()}

fig, ax = plt.subplots(figsize=(30,10))
pos = nx.spring_layout(Gc)
nx.draw_networkx_nodes(Gc, pos, ax = ax, labels=True, node_color='r')
nx.draw_networkx_edges(Gc, pos, width=weights, ax=ax, edge_color='g')
_ = nx.draw_networkx_labels(Gc, pos, labels, ax=ax)
fig.savefig("graph.png")
