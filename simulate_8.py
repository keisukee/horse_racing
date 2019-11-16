# ８章：購入シミュレーション
df = df_pred.copy()
# レースID単位で予測結果をもとに購入フラグを追加
race_id_list = df['race_id'].unique().tolist()
print(f'全レース数：{len(race_id_list)}')
print(f'全レコード数：{len(df)}')


def set_buy_predict(params):
    win3_pred = float(params.split('_')[0])
    odds = float(params.split('_')[1])

    # オッズ（標準化）が1〜8の範囲を購入するなら0.01〜0.08を設定
    if win3_pred >= 0.60 and 0.01 <= odds < 0.08:
        return 1
    else:
        return 0


# win3で予測
df['predict'] = df['win3_pred'].astype(str) + '_' + df['odds'].astype(str)
df['buy_predict'] = df['predict'].map(set_buy_predict)

buy_count = len(df[df['buy_predict'] == 1])
print(f'購入数：{buy_count}')
win_count = len(df[(df['buy_predict'] == 1) & (df['kitaichi'] > 0)])
print(f'的中数：{win_count}')
print(f'的中率：{round(win_count / buy_count * 100, 2)}%')
print(f'購入金額：{buy_count * 100}')
back = df[df['buy_predict'] == 1]['kitaichi'].sum()
profit = back - (buy_count * 100)
print(f'払戻金額：{back}')
print(f'利益：{profit}')
print(f'回収率：{round(((buy_count * 100 + profit)/(buy_count * 100))*100, 2)}%')
# 収益推移
graph = df.reset_index(drop=True)

graph['shushi'] = 0
for idx in range(graph.shape[0]):
    if graph.at[idx, 'buy_predict'] == 1:
        if graph.at[idx, 'kitaichi'] > 0:
            graph.at[idx, 'shushi'] = graph.at[idx, 'kitaichi'] - 100
        else:
            graph.at[idx, 'shushi'] = -100


def cumsum_year(df, year_from, month_from, date_from, year_to, month_to, date_to):
    graph = df[((df['race_date'] >= datetime.date(year_from, month_from, date_from))) & (
        df['race_date'] <= datetime.date(year_to, month_to, date_to))]
    buy_races = graph[['race_date', 'shushi']].groupby('race_date').sum()
    buy_races = buy_races.sort_values(['race_date'], ascending=True)

    buy_cumsum = buy_races.cumsum()
    buy_cumsum.plot(y=['shushi'], figsize=(10, 5), alpha=0.5)


cumsum_year(graph, 2018, 1, 1, 2019, 12, 31)
