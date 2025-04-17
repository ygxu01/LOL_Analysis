#!/usr/bin/env python
# coding: utf-8

# # **Python数据可视化速成教程——以S14世界赛辅助数据为例**
# 
# 看到好多姐妹在为毕业论文画图表而感到烦恼。 
# 
# 其实，用 Python画图并没有那么难。个人认为这是一项可以“边学边用”的技能 —— 如果你打算系统性学习，那当然最好，这样在长期项目中能少走弯路、提高效率；但如果只是为了在毕业论文里产出几张图，或者在 PPT 中放几张加分图，那快速上手、直接改代码模板也完全够用！
# 
# 所以从实用角度来说，了解 Python 能帮我们做什么、能读懂部分代码，达到“能让 AI 帮忙、不被 AI 忽悠”的程度，其实就很棒了。
# 
# 还有就是假如没有用过python还着急出结果的话，建议还是直接用excel或者其他的方法。第一次用python作图除了写码，可能还会碰到很多其他安装上的问题，当然在第一次用完之后，这些问题只要不换电脑基本都不会再出现了~所以推荐找一个比较空的时间段来尝试第一次画图~  
# 
# 
# *注：我不是计算机专业的，代码也好多都是自学并不是写得很好，更加偏向于写最直接的代码而不是最有效率的代码，但好处对于画图来说就是我们只需要在意结果而不是过程~ 这个文档里的代码有很多不是最优解，但是是我认为最直观易懂的写法~所以假如真的想学习python和可视化的化，可以去看更专业的教程书籍，这里只是一些快速出图教程罢了。*
# 
# **完全没有挑事偏袒和分析，就纯数据，由于变量有限有一些图只有教学说明没有什么实际意义~**
# 
# ## **目录**
# ==[目录]==
# 
# 
# ```{note}
# **使用说明**
# 1. 在目录中寻找要画那种类型的图 
# 2. 找到相应的代码
# 3. 改相关参数/直接把代码扔进AI叫ta根据你的数据集画出和这个代码产出相似的图  
# 4. 去掉/加上部件（图例、标题等）
# ```
# 
# ## **一些初始设置**
# 更加推荐去网上找教程，因为我也就安装过一次用到了现在😀   
# 我一般写码用的是**Visual Studio Code**（注意不是Visual Studio），所以参照我的习惯，先要安装两样东西： 
# 
# 1. **Python 本体**（建议从官网 https://www.python.org/ 下载）
# 2. **Visual Studio Code**（注意，不是 Visual Studio！）
# 
# 在 VS Code 中，还需要安装一个插件：**Jupyter Notebook**。  
# Jupyter 是一种类似 Word/Excel 的“文档格式”——扩展名是 `.ipynb`。它的好处是可以将代码分成一格一格，每一格都可以单独运行，非常适合我们一边写一边测试。
# 
# 一般教授也会推荐下载 Jupyter 自带的编辑器，使用界面类似网页，也很好上手。
# 
# Jupyter Notebook 里有两种“格子”：
# - **Markdown**：写文字说明用
# - **Code**：写代码用
# 
# 写好代码后，只需要点击“播放键”就能看到结果啦~
# 
# 
# ## **熟悉自己的数据**
# 在真的开始可视化之前，需要先做一些整理工作，正好可以学习一些基础的Python代码。
# 
# 处理数据最常用的工具是 **pandas** —— 可以理解为Python的“数据处理工具箱”。    
# 在 Python 中，不同的功能通常由不同的工具箱（也叫 package）来提供，而 pandas 里有很多专门用来处理数据的小工具（我们叫做函数 function）。   
# 
# 需要在vscode的terminal里输入 `pip install pandas`来安装。
# 
# 
# 
# 用最基础的代码大概有几步可以做：
# 1. 读取数据
# 2. 选择数据：选择自己想要的部分（可以去除一些不需要的变量和筛选掉某些数据）
# 3. 清洗数据：处理缺失值、统一格式（但有时候缺失值（NaN）本身也有意义，删的时候要小心~）
# 
# 这个说明我用的数据是S14四位进入世界赛的辅助的全年除德杯数据。每一行代表一个小局。

# ### 读取数据
# import是指导入`pandas`这个数据处理工具包，并把它简称为 pd
# 这样每次用这个工具包的时候，只需要写pd就可以了~

# In[ ]:


import pandas as pd


# 我们现在要读取一个数据文件。为了代码简便，这个文件建议事先用 Excel 整理过，并保存成 CSV 格式（UTF-8 编码，逗号分隔）。
# 
# 可以提前把不需要的表头或说明行删掉，只保留数据本体和第一行变量名称。
# 
# 为了让路径更简单，把 CSV 文件和这个 .ipynb 文件放在同一个文件夹里。
# 
# 
# 等号左边是给这个表格起的名字（df 是 “dataframe” 的缩写，意思是“数据表格”），什么名字都可以。

# In[ ]:


df = pd.read_csv("sup_df.csv")


# 可以用 .head() 函数预览  .head(3) 表示只显示前 3 行

# In[ ]:


df.head(3)


# 去掉不想要的变量

# In[ ]:


df = df.drop(columns=["Unnamed: 0"])


# 含有数字的列的基本统计信息

# In[ ]:


df.describe()


# 用value_counts来统计每种数据出现过多少次——这里就代表着每位选手有多少小局比赛。

# In[ ]:


df["player"].value_counts().reset_index()


# 也可以放在后面的括号里。函数可以想现在这样叠加，但是顺序需要注意~

# In[ ]:


df.value_counts(["player","Tournament"]).reset_index().head(5)


# 找到Tournament这一列里面有哪些独特的数据。Tournament是赛事名称变量，所以这里独特的值代表着这些选手参加过的赛事名单。

# In[ ]:


df["Tournament"].unique()


# 除了变量本身以外，我们也可以考虑**去掉某些“不合适”的数据行**。
# 
# 比如在这个辅助数据表中，`Tournament` 这一列记录了比赛名称，我们发现其中包含 “Esports World Cup 2024”（石油杯）这样的赛事。  
# 这个比赛可能在评估 LPL 辅助选手时不太合适，所以我们可能会选择将它从分析中剔除。
# 
# 这里我不会真正删除这部分数据，只是做一个演示。
# 
# 
# >[!TIP]Python逻辑判断符号
# 
# | 符号 | 含义             | 示例                          |
# |------|------------------|-------------------------------|
# | `==` | 等于             | `df["player"] == "Meiko"`     |
# | `!=` | 不等于           | `df["Tournament"] != "Esports World Cup 2024"` |
# | `&`  | “且”（并且）     | `(A条件) & (B条件)`           |
# | `\|`  | “或”             | `(A条件) \| (B条件)`           |
# 
# **注意**：多个条件组合时，外层需要用小括号括起来~
# 

# In[ ]:


# 去掉石油杯的记录
df_filtered = df[df["Tournament"] != "Esports World Cup 2024"]


# In[ ]:


# 验证一下
df_filtered["Tournament"].value_counts()


# 也可以查看选择你想要的信息，也可以通过比如`table=`保存下来,也可以不写直接看
# 比如我想要看ON在石油杯的记录，那这个记录就需要满足两个条件——(player是ON)**并且**(Tournament是Esports World Cup)

# In[ ]:


on_shiyou_df = df[(df["player"] == "ON") & (df["Tournament"] == "Esports World Cup 2024")]
on_shiyou_df


# In[ ]:


# 最后可以粗暴地dropna，去掉没有记录的信息，这样在制表过程中会方便很多
df = df.dropna()


# ## 可视化
# 可以可视化哪些内容呢？我一般会在写代码之前先规划好我的图表会是什么样子的。然后在官网上找相应的代码做出修改。
# 有条件的姐妹可以直接找可视化的python package说明来找灵感。比如说plotly
# ![image.png](attachment:image.png)
# seaborn
# ![image-2.png](attachment:image-2.png)
# 
# 
# 
# 我个人一般使用的是 **Seaborn**。
# 
# 在教学中最常见的绘图工具其实是 **matplotlib**，但它的问题是太繁琐了：图中的每一个元素（比如坐标轴、图例、颜色等）都需要手动设置。
# 
# 相对来说，**Seaborn**在matplotlib基础上，用相同的逻辑只需要输入少量变量就能自动生成图。但是Seaborn不支持中文标签（需要手动输入）……所以这里我们选用 **Plotly**。虽然豆瓣可以贴出的图暂时用不上，但是Plotly的图表是自动“交互式”的，可以在图上移动鼠标查看具体数据值，有些时候图画出来真的显得很酷炫很专业~
# 
# 写这份指南的原因之一也是感觉这些网站对于在国内的姐妹来说比较难搜到，然后真的写起来一个一个翻，没有经验的话，确实很费时间和精力。

# ### 散点图（scatter plot）
# 相对来说图其实比画表要简单一点，所以我们从图开始。首先，先安装`pip install plotly`。
# 
# #### 图1：小局KDA和时长的散点图
# 我们可以画一个每小局KDA和小局时长的散点图~先计算出每一小局KDA。

# In[ ]:


# D值可能为0
df["D_safe"] = df["D"].replace(0, 1)

# 直接做除法计算 KDA
df["KDA"] = (df["K"] + df["A"]) / df["D_safe"]

# lambda有可能比较复杂，但是一次成型
# df["KDA"] = df.apply(lambda row: (row["K"] + row["A"]) / (row["D"] if row["D"] != 0 else 1), axis=1)

#随便看看：预览一些死亡数比较高的小局~(D倒序，KDA正序)
df.sort_values(by = ["D","KDA"], ascending = [False,True]).head(5)


#   
# 用 Plotly Express 画散点图很方便，而且有很多可选项可以自由组合。  
#  
# | 参数名         | 用法                          |
# |----------------|-------------------------------|
# | `x`, `y`       | 横轴、纵轴变量                |
# | `color`        | 用不同颜色区分类别            |
# | `size`         | 点的大小反映另一个变量        |
# | `symbol`       | 用不同图形（圆/方/星等）区分类别 |
# | `opacity`      | 设置透明度（0~1）             |
# | `trendline`    | 加拟合线，可选 `"ols"`, `"lowess"` |
# | `marginal_x/y` | 添加边缘图（箱型图 box, 直方图 hist） |
# | `hover_data`   | 鼠标悬浮时显示的字段           |
# | `template`     | 图的风格（如 `"seaborn"`, `"plotly_white"`） |

# In[ ]:


import plotly.express as px

fig = px.scatter(
    df,
    x="duration_minutes",        # 横轴：比赛时长
    y="KDA",                     # 纵轴：KDA 值
    color="player",              # 用不同颜色区分选手
    opacity=0.7,                 # 散点透明度
    trendline="ols",             # 拟合线：普通最小二乘（OLS）
    template="seaborn",          # 美化风格
    marginal_y="box",            # 右侧加上 KDA 的箱型图
    marginal_x="box"             # 上方加上时长的箱型图
)

# 设置图表标题与轴标签
fig.update_layout(
    title="图1.选手比赛时长 vs KDA 表现",
    xaxis_title="比赛时长（分钟）",
    yaxis_title="KDA",
)

fig.show()


# 用相同的模板和数据，你可以试试各种各种的搭配

# In[ ]:


import plotly.express as px

fig = px.scatter(
    df,
    x="duration_minutes",        # 横轴：比赛时长
    y="KDA",                     # 纵轴：KDA 值
    color="player",              # 用颜色区分不同选手
    
    # size = (df["K"] + df["A"]),  # 点大小可以表示输出/参团强度等
    
    symbol = "Result",           # 用符号表示比赛结果（Victory / Defeat）
    opacity=0.7,                 # 散点透明度，防止遮挡
    
    # trendline="ols",            # 加上线性趋势线（也可以是 "lowess"）
    
    template="seaborn",          # 使用 seaborn 风格
    
    # marginal_y="box",           # 右边加 KDA 的箱型图
    # marginal_x="box"            # 上方加时长的箱型图
)

fig.update_layout(
    title="选手比赛时长 vs KDA 表现",
    xaxis_title="比赛时长（分钟）",
    yaxis_title="KDA",
)

fig.show()


# ### 箱装图（boxplot）  
# 还有比如我想要看每位选手每个赛段的KDA分布情况。
# #### 图2：每个赛段KDA的箱型图

