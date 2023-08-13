'''youtubeの急上昇の動画の情報を取得するプログラム。
'''
import googleapiclient.discovery
import pandas as pd
import datetime

#日付
d_today = datetime.date.today()

# 急上昇のデータを取得する関数
def getYouTubeTop50():
    '''現時点の急上昇top50位までの動画を取得しcsvファイルとして保存する。
    
    Argments:
        API_KEY:YouTube Data API v3を使用し自身のAPIキーを生成したものを使用する。 
        snippet:チャンネル名、動画投稿日、チャンネルID、動画タイトル、動画についてるtagの情報が含まれる。
        statistics:視聴回数、お気に入りの数の情報が含まれる。
    Returns:
        result ddf:取得した動画の必要な情報だけのDataFrameを結合した結果。
    '''
    dic_list = []
    API_KEY = "AIzaSyBJQCgvYt5EVWlAeFtUgA2JBmWsHzATtEs"  # 自分のAPIキーを入れてください
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        maxResults=50,  # 取得する動画の個数
        regionCode="JP"  # 場所（国）の指定
    )
    response = request.execute()

    dic_list = dic_list + response['items']

    df = pd.DataFrame(dic_list)
    
    df1 = pd.DataFrame(list(df['id']))
    df2 = pd.DataFrame(list(df['snippet']))[['channelTitle','publishedAt','channelId','title','tags']]
    df3 = pd.DataFrame(list(df['statistics']))[['viewCount','likeCount']]
    ddf = pd.concat([df1,df2,df3], axis = 1)

    return ddf

videos = getYouTubeTop50()
videos.to_csv('youtubetop50_{}.csv'.format(d_today))#急上昇の動画50本のデータをまとめたcsvファイルを出力