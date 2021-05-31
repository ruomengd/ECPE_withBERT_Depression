from bert_serving.client import BertClient
import numpy as np

words = []
inputFile = open('./data_combine/clause_keywords.csv', 'r', encoding='utf8')
for line in inputFile.readlines():
    line = line.strip().split(',')
    emotion, clause = line[2], line[-1]
    words.extend([emotion] + clause.split())

words = set(words)  # 所有不重复词的集合
word_list = []

for item in enumerate(words):
    word_list.append(item[1])

word_idx = dict((c, k + 1) for k, c in enumerate(words)) # 每个词及词的位置
word_idx_rev = dict((k + 1, c) for k, c in enumerate(words)) # 每个词及词的位置

# Save
fileName1 ="./BERT_RES/wmm-ext/word_idx.csv"
##保存文件
with open(fileName1, 'w', encoding='utf8') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in word_idx.items()]

fileName2 ="./BERT_RES/wmm-ext/word_idx_rev.csv"
##保存文件
with open(fileName2, 'w', encoding='utf8') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in word_idx_rev.items()]

bc = BertClient()
embedding = bc.encode(word_list)

print(embedding.shape)
np.savetxt('./BERT_RES/wmm-ext/word_embedding.txt', embedding)
