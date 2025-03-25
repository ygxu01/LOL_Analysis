"""
Generate KDA columns
identify and label games according to games (LPL, LCK, Others, Worlds)
"""
import pandas as pd 

def calc_kda(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.drop(columns = ["Build"])

def label_world():
    pass

def label_bo5_bo3():
    pass