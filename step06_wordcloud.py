import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud
import collections
from matplotlib import font_manager, rc


font_path = '../malgun.ttf'


font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
mpl.font_manager._rebuild()

df = pd.read_csv('./crawling/yoggiyo_review_test.csv')



from PIL import Image
# cloud_mask = np.array(Image.open('./cloud_mask.png'))

movie_index = 213
words = df.review[movie_index].split(' ')

worddict = collections.Counter(words)
print(worddict)

# stopwords = ['배우', '영화', '감독', '출연', '리뷰', '보기', '연출', '개봉']
stopwords = ['맛있다', '먹다', '주문', '사먹다', '자다', '오다', '배달', '진짜', '들다', '생각나다',
             '좋다', '감사하다', '넘다', '그렇다', '모르다', '해주다', '지난번', '올라오다', '가다',
             '주시', '좋아하다', '사장']

wordcloud_img = WordCloud(
        background_color='white',
        max_words=2000,
        # mask=cloud_mask,
        font_path=font_path,
        stopwords=stopwords,
).generate(df.review[movie_index])

plt.figure(figsize=(8,8))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.title(df.title[movie_index], size=25)
plt.show()