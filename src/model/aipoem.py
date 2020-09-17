
import tensorflow as tf
import numpy as np
import os
import sys


# 전처리한 데이터가 담긴 파일 읽기
tmp = open("DATA.txt","r")
text = tmp.read()


# 생성된 text에서 정렬된 유일한 글자를 추출
word = sorted(set(text))

# 유일한 글자와 숫자를 맵핑할 딕셔너리 생성 
dword= {}
for i in range(len(word)):
    dword[word[i]] = i

arrword = np.array(word)

arrtxt = np.array([dword[i] for i in text])


cdata = tf.data.Dataset.from_tensor_slices(arrtxt)

# 단일 입력에 대해 원하는 문장의 최대 길이 한정
seq_length = 200

# 훈련 샘플/타깃 만들기
char_dataset = tf.data.Dataset.from_tensor_slices(arrtxt)
seq = char_dataset.batch(seq_length+1, drop_remainder=True)


def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

ddset = seq.map(split_input_target)

# 배치 크기
batch_size = 100
buff = 8000

ddset = ddset.shuffle(buff).batch(batch_size, drop_remainder=True)
# 문자로 된 어휘 사전의 크기
vocab_size = len(word)

# 임베딩 차원
emb = 512

# RNN 유닛
rnn_units = 1024

# 모델 생성함수(embedding-> LSTM -> Dense)
def build_model(vocab_size, emb, rnn_units, batch_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, emb,batch_input_shape=[batch_size, None]),
        tf.compat.v1.keras.layers.CuDNNLSTM(rnn_units,
                                            return_sequences=True, # 숨겨진 상태 출력을 반환
                                            stateful=True, #상태 유지
                                            recurrent_initializer='glorot_uniform'),#tanh를 활성함수로 사용할 때 좋은 초기값 활용
        tf.keras.layers.Dense(vocab_size)])
    return model

# 미리 선언해둔 변수를 이용해 모델 생성
model = build_model(
    vocab_size = len(word),
    emb=emb,
    rnn_units=rnn_units,
    batch_size=batch_size)

def loss(labels, logits):
  return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True) #정수 인코딩이므로 sparse_c_c를 사용

# 모델의 손실함수 및 최적화 컴파일
model.compile(loss = loss, optimizer='adam')

# 체크포인트 설정 - 모델 저장
checkpoint_dir = 'mmodel'

checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

# 체크포인트 생성
checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefix,
    save_weights_only=True)

# 에포치
EPOCHS=300

# 모델 학습시키기 - 학습하면서 callback 전달함
history = model.fit(ddset, epochs=EPOCHS, callbacks=[checkpoint_callback],verbose = 2)



# 모델 생성
model = build_model(vocab_size, emb, rnn_units, batch_size=1)

model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

model.build(tf.TensorShape([1, None]))

# 학습된 모델을 통해 시 짓기
def generate_poet(model, sstr, num):

  # 시작 문자열을 숫자로 변환(벡터화)
  itrans = [dword[i] for i in sstr]
  itrans = tf.expand_dims(itrans, 0)
  print(itrans)

  # 결과를 저장할 빈 문자열
  result = []

  model.reset_states()
  for i in range(num):
      pre = model(itrans)
      # 배치 차원 제거
      pre = tf.squeeze(pre, 0)

      # 범주형 분포를 사용하여 모델에서 리턴한 단어 예측
      pred_id = tf.random.categorical(pre, num_samples=1)[-1,0].numpy()

      # 예측된 단어를 다음 입력으로 모델에 전달
      # 이전 은닉 상태와 함께
      itrans = tf.expand_dims([pred_id], 0)

      result.append(arrword[pred_id])

  return (sstr + ''.join(result))

# 사용자로부터 입력받음
sstr = input("시를 짓기 위한 특정 단어 입력: ")
num = int(input("몇 자의 시를 작성하겠습니까? "))
print()
print(generate_poet(model, sstr+' ', num))

