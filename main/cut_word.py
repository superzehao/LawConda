# -*- coding:utf-8 -*-
import json
import jieba
import re
import collections
import pickle
import jieba.posseg as pseg

jieba.setLogLevel('WARN')


# 按行文件，每行按空格进行切分，返回二维数组
def read_fact_cut(fact_cut_path):
    with open(fact_cut_path, encoding='utf-8') as fact_cut_fr:
        fact_cut_list = []
        for line in fact_cut_fr:
            one_fact = line.strip().split(" ")
            fact_cut_list.append(one_fact)
    return fact_cut_list


# 按行读取文件，返回一维数组
def read_line(path):
    line_list = []
    with open(path, encoding='utf-8') as fr:
        for line in fr:
            line = line.strip()
            if len(line):
                line_list.append(line)
    return line_list


# 根据二维数组，返回数据字典
def create_dict(fact_cut_list):
    count_word = [word for one_fact in fact_cut_list for word in one_fact]
    counter = collections.Counter(count_word).most_common(199998)
    word_index_dic = {key[0]: index + 2 for index, key in enumerate(counter)}
    # unk词 和 pad词
    word_index_dic['pad'] = 0
    word_index_dic['unk'] = 1

    return word_index_dic


# 使用pickle方式保存对象
def save_pickle(path, Object):
    with open(path, 'wb') as fw:
        pickle.dump(Object, fw)


# 根据数据字典，转换二维数据，并返回
def fact_transform(fact_cut_list, word_index_dict):
    fact_index = []
    for one_fact in fact_cut_list:
        temp = []
        for word in one_fact:
            if word in word_index_dict:
                temp.append(word_index_dict[word])
            else:
                temp.append(word_index_dict['unk'])
        fact_index.append(temp)
    return fact_index


# 对特殊数词进行离散处理，并返回
def disperse(word,pre_word):
    # 血液酒精浓度离散
    if word == 'mg每100ml':
        if (re.sub("\.", "", pre_word).isdigit()) & (pre_word.count(".") < 2):
            num = float(pre_word)
            if num < 20:
                word = "0-20mg每100ml"
            elif num < 80:
                word = "20-80mg每100ml"
            elif num < 200:
                word = "80-200mg每100ml"
            else:
                word = "200以上mg每100ml"
            return word, ""
    # 食品危害物质含量离散
    if word == 'mg每千克':
        if (re.sub("\.", "", pre_word).isdigit()) & (pre_word.count(".") < 2):
            num = float(pre_word)
            if num < 10:
                word = "0-10mg每千克"
            elif num < 50:
                word = "10-50mg每千克"
            elif num < 200:
                word = "50-200mg每千克"
            elif num < 800:
                word = "200-800mg每千克"
            elif num < 1000:
                word = "800-1000mg每千克"
            elif num < 1500:
                word = "1000-1500mg每千克"
            elif num < 2000:
                word = "1500-2000mg每千克"
            else:
                word = "2000以上mg每千克"
            return word, ""
    # 重量离散
    if (word == 'g') | (word == '克') | (word == 'kg') | (word == '千克'):
        if (re.sub("\.", "", pre_word).isdigit()) & (pre_word.count(".") < 2):
            num = float(pre_word)
            if (word == 'kg') | (word == '千克'):
                num = num * 1000
            if num < 10:
                word = "0-10克"
            elif num < 50:
                word = "10-50克"
            elif num < 200:
                word = "50-200克"
            elif num < 1000:
                word = "200-1千克"
            elif num < 10000:
                word = "1-10千克"
            elif num < 50000:
                word = "10-50千克"
            elif num < 100000:
                word = "50-100千克"
            elif num < 200000:
                word = "100-200千克"
            elif num < 500000:
                word = "200-500千克"
            else:
                word = "500千克以上"
            return word, ""
    # 金钱离散
    if (word == '元') | (word == '万元'):
        if (re.sub("\.", "", pre_word).isdigit()) & (pre_word.count(".") < 2):
            num = float(pre_word)
            if word == '万元':
                num = num * 10000
            if num < 500:
                word = "0-500元"
            elif num < 4000:
                word = "500-4000元"
            elif num < 10000:
                word = "4000-1万元"
            elif num < 50000:
                word = "1-5万元"
            elif num < 100000:
                word = "5-10万元"
            elif num < 200000:
                word = "10-20万元"
            elif num < 500000:
                word = "20-50万元"
            elif num < 1000000:
                word = "50-100万元"
            elif num < 5000000:
                word = "100-500万元"
            else:
                word = "500万元以上"
            return word, ""

    return word, pre_word


