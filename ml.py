'''過去と現在の情報を用いてk-meansクラスタリングしようとしたプログラム。
'''
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import datetime

#日付
d_today = datetime.date.today()

# CSVファイルからデータを読み込む
past_data = pd.read_csv('w_f_2023-07-27.csv')  # 過去のタグの頻出度データが含まれるCSVファイル
current_data = pd.read_csv('w_f_{}.csv'.format(d_today))  # 現在のタグの頻出度データが含まれるCSVファイル

# タグの頻出度データをベクトル化する
vectorizer = CountVectorizer()
X_past = vectorizer.fit_transform(past_data['keyword'])
X_current = vectorizer.transform(current_data['keyword'])

# K-meansクラスタリングを実行
k = 5  # クラスタの数（適宜変更して調整）
kmeans_past = KMeans(n_clusters=k, random_state=42)
kmeans_past.fit(X_past)

kmeans_current = KMeans(n_clusters=k, random_state=42)
kmeans_current.fit(X_current)

# クラスタリング結果をデータに追加
past_data['cluster'] = kmeans_past.labels_
current_data['cluster'] = kmeans_current.labels_

# クラスタリング結果をCSVファイルに保存
past_data.to_csv('past_clustered_data.csv', index=False)
current_data.to_csv('current_clustered_data.csv', index=False)

# クラスタリング結果を可視化（過去のトレンド動画）
plt.figure(figsize=(10, 6))  # 可視化のための図のサイズを設定
plt.scatter(X_past.toarray()[:, 0], X_past.toarray()[:, 1], c=kmeans_past.labels_, cmap='rainbow')
# クラスタリング結果を2次元散布図として表示。X_pastには過去のタグデータのベクトル化結果が含まれる。
# クラスタリングの結果（kmeans_past.labels_）に基づいて色分けし、カラーマップは'rainbow'を使用。
plt.title('K-means Clustering (Past Trending Tags)')  # グラフのタイトルを設定
plt.xlabel('Tag Frequency 1')  # X軸のラベルを設定
plt.ylabel('Tag Frequency 2')  # Y軸のラベルを設定
plt.savefig('past_clustering.png')  # グラフを画像ファイルとして保存

# クラスタリング結果を可視化（現在のトレンド動画）
plt.figure(figsize=(10, 6))  # 可視化のための図のサイズを設定
plt.scatter(X_current.toarray()[:, 0], X_current.toarray()[:, 1], c=kmeans_current.labels_, cmap='rainbow')
# クラスタリング結果を2次元散布図として表示。X_currentには現在のタグデータのベクトル化結果が含まれる。
# クラスタリングの結果（kmeans_current.labels_）に基づいて色分けし、カラーマップは'rainbow'を使用。
plt.title('K-means Clustering (Current Trending Tags)')  # グラフのタイトルを設定
plt.xlabel('Tag Frequency 1')  # X軸のラベルを設定
plt.ylabel('Tag Frequency 2')  # Y軸のラベルを設定
plt.savefig('current_clustering.png')  # グラフを画像ファイルとして保存
