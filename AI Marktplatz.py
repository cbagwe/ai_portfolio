#!/usr/bin/env python
# coding: utf-8

# Automatic identification and structuring of AI companies for product creation

# Author: Chaitali Suhas Bagwe (cbagwe@mail.uni-paderborn.de)


# Install Necessary Libraries
# Remove the comment char '#' for installing the libraries
#!pip install requests
#!pip install beautifulsoup4


#  Import Libraries
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm,metrics
from urllib.request import Request, urlopen

import pandas as pd
import re
import requests
import scrapy


# Read the data from the Excel File
# In this block we read the data from excel file and change the column name of 
# "Relevance of service/app and fit to the portfolio" to "Relevance" for better readability/extraction. 
# Since we are only interested in product engineering companies we will mark the
#  "1 - product engineering" as "1" and others as "0". 
# This makes the classification problem into binary classification.

#Read the input Excel file
dataset = pd.read_excel('App and service store_Long List.xlsx', sheet_name='App and service store_Long List')

#Change column names
dataset.rename(columns = {'Relevance of service/app and fit to the portfolio':'Relevance'}, inplace = True)

#Change Relevance values
dataset.Relevance.replace('1 - product engineering',1, inplace = True)
dataset.Relevance.replace('2 - production',0, inplace = True)
dataset.Relevance.replace('3- AI general',0, inplace = True)
dataset.Relevance.replace('4 - cross sectional processes',0, inplace = True)
dataset.Relevance.replace('5 - not relevant',0, inplace = True)


# Segregration of Test and Train data for our ML model
# The sampling helps us in having random and not fixed input to the model. 
# We have used 60 samples of product engineering companies and 60 samples of other companies as our training dataset. 
# Thus the size of training data is 120. 
# For test data we have used random 20 samples from each type of companies. Thus the size of testing data is 40.

# Segregrate the product engineering and other data from the dataset
prod_engg_data = dataset[dataset['Relevance'] == 1]
other_data = dataset[dataset['Relevance'] == 0]

# Generate train and test data by random sampling of product engineering and other data and then appending it together.
train_data = prod_engg_data.sample(60).append(other_data.sample(60))
test_data = prod_engg_data.sample(20).append(other_data.sample(20))


# #### Stopwords Creation
# To remove some commonly used and unnecessary words like "an", "the", "a", etc., we define stopwords here. 
# Along with the predefined stopwords from PorterStemmer library, we also add words that are not useful 
# for us in the context of websites. These words include the words from header and footer of the websites,
# dropdown menu words of the websites, terms and conditions, etc.

stemmer = PorterStemmer()

stop_words = stopwords.words("english")
# Add custom stop words (frequently occuring but add no value)
stop_words += ['about', 'us', 'contact', 'how','login', 'hello','email','home','blog','terms','conditions']


# Clean Text Function
# This function cleans the text received by the variable "text". 
# Cleaning includes removal of stopwords, white spaces, html tags, numbers,
#  special characters and punctuations. 
# This function also tokenizes the text sent to it and performs stemming on each word.

def clean_text(text):
    
    # remove white spaces, html tags, numbers, special characters, punctuations
    RE_WSPACE = re.compile(r"\s+", re.IGNORECASE)
    RE_TAGS = re.compile(r"<[^>]+>")
    RE_ASCII = re.compile(r"[^A-Za-zÀ-ž ]", re.IGNORECASE)
    RE_SINGLECHAR = re.compile(r"\b[A-Za-zÀ-ž]\b", re.IGNORECASE)

    text = re.sub(RE_TAGS, " ", text)
    text = re.sub(RE_ASCII, " ", text)
    text = re.sub(RE_SINGLECHAR, " ", text)
    text = re.sub(RE_WSPACE, " ", text)

    word_tokens = word_tokenize(text)
    words_tokens_lower = [word.lower() for word in word_tokens]

    # perform stemming on each word
    words_filtered = [
        stemmer.stem(word) for word in words_tokens_lower if word not in stop_words
    ]

    text_clean = " ".join(words_filtered)
    return text_clean




def read_url_content(URL,page):
    soup = BeautifulSoup(page.content, "html.parser")
    for div in soup.find_all('div', attrs={'data-nosnippet' : 'true'}):
        div.decompose()
    for footer in soup.find_all('footer'):
        footer.decompose()
    return clean_text(soup.text)


# In[8]:


def get_cleaned_webdata(dataframe):
    page_data = []
    for index, row in dataframe.iterrows():
        URL = row["Link"]
        try:
            page = requests.get(URL)
            #data = read_url_content(URL)
            page_data.append(read_url_content(URL,page))
            #print(URL, page_data)
        except(ConnectionError, Exception):
            page_data.append("")
    #print(page_data)
    return page_data


# In[9]:


def print_statistics(actual, predicted):
    avg = 'weighted'
    print("Accuracy:",metrics.accuracy_score(actual, predicted))
    print("Precision:",metrics.precision_score(actual, predicted, average=avg))
    print("Recall:",metrics.recall_score(actual, predicted, average=avg))
    print("F1 score:",metrics.f1_score(actual, predicted, average=avg))


# In[10]:


#Clean train and test data
train_data["WebData"] = get_cleaned_webdata(train_data)
test_data["WebData"] = get_cleaned_webdata(test_data)


# In[11]:


train_data["WebData"]


# ***
# #### Feature extraction using TF-IDF
# TF-IDF measures how relvant a word is when compared with the entire document.

# In[12]:


tfidf_vectorizor = TfidfVectorizer()


# In[13]:


train_input = tfidf_vectorizor.fit_transform(train_data["WebData"]).toarray().tolist()
test_input = tfidf_vectorizor.transform(test_data['WebData']).toarray().tolist()
#valinput = tfidf_vectorizor.transform(valdf['cleaned_text']).toarray().tolist()


# In[14]:


train_output = train_data['Relevance'].tolist()
test_output = test_data['Relevance'].tolist()
#valoutput =  valdf['IPC-Hauptklasse'].tolist()


# In[15]:


#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(train_input, train_output)

#Predict the response for test dataset
y_pred = clf.predict(test_input)


# In[16]:


print_statistics(test_output,y_pred)


# In[20]:


round(5/ 2)


# In[ ]:





# In[ ]:





# In[ ]:





# In[17]:


#soup_initial = re.sub("\s{2,}[a-z]+\s{2,}", " ", soup.text,flags=re.IGNORECASE)
#print(clean_text(soup.text))

