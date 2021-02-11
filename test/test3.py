import time # 引入time

nowTime = int(time.time()) # 取得現在時間
struct_time = time.localtime(nowTime) # 轉換成時間元組
timeString = time.strftime("%Y%m%d%I%M%S%P", struct_time) # 將時間元組轉換成想要的字串
print(timeString)