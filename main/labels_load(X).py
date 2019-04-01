# import json
#
# frPath = "C:/Users/24411/Desktop/毕业设计/cail2018_big/cail2018_big.json"
# fwPath = 'C:/Users/24411/Desktop/毕业设计/cail2018_big/ylabels.json'
#
# with open(fwPath,'w+',encoding='utf-8') as fw:
#     with open(frPath,'r',encoding="utf-8") as fr:
#         count = 0
#         for line in fr:
#             count += 1
#             if (count==7001)|(count==15155)|(count==68545)|(count==96577)|(count==131444)|(count==143702):
#                 print(count)
#                 continue
#             dic = json.loads(line)
#             if dic['meta']['term_of_imprisonment']['death_penalty']:
#                 fw.write('302')
#                 fw.write('\n')
#                 continue
#             if dic['meta']['term_of_imprisonment']['life_imprisonment']:
#                 fw.write('301')
#                 fw.write('\n')
#                 continue
#             fw.write(str(dic['meta']['term_of_imprisonment']['imprisonment'])+'\n')
#
#
