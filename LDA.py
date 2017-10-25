import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import os
from gensim import corpora, models, similarities
import gensim
wordnet_lemmatizer=WordNetLemmatizer()

def clean_email_text(text):
    """
    :param text: the original text
    :return: the text after cut noise_pattern
    """
    text = text.replace('\n', ' ')
    noise_pattern = re.compile('|'.join(['-', '\d+\d+\d+',  '\d{4}-\d{2}-\d{2}', '[0-2]?[0-9]:[0-6][0-9]', '[\w]+@[\.\w]+', 'http\S+']))
    clean_text = re.sub(noise_pattern, ' ', text)
    pure_text = ' '
    for letter in clean_text:
        if letter.isalpha() or letter==' ':
            pure_text += letter
    text = ' '.join(word for word in pure_text.split() if len(word)>1)
    return text
def preprocess(sentence):
    #prepocess
    words = [word for word in nltk.word_tokenize(sentence)]
    word_list = [wordnet_lemmatizer.lemmatize(word) for word in words]
    filtered_words = [word.lower() for word in word_list if word not in stopwords.words('english')]
    return filtered_words
def getTrainData(i):
    # tokenize and leave n and 'NN','J','RB'
    tken=[word for word in nltk.word_tokenize(i)]
    tags= [i[0] for i in nltk.pos_tag(tken) if (("NN" in i[1]) or ("J" in i[1]) or ("RB" in i[1]))]
    filtered_0=[word.lower() for word in tags if word not in stopwords.words("english")]
    filtered_1=[word for word in filtered_0 if not any(char.isdigit() for char in word) ]
    filtered=[nltk.stem.SnowballStemmer("english").stem(word) for word in filtered_1]
    return filtered
doclists = []
for path,d,filelist in os.walk('/home/lxy/Downloads/category_1'):
    for filename in filelist:
        direct = os.path.join(path,filename)
        print(direct)
        df = pd.read_csv(direct)
        df = df[['des']].dropna()
        docs = df['des']
        docs = docs.apply(lambda s: clean_email_text(s))
        docs = docs.apply(lambda s: preprocess(s))
        doclist = docs.values
        doclists.extend(doclist)
    # return doclists
dictionary = corpora.Dictionary(doclists)
corpus = [dictionary.doc2bow(text) for text in doclists] #give the word number
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)
print(lda.print_topics(num_topics=10, num_words=5))
#print(corpus[3])
