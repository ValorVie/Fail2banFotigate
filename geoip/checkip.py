import geoip2.database
import os

# 設定相對路徑
dir_path = os.path.dirname(os.path.realpath(__file__))

def get_allowed_countries(file_path=os.path.join(dir_path, 'allowed_countries.txt')): # 引入允許的國家清單
    with open(file_path, 'r') as file:
        return [country.strip() for country in file.readlines()]

def get_country(ip, db_path):
    try:
        with geoip2.database.Reader(db_path) as reader:
            response = reader.country(ip)
            return response.country.names['en']
    except Exception as e:
        print(f"無法獲取IP地址資訊：{str(e)}")
        return None

def check_and_remove_ips():
    db_path = os.path.join(dir_path, 'GeoLite2-Country.mmdb')
    allowed_countries = get_allowed_countries()
    
    # 讀取文件並儲存合適的 IP
    new_ips = []
    with open(os.path.join(dir_path, 'not_allow_country.log'), 'r') as file:
        for line in file:
            ip = line.strip()
            country = get_country(ip, db_path)
            if country not in allowed_countries:
                new_ips.append(ip)

    # 將合適的 IP 寫回文件
    with open(os.path.join(dir_path, 'not_allow_country.log'), 'w') as file:
        for ip in new_ips:
            file.write(f"{ip}\n")

    print("檢查並移除不在允許清單中的 IP 完成")

if __name__ == "__main__":
    check_and_remove_ips()
