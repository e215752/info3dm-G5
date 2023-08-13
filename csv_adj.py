'''取得した動画情報の修正プログラム。
取得した動画情報のtag欄の余分な括弧を削除する。
修正した動画情報のtagの頻出度が2以上の動画を用いて新しくscvファイルとして保存する。
'''
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
import ast
import datetime

#日付
d_today = datetime.date.today()

# CSVファイルからデータを読み込む
data = pd.read_csv('youtubetop50_{}.csv'.format(d_today))  # 入力データが含まれるCSVファイル

# 抽出対象の項目を選択
target_column = 'tags'  # 抽出対象の項目名

# 単語を一つずつ抽出する処理
words = []

for index, row in data.iterrows():
    text = str(row[target_column])  # 抽出対象の項目のデータを取得

    # リスト形式の文字列をリストに変換して、単語リストに追加
    try:
        # リスト形式の文字列をリストに変換して、単語リストに追加
        words_list = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        continue

    # 各単語に含まれる括弧を除去してリストに追加
    words.extend([re.sub(r'[()（）]', '', word) for word in words_list])

# 最初と最後の[]を除去
words = [word.strip() for word in words]

# 単語の頻度を数える
word_counts = Counter(words)

# 頻出度のデータをDataFrameにまとめる
df = pd.DataFrame.from_dict(word_counts, orient='index', columns=['frequency'])
df.index.name = 'keyword'

# 頻出度が2以上の行のみを抽出
df_filtered = df[df['frequency'] >= 2]

# 新しいCSVファイルに保存
df_filtered.to_csv('w_f_{}_filt.csv'.format(d_today), encoding='utf-8')

# 結果をCSVファイルに保存
df.to_csv('w_f_{}.csv'.format(d_today))