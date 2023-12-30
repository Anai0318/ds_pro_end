import psycopg2
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# データベースに接続するための設定
conn = psycopg2.connect(
    dbname="ds_pro", 
    user="yoshi", 
    password="test000", 
    host="localhost",
    port='5432'
)
cur = conn.cursor()

driver = webdriver.Chrome()
driver.get('https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/explorer/crime/crime-trend')
time.sleep(20)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 加害者のデータ
offender_10 = soup.find('p', id='crime-trend-Offender Age-number-10-19-value')
offender_20 = soup.find('p', id='crime-trend-Offender Age-number-20-29-value')
offender_30 = soup.find('p', id='crime-trend-Offender Age-number-30-39-value')
offender_40 = soup.find('p', id='crime-trend-Offender Age-number-40-49-value')
unknown = soup.find('p', id='crime-trend-Offender Age-number-Unknown-value')
# 被害者のデータ
victim_10 = soup.find('p', id='crime-trend-Victim Age-number-10-19-value')
victim_20 = soup.find('p', id='crime-trend-Victim Age-number-20-29-value')
victim_30 = soup.find('p', id='crime-trend-Victim Age-number-30-39-value')
victim_40 = soup.find('p', id='crime-trend-Victim Age-number-10-19-value')
victim_50 = soup.find('p', id='crime-trend-Victim Age-number-50-59-value')
# 犯行手段（武器や素手など）
personal_weapons = soup.find('p', id='crime-trend-Type of weapon involved by offense-number-Personal Weapons-value')
handgun = soup.find('p', id='crime-trend-Type of weapon involved by offense-number-Handgun-value')
knife_cutting_instrument = soup.find('p', id='crime-trend-Type of weapon involved by offense-number-Knife/Cutting Instrument-value')
firearm = soup.find('p', id='crime-trend-Type of weapon involved by offense-number-Firearm-value')
none = soup.find('p', id='crime-trend-Type of weapon involved by offense-number-None-value')



# 文字列を整数に変換する関数
def convert_to_int(string):
    return int(string.replace(",", ""))

if all([offender_20, offender_30, offender_10, offender_40, unknown, victim_10, victim_20, victim_30, victim_40, victim_50, personal_weapons, handgun, knife_cutting_instrument, firearm, none]):
    offender_10_19 = convert_to_int(offender_10.text.strip())
    offender_20_29 = convert_to_int(offender_20.text.strip())
    offender_30_39 = convert_to_int(offender_30.text.strip())
    offender_40_49 = convert_to_int(offender_40.text.strip())
    unknown = convert_to_int(unknown.text.strip())
    victim_10 = convert_to_int(victim_10.text.strip())
    victim_20 = convert_to_int(victim_20.text.strip())
    victim_30 = convert_to_int(victim_30.text.strip())
    victim_40 = convert_to_int(victim_40.text.strip())
    victim_50 = convert_to_int(victim_50.text.strip())
    personal_weapons = convert_to_int(personal_weapons.text.strip())
    handgun = convert_to_int(handgun.text.strip())
    knife_cutting_instrument = convert_to_int(knife_cutting_instrument.text.strip())
    firearm = convert_to_int(firearm.text.strip())
    none = convert_to_int(none.text.strip())
    print(f'10代 : {offender_10_19} | 20代 : {offender_20_29} | 30代 : {offender_30_39} | 40代 : {offender_40} | 不明 : {unknown}') 

    # データベースにデータを挿入
    cur.execute("INSERT INTO crime (offender_10, offender_20, offender_30, offender_40, offender_unknown, victim_10, victim_20, victim_30, victim_40, victim_50, personal_weapons, handgun, knife_cutting_instrument, firearm, none) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (offender_10_19, offender_20_29, offender_30_39, offender_40_49, unknown, victim_10, victim_20, victim_30, victim_40, victim_50, personal_weapons, handgun, knife_cutting_instrument, firearm, none))

    # 変更をコミット
    conn.commit()

# ブラウザを閉じる
driver.quit()

# データベース接続を閉じる
cur.close()
conn.close()