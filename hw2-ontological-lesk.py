#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk 
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import wordnet
from nltk.tokenize import PunktSentenceTokenizer,sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer


# In[2]:


import os
cwd = os.getcwd()
os.chdir('C:/Users/elnaj/Desktop/MSBA Classes/classes-FAll 2020/IDS 566 text analytics/assignments/hw2')
print(os.getcwd() + "\n")


# In[3]:


##
## IDS566: For Homework 2
##

from lxml import etree, objectify


# Read the dictionary file.
Parser = objectify.makeparser(recover=True)
Tree = objectify.fromstring(''.join(open('dictionary.xml').readlines()), Parser)


# function: 
def getSenses(word, pos):
    global Tree
    item = Tree.xpath("//lexelt[@item='%s.%s']" % (word, pos))    
    senses = []
    for sense in item[0].getchildren():
        senses.append(dict(zip(sense.keys(), sense.values())))
    return senses


# function:
def getSense(word, pos, sense_id):
    global Tree
    sense = Tree.xpath("//lexelt[@item='%s.%s']/sense[@id='%d']" % (word, pos, sense_id))
    return dict(zip(sense[0].keys(), sense[0].values()))


    
# Example
print(getSense('begin', 'v', 2))
print(getSenses('begin', 'v'))


# In[4]:


import pandas as pd
##open testing data
test_f = open("test.data", "r")  
print(test_f.readlines())  
test_df = pd.read_csv("test.data", delimiter='|', names=['word', 'sense', 'sentence'])
print(test_df)


# In[13]:


import string
#sentence filter and pre-process
def simpleFilter(sentence):
    s= sentence
    sentence_new = s.translate(str.maketrans('', '', string.punctuation))
    filtered_sentence = []
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    word_tokens = nltk.word_tokenize(sentence_new)
    for w in word_tokens:
        if  w not in stop_words:
            filtered_sentence.append(lemmatizer.lemmatize(w))
    return filtered_sentence


# In[ ]:



#parts of speech(pos) taging for our context for each word in a sentence 
nltk.download('averaged_perceptron_tagger')
sentence= simpleFilter(sentence_new.lower())
print(sentence)
def tagPos(sentence):
    pos=[]
    for w in sentence:
        word = nltk.word_tokenize(w)
        pos.append(nltk.pos_tag(word))
    return pos    
wordPos=tagPos(sentence)
print(wordPos)


# In[ ]:


# define part of speech for a context hha will be compatible with our dictionary POS tags
def wordOfInterest(pos):
    wn_pos=['NN','VB','JJ','JJR','JJS','NNP','VBG','RB','VBD','VBP']

    woi1=[]

    for x in pos:
        arr=[]
        for y in x:
            if y[1] in wn_pos:
                arr.append(y)
        woi1.append(arr) 
    woi=[]


    for i in woi1:
        arr2=[]
        for j in i:

            if j[1]=='VBD' or j[1]=='VB' or j[1]=='VBP':
                tup=(j[0],'v')
                arr2.append(tup)
            elif j[1]=='VBG':
                tup=(j[0],'n')
                arr2.append(tup)
            elif j[1]=='NN' or j[1]=='NNP':
                tup=(j[0],'n')
                arr2.append(tup)
            elif j[1]== 'JJ' or j[1]=='JJR' or j[1]=='JJS':
                tup=(j[0],'a')
                arr2.append(tup)
            elif j[1]=='RB':
                tup=(j[0],'r')
                arr2.append(tup)
        woi.append(arr2)       
            
    return woi


# In[14]:


# retrived first sentence in test file to test our op
sentence_new =test_df.iloc[1]['sentence']
word= test_df.iloc[1]['word']
print(simpleFilter(sentence_new.lower()))


# In[19]:


#overlap metric 
"""
This metric will Calculate overlaps between the context sentence given from the test file and the synsets that are taken from 
the dictionary this is (original signature senses) and returns the synset with the highest overlap words .
"""
# Holds the synsets ->signature dictionary.
# filter senses of original dictionary words 
new_senses = getSenses('capital', 'n')
test_s= simpleFilter(sentence_new.lower())

#print(new_senses)
def overlaps_metric(new_senses, test_s):
    max_overlaps =0
    for i in range(len(new_senses)):
        sentence1= new_senses[i]
        s1= sentence1['examples']
        s2=sentence1['gloss']
        s= s1+s2
        clean_s =simpleFilter(s.lower())
        overlaps = set(clean_s)&set(test_s)
        if len(overlaps) > max_overlaps:
            best_sense = sentence1['id']
            max_overlaps = len(overlaps)
    return best_sense
   


# In[22]:


# we have tested our metric on a subset of target word for the word capital that was embedded within 40 different sentences
#in the test file 
new_senses = getSenses('capital', 'n')
senses_of_ca =[]
LIMIT = 40
for n in range(LIMIT):
    sentence_new =test_df.iloc[n]['sentence']
    word= test_df.iloc[n]['word']
    test_New_s= simpleFilter(sentence_new.lower())
    ss = overlaps_metric(new_senses,test_New_s)
    senses_of_ca.append(ss)
    
print(senses_of_ca)
with open("simple_lesk.txt", "w") as output:
    output.write(str(senses_of_ca))    
    


# In[ ]:




