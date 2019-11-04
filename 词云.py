#Python的警告信息有时候很烦人，特别是因为软件版本引起的警告，
#下面的代码可以去掉python输出的警告：
import warnings
warnings.filterwarnings('ignore')
import jieba #分词包
import numpy as np#numpy计算包
import codecs # codecs提供open方法来指定打开的文件的语言编码，他会在读取的
               #时候自动转换为内部unicode
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib # python的可视化库
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud # 词云包
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
sns.set(font='SimHei')

# 读取新闻数据
df = pd.read_csv('entertainment_news.csv',encoding='utf-8')
#删除nan值行
df = df.dropna()
#print(df.head(5))
content = df.content.values.tolist()
segment = []
i=0
# 分词
for line in content:
   try:
       segs = jieba.lcut(line)
       #print(segs)
       for seg in segs:
           if len(seg)>1 and seg!='\r\n':
               segment.append(seg)
   except:
       print(line)
       continue

#去停用词
words_df = pd.DataFrame({'segment':segment})
#print(words_df.head(5))
#stopwords=pd.read_csv('stopwords.txt',index_col=False,quoting=3,
                      #sep='\t',names=['stopwords'],encoding='utf-8')#quoting=3全不引用
stopwords = pd.read_csv('stopwords.txt',index_col=False,sep='\t',quoting=3,names=['stopword'],encoding='utf-8')
#print(stopwords.head(5))
words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
#print(words_df.head(5))

# 统计词频
words_state = words_df.groupby(by=['segment'])['segment'].agg({'计数':np.size})
#print(words_state)
words_state = words_state.reset_index().sort_values(by=['计数'],ascending=False)
#print(words_state.head())

#做词云
# 字体
wordcloud = WordCloud(font_path='simhei.ttf',background_color='white',max_font_size=80)
word_frequence = {x[0]:x[1] for x in words_state.head(1000).values}

id = dict(list(word_frequence.items())[:50])
wordcloud = wordcloud.fit_words(id)
plt.imshow(wordcloud)
plt.show(wordcloud)





