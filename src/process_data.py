import pandas as pd
import json
import os

# 读取 CSV
df = pd.read_csv("src/matches.csv")

# 计算新变量
df["WinRate_Percent"] = df["WinRate"] * 100

# 确保 docs/data 目录存在
os.makedirs("docs/data", exist_ok=True)

# 保存 JSON 到 GitHub Pages
json_path = "docs/data/matches.json"
df.to_json(json_path, orient="records", indent=4)

print(f"✅ 数据处理完成，JSON 文件已保存至 {json_path}")
