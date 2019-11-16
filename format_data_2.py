import time
import numpy as np
import datetime

def get_weight_gap(weight):
    weight_strs = weight.split('(')
    if len(weight_strs) == 1:
        return 0
    else:
        return int(weight_strs[1].replace(')', '').replace('+', ''))


def calc_time(time):
    min_sec_ms = str(time).split(':')
    return float(min_sec_ms[0]) * 60 + float(min_sec_ms[1])


def get_date(date):
    date_str = date.split('(')[0]
    date_strs = date_str.split('/')
    return datetime.date(int(date_strs[0]), int(date_strs[1]), int(date_strs[2]))


def get_clean(target):
    return target.replace('\u3000', '').replace('\xa0', '')


def make_data(df):
    df = df.dropna(subset=['sexage', 'weight', 'time', 'course_detail',
                            'race_condition', 'race_category', 'race_date']).reset_index(drop=True)
    df['sex'] = df['sexage'].map(lambda sexage: sexage[:1])
    df['age'] = df['sexage'].map(lambda sexage: sexage[1:])
    df['weight_now'] = df['weight'].map(lambda weight: weight.split('(')[0])
    df['weight_gap'] = df['weight'].map(get_weight_gap)
    df['time_sec'] = df['time'].map(calc_time)
    df['course_type'] = df['course_detail'].map(
        lambda course_detail: course_detail[0:1])
    df['course_distance'] = df['course_detail'].map(
        lambda course_detail: course_detail.split('m')[0][1:])
    df['course_lr'] = df['course_detail'].map(
        lambda course_detail: course_detail.split('(')[1].replace(')', ''))
    df['weather'] = df['race_condition'].map(
        lambda condition: condition.split('/')[0].split('：')[1].strip())
    df['ground'] = df['race_condition'].map(
        lambda condition: condition.split('/')[1].split('：')[1].strip())
    df['place'] = df['race_category'].map(
        lambda condition: condition.split('回')[1][:2])
    df['race_date'] = df['race_date'].map(get_date)
    df['jockey'] = df['jockey'].map(get_clean)
    df['win1'] = df['tansho'].map(lambda x: 1 if x > 0 else 0)
    df['win3'] = df['fukusho'].map(lambda x: 1 if x > 0 else 0)
    df = df.drop(columns=['sexage', 'weight', 'time',
                            'course_detail', 'race_condition', 'race_category'])

    return df


