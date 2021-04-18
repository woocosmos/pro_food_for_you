# 데이터 합치기만 할 것임

import pandas as pd

# 중복 제거하고 다시 합치기
# df_dup = pd.read_csv('./crawling/movie_review_2019_1.csv', index_col = 0)
# df_undup = df_dup.drop_duplicates()
# print(df_undup.duplicated().sum())
# df_undup.to_csv('./crawling/movie_review_2019_1.csv')
# exit()

df = pd.read_csv('./crawling/yoggiyo_store_info_2.csv', index_col = 0)
print(df.info())
# print(df.head()) # 타이틀 칼럼, 리뷰 컬럼(전처리 완료)

df1 = pd.read_csv('./crawling/yoggiyo_store_info_3.csv', index_col = 0)
df = pd.concat([df, df1], ignore_index=True)
print(df.info())


df = df.drop_duplicates() # 중복 제거

df.to_csv('./crawling/yoggiyo_store_info_2_and_3.csv')