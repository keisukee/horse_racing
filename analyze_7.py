# ７章：傾向分析（グラフ化）
import matplotlib.pyplot as plt
df = df_pred.copy()

# オッズを標準化前に戻す


def get_all_ss():
    standard_file = 'standard.csv'
    tmp_all = pd.read_csv(standard_file)
    ss = StandardScaler()
    ss.fit(tmp_all)
    return ss, tmp_all.columns


ss, ss_columns = get_all_ss()
tmp = df[ss_columns]
tmp = pd.DataFrame(ss.inverse_transform(
    tmp), columns=tmp.columns, index=tmp.index)
df['odds_org'] = tmp['odds']

# 3着指数（予測結果の100倍で見やすく）
df['win3_index'] = df['win3_pred'] * 100

# 3着指数の一定範囲ごとに分割
last_pred, step = 100, 5
labels = [f'{i}' for i in range(0, last_pred, step)]
cut = pd.cut(df['win3_index'],
            np.arange(0, last_pred+1, step),
            include_lowest=True,
            right=False,
            labels=labels)

# 的中率
df_means = df.groupby(cut)['win3'].mean().reset_index()
df_means['win3'] = df_means['win3'] * 100

# 期待値
kitaichi_mean = df.groupby(
    cut)['kitaichi'].mean().reset_index().pop('kitaichi')
df_means['kitaichi'] = kitaichi_mean

fig, ax = plt.subplots()
df_means.set_index('win3_index').plot(ax=ax)

ax.set_xlabel('win3_index')
ax.set_ylabel('kitaichi / win3')
ax.legend(['win3', 'kitaichi'])
plt.show()
# 平均オッズ
df_means = df.groupby(cut)['odds_org'].mean().reset_index()
df_means['win3_index'] = df_means['win3_index'].astype(int)

plt.scatter(df_means['win3_index'], df_means['odds_org'])
plt.ylabel("odds")
plt.xlabel("win3_index")
# 指数60以上のものを分析
df = df_pred.copy()
df = df[df['win3_pred'] > 0.6]
df['shushi'] = df['kitaichi'] - 100

df = df.reset_index(drop=True)
df['odds2'] = df['odds'] * 100

labels = [f'{i}' for i in range(-60, 61, 1)]
cut1 = pd.cut(df['odds2'], np.arange(-60, 62, 1),
            include_lowest=True,
            right=False,
            labels=labels)

df['odds_each'] = cut1.values

for idx in range(df.shape[0]):
    odds_each = df.at[idx, 'odds_each']
    df.at[idx, str(odds_each)] = df.at[idx, 'shushi']

odds_list = list(map(str, list(range(-60, 61))))
add_columns = list(set(odds_list) - set(df.columns))
for column in add_columns:
    df[column] = 0

df['win3_index'] = df['win3_pred'] * 100
labels = ["w{0}-{1}".format(i, i + 4) for i in range(0, 100, 5)]
cut2 = pd.cut(df['win3_index'], np.arange(0, 101, 5),
                include_lowest=True,
                right=False,
                labels=labels)

shushi_sum = df.groupby(cut2)[odds_list].sum().reset_index()
shushi_sum = shushi_sum.sum()[1:]
shushi_sum.plot()

# 0以上が続く部分のオッズが狙い目（モデルによるが、1〜7ぐらいが安定することが多い）
# ※標準化しているため、実際のオッズとは異なることに注意
shushi_sum[shushi_sum > 0]
