import pymysql
import re

# 连接数据库
db = pymysql.connect(host="localhost", port=3306, user="root",
                     password="123456", database="dict", charset="utf8")

# 创建游标
cur = db.cursor()

# 数据操作
data = []
with open("dict.txt", "r", encoding="utf-8") as file:
    for line in file:
        one_word = re.findall(r"(\w+)\s+(.*)", line)
        data.append(one_word[0])

try:
    sql = "insert into words (word,mean) values (%s,%s);"
    cur.executemany(sql, data)
    db.commit()
except:
    print("no")
    db.rollback()
# 关闭游标
cur.close()

# 关闭数据库
db.close()