# In[ ]:


import plotly.express as px

fig = px.box(
    df,
    x="Tournament",           # 横轴为比赛名称
    y="KDA",                  # 纵轴为 KDA 值
    color="player",           # 按选手上色
    template="seaborn"
)

# 添加图表标题和坐标轴名称
fig.update_layout(
    title="不同赛事中各辅助选手的KDA分布",
    xaxis_title="赛事名称",
    yaxis_title="KDA",
    title_font_size=18,
    legend_title_text="选手",
    margin=dict(l=40, r=40, t=60, b=40)
)

fig.show()


# 但是还有可以提升的地方，比如，比赛顺序按照实际时间排列，而不是默认的字母排序，还有要注意选手颜色在各图中保持一致（基本不要不重新sort表格，默认是一致的），方便横向对比。

# In[ ]:


import plotly.express as px

# 先按照时间排序比赛名称
tournament_order = df.sort_values("Date")["Tournament"].drop_duplicates().tolist()

# 设定选手顺序（确保颜色一致）
player_order = sorted(df["player"].unique())

fig = px.box(
    df,
    x="Tournament",           # 横轴为比赛名称
    y="KDA",                  # 纵轴为 KDA 值
    color="player",           # 按选手上色
    template="seaborn",
    category_orders={
        "Tournament": tournament_order,
        "player": player_order
    },
)


# 添加图表标题和坐标轴名称
fig.update_layout(
    title="图2.不同赛事中各辅助选手的KDA分布",
    xaxis_title="赛事名称",
    yaxis_title="KDA",
    title_font_size=18,
    legend_title_text="选手",
    margin=dict(l=40, r=40, t=60, b=40)
)

fig.show()


# #### 图3：每个赛段KDA的箱型图，分选手
# 还可以每位选手单独分图显示~这种比较类型的，我其实更加倾向于图2，图3的形式可能更加适合不同类型的变量~

# In[ ]:


# 先按照时间排序比赛名称
tournament_order = df.sort_values("Date")["Tournament"].drop_duplicates().tolist()

# 设定选手顺序（确保颜色一致）
player_order = sorted(df["player"].unique())

fig = px.box(
    df,
    x="Tournament",
    y="KDA",
    color="player",
    facet_col="player",
    category_orders={
        "Tournament": tournament_order,
        "player": player_order
    },
    template="seaborn",
    points="outliers"  # 也可设为 "all" 显示全部点
)

fig.update_layout(
    title="图3.不同赛事中各辅助选手的 KDA 分布",
    xaxis_title="赛事",
    yaxis_title="KDA",
    showlegend=False,  # 隐藏图例
    margin=dict(t=60, l=40, r=40, b=40)
)

fig.show()


# ### 分布曲线图（distribution plot）
# #### 图4. 各选手KDA分布曲线图

# In[ ]:


# 提取选手名
players = df["player"].unique()

# 为每位选手构建一个 KDA 列表（去除缺失值）
kda_groups = [df[df["player"] == player]["KDA"].dropna().tolist()
              for player in players]

print(kda_groups)


# `kda_groups = [
#     df[df["player"] == player]["KDA"].dropna().tolist()
#     for player in players
# ]`
# 这行代码看起来复杂，其实可以理解为，我们要为每个选手，提取出他所有比赛中的 KDA 数值，存成一个列表。所有选手的列表再组成一个大列表。
# 
# 1. `for player in players`
# 遍历所有选手
# 
# players 是一个列表，比如：["Meiko", "Crisp", "Hang", "ON"]
# 
# 2. `df[df["player"] == player]`
# 这是“过滤数据”的方式
# 
# 只保留这个选手打的所有比赛
# 
# 举个例子：df[df["player"] == "Meiko"] 只留下 Meiko 的比赛记录
# 
# 3. `["KDA"]`
# 从刚才留下的比赛记录中，只取出 KDA 那一列
# 
# 4. `.dropna()`
# 去掉空值（有些比赛可能没有 KDA 数据）
# 
# 5. `.tolist()`
# 把这一列转成 Python 里的普通列表

# In[ ]:


