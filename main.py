import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm #normal distribution

#各種画面設定
st.set_page_config(layout="wide") #広めのレイアウト

#データフレームのレイアウト
df_width = 600
df_height = 600

#各種変数設定
data_upper_bound = 8.0 #データがとりうる上限値
data_lower_bound = 4.0 #データがとりうる下限値
hist_range = 0.01 #ヒストグラムの横軸の幅(階級)

hist_bins = int(abs(data_upper_bound - data_lower_bound)/hist_range) #ヒストグラムのバーの本数


#データの受け渡し(辞書形式で引数に渡すこと)
label = "1列目" #列の名前はlabelに渡す
data = {f'{label}': np.random.normal((data_upper_bound+data_lower_bound)/2,2, np.random.randint(20,10000))} #ダミーデータ

df = pd.DataFrame(data)

#データ解析
count = df[label].count() #データの個数
mean = df[label].mean() #平均
std = df[label].std() #標準偏差
var = std * std #分散
x_min, x_max = df[label].min(), df[label].max() #データの最小値、最大値

x_axis = np.linspace(x_min, x_max, 100)
gaussian_y = norm.pdf(x_axis, loc=mean, scale=std) #正規分布による近似

def color_for_danger(val):
    color = 'red' if not mean-3*std <= val <= mean+3*std else 'black'
    return 'color: %s' % color # 返り値はCSS文字列


#基準値(μ±3σ)を逸脱するデータの個数をカウント
count_danger = 0
for i in range(count):
    if df[label][i] >= mean + 3*std or df[label][i] <= mean - 3*std:
        count_danger += 1


#以下、画面出力
col_data, col_graph = st.columns((1,1))

#データカラム
with col_data:
    with st.container():
        st.subheader("データ")
        # 表示
        st.dataframe(df.style.applymap(color_for_danger), df_width, df_height)

#グラフカラム
with col_graph:
    with st.container():
        st.subheader("グラフ")
        # グラフ設定（matplotlib）
        fig, ax = plt.subplots()

        # ヒストグラム
        ax.hist(df,  # データ
                bins=hist_bins,   # BIN数
                density = True  #確率密度で表す
                ) 
        
        #正規分布
        ax.plot(x_axis, gaussian_y)

        #補助線一覧
        #平均の縦線
        ax.axvline(x=mean ,color='lightgray',linestyle='--')
        #平均からσの縦線
        ax.axvline(x=mean+std ,color='cyan',linestyle='--')
        ax.axvline(x=mean-std,color='cyan',linestyle='--')
        #平均から2σの縦線
        ax.axvline(x=mean+2*std ,color='green',linestyle='--')
        ax.axvline(x=mean-2*std,color='green',linestyle='--')
        #平均から3σの縦線
        ax.axvline(x=mean+3*std ,color='red',linestyle='--')
        ax.axvline(x=mean-3*std,color='red',linestyle='--')

        # ヒストグラム可視化
        st.pyplot(fig, use_container_width=True)

        st.write(f'総データ数: {count}')
        st.write(f"平均値: {round(mean,5)}")
        st.write(f"標準偏差: {round(std,5)}")
        st.write(f'レッドラインを超えている個数: {count_danger}個')
        prob_danger = round((count_danger/count)*100,5)
        st.write(f'レッドラインを超えている確率: {prob_danger}%')