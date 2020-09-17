# 시 짓는 인공지능  
[관련자료](http://yerin.creatorlink.net/%EC%8B%9C-%EC%A7%93%EB%8A%94-%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5)  

### 내용
기존 시를 짓는 인공지능은 한국어가 아닌 외국어로 작성되기 때문에, 이와 차별점을 두어 RNN을 활용하여 한국 시를 학습시킨 후 한국어로 된 시를 짓는 AI를 개발함 

### 과정

 1) 크롤링을 통한 한국 시 데이터 수집 및 전처리      
 2) LSTM을 이용해 1)에서 전처리한 데이터를 이용해 모델 구축    
 3) 학습을 통해 완성된 모델을 이용해 특정 단어를 input data로 넣어서 sampling 했을 때 나타나는 [결과](http://yerin.creatorlink.net/%EC%8B%9C-%EC%A7%93%EB%8A%94-%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5)를 다룸    