import plotly.figure_factory as ff
# 创建分布图（平滑曲线）
fig = ff.create_distplot(
    kda_groups,
    group_labels=players,
    show_hist=False,     # 不显示直方图，只保留平滑线
    show_rug=False       # 不显示底部小tick线
)

# 美化图表 & 去除图例
fig.update_layout(
    template="seaborn",
    title="图4.KDA 分布曲线图（各辅助选手）",
    xaxis_title="KDA",
    yaxis_title="密度",
    showlegend=True
)

fig.show()


# ### 表格
# 
# 这里我们用的package叫great_tables，所以我们需要`pip install great_tables`和`pip install polars`来安装。  
# 
# #### 表1： ON石油杯小局数据
# 可以先做一个最简单的表格，就拿刚刚ON石油杯的表现（我看BLG比赛比较多🕶）：

# In[ ]:


from great_tables import GT, loc, style


# In[ ]:


on_shiyou_df


# 比如，这里我做表格的话我会觉得可能信息有些过多了，可以减少一些，因为我们已经明确知道这张表格只有ON在石油杯的表现了。

# In[ ]:


# 选取我需要的变量
on_shiyou_df = on_shiyou_df[["Champion","Result","duration_minutes","K","D","A"]]
# 时长这一栏小数点后有点多
on_shiyou_df["duration_minutes"] = on_shiyou_df["duration_minutes"].round(2)
# 重新命名一下
on_shiyou_df = on_shiyou_df.rename(columns = {"Champion": "英雄","Result":"赛果","duration_minutes":"时长","K":"击杀","D":"死亡","A":"助攻"})


# In[ ]:


on_shiyou_df


# In[ ]:


# 生成图片
GT(on_shiyou_df)


# In[ ]:


table = GT(on_shiyou_df)

(
    table

    # Table header ----
    .tab_header(
        title = "表1. ON选手石油杯比赛小局数据",
        subtitle = "2024-7-4，BLG vs T1"
    )
)


# ### 表格进阶——pivot和groupby
# *其实表格很多时候要比单纯画图要复杂，因为表格你需要把每一行每一列都想得很清楚，并且用码来表现出来。而且excel的透视（？）功能也可以达到一样的效果~所以假如不想可视化表的话可以直接跳到后面画图的部分。*    
# 
# #### 表2： 不同赛制的场数胜率比较, 按赛制  
# 有些时候，我们想要更复杂一些的数据统计，比如每位选手在每个大局和小局的数据。这种时候我们就需要先提前想好自己需要什么数据然后再整合出来。
# 比如，我最后的图是要这样的：
# ![image.png](attachment:image.png)
# 
# 从数据上看，我需要每一种比赛形式的大局小局数和胜率。  
# 
# 大局数和小局数是不一样的算法——小局数只要数每位选手一共有多少行，其中多少是胜利就行了，但是大局数，我们得先整理出每位选手的每个大局才行。
# 
# 这个时候就可以用到`groupby`。即先把表格里的数据按某个条件分好组，再对每组做统计。
# 

# In[ ]:


df_game = df.groupby(["player", "match_type"]).apply(
    lambda group: pd.Series({
        "小局数": group["Result"].count(),
        "小局胜率": (group["Result"] == "Victory").mean().round(2)
    })
).reset_index()
df_game.head(3)


# 这里，  
# `groupby(["player", "match_type"])`：意思是“把数据按选手和赛制分组”
# 
# `apply(...)`：对每组分别执行一个自定义的函数
# 
# `group["Result"] == "Victory"`：判断哪些是胜利（得到 True/False 的列表）
# 
# `.mean()`：True=1, False=0，所以平均值就是胜率

# In[ ]:


# 假设同一天两个队之间只会有一个大局
match_result = df[["player","Game","Date","match_result","match_type"]]
df_match = match_result.groupby(["player", "match_type"]).apply(
    lambda group: pd.Series({
        "大局数": group["match_result"].count(),
        "大局胜率": (group["match_result"] == "Victory").mean()
    })
).reset_index()
df_match.head(3)


# [!TIP]合并表格
# [merge cheat sheet]

# In[ ]:


#合并表格
df_winrate_summary = pd.merge(df_game, df_match, on=["player", "match_type"])

