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

# 第一個參數是被 ban 的 IP
ip = sys.argv[1]

# 獲取當前時間
now = datetime.datetime.now()

# 將IP address加到subnet和name裡面
ban_ip_address = {
    "name": f"banned_{ip}",
    "subnet": f"{ip}/32",
    "color": "0"
}

deleteaddressurl = f"{api_url_base}{ban_ip_address['name']}{token}"
deletegroupurl = f"{group_api_url_base}{ban_ip_address['name']}{token}"

try:
    # 初始化標記
    deleted_from_group = False
    deleted_from_address = False

    # 檢查 IP 地址是否已存在 Group
    response_check_group = requests.get(deletegroupurl, verify=False)
    if response_check_group.status_code == 200:
        print(f"IP address {ban_ip_address['name']} 存在 BanVPNLoginFailed group。")
        response_group_delete = requests.delete(deletegroupurl, verify=False)
        if response_group_delete.status_code == 200:
            print("IP address 成功從 BanVPNLoginFailed group 刪除！")
            print("回應狀態碼：", response_group_delete.status_code)
            print("回應內容：", response_group_delete.json())
            deleted_from_group = True
        else:
            print("IP address 從 BanVPNLoginFailed group 刪除失敗，錯誤碼：", response_group_delete.status_code)
    else:
        print(f"IP address {ban_ip_address['name']} 不存在 BanVPNLoginFailed group。")
        deleted_from_group = True  # 如果 IP 本來就不存在，我們也將標記設為 True

    # 檢查 IP 地址是否已存在
    response_check = requests.get(deleteaddressurl, verify=False)
    if response_check.status_code == 200:
        print(f"IP address {ban_ip_address['name']} 存在。")
        response_delete = requests.delete(deleteaddressurl, verify=False)
        if response_delete.status_code == 200:
            print("IP address 刪除成功！")
            print("回應狀態碼：", response_delete.status_code)
            print("回應內容：", response_delete.json())
            deleted_from_address = True
        else:
            print("IP address 刪除失敗，錯誤碼：", response_delete.status_code)
            print("回應內容：", response_delete.json())        
    else:
        print(f"IP address {ban_ip_address['name']} 不存在。")
        deleted_from_address = True  # 如果 IP 本來就不存在，我們也將標記設為 True

    if deleted_from_group and deleted_from_address:
        # 將信息寫入到linux日誌文件
        with open('/var/log/fortinet/ban.log', 'a') as f:
            f.write(f"[{now}] IP {ip} has been unbaned, address name: {ban_ip_address['name']}\n")

        # # 將信息寫入到windows日誌文件
        # with open('D:\\downloads\\test.log', 'a') as f:
        #     f.write(f"[{now}] IP {ip} has been unban, address name: {ban_ip_address['name']}\n")

        # 發送通知到Teams
        teams_message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": "IP Unbaned Notification",
            "title": "IP Unbaned",
            "text": f"[{now}] IP {ip} has been unbaned, address name: {ban_ip_address['name']},  https://ipinfo.io/{ip}",
        }
        requests.post(teams_webhook_url, json=teams_message, verify=False)        
except requests.exceptions.RequestException as e:
    print("連線錯誤：", e)