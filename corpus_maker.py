import nltk
import os
import random

def clean(line):
    if len(line) < 1:
        return " ----"
    if line.find('[') != -1:
        return "----"
    if line.find('**') != -1:
        return "----"
    return ''.join([s for s in line if s not in punct]).strip()


texts = []
artist = 'beyonce'
path = "lyrics" 
punct = '\',.!?();-_'
for subdir, dirs, files in os.walk(path + "//" + artist):
    for file in files:
        temppath = os.path.join(subdir, file)
        with open(temppath, 'r', encoding='UTF-8') as rfile:
            for line in rfile.readlines():
                texts.append(line.replace('\n','').lower())
clean_texts = list(set([clean(x) for x in texts]))