# 四舍五入
df_winrate_summary[["大局数", "小局数"]] = df_winrate_summary[["大局数", "小局数"]].round(0)
df_winrate_summary[["大局胜率", "小局胜率"]] = df_winrate_summary[["大局胜率", "小局胜率"]].round(2)

df_winrate_summary.head()


# 在这里我们还需要用到pivot来让match_type来作为列名。

# In[ ]:


pivot_df = df_winrate_summary.pivot(index="player", columns="match_type")
pivot_df


# 这里其实已经可以算完成了，但是假如想把图做得更漂亮一些的话，可以尝试用great_tables。  
# great_tables这个package的特点就是他不能读取有多层列名的表格，比如现在pivot_df，他每一列的名称都是（第一行，第二行）的形式。

# In[ ]:


pivot_df.columns


# In[ ]:


pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]  # 把多层列名拍扁
pivot_df = pivot_df.reset_index()
pivot_df.head()


# 再用great_tables美化

# In[ ]:


import polars as pl
import polars.selectors as cs
from great_tables import GT, loc, style

# 提取列名：按赛制分组
bo1 = [col for col in pivot_df.columns if col.endswith("_BO1")]
bo3 = [col for col in pivot_df.columns if col.endswith("_BO3")]
bo5 = [col for col in pivot_df.columns if col.endswith("_BO5")]

# 创建表格对象并格式化展示
great_table = (
    GT(pivot_df)
    .tab_header("不同赛制的场数胜率比较（按赛制分组）")
    
    .tab_spanner(label="BO1", columns=bo1)
    .tab_spanner(label="BO3", columns=bo3)
    .tab_spanner(label="BO5", columns=bo5)

    .cols_label(
        player = "选手",
        大局数_BO1 = "大局数", 小局数_BO1 = "小局数", 大局胜率_BO1 = "大局胜率", 小局胜率_BO1 = "小局胜率",
        大局数_BO3 = "大局数", 小局数_BO3 = "小局数", 大局胜率_BO3 = "大局胜率", 小局胜率_BO3 = "小局胜率",
        大局数_BO5 = "大局数", 小局数_BO5 = "小局数", 大局胜率_BO5 = "大局胜率", 小局胜率_BO5 = "小局胜率"
    )

    .fmt_number(columns=[col for col in pivot_df.columns if "数" in col], compact=True, decimals=0)
    .fmt_percent(columns=[col for col in pivot_df.columns if "率" in col], decimals=0)

    .tab_style(style=style.fill(color="floralwhite"), locations=loc.body(columns=bo1))
    .tab_style(style=style.fill(color="aliceblue"), locations=loc.body(columns=bo3))
    .tab_style(style=style.fill(color="lavenderblush"), locations=loc.body(columns=bo5))

    # （可选）手动高亮表现突出的选手某列
    .tab_style(style=style.fill(color="moccasin"), locations=[
        loc.body(columns="大局胜率_BO1", rows=[1]),
        loc.body(columns="小局胜率_BO1", rows=[1])
    ])
)
great_table


# ### 饼状图 + 一些拼接~
# 
# 这里想要把前面的几个知识连起来做一个英雄池的饼状图。
# 
# 首先我想要收集一些英雄池的信息来给我画图~这里又可以用上`groupby`（其实假如搞不懂groupby的话，可以直接筛选相应的数据，每个选手做一张表塞进模板里也是可以的~）    
# 这里只是因为想要试验不同的图做出来的效果，所以计算了很多变量~

# In[ ]:


champion_df = df.groupby(["player","Champion"]).apply(
    lambda group: pd.Series({
        "总局数": group["Result"].count(),
        "平均时长": group["duration_minutes"].mean().round(2),
        "平均KDA": round((group["K"].sum() + group["A"].sum()) / (group["D"].sum() if group["D"].sum() != 0 else 1), 2),
        "胜率" : (group["Result"] == "Victory").mean().round(2),
        "胜局": (group["Result"] == "Victory").sum(),
        "平均死亡数" : group["D"].mean().round(2),
        "平均K+A": (group["K"].mean() + group["A"].mean()).round(2),
        "总死亡数" : group["D"].sum(),
        "总K+A": (group["K"].sum() + group["A"].sum())
    })
).reset_index()
champion_df.head(3)


