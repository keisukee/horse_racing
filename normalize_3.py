from sklearn.preprocessing import StandardScaler
file_name2 = 'data2.csv'
df = pd.read_csv(file_name2)
df['race_date'] = pd.to_datetime(df['race_date']).dt.date
# 情報不足行を削除
df = df.dropna(subset=['past_time_sec1', 'past_time_sec2', 'past_time_sec3',
                       'past_time_sec4', 'past_time_sec5']).reset_index(drop=True)

# レースID付与


def set_race_id(params):
    param_list = params.split('_')
    race_date, place, race_num = param_list[0], param_list[1], param_list[2],
    return f'{race_date}{place}{race_num}'


df['tmp'] = df['race_date'].astype(
    str) + '_' + df['place'].astype(str) + '_' + df['race_num'].astype(str)
df['race_id'] = df['tmp'].map(set_race_id)
df = df.drop(columns=['tmp'])

# 予測に使用しない列を削除（必要に応じて変更）
df = df.drop(columns=['horse', 'jockey', 'race_num', 'stable',
                    'race_name', 'rank', 'pop',  'gap', 'tansho', 'win1', 'time_sec'])

# ダミー列定義（One-Hot変換対象）
dummy_columns = ['sex', 'place', 'course_type', 'course_lr', 'weather', 'ground', 'past_course_type1', 'past_course_lr1', 'past_weather1', 'past_ground1', 'past_gap1', 'past_course_type2', 'past_course_lr2', 'past_weather2', 'past_ground2', 'past_gap2',
                'past_course_type3', 'past_course_lr3', 'past_weather3', 'past_ground3', 'past_gap3', 'past_course_type4', 'past_course_lr4', 'past_weather4', 'past_ground4', 'past_gap4', 'past_course_type5', 'past_course_lr5', 'past_weather5', 'past_ground5', 'past_gap5']

# ダミー化
df_dummy = df[dummy_columns]
df_dummy = pd.get_dummies(df_dummy, dummy_na=True)
df_main = df.drop(columns=dummy_columns)

# 標準化前に必要な情報を退避
df_main['kitaichi'] = df_main['win3'] * df_main['fukusho']
train_kitaichi = df_main.pop('kitaichi')
train_labels = df_main.pop('win3')
train_date = df_main.pop('race_date')
train_raceids = df_main.pop('race_id')
df_main = df_main.drop(columns=['fukusho'])

df_main = df_main.astype(float)
standard_file = 'standard.csv'
df_main.to_csv(standard_file, index=False)
# 標準化

ss = StandardScaler()
df_main = pd.DataFrame(ss.fit_transform(
    df_main), columns=df_main.columns, index=df_main.index)

# ダミー列とマージ
df = pd.concat([df_main, df_dummy], axis=1)

df['kitaichi'] = train_kitaichi.values
df['win3'] = train_labels.values
df['race_date'] = train_date.values
df['race_id'] = train_raceids.values
file_name3 = 'data3.csv'
df.to_csv(file_name3, index=False)

