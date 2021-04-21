import csv

def add(filename,note):
# 開啟輸出的 CSV 檔案
    with open('C:\\temp\\'+filename+'_re.csv', 'a', newline='') as csvfile:
    # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)

        # 寫入一列資料
        writer.writerow(note)