# #### 一些探索：
# 英雄池大小

# In[ ]:


df.groupby("player")['Champion'].nunique().reset_index()


# 平均时长最短的英雄

# In[ ]:


champion_df[champion_df["总局数"] > 3].sort_values("平均时长",ascending=True).head(5)


# ##### 图5. 选手英雄池饼状图  

# In[ ]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 从 groupby 得到的 champion_df 中分别筛选每位选手的数据
meiko_df = champion_df[champion_df["player"] == "meiko"]
crisp_df = champion_df[champion_df["player"] == "Crisp"]
hang_df = champion_df[champion_df["player"] == "Hang"]
on_df = champion_df[champion_df["player"] == "ON"]

# 创建子图 2x2（四张饼图）
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}],
           [{'type': 'domain'}, {'type': 'domain'}]],
    subplot_titles=['Crisp', 'Hang', 'ON', 'Meiko']
)

# 分别添加每位选手的饼图
fig.add_trace(go.Pie(
    labels=crisp_df["Champion"],
    values=crisp_df["总局数"],
    name="Crisp",
    textinfo='percent+label'
), row=1, col=1)

fig.add_trace(go.Pie(
    labels=hang_df["Champion"],
    values=hang_df["总局数"],
    name="Hang",
    textinfo='percent+label'
), row=1, col=2)

fig.add_trace(go.Pie(
    labels=on_df["Champion"],
    values=on_df["总局数"],
    name="ON",
    textinfo='percent+label'
), row=2, col=1)

fig.add_trace(go.Pie(
    labels=meiko_df["Champion"],
    values=meiko_df["总局数"],
    name="meiko",
    textinfo='percent+label'
), row=2, col=2)

fig.update_traces(textposition='inside', textinfo='percent+label')

# 这里可以设置最小的字号
fig.update_layout(uniformtext_minsize=7, uniformtext_mode='hide')
# 图表整体布局
fig.update_layout(
    title_text="图5.各辅助选手的英雄使用频率分布",
    template="seaborn",
    showlegend=True,
    height=700,
    width=700,
    margin=dict(t=60, l=40, r=40, b=40)
)

fig.show()


# 除了设置最小的字号，所以可以把小的饼都转化成“其他”。

# In[ ]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 设置阈值：低于这个值的英雄会被合并为 "Others"
min_threshold = 3

# 创建子图
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}],
           [{'type': 'domain'}, {'type': 'domain'}]],
    subplot_titles=['Crisp', 'Hang', 'ON', 'Meiko']
)

# 工具函数：给一个 dataframe 合并低频英雄为 "其他"
def collapse_small_slices(df, threshold=5):
    df = df.copy()
    small_df = df[df["总局数"] < threshold]
    other_count = small_df["总局数"].sum()
    main_df = df[df["总局数"] >= threshold]
    if other_count > 0:
        main_df = pd.concat([
            main_df,
            pd.DataFrame({"Champion": ["其他"], "总局数": [other_count]})
        ])
    return main_df

# === 分别为每位选手画图 ===
# Crisp
df_crisp = collapse_small_slices(champion_df[champion_df["player"] == "Crisp"], threshold=min_threshold)
fig.add_trace(go.Pie(labels=df_crisp["Champion"], values=df_crisp["总局数"]), row=1, col=1)

# Hang
df_hang = collapse_small_slices(champion_df[champion_df["player"] == "Hang"], threshold=min_threshold)
fig.add_trace(go.Pie(labels=df_hang["Champion"], values=df_hang["总局数"]), row=1, col=2)

# ON
df_on = collapse_small_slices(champion_df[champion_df["player"] == "ON"], threshold=min_threshold)
fig.add_trace(go.Pie(labels=df_on["Champion"], values=df_on["总局数"]), row=2, col=1)

# Meiko
df_meiko = collapse_small_slices(champion_df[champion_df["player"] == "meiko"], threshold=min_threshold)
fig.add_trace(go.Pie(labels=df_meiko["Champion"], values=df_meiko["总局数"]), row=2, col=2)

