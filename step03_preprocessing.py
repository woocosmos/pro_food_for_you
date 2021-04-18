import pandas as pd
from konlpy.tag import Okt
import re


#크롤링한 데이터 가져오기
# df_popular = pd.read_csv('./yoggiyo_popular_menu.csv', index_col=0)
df_review = pd.read_csv('./test_yoggiyo_data_all.csv', index_col=0)
# df_info = pd.read_csv('./yoggiyo_store.csv', index_col=0)


stopwords = pd.read_csv('../datasets/stopwords.csv', index_col=0)
stopwords = list(stopwords.stopword)
temp_stopwords = ['맛있다', '먹다', '주문', '사먹다', '자다', '오다', '배달', '진짜', '들다', '생각나다',
             '좋다', '감사하다', '넘다', '그렇다', '모르다', '해주다', '지난번', '올라오다', '가다',
             '주시', '좋아하다', '사장']



print(type(df_review.review))

# df_popular = pd.DataFrame({'title':popular_store_title, 'menu':popular_menu_title,'menu_img':popular_menu_img})
# df_review = pd.DataFrame({'title':review_store_title, 'review':review_reviews})
# df_info = pd.DataFrame({'title':info_store_title, 'hour':info_store_operation_hours,
#                         'min_order':info_min_order_amount, 'address':into_address})



print(df_review.isnull().sum())

stopwords = stopwords + temp_stopwords
okt = Okt()
cleaned_sentences = []

for sentence in df_review.review:
    print('.', end='')
    sentence = re.sub('[^가-힣]', ' ', sentence)
    token = okt.pos(sentence, stem=True) # 어근 분리해서 기본형으로
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
                                (df_token['class'] == 'Verb') |
                                (df_token['class'] == 'Adjective')]

    words = []
    for word in df_cleaned_token['word']:
        if len(word) > 1:
            if word not in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df_review['cleaned_review'] = cleaned_sentences
print(df_review.head())
df_review = df_review[['title', 'cleaned_review']]

one_sentences = []
for title in df_review['title'].unique():
    temp = df_review[df_review['title'] == title]['cleaned_review']
    if len(temp) > 100:
        temp = temp[:100]
    one_sentence = ' '.join(list(temp))
    one_sentences.append(one_sentence)
df_one_sentences = pd.DataFrame({'title':df_review['title'].unique(), 'review':one_sentences})


print(df_one_sentences.head())
print(df_one_sentences.info())

df_one_sentences.to_csv('./test_cleaned_yoggiyo_review_test.csv')