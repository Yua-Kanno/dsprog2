import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

class HotelAnalyzer:
    def __init__(self, db_path='travel_data.db'):
        self.db_path = db_path

    def get_data(self):
        if not os.path.exists(self.db_path):
            print(f"Error: {self.db_path} not found.")
            return pd.DataFrame()
        
        conn = sqlite3.connect(self.db_path)
        query = "SELECT hotel_name, price, total_reviews FROM hotels WHERE price > 0 AND total_reviews > 0"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # 不要なゴミデータを除去
        df = df[~df['hotel_name'].str.contains('ビュー|地図|プラン')]
        return df.drop_duplicates(subset=['price', 'total_reviews'])

    def plot_data(self, df):
        plt.figure(figsize=(10, 6))
        plt.scatter(df['price'], df['total_reviews'], alpha=0.6, c='dodgerblue', s=100, edgecolors='white')
        
        # 英語なら100%文字化けしません
        plt.title('Kyoto Hotels: Price vs Reviews', fontsize=16)
        plt.xlabel('Price (JPY)', fontsize=12)
        plt.ylabel('Number of Reviews', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)

        plt.tight_layout()
        plt.savefig('analysis_result.png')
        print("\nSuccess! Plot saved as 'analysis_result.png'")
        plt.show()

if __name__ == "__main__":
    analyzer = HotelAnalyzer()
    df = analyzer.get_data()
    if not df.empty:
        analyzer.plot_data(df)
    else:
        print("No valid data found in DB.")