# 根据一条文本数据按一定规则进行分词，并返回
def fact_cut(text, stop_words):
    fact_label = text.strip().split("&&[")
    fact = fact_label[0]

    # 为特殊数词离散化做准备
    fact = re.sub("(mg/100ml)|(mg/100mg)|(mg／100mg)|(mg／100ml)", "mg每100ml", fact)
    fact = re.sub("(mg/kg)|(mg/l)|(mg／kg)|(mg／l)", "mg每千克", fact)
    fact = re.sub("多千克", "千克", fact)
    fact = re.sub("，", "", fact)
    fact = re.sub("(余元后)|(余元)|(多元后)|(多元)|(元后)", "元", fact)
    fact = re.sub("(万余元)|(多万元)|(余万元)", "万元", fact)

    # 通过正则表达式，删除部分词
    fact = re.sub("\d+[年月日号时点分秒型期天单楼宿室次层栋路街厂店里鉴包饮组酒弄幢小区房户步船海团连]", "", fact)
    fact = re.sub("(\[\d*\])|【\d*】|(\（\d*\）)", "", fact)

    fact = re.sub("\S[某]+[甲乙丙丁12345678]|\S[甲乙丙丁12345678][某]+|\S某某|\S某", "x", fact)
    fact = re.sub("[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]([a-z]|\d*)*", "x", fact)
    fact = re.sub("(卡号码名下为)\d+", "", fact)
    fact = re.sub("(。|：|，)\d+(.|、)", "。", fact)
    fact = re.sub("(\d*、\d*)|(\[\d*\])|【\d*】|(\d*\.com)|(\（\d*\）)|\d*(×|X)\d*|\d+\.(\d+\.)+", "", fact)
    fact = re.sub("[abdefhijnopqrstuvwxyz]", "", fact)
    words = pseg.cut(fact)
    fact_words = ''
    pre_word = ''
    # 停用词性
    stop_speech = ["Ag","ad","an","dg","e","f","g","h","i","j","k","l","Ng","nr","ns","nz","o","s","u","w","x","y","un"]

    for word, flag in words:
        word, pre_word = disperse(word,pre_word)
        # if flag in stop_speech:
        #     continue
        # if word in stop_words:
        #     continue
        # if word in fact_words:
        #     continue
        if len(word)<2:
            continue

        # 其它数词，按字符分开
        if (re.sub("\.", "", pre_word).isdigit()) & (pre_word.count(".") < 2):
            pre_word = re.sub("(?<=\S)", " ", pre_word)
        fact_words += pre_word + " "
        pre_word = word
    fact_words = (fact_words+pre_word).strip()
    label = fact_label[1].replace(']', '')
    return fact_words, label


# 根据文本数据，保存分词结果
def save_fact_cut(fact_label_path, fact_cut_path, label_path, stop_words):
    with open(fact_cut_path, 'w+', encoding='utf-8') as fact_cut_fw:
        with open(label_path, 'w+', encoding='utf-8') as labels_fw:
            with open(fact_label_path, encoding="utf-8") as fact_label_fr:
                count = 0
                for text in fact_label_fr:
                    count += 1
                    fact_words, label = fact_cut(text, stop_words)
                    fact_cut_fw.write(fact_words + '\n')
                    labels_fw.write(label + '\n')
                    if count % 1000 == 0:
                        print(count)


# 对数据进行分词和保存
def create_fact_cut(fact_label_train_path, train_fact_path, train_label_path,
                    fact_label_test_path, test_fact_path, test_label_path):

    # print("   添加自定义词典...")
    # jieba.load_userdict("saved_big_data/user.dict")
    print("   加载停用词...")
    stop_words = read_line("../data/jieba_cut/stop_words.txt")

    print("   开始分词，保存分词结果及标签...   ")
    print("   训练集...")
    save_fact_cut(fact_label_train_path, train_fact_path, train_label_path, stop_words)
    print("   测试集...")
    save_fact_cut(fact_label_test_path, test_fact_path, test_label_path, stop_words)


# 对所给定的数据进行转换，并保存
def create_data(fact_cut_path, label_path, fact_cut_pkl, label_pkl, train=False):
    fact_cut_list = read_fact_cut(fact_cut_path)
    if train:
        word_index_dict = create_dict(fact_cut_list)
        save_pickle("saved_big_data/dispersed/word_index_dic.dat", word_index_dict)
    else:
        file = open("saved_big_data/dispersed/word_index_dic.dat", 'rb')
        word_index_dict = pickle.load(file)
        file.close()
    fact_index = fact_transform(fact_cut_list, word_index_dict)
    label = [int(i) for i in read_line(label_path)]
    save_pickle(fact_cut_pkl, fact_index)
    save_pickle(label_pkl, label)
    del fact_cut_list, fact_index, label


# 处理数据，生成能输入模型的数据
def create_model_data(train_fact_path,train_label_path,test_fact_path,test_label_path):
    path = "saved_big_data/dispersed/"
    print("   训练集...")
    create_data(train_fact_path, train_label_path, path + "xes_train.dat", path + "ys_train.dat", train=True)

    print("   测试集...")
    create_data(test_fact_path, test_label_path, path + "xes_test.dat", path + "ys_test.dat")


# 真实数据
# with open('../data/train_fact.txt','r', encoding='utf-8') as f:
# 测试数据
with open('C:/Users/24411/Desktop/毕业设计/cail2018_big/json_100test.json', 'r', encoding='utf-8') as f:
    line = f.readline()
    while line:
        jsonData = json.loads(line)
        # print(type(jsonData))
        fact = jsonData['fact']
        # print("fact:" + fact)
        seg_list = jieba.cut(fact)
        # print("Default Mode: " + "/ ".join(seg_list))
        cutWordFile = open('../data/jieba_cut/cut_words_100test.txt', 'a', encoding='utf-8')
        for data in seg_list:
            # print('data:'+data)
            cutWordFile.write(data+'\n')

        cutWordFile.close()
        line = f.readline()

