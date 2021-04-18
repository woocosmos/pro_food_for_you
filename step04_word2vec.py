import pandas as pd
from gensim.models import Word2Vec

review_words = pd.read_csv('./crawling/yoggiyo_review_test.csv',
                           index_col=0)

review_words = review_words.dropna(subset=['review'], how = 'any', axis = 0)

clean_token_review = list(review_words['review'])
print(clean_token_review[0])



cleaned_tokens = []
for sentence in clean_token_review:
    token = sentence.split(' ')
    cleaned_tokens.append(token)


print(cleaned_tokens[0])

embedding_model = Word2Vec(cleaned_tokens, size=100, #size:100차원
                          window=4, min_count=5, #window: min_count:모든 단어 20번이상
                          workers=4, iter=100, sg=1)

embedding_model.save('./crawling/yoggiyo_review_test.model')


print(embedding_model.wv.vocab.keys())
print(len(embedding_model.wv.vocab.keys()))


