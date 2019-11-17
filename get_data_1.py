import time
import shutil
import glob
import os
import sys
import pandas as pd
from tqdm import tqdm
import urllib.request
from bs4 import BeautifulSoup


def get_common_info(html, df):
    """
    レース単位で持つ共通情報をスクレイピングする。

    Parameters
    ----------
    html : スクレイピング対象のHTML
    df : レース情報を追加したいDataframe

    Returns
    -------
    df : レース情報を追加済みのDataframe
    """

    s_soup = BeautifulSoup(html)

    # レース番号
    race_div = s_soup.find("div", class_="mainrace_data fc")
    race_num_dt = race_div.find('dt')
    race_num = race_num_dt.text.replace('R', '').replace('\n', '')

    # レース名
    race_h1 = race_div.find('h1')
    race_name = race_h1.text

    race_div_p = race_div.find_all('p')

    # コース詳細
    course_detail_p = race_div_p[0]
    course_detail = course_detail_p.text

    # 状態
    condition_p = race_div_p[1]
    race_condition = condition_p.text

    # 日付
    date_p = race_div_p[2]
    race_date = date_p.text

    # レース種別
    race_category_p = race_div_p[3]
    race_category = race_category_p.text

    df['race_num'] = race_num
    df['race_name'] = race_name
    df['course_detail'] = course_detail
    df['race_condition'] = race_condition
    df['race_date'] = race_date
    df['race_category'] = race_category
    return df

# tdタグ内の払い戻し額をリストで取得する簡易的関数


def get_td_int_list(html):
    td_text = str(html).replace('<td>', '').replace('<td class="txt_r">', '').replace(
        '</td>', '').replace('円', '').replace(',', '').split('<br/>')
    td_int = [int(s) for s in td_text]
    return td_int


def get_prize_info(html, df):
    """
    レース単位で持つ払い戻し情報をスクレイピングする。

    Parameters
    ----------
    html : スクレイピング対象のHTML
    df : 払い戻し情報を追加したいDataframe。既に馬情報が設定されている必要あり。

    Returns
    -------
    df : 払い戻し情報を追加済みのDataframe
    """

    s_soup = BeautifulSoup(html)
    prize_table = s_soup.find('table', class_='pay_table_01')
    td_list = prize_table.find_all('td')
    th_list = prize_table.find_all('th')

    # 単勝払い戻し額、複勝払い戻し額の列を作成（初期値0）
    df['tansho'] = 0
    df['fukusho'] = 0

    # 単勝払い戻し対象の馬番のリスト取得
    t_horse_num_list = get_td_int_list(td_list[0])
    # 単勝払い戻し額のリスト取得
    t_prize_list = get_td_int_list(td_list[1])

    # dfに設定済みの馬番と合致するレコードに、単勝払い戻し額を設定
    for i in range(len(t_horse_num_list)):
        df.loc[df['horse_num'] == t_horse_num_list[i], 'tansho'] = t_prize_list[i]

    # テーブルに'複勝'を含む場合のみ（複勝が存在しないレースもある）
    if('複勝' in th_list[1]):
        # 複勝払い戻し額のリスト取得
        f_horse_num_list = get_td_int_list(td_list[3])
        f_prize_list = get_td_int_list(td_list[4])

        # dfに設定済みの馬番と合致するレコードに、複勝払い戻し額を設定
        for i in range(len(f_horse_num_list)):
            df.loc[df['horse_num'] == f_horse_num_list[i],
                    'fukusho'] = f_prize_list[i]

    return df


# CSV結合

def join_csv(dir, file_name):
    """
    dirディレクトリにある全てのCSVファイルを結合し、
    カレントディレクトリにCSVファイル（ファイル名：file_name）として保存する。

    Parameters
    ----------
    dir : CSVが保存されているディレクトリ
    file_name : 保存するファイル名

    """
    # フォルダ中のパスを取得
    all_csv_files = glob.glob(f'{dir}/*.csv')
    df = None
    for file in all_csv_files:
        if df is None:
            df = pd.read_csv(file)
        else:
            df = df.append(pd.read_csv(file), ignore_index=True)

    # csv出力
    df.to_csv(f'{file_name}', index=False)


def zfill(num): return str(num).zfill(2)


