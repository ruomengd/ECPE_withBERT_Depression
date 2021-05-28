'''
输入文件：
predicate.txt：待预测的文本
pair.txt：预测的结果
输出文件：
result.txt：将predicate中情感与原因取出来放在其中
del_re.txt：将result中情感中单字词去除，因为字典中不会存在单字，减少查字典速度
evaluate_file.txt：查字典后的结果后面跟上原因
final.txt：按七大类分类后的原因
'''
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#把情感与原因结合起来了放在result.txt中
def chongpai(predict,pair):
    predict = str(predict)
    pair = str(pair)
    temp = 1#用于判断predicate中是否有这一段
    f_predict = open(predict,encoding='UTF-8')
    f_pair = open(pair,encoding='UTF-8')
    f_result = open("result.txt", 'w',encoding='UTF-8')
    for line_pair in f_pair.readlines():
        line_pair = line_pair.strip().split()
        len_line = len(line_pair)
        duanhao = line_pair[0]

        if temp == 1:#如果没有这一段就不读下一行了
            line_pre = f_predict.readline()
            line_pre = line_pre.strip().split()
        if line_pre[0] != duanhao:# 说明predicate中缺少段落，下次不读下一行了
            temp = 0
            continue
        temp = 1
        temp2 = 1 #用来去除predicate文本中的正确结果，给定测试集中使用，自己文本时候需不需要看文本格式
        context = []
        context_len = 0
        for i in range (int(line_pre[1])+1):
            line_pre = f_predict.readline()
            line_pre = line_pre.strip().split(',')
            if temp2 == 1:#省略第一行
                temp2 = 0
                continue
            context.append(line_pre)#把这么多行的内容取出来存好
            context_len=context_len+1
        for j in range(int((len_line-1)/2)):#确定有多少个情感原因对
            emotion = line_pair[j*2+1].replace('(','').replace(',','')
            cause = line_pair[j*2+2].replace(')','').replace(',','')
            for k1 in range(context_len):
                if emotion == context[k1][0]:#这一句是情感句
                    f_result.write(context[k1][-1])
                    f_result.write(',')
            for k2 in range(context_len):
                if cause == context[k2][0]:  # 这句是原因句
                    f_result.write(context[k2][-1])
                    f_result.write('\n')
    f_result.close()
    f_pair.close()
    f_predict.close()

#字典中没有单个字的，所以去掉情感中单字，提高查字典的效率
def del_word(result):
    f_result = open(result, encoding='UTF-8')
    f_del_re = open('del_re.txt','w',encoding='UTF-8')
    temp = ''
    for line in f_result.readlines():
        line = line.strip().split(',')
        emotion = line[0].split()

        for i in range(len(emotion)):
            if len(emotion[i]) != 1:
                temp = temp + emotion[i] + ' '
        f_del_re.write(temp)
        f_del_re.write(',')
        f_del_re.write(line[1])
        f_del_re.write('\n')
        temp = ''
    f_del_re.close()
    f_result.close()

class EmotionDict(object):
    """docstring for EmotionDict."""
    def __init__(self):
        super(EmotionDict, self).__init__()
        self.dictionary = pd.read_excel('情感词汇.xlsx',engine='openpyxl')


    def evaluate(self, word):
        try:
            target = self.dictionary[self.dictionary.词语 == word].index[0]
            target = self.dictionary.loc[[target]]
        except IndexError:
            return None

        return (target.词语.values[0], target.情感分类.values[0], target.强度.values[0], target.极性.values[0])
        #return target

def evaluate_file(result):
    file = open(result, encoding='UTF-8')
    evaluate_file = open('evaluate_file.txt', 'w', encoding='UTF-8')
    handler = EmotionDict()
    for line in file.readlines():
        line = line.strip().split(',')
        emotion = line[0].split()
        for i in range(len(emotion)):
            result = handler.evaluate(emotion[i])
            if result is not None:
                evaluate_file.write(str(result))
                evaluate_file.write(',')
                evaluate_file.write(line[1])
                evaluate_file.write('\n')
            else:
                continue
    file.close()
    evaluate_file.close()
