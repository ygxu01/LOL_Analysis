"""
Pull all Match History from GOL GG
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pathlib import Path
import time

from settings import config
from load_player_id import load_player_id_df

# === Constants ===
DATA_DIR = Path(config("DATA_DIR"))
MANUAL_DATA_DIR = Path(config("MANUAL_DATA_DIR"))
HEADERS = {"User-Agent": "Mozilla/5.0"}


def scrape_one_unit(player_name, player_id, season, scraped_urls):
    base_url = "https://gol.gg/players/player-matchlist/{player_id}/season-{season}/split-ALL/tournament-ALL/"
    url = base_url.format(player_id=player_id, season=season)

    if url in scraped_urls:
        print(f"Skipping already scraped URL: {url}")
        return None
    scraped_urls.add(url)

    print(f"Scraping: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"Failed to scrape {url}: {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "table_list"})
        if not table:
            print(f"No data found for {player_name} ({player_id}) - {season} {split}")
            return None

        rows = table.find_all("tr")
        columns = [header.text.strip() for header in rows[0].find_all("th")]
        data = []

        for row in rows[1:]:
            cells = row.find_all("td")
            if len(cells) != len(columns):
                continue  # skip malformed row
            data.append([cell.text.strip() for cell in cells])

        df = pd.DataFrame(data, columns=columns)
        df['player'] = player_name
        df['gg_id'] = player_id
        df['season'] = season
        return df

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def scrape_all_matches(player_id_df, start_season = 10, current_season = 15):
    all_data = []
    error_log = []
    scraped_urls = set()
    total_players = len(player_id_df)

    seasons = [f"S{i}" for i in range(start_season, current_season + 1)]
    # splits = ["Pre-Season", "Spring", "Summer"]

    for idx, player, in player_id_df.iterrows():
        player_name = player['player']
        player_id = player['gg_id']
        for season in seasons:
            print(f"Processing player {idx + 1} of {total_players}: {player_name} ({player_id})")

            df = scrape_one_unit(player_name, player_id, season, scraped_urls)
            if df is not None:
                all_data.append(df)
            else:
                error_log.append(f"{player_name} {season}")
            time.sleep(1)  # polite scraping delay

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        return final_df

    print("No match data collected.")
    return pd.DataFrame()

def load_match_list():
    path = DATA_DIR / "all_players_matchlist_S10-S15.parquet"
    df = pd.read_parquet(path)

    return df

if __name__ == "__main__":
    player_id_df = load_player_id_df()
    start_season = 10
    current_season=15
    all_match_df = scrape_all_matches(player_id_df, start_season, current_season)
    if not all_match_df.empty:
        path = DATA_DIR / f"all_players_matchlist_S{start_season}-S{current_season}.parquet"
        all_match_df.to_parquet(path)