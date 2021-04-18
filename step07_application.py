import sys
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmwrite, mmread
import pickle

import urllib.request

form_window = uic.loadUiType('./data/application_ui.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.df_review = pd.read_csv('./data/yoggiyo_data_all.csv', index_col = 0)
        self.Tfidf_matrix = mmread('./data/tfidf_yoggiyo_data_all.mtx').tocsr()
        # type이 달라서 csr로 바꾸어줘야 함
        self.embedding_model = Word2Vec.load('./data/yoggiyo_data_all_filtered.model')
        with open('./data/tfidf_data_all.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        titles = list(self.df_review.title)
        # titles = sorted(titles)
        for title in titles:
            self.cmb_title.addItem(title)

        # 웹에서 Load한 Image를 이용하여 QPixmap에 사진데이터를 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapWebVar1 = QPixmap()
        self.qPixmapWebVar2 = QPixmap()
        self.qPixmapWebVar3 = QPixmap()

        # 자동완성
        model = QStringListModel()
        model.setStringList(list(titles)) # 시리즈가 아닌 리스트로 넘겨주기
        completer = QCompleter(model)
        completer.setModel((model))

        # 자동완성하는 QCompleter에게 모델을 넘겨주는데, 그 모델은 자동완성될 문자열들의 리스트가 필요
        self.le_title.setCompleter(completer)

        self.btn_recommend.clicked.connect(self.btn_recommend_slot) # 버튼 클릭시 추천 영화 뜨게
        self.cmb_title.currentIndexChanged.connect(self.cmb_title_slot) # 콤보 박스에서 다른 거 선택하면 알아서 영화 뜨게
        self.btn_one.clicked.connect(self.btn_one_slot) # 가성
        self.btn_two.clicked.connect(self.btn_one_slot) # 친절한
        self.btn_three.clicked.connect(self.btn_one_slot) # 빠르다
        self.btn_four.clicked.connect(self.btn_one_slot) # 양도

    def btn_one_slot(self):
        btn_title = self.sender().text()

        if btn_title == '가성비':
            print(btn_title)
            title = '퀄리티'
        elif btn_title == '서비스':
            print(btn_title)
            title = '서비스'
        elif btn_title == '신속 배달':
            print(btn_title)
            title = '빠른'
        elif btn_title == '푸짐':
            print(btn_title)
            title = '양도'

        sentence = [title] * 10  # 입력받은 키워드로 진행
        if title in self.embedding_model.wv.vocab:  # 키워드가 있어야 진행
            sim_word = self.embedding_model.wv.most_similar(title, topn=10)
            labels = []  # 유사 단어만 뽑아서 label 리스트에 넣기
            for label, _ in sim_word:
                labels.append(label)
            print(labels)
            for i, word in enumerate(labels):  # 0부터시작하는 인덱스 붙여줌
                sentence += [word] * (9 - i)  # ['서로'] * 9, ['헤어지는'] * 8 ... ['있을까'] * 0
        sentence = ' '.join(sentence)
        sentence_vec = self.Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommend = self.getRecommendation(cosine_sim)
        self.set_store_info(recommend)

    def getRecommendation(self, cosine_sim):
        simScores = list(enumerate(cosine_sim[-1]))  # 밑의 enumerate 함수 참고
        simScores = sorted(simScores, key=lambda x: x[1], reverse=True)  # 뒤에 있는 값을 가지고 내림차순으로 sorted
        simScores = simScores[0:4]  # 이걸로 출력될 영화 개수 설정 가능
        foodidx = [i[0] for i in simScores]  # 제일 유사한 영화들의 인덱스가 들어가 있음
        RecFoodList = self.df_review.iloc[foodidx]  # 데이터 프레임
        return RecFoodList  # 뒤 데이터 프레임의 title만 시리즈로 리턴

    def cmb_title_slot(self):
        title = self.cmb_title.currentText() # 현재 선택되어 있는 텍스트
        food_idx = self.df_review[self.df_review['title'] == title ].index[0]
        # Tfidf = TfidfVectorizer(sublinear_tf=True)
        # Tfidf_matrix = Tfidf.fit_transform(self.df_review['review'])
        cosine_sim = linear_kernel(self.Tfidf_matrix[food_idx], self.Tfidf_matrix)
        # recommend = '\n'.join(list(self.getRecommendation(cosine_sim))[1:]) # 인덱싱: 자기 자신 제외
        # 시리즈를 하나의 문자열로 붙임(리스토로 바꿔도 되고 안 바꿔도 되고) + 줄바꿈
        recommend = self.getRecommendation(cosine_sim)
        self.set_store_info(recommend)

    def btn_recommend_slot(self):
        title = self.le_title.text()  # 라인 에디트에 입력되는 내용 가져오기
        cosine_sim = None
        if title in list(self.df_review['title']): # 타이틀이 있으면
            food_idx = self.df_review[self.df_review['title'] == title].index[0]
            # Tfidf = TfidfVectorizer(sublinear_tf=True)
            # Tfidf_matrix = Tfidf.fit_transform(self.df_review['review'])
            # 반복 되므로 생성자 함수 안에 넣어줌
            cosine_sim = linear_kernel(self.Tfidf_matrix[food_idx], self.Tfidf_matrix)
            # recommend = '\n'.join(list(self.getRecommendation(cosine_sim))[1:])
            recommend = self.getRecommendation(cosine_sim)
            # 시리즈를 하나의 문자열로 붙임 + 줄바꿈
        else: # 해당 타이틀이 없으면 키워드 기반으로 영화 추천
            #self.lbl_result.setText('영화 제목을 정확하게 입력해주세요')
            sentence = [title] * 10 # 입력받은 키워드로 진행
            if title in self.embedding_model.wv.vocab:  # 키워드가 있어야 진행
                sim_word = self.embedding_model.wv.most_similar(title, topn=10)
                labels = []  # 유사 단어만 뽑아서 label 리스트에 넣기
                for label, _ in sim_word:
                    labels.append(label)
                print(labels)
                for i, word in enumerate(labels):  # 0부터시작하는 인덱스 붙여줌
                    sentence += [word] * (9 - i)  # ['서로'] * 9, ['헤어지는'] * 8 ... ['있을까'] * 0
            sentence = ' '.join(sentence)
            sentence_vec = self.Tfidf.transform([sentence])
            # sentence를 벡터화해서 넘겨줌
            cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
            recommend = self.getRecommendation(cosine_sim)
        self.set_store_info(recommend)

    def set_store_info(self, recommend):
        recommend_title_list = []
        recommend_menu_list = []
        recommend_menu_img_list = []
        for i in range(1, 4):
            recommend_title_list.append(recommend.iloc[i].title)
            recommend_menu_list.append(recommend.iloc[i].menu)
            recommend_menu_img_list.append(recommend.iloc[i].menu_img)
        try:
            imageFromWeb1 = urllib.request.urlopen(recommend_menu_img_list[0]).read()
            self.qPixmapWebVar1.loadFromData(imageFromWeb1)
            self.qPixmapWebVar1 = self.qPixmapWebVar1.scaledToWidth(150)
            self.lbl_img_1.setPixmap(self.qPixmapWebVar1)
            self.lbl_title_1.setText(recommend_title_list[0])
            self.lbl_menu_1.setText(recommend_menu_list[0])
        except:
            self.lbl_img_1.setText('no image')
            self.lbl_title_1.setText(recommend_title_list[0])
            self.lbl_menu_1.setText(recommend_menu_list[0])

        try:
            imageFromWeb2 = urllib.request.urlopen(recommend_menu_img_list[1]).read()
            self.qPixmapWebVar2.loadFromData(imageFromWeb2)
            self.qPixmapWebVar2 = self.qPixmapWebVar2.scaledToWidth(150)
            self.lbl_img_2.setPixmap(self.qPixmapWebVar2)
            self.lbl_title_2.setText(recommend_title_list[1])
            self.lbl_menu_2.setText(recommend_menu_list[1])
        except:
            self.lbl_img_2.setText('no image')
            self.lbl_title_2.setText(recommend_title_list[1])
            self.lbl_menu_2.setText(recommend_menu_list[1])

        try:
            imageFromWeb3 = urllib.request.urlopen(recommend_menu_img_list[2]).read()
            self.qPixmapWebVar3.loadFromData(imageFromWeb3)
            self.qPixmapWebVar3 = self.qPixmapWebVar3.scaledToWidth(150)
            self.lbl_img_3.setPixmap(self.qPixmapWebVar3)
            self.lbl_title_3.setText(recommend_title_list[2])
            self.lbl_menu_3.setText(recommend_menu_list[2])
        except:
            self.lbl_img_3.setText('no image')
            self.lbl_title_3.setText(recommend_title_list[2])
            self.lbl_menu_3.setText(recommend_menu_list[2])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Exam()
    w.show()
    sys.exit(app.exec_())