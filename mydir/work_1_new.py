"""
    导入文本字典(字符串操作)
"""
import pymysql

# 连接数据库
db = pymysql.connect(host="localhost", port=3306, user="root",
                     password="123456", database="dict", charset="utf8")

# 创建游标
cur = db.cursor()

# 数据操作
data = []
with open("dict.txt", "r", encoding="utf0-8") as file:
    for line in file:
        word_list = line.split(" ", 1)
        word = word_list[0]
        mean = word_list[1].lstrip()
        data.append((word, mean))
try:
    sql = "insert into words (word,mean) values (%s,%s);"
    cur.executemany(sql, data)
    db.commit()
except:
    print("no")
    db.rollback()

# 关闭游标
cur.close()

# 关闭数据库连接
db.close()
