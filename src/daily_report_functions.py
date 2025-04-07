import pandas as pd
import numpy as np
import polars as pl
import polars.selectors as cs
from great_tables import GT, loc, style

from pull_match_list import load_match_list
from load_player_id import load_player_id_df
from daily_report_functions import *

# from pathlib import Path
# from settings import config

# DATA_DIR = Path(config("DATA_DIR"))
# MANUAL_DATA_DIR = Path(config("MANUAL_DATA_DIR"))


"""
from pull_match_list import load_match_list
from load_player_id import load_player_id_df
from daily_report_functions import *
df = load_match_list()
player_df = load_player_id_df()

blue_team = ...
red_team = ...
blue_team_name = ...
red_team_name = ...

blue, red = get_official_name(blue_team, red_team, player_df)
lst = shared_games_list(blue,red,df)
compete = generate_compete_summary_df(lst)
hero = generate_hero_summary_df(lst)
display_compete_table(compete, f"{blue_team_name} vs {red_team_name}", None,blue_team_name ,"red_team_name")
display_hero_table(compete, f"{blue_team_name} vs {red_team_name}", None,blue_team_name ,"red_team_name")
"""


def get_official_name(blue_team, red_team, player_df):
    """
    ensure that blue and red team values are all lower cases.
    both variables are lists
    """
    player_df["player_lower"] = player_df["player"].str.lower().str.strip()

    name_map = dict(zip(player_df["player_lower"], player_df["player"]))

    blue = [name_map.get(name, name) for name in blue_team]
    red = [name_map.get(name, name) for name in red_team]

    return blue, red


def calc_kda(df,score_column_name,target_column_suffix):
    kda_split = df[score_column_name].str.strip().str.split("/", expand=True)
    df[f"K{target_column_suffix}"] = kda_split[0].astype(int)
    df[f"D{target_column_suffix}"] = kda_split[1].astype(int)
    df[f"A{target_column_suffix}"] = kda_split[2].astype(int)
    return df



def shared_games_list(blue_team, red_team, match_df):
    result = []
    match_df["duration_minutes"] = match_df["Duration"].str.split(":").apply(lambda x: int(x[0]) + int(x[1]) / 60)
    match_df = calc_kda(match_df ,"Score","")


    for blue, red in zip(blue_team, red_team):
        blue_df = match_df[match_df["player"] == blue]
        red_df  = match_df[match_df["player"] == red]
        merged_df = pd.merge(blue_df, red_df, on=["Date", "Game","Duration"],suffixes=('_blue', '_red'))
        

        if merged_df.empty:
            merged_df = pd.DataFrame([{
                "player_blue": blue,
                "player_red": red,
                
                "Champion_blue": "NoHero",  
                "Champion_red": "NoHero",
                
                "Result_blue": "NoGame",  
                "Result_red": "NoGame",
                
                "duration_minutes_blue": 0.0,
                "duration_minutes_red": 0.0,

                "K_blue": 0, "D_blue": 0, "A_blue": 0,
                "K_red": 0, "D_red": 0, "A_red": 0,

                "Date": "NoDate",       # or None / ""
                "Game": "NoGame",       # just consistent placeholders
                "Duration": "00:00"
            }])

        result.append(merged_df)

    return result