def set_past_info(df, year_from, month_from, date_from, year_to, month_to, date_to):
    df['past_days'] = np.nan

    df['past_course_type1'] = ''
    df['past_course_distance1'] = np.nan
    df['past_course_lr1'] = ''
    df['past_weather1'] = ''
    df['past_ground1'] = ''
    df['past_time_sec1'] = np.nan
    df['past_gap1'] = ''
    df['past_rank1'] = np.nan
    df['past_pop1'] = np.nan
    df['past_odds1'] = np.nan

    df['past_course_type2'] = ''
    df['past_course_distance2'] = np.nan
    df['past_course_lr2'] = ''
    df['past_weather2'] = ''
    df['past_ground2'] = ''
    df['past_time_sec2'] = np.nan
    df['past_gap2'] = ''
    df['past_rank2'] = np.nan
    df['past_pop2'] = np.nan
    df['past_odds2'] = np.nan

    df['past_course_type3'] = ''
    df['past_course_distance3'] = np.nan
    df['past_course_lr3'] = ''
    df['past_weather3'] = ''
    df['past_ground3'] = ''
    df['past_time_sec3'] = np.nan
    df['past_gap3'] = ''
    df['past_rank3'] = np.nan
    df['past_pop3'] = np.nan
    df['past_odds3'] = np.nan

    df['past_course_type4'] = ''
    df['past_course_distance4'] = np.nan
    df['past_course_lr4'] = ''
    df['past_weather4'] = ''
    df['past_ground4'] = ''
    df['past_time_sec4'] = np.nan
    df['past_gap4'] = ''
    df['past_rank4'] = np.nan
    df['past_pop4'] = np.nan
    df['past_odds4'] = np.nan

    df['past_course_type5'] = ''
    df['past_course_distance5'] = np.nan
    df['past_course_lr5'] = ''
    df['past_weather5'] = ''
    df['past_ground5'] = ''
    df['past_time_sec5'] = np.nan
    df['past_gap5'] = ''
    df['past_rank5'] = np.nan
    df['past_pop5'] = np.nan
    df['past_odds5'] = np.nan

    df_all = df.copy()
    df_new = df[(df['race_date'] >= datetime.date(year_from, month_from, date_from)) & (
        df['race_date'] <= datetime.date(year_to, month_to, date_to))].reset_index(drop=True)
    print(f'設定対象レコード数：{len(df_new)}')
    for idx in range(df_new.shape[0]):
        # 直近5レース
        recent_df = df_all[(df_all['horse'] == df_new.at[idx, 'horse']) & (
            df_all['race_date'] < df_new.at[idx, 'race_date'])].sort_values(by=['race_date'], ascending=False).reset_index(drop=True)

        if len(recent_df) >= 1:
            df_new.at[idx, 'past_days'] = (
                df_new.at[idx, 'race_date'] - recent_df.at[0, 'race_date']).days

            df_new.at[idx, 'past_course_type1'] = recent_df.at[0, 'course_type']
            df_new.at[idx, 'past_course_distance1'] = recent_df.at[0,
                                                                    'course_distance']
            df_new.at[idx, 'past_course_lr1'] = recent_df.at[0, 'course_lr']
            df_new.at[idx, 'past_weather1'] = recent_df.at[0, 'weather']
            df_new.at[idx, 'past_ground1'] = recent_df.at[0, 'ground']
            df_new.at[idx, 'past_time_sec1'] = recent_df.at[0, 'time_sec']
            df_new.at[idx, 'past_gap1'] = recent_df.at[0, 'gap']
            df_new.at[idx, 'past_rank1'] = recent_df.at[0, 'rank']
            df_new.at[idx, 'past_pop1'] = recent_df.at[0, 'pop']
            df_new.at[idx, 'past_odds1'] = recent_df.at[0, 'odds']

        if len(recent_df) >= 2:
            df_new.at[idx, 'past_course_type2'] = recent_df.at[1, 'course_type']
            df_new.at[idx, 'past_course_distance2'] = recent_df.at[1,
                                                                    'course_distance']
            df_new.at[idx, 'past_course_lr2'] = recent_df.at[1, 'course_lr']
            df_new.at[idx, 'past_weather2'] = recent_df.at[1, 'weather']
            df_new.at[idx, 'past_ground2'] = recent_df.at[1, 'ground']
            df_new.at[idx, 'past_time_sec2'] = recent_df.at[1, 'time_sec']
            df_new.at[idx, 'past_gap2'] = recent_df.at[1, 'gap']
            df_new.at[idx, 'past_rank2'] = recent_df.at[1, 'rank']
            df_new.at[idx, 'past_pop2'] = recent_df.at[1, 'pop']
            df_new.at[idx, 'past_odds2'] = recent_df.at[1, 'odds']

        if len(recent_df) >= 3:
            df_new.at[idx, 'past_course_type3'] = recent_df.at[2, 'course_type']
            df_new.at[idx, 'past_course_distance3'] = recent_df.at[2,
                                                                    'course_distance']
            df_new.at[idx, 'past_course_lr3'] = recent_df.at[2, 'course_lr']
            df_new.at[idx, 'past_weather3'] = recent_df.at[2, 'weather']
            df_new.at[idx, 'past_ground3'] = recent_df.at[2, 'ground']
            df_new.at[idx, 'past_time_sec3'] = recent_df.at[2, 'time_sec']
            df_new.at[idx, 'past_gap3'] = recent_df.at[2, 'gap']
            df_new.at[idx, 'past_rank3'] = recent_df.at[2, 'rank']
            df_new.at[idx, 'past_pop3'] = recent_df.at[2, 'pop']
            df_new.at[idx, 'past_odds3'] = recent_df.at[2, 'odds']

        if len(recent_df) >= 4:
            df_new.at[idx, 'past_course_type4'] = recent_df.at[3, 'course_type']
            df_new.at[idx, 'past_course_distance4'] = recent_df.at[3,
                                                                    'course_distance']
            df_new.at[idx, 'past_course_lr4'] = recent_df.at[3, 'course_lr']
            df_new.at[idx, 'past_weather4'] = recent_df.at[3, 'weather']
            df_new.at[idx, 'past_ground4'] = recent_df.at[3, 'ground']
            df_new.at[idx, 'past_time_sec4'] = recent_df.at[3, 'time_sec']
            df_new.at[idx, 'past_gap4'] = recent_df.at[3, 'gap']
            df_new.at[idx, 'past_rank4'] = recent_df.at[3, 'rank']
            df_new.at[idx, 'past_pop4'] = recent_df.at[3, 'pop']
            df_new.at[idx, 'past_odds4'] = recent_df.at[3, 'odds']

        if len(recent_df) >= 5:
            df_new.at[idx, 'past_course_type5'] = recent_df.at[4, 'course_type']
            df_new.at[idx, 'past_course_distance5'] = recent_df.at[4,
                                                                    'course_distance']
            df_new.at[idx, 'past_course_lr5'] = recent_df.at[4, 'course_lr']
            df_new.at[idx, 'past_weather5'] = recent_df.at[4, 'weather']
            df_new.at[idx, 'past_ground5'] = recent_df.at[4, 'ground']
            df_new.at[idx, 'past_time_sec5'] = recent_df.at[4, 'time_sec']
            df_new.at[idx, 'past_gap5'] = recent_df.at[4, 'gap']
            df_new.at[idx, 'past_rank5'] = recent_df.at[4, 'rank']
            df_new.at[idx, 'past_pop5'] = recent_df.at[4, 'pop']
            df_new.at[idx, 'past_odds5'] = recent_df.at[4, 'odds']

        if idx % 1000 == 0:
            print(f'{idx}レコード設定完了')
    return df_new


file_name1 = 'data1.csv'
df = pd.read_csv(file_name1)

# 欠損値（順位や人気が欠けているレコード）を削除
df = df.dropna(subset=['rank', 'pop']).reset_index(drop=True)

# データ加工
df = make_data(df)
# 過去データ設定（かなり時間がかかります）
# 当初、引数の1つ目が2011になっていましたが、2010の誤りでした。
for year in range(2010, 2020):
    dftmp = set_past_info(df, year, 1, 1, year, 12, 31)
    file_name_tmp = f'data2_{year}.csv'
    dftmp.to_csv(file_name_tmp, index=False)
# data2_2010〜2019のCSVがカレントディレクトリにある状態で実行
file_name2 = 'data2.csv'
join_csv('.', file_name2)
