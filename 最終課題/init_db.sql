-- エリアテーブル
CREATE TABLE IF NOT EXISTS areas (
  area_id INTEGER PRIMARY KEY,
  area_name TEXT
);

-- エリアデータの初期投入（京都の主要エリア）
INSERT OR IGNORE INTO areas (area_id, area_name) VALUES 
(1, '京都駅周辺'),
(2, '河原町・祇園・東山'),
(3, '嵐山・太秦'),
(4, '大原・鞍馬');

-- 宿泊施設テーブル
CREATE TABLE IF NOT EXISTS hotels (
  hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
  hotel_name TEXT,
  area_id INTEGER,
  price INTEGER,
  total_reviews INTEGER,
  FOREIGN KEY (area_id) REFERENCES areas(area_id)
);

-- 外国語レビュー集計テーブル
CREATE TABLE IF NOT EXISTS foreign_reviews (
  review_id INTEGER PRIMARY KEY AUTOINCREMENT,
  hotel_id INTEGER,
  country TEXT,
  review_count INTEGER,
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);