fig.update_traces(
    textinfo='label+percent',
    hoverinfo='label+value+percent',
    textposition='inside'
)
fig.update_layout(
    title_text="图6.各辅助选手的英雄使用频率分布（其他）",
    template="seaborn",
    showlegend=True,
    height=600,
    width=700,
    margin=dict(t=60, l=40, r=40, b=40)
)

fig.show()


# ### 柱状图
# #### 可调参数说明
# 
# | 可调参数                          | 效果说明                                                   |
# |-----------------------------------|------------------------------------------------------------|
# | `barmode='stack'`                 | 改为堆叠柱图，查看每个英雄胜率总和中各选手的占比          |
# | `facet_col="player"`              | 把每位选手拆成单独的子图，便于纵向观察                    |
# | `hover_data=["平均KDA", "总局数"]` | 鼠标悬停时显示更多信息，比如该英雄的其他表现维度         |
# | `category_orders={"Champion": [...排序列表...]}` | 手动排序英雄顺序，例如按使用次数从多到少排列         |
# | `color_discrete_sequence=[...]`   | 自定义颜色顺序，保持一致性    | 
# #### 图7.柱状图各选手英雄胜率统计

# In[ ]:


import plotly.express as px

fig = px.histogram(
    champion_df,
    x="Champion",          # 英雄名作为横轴
    y="胜率",              # 柱子的高度为胜率
    color="player",         # 用颜色区分选手
    barmode="group",        # 分组显示柱子（默认是堆叠 stacked）
    opacity=0.7,
    height=400
)

fig.update_layout(
    template="seaborn",
    title="各辅助选手在不同英雄上的胜率",
    xaxis_title="英雄",
    yaxis_title="胜率",
    showlegend=True
)

fig.show()


# 但是感觉还是有可以改进的，首先有些英雄只有一两个人玩过，可以去掉，还有0胜率的英雄可以显示一点点长度来表明这个英雄也是被玩过的。

# In[ ]:


champion_counts = champion_df['Champion'].value_counts()

champions_over_3 = champion_counts[champion_counts > 3].index

filtered_df = champion_df[champion_df['Champion'].isin(champions_over_3)]
filtered_df["胜率_p"] = filtered_df["胜率"].apply(lambda x: 0.01 if x == 0 else x)
# 这样sort的话其实实际在画图的时候就不用特别设置order了，他会默认按照表格中出现的顺序来展示
filtered_df = filtered_df.sort_values(by = "总局数",ascending=False).sort_values(by = "player",ascending=True)
filtered_df.head(3)


# In[ ]:


import plotly.express as px

fig = px.histogram(
    filtered_df,
    x="Champion",          # 英雄名作为横轴
    y="胜率_p",              # 柱子的高度为胜率
    color="player",         # 用颜色区分选手
    barmode="group",        # 分组显示柱子（默认是堆叠 stacked）
    opacity=0.7,
    height=400,
    hover_data= ["胜率", "总局数"] 
)

fig.update_layout(
    template="seaborn",
    title="图7.各辅助选手在不同英雄上的胜率",
    xaxis_title="英雄",
    yaxis_title="胜率",
    showlegend=True
)

fig.show()


# In[ ]:


import plotly.express as px

# 按总局数降序排列英雄顺序
hero_order = (
    filtered_df.groupby("Champion")["总局数"]
    .sum()
    .sort_values(ascending=False)
    .index.tolist()
)

# 画图
fig = px.bar(
    filtered_df,
    x="Champion",
    y=filtered_df["平均K+A"] / filtered_df["平均死亡数"],
    color="player",
    facet_col="player",               # 每位选手单独展示
    category_orders={"Champion": hero_order},  # 英雄排序按总局数降序
    hover_data=["胜率", "总局数", "平均K+A"],   # 鼠标悬停显示更多变量
    opacity=0.8,
    template="seaborn",
    height=500
)

fig.update_layout(
    title="图8. 每位选手使用不同英雄时的平均KDA",
    xaxis_title="Champion",
    yaxis_title="平均KDA",
    showlegend=False,
    margin=dict(t=60, l=40, r=40, b=40)
)
# 设置一下每个小图的标题
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

fig.show()

