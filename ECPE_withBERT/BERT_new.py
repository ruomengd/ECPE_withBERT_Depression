from bert_serving.client import BertClient
import numpy as np

with open('wordList.txt', 'r', encoding='utf-8') as f:
    words = []
    for line in f.readlines():
        line = line.strip('\n')  # 去掉换行符\n
        b = line.split(' ')  # 将每一行以空格为分隔符转换成列表

        def not_empty(s):
            return s and s.strip()
        c = filter(not_empty, b)

        words.extend(c)

words = set(words)  # 所有不重复词的集合
word_list = []
count = 0

for item in enumerate(words):
    # print(item)
    count += 1
    word_list.append(item[1])

print(str(count))

word_idx = dict((c, k + 1) for k, c in enumerate(words)) # 每个词及词的位置
word_idx_rev = dict((k + 1, c) for k, c in enumerate(words)) # 每个词及词的位置

# Save
fileName1 ="./BERT_RES/depression/word_idx.csv"
##保存文件
with open(fileName1, 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in word_idx.items()]

fileName2 ="./BERT_RES/depression/word_idx_rev.csv"
##保存文件
with open(fileName2, 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in word_idx_rev.items()]

bc = BertClient()
embedding = bc.encode(word_list)

print(embedding.shape)
np.save('./BERT_RES/depression/word_embedding.npy', embedding)