def scraping(year, dir_tmp):
    """
    year年のデータをスクレイピングし、dir_tmpディレクトリにCSVファイル（複数）に保存する。

    Parameters
    ----------
    year : スクレイピング対象年
    dir_tmp : 保存する一時ディレクトリ名

    """
    DF_MEMORY_SIZE = 4000000
    BASE_URL = 'https://race.netkeiba.com/?pid=race&id=p'
    # 馬情報の列名
    DF_TMP_COL = ['rank', 'frame', 'horse_num', 'horse', 'sexage',
                    'futan', 'jockey', 'time', 'gap', 'pop', 'odds', 'stable', 'weight']
    # レース情報、払い戻し情報、馬情報全て含めた列名
    DF_ALL_COL = ['rank', 'frame', 'horse_num', 'horse', 'sexage', 'futan', 'jockey', 'time', 'gap', 'pop', 'odds', 'stable',
                    'weight', 'race_num', 'race_name', 'course_detail', 'race_condition', 'race_date', 'race_category', 'tansho', 'fukusho']

    df_all = pd.DataFrame(columns=DF_ALL_COL)
    csv_count = 0

    for i in tqdm(range(1, 11)):
        for j in range(1, 11):
            print("df size:{}bite".format(sys.getsizeof(df_all)))
            for k in range(1, 11):
                for l in range(1, 13):
                    time.sleep(1)
                    page_id = f'{year}{zfill(i)}{zfill(j)}{zfill(k)}{zfill(l)}'
                    url = BASE_URL + page_id
                    html = urllib.request.urlopen(url).read()
                    try:
                        # 1つ目のテーブルに'単勝'を含む場合のみ取得対象とする
                        df = pd.read_html(html, match='単勝')[0]
                        print(f'OK: {url}')
                    except:
                        # 1つ目のテーブルに'単勝'を含まない場合はエラーとなるためスキップ
                        print(f'NoTable: {url}')
                        break
                    df.drop([0])
                    try:
                        # 1つ目のテーブル取得情報に、馬情報の列名を設定
                        df.columns = DF_TMP_COL
                    except:
                        # 列数が合わない場合はエラーとなるためスキップ
                        print('列不一致のため取得できず')
                        break
                    # レース共通情報を設定
                    df = get_common_info(html, df)
                    # 払い戻し情報を設定
                    df = get_prize_info(html, df)

                    # 取得できた馬の数（対象レースの出走馬数）を設定
                    df['run_count'] = len(df)
                    df_all = df_all.append(df)

                    # 指定メモリサイズを超えたら一旦CSV出力しリセット
                    if sys.getsizeof(df_all) >= DF_MEMORY_SIZE:
                        df_all.to_csv(
                            f'{dir_tmp}/{str(year)}{str(csv_count)}.csv', index=False)
                        print('csv No.{} 出力完了'.format(csv_count))
                        df_all = pd.DataFrame(columns=DF_ALL_COL)
                        csv_count += 1

    # 全て取得できたらCSV出力しリセット
    df_all.to_csv(f'{dir_tmp}/{str(year)}{str(csv_count)}.csv', index=False)
    print('csv No.{} 出力完了'.format(csv_count))
    print('プログラムが正常に終了しました')


def year_scraping(year):
    """
    year年のデータをスクレイピングし、
    カレントディレクトリに1つのCSV（ファイル名：keiba_YYYY.csv）として保存する。

    Parameters
    ----------
    year : スクレイピング対象年

    """
    # 一時的なCSVディレクトリ作成
    dir_tmp = 'tmp'
    if os.path.exists(dir_tmp):
        # 既に存在するなら削除して再作成
        shutil.rmtree(dir_tmp)
        os.mkdir(dir_tmp)
    else:
        os.mkdir(dir_tmp)

    # スクレイピングCSVを作成
    scraping(year, dir_tmp)
    file_name = f'keiba_{year}.csv'
    # この時点では一時フォルダに複数CSVがあるので、結合して出力する
    join_csv(dir_tmp, file_name)


# year_scraping(2009)
# year_scraping(2010)
# year_scraping(2011)
year_scraping(2012)
year_scraping(2013)
year_scraping(2014)
year_scraping(2015)
year_scraping(2016)
year_scraping(2017)
year_scraping(2018)
# year_scraping(2019)
# 2009〜2019のCSVのみがカレントディレクトリにある状態で実行
# 他の形式のCSVが入っていると、エラーになると思います
# file_name1 = 'data1.csv'
# join_csv('.', file_name1)
