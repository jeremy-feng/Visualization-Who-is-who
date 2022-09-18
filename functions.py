# 导入数据处理的包
import pandas as pd
import numpy as np
# 导入查看系统文件的包
import os
# 导入画图的包
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
# 设置全局字体
plt.rc('font',family=['KaiTi', 'Arial'])
#从pylab导入子模块mpl
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']#设置中文字体。
mpl.rcParams['axes.unicode_minus']=False#避免出现显示为方块的问题。
# 导入绘制词云图的包
from imageio import imread
from wordcloud import WordCloud, ImageColorGenerator


# =====是否经历过隔离或做过志愿者=====
def isolation_volunteer(blocked, type):
    fig=plt.figure(figsize=(8,6),dpi=100)
    ax=plt.axes()
    for line in ['right','top']:
        ax.spines[line].set_visible(False)
    # 去除横坐标的刻度线
    ax.tick_params(bottom=False)
    # 绘制柱状图
    plt.bar([0, 0.5], blocked.loc[type], color='#084082', width=0.3, edgecolor='white')
    # 在柱子上方显示纵坐标
    plt.text(0, blocked.loc[type]['本科在上海']+0.02,'%1.0f'%(100*blocked.loc[type]['本科在上海']) + '%', ha='center',va='bottom', fontsize=16)
    plt.text(0.5, blocked.loc[type]['本科不在上海']+0.02,'%1.0f'%(100*blocked.loc[type]['本科不在上海']) + '%', ha='center',va='bottom', fontsize=16)
    # 添加横刻度
    plt.xticks([0, 0.5], ['本科在上海', '本科不在上海'], fontsize=16)
    # 添加纵刻度
    plt.yticks(np.arange(0, 1.1, 0.5), fontsize=16)
    # 显示百分比
    def to_percent(temp, position):
        return '%1.0f'%(100*temp) + '%'
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
    # 保存为本地文件
    fig.savefig('output/{}.png'.format(type),format='png', facecolor='white', bbox_inches='tight')

# =====星座柱状图=====
def draw_constellations(df):
    # 统计各星座的频率
    constellations = df['星座'].value_counts().reset_index()
    # 修改列名
    constellations.rename(columns={'星座': '人数'}, inplace=True)
    # 将星座名映射为带有日期的星座名，并为每一个星座按时间指定顺序。同时，为每一个星座指定颜色
    constellations_order = {
        '水瓶座': ['水瓶座\n(1.20-2.18)',1,'#1e3482'],
        '双鱼座': ['双鱼座\n(2.19-3.2)',2,'pink'],
        '白羊座': ['白羊座\n(3.21-4.19)',3,'#F08080'],
        '金牛座': ['金牛座\n(4.20-5.20)',4,'yellow'],
        '双子座': ['双子座\n(5.21-6.20)',5,'#6ac8cf'],
        '巨蟹座': ['巨蟹座\n(6.21-7.21)',6,'#dddbde'],
        '狮子座': ['狮子座\n(7.22-8.22)',7,'gold'],
        '处女座': ['处女座\n(8.23-9.22)',8,'#b7e1fb'],
        '天秤座': ['天秤座\n(9.23-10.22)',9,'#e5e2f4'],
        '天蝎座': ['天蝎座\n(10.23-11.21)',10,'#6766bc'],
        '射手座': ['射手座\n(11.22-12.21)',11,'#f67524'],
        '摩羯座': ['摩羯座\n(12.22-1.19)',12,'#5c5c5c'],
    }
    constellations['星座'] = constellations['index'].apply(lambda constellations: constellations_order[constellations][0])
    constellations['顺序'] = constellations['index'].apply(lambda constellations: constellations_order[constellations][1])
    # 升序排列所有星座，即1月的星座在最上方
    constellations.sort_values(by=['顺序'], inplace=True)
    # 挑选出需要的列
    constellations = constellations[['星座', '人数']]
    #设置画布的尺寸
    fig=plt.figure(figsize=(18,9), dpi=300)
    ax=plt.axes()
    # 隐藏上侧和右侧的框线
    for line in ['right','top']:
        ax.spines[line].set_visible(False)
    # 去除横坐标的刻度线
    ax.tick_params(bottom=False)
    # 绘制柱状图
    plt.bar(x = constellations['星座'], height = constellations['人数'], color=[value[2] for value in list(constellations_order.values())])
    # 添加平均线
    plt.axhline(constellations['人数'].mean(), color='gray', ls='--', label='平均人数')
    #设置y轴坐标标签
    plt.ylabel('人数', fontsize=16)
    # 添加横刻度
    plt.xticks(constellations['星座'], fontsize=13)
    # 添加纵刻度
    plt.yticks(np.arange(0, 19, 2), fontsize=16)
    plt.legend(loc='upper left', fontsize=16)
    # 保存为本地文件
    fig.savefig('output/星座.png',format='png', facecolor='white', bbox_inches='tight')


