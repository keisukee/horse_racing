import tensorflow as tf
import matplotlib.pyplot as plt
５章：予測モデル作成
file_name4 = 'data4.csv'
df = pd.read_csv(file_name4)
df['race_date'] = pd.to_datetime(df['race_date']).dt.date
# 学習用と評価用を分ける
df_train = df[df['race_date'] < datetime.date(2018, 1, 1)]
df_valid = df[df['race_date'] >= datetime.date(2018, 1, 1)]

train_labels = df_train.pop('win3')
train_odds = df_train.pop('odds')
train_date = df_train.pop('race_date')
train_raceids = df_train.pop('race_id')
train_kitaichi = df_train.pop('kitaichi')

valid_labels = df_valid.pop('win3')
valid_odds = df_valid.pop('odds')
df_valid.pop('race_date')  # 未使用
df_valid.pop('race_id')  # 未使用
df_valid.pop('kitaichi')  # 未使用

# 予測する際はこの列順でデータを渡す
print(df_train.columns.tolist())
# グラフ描画


def plot_history(history):
   hist = pd.DataFrame(history.history)
   hist['epoch'] = history.epoch

   plt.figure()
   plt.xlabel('Epoch')
   plt.ylabel('Acc')
   plt.plot(hist['epoch'], hist['acc'],
            label='Train Acc')
   plt.plot(hist['epoch'], hist['val_acc'],
            label='Val Acc')
   plt.ylim([0.7, 0.8])
   plt.legend()
   plt.show()

   plt.figure()
   plt.xlabel('Epoch')
   plt.ylabel('Loss')
   plt.plot(hist['epoch'], hist['loss'],
            label='Train Loss')
   plt.plot(hist['epoch'], hist['val_loss'],
            label='Val Loss')
   plt.ylim([0.5, 0.6])
   plt.legend()
   plt.show()

# モデルを保存


def save_model(model):
   now = datetime.datetime.now().strftime('%Y%m%d%H%M')
   model_file = f'model_{now}.h5'
   print(model_file)
   model.save(model_file)


def make_model(df_train, train_labels, df_valid, valid_labels, node_size, batch_size, shuffle, epochs):
   model = tf.keras.Sequential([
       tf.keras.layers.Dense(node_size, kernel_regularizer=tf.keras.regularizers.l2(
           0.001), activation=tf.nn.relu, input_dim=len(df_train.columns)),
       tf.keras.layers.Dropout(0.2),
       tf.keras.layers.Dense(node_size, kernel_regularizer=tf.keras.regularizers.l2(
           0.001), activation=tf.nn.relu),
       tf.keras.layers.Dropout(0.2),
       tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)
   ])

   model.compile(
       loss='binary_crossentropy',
       optimizer=tf.keras.optimizers.Adam(),
       metrics=['accuracy'])

   # print(model.summary())

   fit = model.fit(df_train,
                   train_labels,
                   validation_data=(df_valid, valid_labels),
                   epochs=epochs,
                   batch_size=batch_size,
                   shuffle=shuffle,
                   verbose=0)

   plot_history(fit)
   save_model(model)


# モデル作成
node_size, batch_size, epochs, shuffle = 300, 32, 30, True
make_model(df_train, train_labels, df_valid, valid_labels,
           node_size, batch_size, shuffle, epochs)
