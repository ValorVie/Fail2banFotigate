import sys
import geoip2.database


def get_allowed_countries(file_path='/geoip/allowed_countries.txt'): # 引入允許的國家清單
    with open(file_path, 'r') as file:
        return [country.strip() for country in file.readlines()]

def get_country(ip, db_path):
    try:
        with geoip2.database.Reader(db_path) as reader:
            response = reader.country(ip)
            return response.country.names['en']
    except Exception as e:
        print(f"無法獲取IP地址資訊：{str(e)}")
        sys.exit(1)

def write_ip_to_log(ip):
    with open('/geoip/not_allow_country.log', 'a') as file:
        file.write(f"{ip}\n")

def main():
    ip = sys.argv[1]
    db_path = "/geoip/GeoLite2-Country.mmdb"
    country = get_country(ip, db_path)

    allowed_countries = get_allowed_countries()

    if country in allowed_countries:  # 判斷國家是否在清單中
        print("True")
        sys.exit(0)  # 程式成功結束
    else:
        print("False")
        write_ip_to_log(ip)  # 將不在清單中的IP寫入日誌
        sys.exit(1)  # 程式失敗結束

if __name__ == "__main__":
    main()



# 另一種寫法
# import sys
# import geoip2.database

# def get_country(ip, db_path):
#     try:
#         with geoip2.database.Reader(db_path) as reader:
#             response = reader.country(ip)
#             return response.country.names['en']
#     except Exception as e:
#         print(f"無法獲取IP地址資訊：{str(e)}")
#         sys.exit(1)

# def main():
#     ip = sys.argv[1]
#     db_path = "/geoip/GeoLite2-Country.mmdb"
#     country = get_country(ip, db_path)

#     allowed_countries = ["Taiwan", "United States"]  # 將需要的國家放入此清單中

#     if country in allowed_countries:  # 判斷國家是否在清單中
#         print(1)
#         sys.exit(0)
#     else:
#         from ban import ban_ip
#         ban_ip(ip)

# if __name__ == "__main__":
#     main()
