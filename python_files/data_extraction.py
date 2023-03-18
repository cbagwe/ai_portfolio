from wordcloud import WordCloud

import gensim
import gensim.corpora as corpora
import yake


#### Initialize the keyword extractor from Yake library
max_ngram_size = 1
deduplication_threshold = 0.9
num_of_keywords = 130
window_size = 1

kw_extractor = yake.KeywordExtractor(n=max_ngram_size, dedupLim=deduplication_threshold, top=num_of_keywords, windowsSize=window_size)

#### 1) Extract Keywords Function
def extract_keywords(string):
    keywords = kw_extractor.extract_keywords(string)
    keywords = [x for (x,_) in keywords]
    return " ".join(keywords)

#### 2) Extract Topics from websites
def extract_topics(long_string):
    num_topics = 300
    # Create Dictionary
    id2word = corpora.Dictionary([long_string.split()])
    # Create Corpus
    texts = [long_string.split()]
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    try:
        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=id2word,
                                       num_topics=num_topics)
        x=lda_model.show_topics(num_topics=1, num_words=300,formatted=False)
        topics_words = [(tp[0], [wd[0] for wd in tp[1]]) for tp in x]

        #Below Code returns Only Words 
        for topic,words in topics_words:
            return " ".join(words)
    except Exception as e:
        print(e)
        return ""

#### 3) Create Wordcloud
def create_wordcloud(long_string):
    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
    # Generate a word cloud
    wordcloud.generate(long_string)
    # Visualize the word cloud
    return wordcloud.to_image()

#### 4) Perform feature extraction on the data inside the passed dataframe according to the method specified
#### Input: Dataframe, Method to be used
#### Output: Nothing. The extracted features are stored in the same dataframe under the column method_name
def extraction_on_cleaned_webdata(dataframe, method):
    if method == "keywords":
        dataframe["Keywords"] = dataframe["WebData"].apply(extract_keywords)
    else:
        print("Outside keywords")
        dataframe["Topics"] = dataframe["WebData"].apply(extract_topics)
