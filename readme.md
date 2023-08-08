## 台灣美國IP
1.1天內登入失敗5次 > 加入fail2ban資料庫 > 透過API加到fortigate封鎖清單
2.時間到API fortigate解封
3.存在fail2ban資料庫的IP在365天內，每登入失敗5次，封鎖時間依次遞增，最長365天

## 非台灣美國IP
1.登入失敗1次 > 加入fail2ban資料庫 > 透過API加到fortigate封鎖清單 + 加入not_allow_country清單
2.時間到API fortigate解封
3.fortigate載入not_allow_country清單
4.每天檢查not_allow_country清單，如果有包含台灣美國IP則刪除