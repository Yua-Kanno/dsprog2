const searchBtn = document.getElementById('search-btn');
const backBtn = document.getElementById('back-btn');
const searchScreen = document.getElementById('search-screen');
const resultScreen = document.getElementById('result-screen');
const prefSelect = document.getElementById('pref-select');

// 1. 都道府県リストの取得
async function init() {
    try {
        const res = await fetch('https://www.jma.go.jp/bosai/common/const/area.json');
        const data = await res.json();
        prefSelect.innerHTML = '<option value="">都道府県を選択</option>';
        for (const code in data.offices) {
            const opt = document.createElement('option');
            opt.value = code;
            opt.textContent = data.offices[code].name;
            prefSelect.appendChild(opt);
        }
    } catch (e) {
        prefSelect.innerHTML = '<option value="">読み込み失敗</option>';
    }
}

// 2. 天気チェック処理
searchBtn.addEventListener('click', async () => {
    const code = prefSelect.value;
    if (!code) return alert("都道府県を選択してください");

    try {
        const res = await fetch(`https://www.jma.go.jp/bosai/forecast/data/forecast/${code}.json`);
        const data = await res.json();

        // データの反映
        document.getElementById('display-location').textContent = prefSelect.selectedOptions[0].text;
        
        const weatherText = data[0].timeSeries[0].areas[0].weathers[0];
        const iconBox = document.getElementById('weather-icon-large');
        
        // アイコン判定（画像がない場合は絵文字を表示）
        if (weatherText.includes("晴")) {
            iconBox.innerHTML = '<img src="kkrn_icon_taiyou_1.png" alt="晴" onerror="this.outerHTML=\'☀️\'">';
        } else if (weatherText.includes("雨")) {
            iconBox.innerHTML = '<img src="weather_parasol_rain_illust_1087.png" alt="雨" onerror="this.outerHTML=\'☔\'">';
        } else {
            iconBox.innerHTML = '<img src="kkrn_icon_kumo_1.png" alt="曇" onerror="this.outerHTML=\'☁️\'">';
        }

        // 気温の取得（安全な抽出）
        let temp = "--";
        const tempArea = data[0].timeSeries.find(s => s.areas[0].temps);
        if (tempArea) temp = tempArea.areas[0].temps[0];
        document.getElementById('temp-val').textContent = temp;

        // 湿度と風速のダミー値（気象庁APIには数値がないため）
        document.getElementById('hum-val').textContent = Math.floor(Math.random() * (70 - 40) + 40);
        document.getElementById('wind-val').textContent = (Math.random() * 5).toFixed(1);

        // 画面切り替え（クラスの付け替えのみ）
        searchScreen.classList.add('hidden');
        resultScreen.classList.remove('hidden');

    } catch (e) {
        alert("データの取得に失敗しました。");
    }
});

// 3. 戻るボタンの処理
backBtn.addEventListener('click', () => {
    resultScreen.classList.add('hidden');
    searchScreen.classList.remove('hidden');
});

init();