import json
import jieba
import gensim
from gensim import corpora, models, similarities
def make_word_set(word_file):
    """
    :param word_file: txt
    :return: remove duplicate
    """
    word_set = set()
    with open(word_file, 'r') as fp:
        for line in fp.readlines():
            word = line.strip()
            if len(word) > 0 and word not in word_set:
                word_set.add(word)
    return word_set
stopwords_file = '/home/richard/Documents/stopwords_cn.txt'
stopwords_set = make_word_set(stopwords_file)
doclists = []
path = '/home/richard/Documents/2017-10-26.json'
def read_news(path):
    for line in open(path):
        content = json.loads(line)['content']
        #print(content)
        content = content.replace('[财经头条网导读]','')
        content = content.replace('\n','')
        word_cut = jieba.cut(content,cut_all=False)
        word_list = [word for word in word_cut if word not in stopwords_set]
        no_space_content = [word.strip() for word in word_list if word >= '\u4e00' and word<= '\u9fa5']
        doclists.append(no_space_content)
    dictionary = corpora.Dictionary(doclists)
    corpus = [dictionary.doc2bow(text) for text in doclists] #give the word number
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=2)
    data = lda.print_topics(num_topics=10, num_words=10)
    return data
print(read_news(path))