def generate_compete_summary_df(lst, top_n_heroes=3):
    summary_list = []

    for df in lst:
        result = df.groupby(["player_blue", "player_red"], group_keys=False).apply(
            lambda group: pd.Series({
                "蓝方胜场": int((group["Result_blue"] == "Victory").sum()),
                "红方胜场": int((group["Result_red"] == "Victory").sum()),

                "蓝方平均K": group["K_blue"].mean(),
                "蓝方平均D": group["D_blue"].mean(),
                "蓝方平均A": group["A_blue"].mean(),

                "红方平均K": group["K_red"].mean(),
                "红方平均D": group["D_red"].mean(),
                "红方平均A": group["A_red"].mean(),

                "蓝方常用英雄": ", ".join(group["Champion_blue"].value_counts().head(top_n_heroes).index),
                "红方常用英雄": ", ".join(group["Champion_red"].value_counts().head(top_n_heroes).index),

                "平均时长(min)": group["duration_minutes_blue"].mean().round(2),
                "总小局数": int(len(group)),
                "总大局数": int(group[["Game", "Date"]].drop_duplicates().shape[0]),
            })
        )
        for col in result.index.names:
    # If col is also a normal column in result, drop it
            if col in result.columns:
                result = result.drop(columns=col)

        result = result.reset_index()

        # 胜率列
        result["蓝方小局胜率"] = result["蓝方胜场"] / result["总小局数"]
        result["红方小局胜率"] = result["红方胜场"] / result["总小局数"]

        # KDA列
        result["蓝方小局KDA"] = result.apply(
            lambda row: f"{row['蓝方平均K']:.2f}/{row['蓝方平均D']:.2f}/{row['蓝方平均A']:.2f}", axis=1
        )
        result["红方小局KDA"] = result.apply(
            lambda row: f"{row['红方平均K']:.2f}/{row['红方平均D']:.2f}/{row['红方平均A']:.2f}", axis=1
        )

        # 胜场(胜率)
        result["蓝方胜场(胜率)"] = result.apply(
            lambda row: f"{row['蓝方胜场']} ({row['蓝方小局胜率']:.2%})", axis=1
        )
        result["红方胜场(胜率)"] = result.apply(
            lambda row: f"{row['红方胜场']} ({row['红方小局胜率']:.2%})", axis=1
        )

        # 重命名选手列
        result = result.rename(columns={
            "player_blue": "蓝方选手",
            "player_red": "红方选手"
        })

        # 删除中间列
        result = result.drop(columns=[
            "蓝方平均K", "蓝方平均D", "蓝方平均A",
            "红方平均K", "红方平均D", "红方平均A",
            "蓝方小局胜率", "红方小局胜率"
        ])

        # 重新排布列顺序（对称结构）
        column_order = [
            "蓝方选手", "蓝方胜场", "蓝方胜场(胜率)", "蓝方小局KDA", "蓝方常用英雄",
            "总小局数", "总大局数", "平均时长(min)",
            "红方常用英雄", "红方小局KDA", "红方胜场(胜率)", "红方胜场", "红方选手"
        ]
        result = result[column_order]

        summary_list.append(result)

    final_df = pd.concat(summary_list, ignore_index=True)
    return final_df


