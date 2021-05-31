## 目录说明

**详细报告**
https://czardas42.github.io/post/ECPE/

- ./ECPE_withBERT **改进的模型**
  
  **【参考论文】**
  
  Rui Xia and Zixiang Ding. Emotion-Cause Pair Extraction: A New Task to Emotion Analysis in Texts. ACL 2019 (Outstanding Paper Award). [[pdf](https://www.aclweb.org/anthology/P19-1096.pdf)]
  
  **原模型的GitHub地址**：  https://github.com/NUSTM/ECPE
  
- ./bert-utils 

  使用BERT预训练模型生成句向量的部分

  **【参考】腾讯 AI Lab 开源的 BERT 服务**： https://github.com/hanxiao/bert-as-service 

- ./visualization 

  识别结果分析可视化部分

  **【参考】大连理工大学情感词汇本体库**： https://github.com/ZaneMuir/DLUT-Emotionontology

- ./spider 

  抑郁数据爬取部分

## Requirements

- tensorlfow==1.14.0  
- numpy==1.16.0  
- python==3.7



## 前期准备

- 下载`w2v_200.txt`放入ECPE_withBERT\data_combine目录下

  https://github.com/NUSTM/ECPE/blob/master/data_combine/w2v_200.txt



## BERT预训练模型生成句向量

#### Requirments

- tensorflow-gpu  >= 1.11.0
- GPU version of TensorFlow.

#### 方法


1. 下载并解压BERT中文模型 
地址：  https://github.com/ymcui/Chinese-BERT-wwm
- （选择一）chinese_wwm_ext_L-12_H-768_A-12
- （选择二）chinese_bert_chinese_wwm_L-12_H-768_A-12

2. 句向量生成
生成句向量不需要做fine tune，使用预先训练好的模型即可,注意参数必须是一个list

     

## ECPE_withBERT 模型

##### Step0：使用BERT预训练模型生成语料库词向量（可选）

须预先启动 bert-as-service
###### 基于新浪新闻的 ECPE 语料库
`python BERT.py`
###### 自定义数据
1. 使用前提：将需要生成词向量的数据集的词语汇总为一个List,保存为同一目录下的wordList.txt;
2. `python BERT_new.py`
    调用 BERT-wwm 或 BERT-wwm-ext 为其生成词向量，并将其用于之后的 ECPE 任务


##### Step1 (一共九种方法供选择):

1. 使用200维word2vec（./data_combine/w2v_200.txt）

- python Ind-BiLSTM.py
- python P_cause.py
- python P_emotion.py

2. 使用BERT-wwm预训练模型

- python Ind-BiLSTM_BERT.py
- python P_cause_BERT.py
- python P_emotion_BERT.py

3. 使用BERT-wwm-ext预训练模型

- python Ind-BiLSTM_BERT_ext.py
- python P_cause_BERT_ext.py
- python P_emotion_BERT_ext.py

##### Step2:(按照Step1选用对应的Step2)

- python pair.py
- python pair_BERT.py
- python pair_BERT_ext.py

##### 训练数据集

./data_combine/fold_train.txt
./data_combine/fold_test.txt

##### 结果保存

1. Step0生成结果保存在./BERT_RES
2. Step1结果保存在./pair_data
3. Step2结果保存在./pair_res
4. 训练完成后模型将保存于./save

##### 实验数据

详见 ./training_info



## Visualization

#### 可执行文件：

1. evaluate_test.py：是对测试集中数据进行处理，并根据数据生成词云
2. evaluate_crawler.py：是对爬取数据的分析整理，并生成词云

#### 使用到的文件：

1. predict.txt：测试集的文件
2. pair.txt：模型预测的结果
3. from_web：从抑郁吧爬取的数据及预测结果
4. hit_stopwords.txt：是使用的停用词的库，里面包含了常见的停用词，来自哈工大
5. 情感词汇.xlsx：对应情感词汇分类的excel文件，提供了常见情感词的分类，来自大连理工大学
6. simsun.ttc：生成词云需要的字体文件，这里使用的是仿宋

#### 中间文件：

1. 词频字典（文件见）：是evaluate_test.py统计的测试集中7类原因中词出现的频次
2. 分类结果（文件夹）：是evaluate_test.py产生根据情感对原因分类的结果，里面包含了7类情感原因的集合
3. result.txt：把predicate.txt中情感句与原因句结合起来的结果
4. del_re.txt：删除result.txt中单字的词，减少查找的次数，加快运行速度
5. evaluate_file.txt：情感分类的结果与情感原因放在一起的结果
6. web_cause.txt：从from_web.txt文件提取出的原因句
7. web_emotion.txt：从from_web.txt文件提取出的情感句

#### 结果文件：

1. 测试集词云：包含了7类情感原因的词云
2. 爬取数据词云：包含了情感和原因的词云

