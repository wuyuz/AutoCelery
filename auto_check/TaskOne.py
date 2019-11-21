import time
import pymysql
from .conf import DATABASES
from auto_check.celery import DDQ
import random
import re
import requests
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=20)
Error_list = []

def task(msg):
    try:
        if not get_text(msg):
            data = {
                'ip': msg,
                'status': 1,
            }
            Error_list.append(data)
        else:
            data = {
                'ip': msg,
                'status': 0,
            }
            Error_list.append(data)
    except Exception as e:
        print(e)
        data = {
            'ip': msg,
            'status': 2,
        }
        Error_list.append(data)



@DDQ.task
def check(status):
    ret = get_ips(status)
    print(len(ret))
    all_task = []
    for msg in ret:
        all_task.append(executor.submit(task, msg[1]))
    executor.shutdown()

    conn = pymysql.connect(
        host=DATABASES['HOST'],
        user=DATABASES['USER'],
        password=DATABASES['PASSWORD'],
        db=DATABASES['DB'],
        charset='utf8'
    )
    cursor = conn.cursor()  # 创建游标
    print(len(Error_list))
    for i in range(len(Error_list)):
        obj = Error_list.pop()
        sql = f" UPDATE ip_check_ips SET status = {obj['status']} WHERE ip = '{obj['ip']}';"
        # cursor.execute(sql,obj['status'],obj['ip'])
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()


# 爬取操纵
requests.packages.urllib3.disable_warnings()
username = 'lum-customer-hl_8cea7d90-zone-zone1'
password = 'vxlqxioh3tsb'
port = 22225
session_id = random.random()
proxy = {
    'http': ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' % (username, session_id, password, port)),
    'https': ('https://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' % (username, session_id, password, port))
}
headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept - Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

url = 'https://cgi.urlsec.qq.com/index.php?m=check&a=check=&url=http://%s'


def get_text(ip):
    # print(threading.current_thread())
    headers['Referer'] = 'https://guanjia.qq.com/online_server/result.html?url=%s' % ip
    new_url = url % ip
    content = requests.get(url=new_url, proxies=proxy, headers=headers, timeout=30, verify=False).text.encode(
        'utf-8').decode(
        'unicode_escape')
    ret = re.findall(r'"WordingTitle":(.*),"Wording"', content)
    if len(ret[0]) > 3:
        return False
    return True


def get_ips(status):
    """
    向数据库中获取数据
    :param status:
    :return:
    """
    conn = pymysql.connect(
        host=DATABASES['HOST'],
        user=DATABASES['USER'],
        password=DATABASES['PASSWORD'],
        db=DATABASES['DB'],
        charset='utf8'
    )
    cursor = conn.cursor()  # 创建游标
    sql = 'select * from ip_check_ips where status="%s"'

    try:
        cursor.execute(sql, status)
        conn.commit()
        return cursor.fetchmany(300)
    except:
        conn.rollback()