#将小类统计到7大类
def fenlei(evaluate_file):
    file = open(evaluate_file,encoding='UTF-8')
    le = open('分类结果/le.txt','w', encoding='UTF-8')
    hao = open('分类结果/hao.txt', 'w', encoding='UTF-8')
    nu = open('分类结果/nu.txt', 'w', encoding='UTF-8')
    ai = open('分类结果/ai.txt', 'w', encoding='UTF-8')
    ju = open('分类结果/ju.txt', 'w', encoding='UTF-8')
    wu = open('分类结果/wu.txt', 'w', encoding='UTF-8')
    jing = open('分类结果/jing.txt', 'w', encoding='UTF-8')
    for line in file.readlines():
        line = line.strip().split(',')
        fenlei = line[1].replace(' ','')
        if fenlei == '\'PA\'' or fenlei == '\'PE\'':
            le.write(line[-1])
        elif fenlei == '\'PD\'' or fenlei == '\'PH\'' or fenlei == '\'PG\'' or fenlei == '\'PB\'' or fenlei == '\'PK\'':
            hao.write(line[-1])
        elif fenlei == 'nan':
            nu.write(line[-1])
        elif fenlei == '\'NB\'' or fenlei == '\'NJ\'' or fenlei == '\'NH\'' or fenlei == '\'PF\'':
            ai.write(line[-1])
        elif fenlei == '\'NI\'' or fenlei == '\'NC\'' or fenlei == '\'NG\'':
            ju.write(line[-1])
        elif fenlei == '\'NE\'' or fenlei == '\'ND\'' or fenlei == '\'NN\'' or fenlei == '\'NK\'' or fenlei == '\'NL\'':
            wu.write(line[-1])
        else:
            jing.write(line[-1])
    file.close()
    le.close()
    hao.close()
    nu.close()
    ai.close()
    ju.close()
    wu.close()
    jing.close()
#生成词频字典并生成词云
def ciyun(fenlei):
    file = open(fenlei, encoding='UTF-8')
    stopwords = open('stopwords/hit_stopwords.txt', encoding='UTF-8')
    name = fenlei[5:7]+'.txt'
    dict=open(name,'w', encoding='UTF-8')
    stopwords_list = []
    for line2 in stopwords.readlines():
        line2 = line2.strip().split()
        stopwords_list.append(line2[0])
    line = file.readline()
    line = line.strip().split()
    word_list = []
    word_dict = {}
    for i in range(len(line)):
        ci = line[i]
        if ci in stopwords_list:
            continue
        if ci not in word_list:
            word_list.append(ci)
            word_dict[ci] = 1
        else:
            word_dict[ci] = word_dict[ci] + 1
    file.close()
    sort_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
    print(len(sort_words))
    print(sort_words[0])
    print(sort_words[0:101])  # 输出前0-100的词
    for i in range(len(sort_words)):
        xuhao = str(sort_words[i]).replace('(','').replace(')','')
        dict.write(xuhao)
        dict.write('\n')

    wc = WordCloud(
        max_words=500,  # 最多显示词数
        # max_font_size=100,  # 字体最大值
        background_color="white",  # 设置背景为白色，默认为黑色
        width=1500,  # 设置图片的宽度
        height=960,  # 设置图片的高度
        font_path='simsun.ttc',
        margin=10  # 设置图片的边缘
    )
    wc.generate_from_frequencies(word_dict)  # 从字典生成词云
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像
    path=fenlei[5:7]+'.jpg'
    wc.to_file(path)  # 保存图片
    stopwords.close()

chongpai("predict.txt", "pair.txt")
del_word("result.txt")
evaluate_file("del_re.txt")
fenlei("evaluate_file.txt")
ciyun("分类结果/ai.txt")#哀
ciyun("分类结果/hao.txt")#好
ciyun("分类结果/ju.txt")#惧
ciyun("分类结果/le.txt")#乐
ciyun("分类结果/nu.txt")#怒
ciyun("分类结果/wu.txt")#恶
ciyun("分类结果/jing.txt")#惊