# =====本科毕业院校柱状图=====
def draw_undergraduate_university(df):
    # 提取出各年份的本科毕业院校
    undergraduate_university = df.groupby('入学年份')['本科毕业院校'].value_counts().to_frame()
    # 修改列名
    undergraduate_university.columns = ['人数']
    # 重设索引，避免处理多重索引
    undergraduate_university.reset_index(inplace=True)
    # 将长型数据转换为宽型数据
    undergraduate_university = undergraduate_university.pivot(index='本科毕业院校', columns='入学年份', values='人数')
    # 将空值填充为0
    undergraduate_university.fillna(0, inplace=True)
    # 将数据降序排列
    undergraduate_university.sort_values(by=['2022', '2021', '2020'], ascending=False, na_position='last', inplace=True)
    # 创建年份与颜色的字典
    color_year = {'2020': '#FFA500',
                  '2021': '#00BFFF',
                  '2022': '#9370DB',}
    # 创建画布
    fig=plt.figure(figsize=(18,9), dpi=300)
    ax=plt.axes()
    # 隐藏上侧和右侧的框线
    for line in ['right','top']:
        ax.spines[line].set_visible(False)
    # 去除横坐标的刻度线
    ax.tick_params(bottom=False)
    # 设定每一个柱子的宽度
    bar_width=0.2
    # 画图
    for year in undergraduate_university.columns:
        # 指定各年的所有柱子的横坐标。乘以0.8是因为一个柱子群一共只有3个柱子，0.8就代表4个柱子，剩下一个柱子的距离用来分割每个柱子群。
        globals()['x_'+year] = np.arange(undergraduate_university.shape[0])*0.8 + (int(year)-2020)*bar_width
        # 获取各年的所有柱子的纵坐标
        globals()['data_'+year] = undergraduate_university[year]
        plt.bar(globals()['x_'+year], globals()['data_'+year], width=bar_width, color=color_year[year],
                 edgecolor='None', label=year)
        # 在柱子上方显示纵坐标
        for x,y in zip(globals()['x_'+year], globals()['data_'+year]):
            plt.text(x,y+0.05,'%.0f' %y, ha='center',va='bottom')
    #设置y轴坐标标签
    plt.ylabel('人数',fontsize=16)
    # 添加纵刻度
    plt.yticks(np.arange(0, 11, 2), fontsize=16)
    # 添加横刻度
    plt.xticks(globals()['x_'+undergraduate_university.columns[int(undergraduate_university.shape[1]/2)]], undergraduate_university.index, rotation=90, fontsize=16)
    # 添加图例
    plt.legend(fontsize=16)
    # 保存为本地文件
    fig.savefig('output/本科毕业院校.png',format='png', facecolor='white', bbox_inches='tight')


# =====绘制词云图=====
def draw_word_cloud(text_path, output_path, outline_image_path = imread(r'.\data\黑圆点.png')):
    # 字体路径
    font_path = r'C:\Windows\Fonts\simkai.ttf'
    # 读取文本
    text = open(text_path, encoding='UTF-8').read()
    # 配置词云图
    wc = WordCloud(font_path=font_path, background_color="white", max_words=2000, mask=outline_image_path,
                   max_font_size=100, random_state=42, width=1000, height=860, margin=2)
    # 生成词云图
    wc.generate(text)
    plt.figure(dpi=300)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    # 保存为本地文件
    wc.to_file(output_path)




