from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

import re
import requests

### Text Preprocessing

#### Setting up stop-words and stemmer
#Stop Words : Removing commonly used english stop words like *and*, *the*, *a*, *an*, etc. We have also removed the words that are not useful for us in the context of websites. These include the words from header and footer of the websites, dropdown menu words of the websites, terms and conditions, etc.
#Stemmer : Reducing the word to its word stem; *extraction* -> *extract*
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words("english")
# Add custom stop words (frequently occuring but add no value)
stop_words += ['about', 'us', 'contact', 'how','login', 'hello','email','home','blog','terms','conditions',
               'jobs','openings','careers','privacy','policy','legal','imprint','demo','support','team',
              'conditions']


#### 1) Clean Text Function
#This function cleans the text received by the variable "text". Cleaning includes removal of stopwords, white spaces, html tags, numbers, special characters and punctuations. This function also tokenizes the text sent to it and performs stemming on each word.
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
        #stemmer.stem(word) 
        #lemmatizer.lemmatize(word)
        word for word in words_tokens_lower if word not in stop_words
    ]

    text_clean = " ".join(words_filtered)
    return text_clean


#### 2) Read Content from URL of the company
#BeautifulSoup library is used for the extraction of content from the given URL. Additionally, the footer attributes and the website's cookies attributes are removed in this function.
def read_url_content(page):
    # read the content
    soup = BeautifulSoup(page.content, "html.parser")
    
    # remove the website cookies content
    for div in soup.find_all('div', attrs={'data-nosnippet' : 'true'}):
        div.decompose()
        
    # remove footer
    for footer in soup.find_all('footer'):
        footer.decompose()
        
    # translate the content to English  
    translator = GoogleTranslator(source='auto', target='en')
    translated_text = translator.translate(soup.text[:4999])
        
    # return the cleaned content
    return clean_text(translated_text)


#### 3) Parse the required contents from the dataframe.
#This function reads the data from the dataframe and passes the URL of each company to the read_url_content() function. A try and catch block is added for checking if the URL is accessible or not.
def get_cleaned_webdata(dataframe):
    # create an empty list of page data
    page_data = []
    
    for index, row in dataframe.iterrows():
        URL = row["Link"]
        try:
            # access the URL
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
            page = requests.get(URL, headers = headers)
            # append the URL content to the list
            page_data.append(read_url_content(page))
        except(ConnectionError, Exception):
            # for websites not accessible append empty string to the list
            page_data.append("")
    return page_data

