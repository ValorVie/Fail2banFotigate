#!/bin/bash
# 載入.env檔案中的環境變數
source ../fail2bandata/action.d/.env

cd /root/docker/fail2ban/geoip
curl -o GeoLite2-Country.tar.gz "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key=$LICENSE_KEY&suffix=tar.gz"
tar -xvzf GeoLite2-Country.tar.gz
mv GeoLite2-Country*/GeoLite2-Country.mmdb .
rm -rf GeoLite2-Country_*/ GeoLite2-Country.tar.gz