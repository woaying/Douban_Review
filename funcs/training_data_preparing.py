import pandas as pd
import numpy as np
import jieba

def get_training_data(dataset, w2v_model):
    train_x = []
    train_y = []
    # model = gensim.models.Word2Vec.load("data/word2vec_gensim")
    for i in range(0, len(dataset)):
        comment = dataset['comment'][i]
        words = jieba.cut(comment)
        wordvec = []
        for word in words:
            if not word or word == " " or word == "\n":
                continue
            try:
                wordvec.append(w2v_model.wv[str(word)])
            except KeyError:
                pass
        train_x.append(wordvec)
        senti_dict = {'1': 0, '2': 0, '3': 1, '4': 2, '5': 2}
        train_y.append(senti_dict[dataset['star'][i]])

        if i % (len(dataset)//10) == 0:
            print("已处理:百分之%s" % str(i * 100.0 / len(dataset)))

    return train_x, train_y

