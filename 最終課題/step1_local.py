import sqlite3
from bs4 import BeautifulSoup
import re
import os
import time  # 1. サーバー負荷配慮のために追加

def check_files():
    print("--- 現在のフォルダにあるファイル一覧 ---")
    files = os.listdir()
    for f in files:
        print(f"- {f}")
    print("---------------------------------------")

class LocalRakutenParser:
    def __init__(self, db_path='travel_data.db'):
        self.db_path = db_path

    def parse_num(self, text):
        num = re.sub(r'\D', '', text)
        return int(num) if num else 0

    def save_to_db(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO hotels (hotel_name, area_id, price, total_reviews) VALUES (?, ?, ?, ?)",
                       (data['name'], data['area_id'], data['price'], data['reviews']))
        conn.commit()
        conn.close()

    def run(self, filename):
        if not os.path.exists(filename):
            print(f"【エラー】'{filename}' というファイルが見つかりません。")
            return

        with open(filename, "r", encoding="utf-8", errors='ignore') as f:
            soup = BeautifulSoup(f, "html.parser")

        count = 0
        for target in soup.find_all(["h2", "h3", "a"]):
            # 2. ループの先頭で1秒待機（スクレイピング時のマナー）
            time.sleep(1) 
            
            name = target.get_text(strip=True)
            if len(name) < 5: continue 
            
            parent = target.find_parent(["div", "section", "li"])
            if parent:
                text = parent.get_text()
                if "円" in text:
                    price = self.parse_num(re.search(r'[\d,]+円', text).group()) if re.search(r'[\d,]+円', text) else 0
                    review = self.parse_num(re.search(r'[\d,]+件', text).group()) if re.search(r'[\d,]+件', text) else 0
                    
                    if price > 0:
                        self.save_to_db({'name': name, 'area_id': 1, 'price': price, 'reviews': review})
                        print(f"成功: {name[:15]}... | {price}円")
                        count += 1
        print(f"\n完了！ {count}件保存しました。")

if __name__ == "__main__":
    check_files()
    parser = LocalRakutenParser()
    parser.run("kyoto.html")