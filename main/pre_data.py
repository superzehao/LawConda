import json
import random

frPath = '../data/cail2018_big.json'

# train: test: valid = 7: 2: 1
# 训练集数据
trainFactPath = '../data/train_fact.txt'
trainLabelPath = '../data/train_label.txt'
# 测试集数据
testFactPath = '../data/test_fact.txt'
testLabelPath = '../data/test_label.txt'
# 验证集数据
validFactPath = '../data/valid_fact.txt'
validLabelPath = '../data/valid_label.txt'

# 使用随机seed，结果可重现
random.seed(0)
with open(trainFactPath, 'w+', encoding='utf-8') as tfp:
    with open(trainLabelPath, 'w+', encoding='utf-8') as tlp:
        with open(testFactPath, 'w+', encoding='utf-8') as ttfp:
            with open(testLabelPath, 'w+', encoding='utf-8') as ttlp:
                with open(validFactPath, 'w+', encoding='utf-8') as vfp:
                    with open(validLabelPath, 'w+', encoding='utf-8') as vlp:
                        with open(frPath, 'r', encoding='utf-8') as fr:
                            count = 0
                            for line in fr:
                                dic = json.loads(line)
                                if dic['meta']['term_of_imprisonment']['death_penalty']:
                                    continue
                                if dic['meta']['term_of_imprisonment']['life_imprisonment']:
                                    continue
                                randNum = random.random()
                                if randNum <= 0.7:
                                    tfp.write(str(dic['fact']) + '\n')
                                    tlp.write(str(dic['meta']['term_of_imprisonment']['imprisonment'])+'\n')
                                elif 0.7 <= randNum <= 0.9:
                                    ttfp.write(str(dic['fact']) + '\n')
                                    ttlp.write(str(dic['meta']['term_of_imprisonment']['imprisonment']) + '\n')
                                else:
                                    vfp.write(str(dic['fact']) + '\n')
                                    vlp.write(str(dic['meta']['term_of_imprisonment']['imprisonment']) + '\n')

                                count += 1

                                if count % 10000 == 0:
                                    print('已完成：' + str(round(count / 17000, 2)) + '%')
