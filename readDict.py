# psyLex: an open-source implementation of the Linguistic Inquiry Word Count
# Created by Sean C. Rife, Ph.D.
# srife1@murraystate.edu // seanrife.com // @seanrife
# Licensed under the MIT License

# Function to read in an LIWC-style dictionary


# this version was tweaked by Maria Priestley, priestleymaria@yahoo.co.uk
# Sean's original code can be found at https://github.com/seanrife/psyLex


import sys, re, collections

def readDict(dictionaryPath):
    catList = collections.OrderedDict()
    catLocation = []
    wordList = {}
    finalDict = collections.OrderedDict()
    
    # Check to make sure the dictionary is properly formatted
    with open(dictionaryPath, "r") as dictionaryFile:
        for idx, item in enumerate(dictionaryFile):
            if "%" in item:
                catLocation.append(idx)
        if len(catLocation) > 2:
            # There are apparently more than two category sections; throw error and die
            sys.exit("Invalid dictionary format. Check the number/locations of the category delimiters (%).")
    
    # Read dictionary as lines
    with open(dictionaryPath, "r") as dictionaryFile:
        lines = dictionaryFile.readlines()
    
    # Within the category section of the dictionary file, grab the numbers associated with each category
    for line in lines[catLocation[0] + 1:catLocation[1]]:
        try:
            if re.split(r'\t+', line)[0] == '':
                catList[re.split(r'\t+', line)[1]] = [re.split(r'\t+', line.rstrip())[2]]
            else:
                catList[re.split(r'\t+', line)[0]] = [re.split(r'\t+', line.rstrip())[1]]
        except: # likely category tags
            pass
    
    # Now move on to the words
    for idx, line in enumerate(lines[catLocation[1] + 1:]):
        # Get each line (row), and split it by tabs (\t)
        workingRow = re.split('\t', line.rstrip())
        wordList[workingRow[0]] = list(workingRow[1:])
    
    # Merge the category list and the word list
    for key, values in wordList.items():
        if "(" in key and ")" in key:
            key = key.replace("(","").replace(")","")
        # these words are ambiguous and cause errors
        if key == "kind" or key== "like":
            continue
        if not key in finalDict:
            finalDict[key] = []
        for catnum in values:
            try: # catch errors (e.g. with dic formatting)
                workingValue = catList[catnum][0]
                finalDict[key].append(workingValue)
            except:
                print(catnum)
    return (finalDict, catList.values())