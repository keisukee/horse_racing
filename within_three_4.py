
file_name3 = 'data3.csv'
df = pd.read_csv(file_name3)
df['race_date'] = pd.to_datetime(df['race_date']).dt.date
win3_sums = df.groupby('race_id')['win3'].sum()
win3_races = win3_sums[win3_sums == 3]
win3_races_indexs = win3_races.index.tolist()

win3_counts = df.groupby('race_id')['win3'].count()
win3_races2 = win3_counts[win3_counts >= 6]
win3_races_indexs2 = win3_races2.index.tolist()

race_id_list = list(set(win3_races_indexs) & set(win3_races_indexs2))

# 結構時間かかります
df_train = None
for id in race_id_list:
    id_df = df[df['race_id'] == id]
    df_tmp = id_df[id_df['win3'] == 1]
    loselen = len(id_df[id_df['win3'] == 0])
    df_tmp = df_tmp.append(id_df[id_df['win3'] == 0].iloc[[
                            loselen-3, loselen-2, loselen-1]], ignore_index=True)
    if df_train is None:
        df_train = df_tmp.sample(frac=1)
    else:
        df_train = df_train.append(df_tmp.sample(frac=1), ignore_index=True)

df_train = df_train.reset_index(drop=True)
file_name4 = 'data4.csv'
df_train.to_csv(file_name4, index=False)
