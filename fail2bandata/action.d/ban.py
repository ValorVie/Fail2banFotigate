from dotenv import load_dotenv
import sys
import requests
import datetime
import os

# 載入 .env 檔案
load_dotenv()

# 讀取變數
api_url_base = os.getenv('API_URL')
group_api_url_base = os.getenv('GROUP_API_URL')
token = os.getenv('TOKEN')
teams_webhook_url = os.getenv('TEAMS_WEBHOOK_URL') 

# API連結
api_url = f"{api_url_base}{token}"
group_api_url = f"{group_api_url_base}{token}"

# 第一個參數是被 ban 的 IP
ip = sys.argv[1]


def ban_ip(ip):

    # 獲取當前時間
    now = datetime.datetime.now()

    # 將IP address加到subnet和name裡面
    ban_ip_address = {
        "name": f"banned_{ip}",
        "subnet": f"{ip}/32",
        "color": "0"
    }

    try:
        # 初始化標記
        created_in_group = False
        created_in_address = False

        # 檢查 IP 地址是否已存在
        check_url = f"{api_url_base}{ban_ip_address['name']}{token}"
        response_check = requests.get(check_url, verify=False)

        # 如果該 IP 地址對象已存在（HTTP 狀態碼為 200），則跳過創建步驟
        if response_check.status_code == 200:
            print(f"IP address {ban_ip_address['name']} 已存在，將不再創建。")
            created_in_address = True
        else:
            # 如果該 IP 地址對象不存在（HTTP 狀態碼不為 200），則創建新的 IP 地址對象
            response = requests.post(api_url, json=ban_ip_address, verify=False)

            if response.status_code == 200:
                print("IP address 新增成功！")
                print("回應狀態碼：", response.status_code)
                print("回應內容：", response.json())
                created_in_address = True
            else:
                print("IP address 新增失敗，錯誤碼：", response.status_code)
                print("回應內容：", response.json())
                exit()

        if created_in_address:
            # 取得新增IP address的名稱
            ip_name = ban_ip_address['name']

            # 準備加入Group的Payload
            group_payload = {
                "name": f"{ip_name}"
            }

            # 檢查 IP 地址是否已存在 Group
            check_group_url = f"{group_api_url_base}{ip_name}{token}"
            response_check_group = requests.get(check_group_url, verify=False)

            # 如果該 IP 地址對象已存在 Group（HTTP 狀態碼為 200），則跳過加入步驟
            if response_check_group.status_code == 200:
                print(f"IP address {ip_name} 已存在 BanVPNLoginFailed group，將不再加入。")
                created_in_group = True
            else:
                # 發送POST請求將IP加入Group
                response_group = requests.post(group_api_url, json=group_payload, verify=False)

                # 檢查回應狀態碼，200表示請求成功
                if response_group.status_code == 200:
                    print("IP address 成功加入到BanVPNLoginFailed group！")
                    print("回應狀態碼：", response_group.status_code)
                    print("回應內容：", response_group.json())
                    created_in_group = True
                else:
                    print("IP address 加入到BanVPNLoginFailed group失敗，錯誤碼：", response_group.status_code)

        if created_in_group and created_in_address:
            # 將信息寫入到linux日誌文件
            with open('/var/log/fortinet/ban.log', 'a') as f:
                f.write(f'[{now}] IP {ip} has been banned, address name: {ip_name}\n')

            # # 將信息寫入到windows日誌文件
            # with open('D:\\downloads\\test.log', 'a') as f:
            #     f.write(f'[{now}] IP {ip} has been banned, address name: {ip_name}\n')

            # 發送通知到Teams
            teams_message = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "summary": "IP Banned Notification",
                "title": "IP Banned",
                "text": f"[{now}] IP {ip} has been banned, address name: {ip_name}, https://ipinfo.io/{ip}",
            }
            requests.post(teams_webhook_url, json=teams_message, verify=False)
    except requests.exceptions.RequestException as e:
        print("連線錯誤：", e)

if __name__ == "__main__":
    ban_ip(ip)