def generate_hero_summary_df(lst):
    hero_summary_list = []

    for df in lst:
        df["player_pair"] = df.apply(lambda row: tuple(sorted([row["player_blue"], row["player_red"]])), axis=1)

        for pair, match_df in df.groupby("player_pair"):

            blue = match_df["player_blue"][0]
            red = match_df["player_red"][0]

            blue_heroes = match_df["Champion_blue"]
            red_heroes = match_df["Champion_red"]

            blue_counts = blue_heroes.value_counts()
            red_counts = red_heroes.value_counts()

            blue_win_rate = match_df.groupby("Champion_blue")["Result_blue"].apply(lambda x: (x == "Victory").mean())
            red_win_rate = match_df.groupby("Champion_red")["Result_red"].apply(lambda x: (x == "Victory").mean())

            blue_most = blue_counts.idxmax()
            red_most = red_counts.idxmax()

            blue_most_str = f"{blue_most} ({blue_counts[blue_most]}/{blue_win_rate[blue_most]*100:.1f}%)"
            red_most_str = f"{red_most} ({red_counts[red_most]}/{red_win_rate[red_most]*100:.1f}%)"

            # 蓝方胜率最高英雄（优先使用场次最多者）
            max_blue_win = blue_win_rate.max()
            blue_best = blue_win_rate[blue_win_rate == max_blue_win].index
            blue_best = blue_best.to_series().map(blue_counts).idxmax()

            # 蓝方胜率最低英雄（优先使用场次最多者）
            min_blue_win = blue_win_rate.min()
            blue_worst = blue_win_rate[blue_win_rate == min_blue_win].index
            blue_worst = blue_worst.to_series().map(blue_counts).idxmax()

            # 红方同理
            max_red_win = red_win_rate.max()
            red_best = red_win_rate[red_win_rate == max_red_win].index
            red_best = red_best.to_series().map(red_counts).idxmax()

            min_red_win = red_win_rate.min()
            red_worst = red_win_rate[red_win_rate == min_red_win].index
            red_worst = red_worst.to_series().map(red_counts).idxmax()

            blue_best_str = f"{blue_best} ({blue_counts[blue_best]}/{blue_win_rate[blue_best]*100:.1f}%)"
            blue_worst_str = f"{blue_worst} ({blue_counts[blue_worst]}/{blue_win_rate[blue_worst]*100:.1f}%)"

            red_best_str = f"{red_best} ({red_counts[red_best]}/{red_win_rate[red_best]*100:.1f}%)"
            red_worst_str = f"{red_worst} ({red_counts[red_worst]}/{red_win_rate[red_worst]*100:.1f}%)"

            all_heroes = pd.concat([blue_heroes, red_heroes])
            total_unique = all_heroes.nunique()
            most_common = all_heroes.value_counts().idxmax()
            most_common_str = f"{most_common} ({all_heroes.value_counts()[most_common]})"

            hero_summary_list.append({
                "蓝方选手": blue,
                "蓝方最常用英雄": blue_most_str,
                "蓝方最高胜率英雄": blue_best_str,
                "蓝方最低胜率英雄": blue_worst_str,
                "蓝方使用英雄数": blue_heroes.nunique(),
                "对局英雄总数": total_unique,
                "对局中最常用英雄": most_common_str,
                "红方使用英雄数": red_heroes.nunique(),
                "红方最常用英雄": red_most_str,
                "红方最高胜率英雄": red_best_str,
                "红方最低胜率英雄": red_worst_str,
                "红方选手": red
            })

    df_summary = pd.DataFrame(hero_summary_list)

    # 重新排列表头，实现左右对称 + 中间公共字段
    column_order = [
        "蓝方选手",
        "蓝方最常用英雄", "蓝方最高胜率英雄", "蓝方最低胜率英雄", "蓝方使用英雄数",
        "对局英雄总数", "对局中最常用英雄",
        "红方使用英雄数", "红方最低胜率英雄","红方最高胜率英雄", "红方最常用英雄", 
        "红方选手"
    ]

    return df_summary[column_order]





def display_compete_table(df, title=None, subtitle=None, team_a_name="队伍A", team_b_name="队伍B"):
    df = df.rename(columns={
        "蓝方选手": "选手A", "红方选手": "选手B",
        "蓝方胜场(胜率)": "胜场(胜率)A", "红方胜场(胜率)": "胜场(胜率)B",
        "蓝方小局KDA": "KDA_A", "红方小局KDA": "KDA_B",
        "蓝方常用英雄": "常用英雄A", "红方常用英雄": "常用英雄B"
    })

    df = df[[
        "选手A", "胜场(胜率)A", "KDA_A", "常用英雄A",
        "总小局数", "总大局数", "平均时长(min)",
        "常用英雄B", "KDA_B", "胜场(胜率)B", "选手B"
    ]]

    gt = GT(df)

    if title or subtitle:
        gt = gt.tab_header(title=title, subtitle=subtitle)

    gt = (
        gt
        .tab_spanner(team_a_name, columns=["选手A", "胜场(胜率)A", "KDA_A", "常用英雄A"])
        .tab_spanner("对局信息", columns=["总小局数", "总大局数", "平均时长(min)"])
        .tab_spanner(team_b_name, columns=["常用英雄B", "KDA_B", "胜场(胜率)B", "选手B"])
        .cols_align("center")
        .cols_label(**{
            "选手A": "选手", "选手B": "选手",
            "胜场(胜率)A": "胜场(胜率)", "胜场(胜率)B": "胜场(胜率)",
            "KDA_A": "KDA", "KDA_B": "KDA",
            "常用英雄A": "常用英雄", "常用英雄B": "常用英雄"
        })
        .tab_style(style=style.fill(color="aliceblue"), locations=loc.body(columns=["选手A", "胜场(胜率)A", "KDA_A", "常用英雄A"]))
        .tab_style(style=style.fill(color="mistyrose"), locations=loc.body(columns=["常用英雄B", "KDA_B", "胜场(胜率)B", "选手B"]))
    )

    return gt


