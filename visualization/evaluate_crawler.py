from wordcloud import WordCloud
import matplotlib.pyplot as plt

def make_file():
    file = open('hh.txt', encoding='UTF-8')
    file_emotion = open('hh_emotion.txt','w',encoding='UTF-8')
    file_cause = open('hh_cause.txt', 'w', encoding='UTF-8')
    while(True):
        line = file.readline()
        line = line.strip().split()
        #paragraph = int(line[0])
        paragraph_len = int(line[1])
        for i in range(paragraph_len):
            line2 = file.readline()
            line2 = line2.strip().split(',')
            line2[1] = line2[1].replace(' ', '')
            line2[2] = line2[2].replace(' ','')
            if line2[1] == '1':
                file_emotion.write(line2[-1])
                file_emotion.write('\n')
            if line2[2] == '1':
                file_cause.write(line2[-1])
                file_cause.write('\n')

def ciyun():
    emotion_file = open('hh_emotion.txt',encoding='UTF-8')
    cause_file = open('hh_cause.txt',encoding='UTF-8')
    stopwords = open('stopwords/hit_stopwords.txt', encoding='UTF-8')
    stopwords_list = []
    for line2 in stopwords.readlines():
        line2 = line2.strip().split()
        stopwords_list.append(line2[0])
    dict_emotion={}
    list_emotion=[]
    dict_cause={}
    list_cause=[]
    for line in emotion_file.readlines():
        line = line.strip().split()
        for i in range(len(line)):
            if line[i] in stopwords_list:
                continue
            if line[i] not in list_emotion:
                list_emotion.append(line[i])
                dict_emotion[line[i]] = 1
            else:
                dict_emotion[line[i]] = dict_emotion[line[i]] + 1
    sort_words1 = sorted(dict_emotion.items(), key=lambda x: x[1], reverse=True)
    print(sort_words1[0:101])  # 输出前0-100的词
    wc1 = WordCloud(
        max_words=500,  # 最多显示词数
        # max_font_size=100,  # 字体最大值
        background_color="white",  # 设置背景为白色，默认为黑色
        width=1500,  # 设置图片的宽度
        height=960,  # 设置图片的高度
        font_path='simsun.ttc',
        margin=10  # 设置图片的边缘
    )
    wc1.generate_from_frequencies(dict_emotion)  # 从字典生成词云
    plt.imshow(wc1)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像
    wc1.to_file('emotion_ciyun.jpg')  # 保存图片

    for line in cause_file.readlines():
        line = line.strip().split()
        for i in range(len(line)):
            if line[i] in stopwords_list:
                continue
            if line[i] not in list_cause:
                list_cause.append(line[i])
                dict_cause[line[i]] = 1
            else:
                dict_cause[line[i]] = dict_cause[line[i]] + 1
    sort_words2 = sorted(dict_cause.items(), key=lambda x: x[1], reverse=True)
    print(sort_words2[0:101])  # 输出前0-100的词
    wc2 = WordCloud(
        max_words=500,  # 最多显示词数
        # max_font_size=100,  # 字体最大值
        background_color="white",  # 设置背景为白色，默认为黑色
        width=1500,  # 设置图片的宽度
        height=960,  # 设置图片的高度
        font_path='simsun.ttc',
        margin=10  # 设置图片的边缘
    )
    wc2.generate_from_frequencies(dict_cause)  # 从字典生成词云
    plt.imshow(wc2)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像
    wc2.to_file('cause_ciyun.jpg')  # 保存图片

ciyun()