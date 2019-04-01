from gensim.models import word2vec


# sentences = word2vec.LineSentence('../data/jieba_cut/cut_words_100test.txt')
# model = word2vec.Word2Vec(sentences, sg=1, size=100, window=10, min_count=1, negative=3, sample=0.001, hs=1, workers=4)
# model.save('../data/word2vec/100test.model')

model = word2vec.Word2Vec.load('../data/word2vec/100test.model')
print(model.most_similar('支付宝'))

# print(model.wv.save_word2vec_format('../data/word2vec/100test.txt'))