def display_hero_table(df, title=None, subtitle=None, team_a_name="队伍A", team_b_name="队伍B"):
    df = df.rename(columns={
        "蓝方选手": "选手A", "红方选手": "选手B",
        "蓝方最常用英雄": "最常用英雄A", "红方最常用英雄": "最常用英雄B",
        "蓝方最高胜率英雄": "胜率最高英雄A", "红方最高胜率英雄": "胜率最高英雄B",
        "蓝方最低胜率英雄": "胜率最低英雄A", "红方最低胜率英雄": "胜率最低英雄B",
        "蓝方使用英雄数": "使用英雄数A", "红方使用英雄数": "使用英雄数B"
    })

    df = df[[
        "选手A", "最常用英雄A", "胜率最高英雄A", "胜率最低英雄A", "使用英雄数A",
        "对局英雄总数", "对局中最常用英雄",
        "使用英雄数B", "最常用英雄B", "胜率最高英雄B", "胜率最低英雄B", "选手B"
    ]]

    gt = GT(df)

    if title or subtitle:
        gt = gt.tab_header(title=title, subtitle=subtitle)

    gt = (
        gt
        .tab_spanner(team_a_name, columns=["选手A", "最常用英雄A", "胜率最高英雄A", "胜率最低英雄A", "使用英雄数A"])
        .tab_spanner("对局信息", columns=["对局英雄总数", "对局中最常用英雄"])
        .tab_spanner(team_b_name, columns=["使用英雄数B", "胜率最低英雄B",  "胜率最高英雄B", "最常用英雄B","选手B"])
        .cols_align("center")
        .cols_label(**{
            "选手A": "选手", "选手B": "选手",
            "最常用英雄A": "最常用英雄", "最常用英雄B": "最常用英雄",
            "胜率最高英雄A": "胜率最高英雄", "胜率最高英雄B": "胜率最高英雄",
            "胜率最低英雄A": "胜率最低英雄", "胜率最低英雄B": "胜率最低英雄",
            "使用英雄数A": "使用英雄数", "使用英雄数B": "使用英雄数"
        })
        .tab_style(style=style.fill(color="aliceblue"), locations=loc.body(columns=["选手A", "最常用英雄A", "胜率最高英雄A", "胜率最低英雄A", "使用英雄数A"]))
        .tab_style(style=style.fill(color="mistyrose"), locations=loc.body(columns=["使用英雄数B", "最常用英雄B", "胜率最高英雄B", "胜率最低英雄B", "选手B"]))
    )

    return gt

    
def all_funcs(blue_team,red_team,blue_team_name,red_team_name):


    df = load_match_list()
    player_df = load_player_id_df()

    blue, red = get_official_name(blue_team, red_team, player_df)
    print(blue,"\n", red)
    lst = shared_games_list(blue,red,df)
    compete = generate_compete_summary_df(lst)
    hero = generate_hero_summary_df(lst)
    return compete, hero

    # display_compete_table(compete, f"{blue_team_name} vs {red_team_name}", None,blue_team_name ,"red_team_name")
    # display_hero_table(hero, f"{blue_team_name} vs {red_team_name}", None,blue_team_name ,"red_team_name")