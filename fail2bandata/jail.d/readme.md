bantime.increment = true：此設定啟用了封鎖時間的增長功能。若一個IP被封鎖後，再次違規，它的封鎖時間會按照一定的公式增長。該公式預設為封鎖時間的倍數增長，例如第一次封鎖10分鐘，第二次為20分鐘，第三次為40分鐘等。

bantime.rndtime = 2048：此設定定義了用於混合隨機時間的最大秒數，這能防止機器人網絡計算出IP可以再次被解封的確切時間。

bantime.multipliers = 1 10 30 60 300 720 1440 2880：這是一個列表，定義了封鎖時間增長的倍數。例如，如果bantime.increment = true，第一次封鎖的時間將乘以列表中的第一個數字，第二次封鎖的時間將乘以第二個數字，依此類推。

dbpurgeage = 30d：此設定指定了Fail2Ban會自動刪除超過30天的違規IP記錄。

接下來是[general-forceful-browsing]區塊的設定：

enabled = true：此設定表示啟用此封鎖規則。

ignoreip = ...：此設定列出了不會被此封鎖規則影響的IP範圍。例如，這可以防止封鎖來自Cloudflare CDN或特定私有網絡的流量。

filter = general-forceful-browsing：此設定指定了用於判定違規行為的過濾器。

logpath = /var/log/fortinet/syslog.log：此設定指定了Fail2Ban將監視的日誌檔案路徑。

action = action-ban-forceful-browsing：此設定指定了當觸發封鎖規則時Fail2Ban將執行的動作。

maxretry = 5：此設定表示一個IP在findtime期間內允許的最大違規次數。超過此次數，IP將被封鎖。

findtime = 1 day：此設定定義了尋找違規行為的時間窗口。

bantime = 10 min：此設定定義了初次封鎖的時間長度。如果bantime.increment = true，此時間將被用作後續封鎖時間計算的基礎。


Example:
假設我們有一個違規的IP地址：27.52.99.186。

首次違規：在[general-forceful-browsing]設定的findtime（1天）內，這個IP地址觸發了5次違規（達到maxretry次數）。根據bantime的設定，這個IP地址會被封鎖10分鐘。在這段時間內，這個IP的所有請求都會被拒絕。

第二次違規：假設在封鎖解除後的短時間內，這個IP地址再次觸發5次違規。由於bantime.increment設定為true，我們會參照bantime.multipliers的設定來計算新的封鎖時間。所以，第二次的封鎖時間將會是10分鐘（基礎時間）乘以10（bantime.multipliers列表的第二個數字），等於100分鐘。

第三次違規：假設在第二次封鎖解除後，這個IP地址又再次觸發5次違規。根據bantime.increment和bantime.multipliers的設定，第三次的封鎖時間將會是10分鐘（基礎時間）乘以30（bantime.multipliers列表的第三個數字），等於300分鐘。

假設這個IP地址在被封鎖後停止了違規行為，並在30天後再次違規。由於我們的dbpurgeage設定為30天，那麼Fail2Ban將清空這個IP的違規記錄，所以下一次的封鎖時間將會是基礎的10分鐘，而不是繼續增長。