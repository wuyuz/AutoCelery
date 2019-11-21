#
#
# import pymysql
#
# from auto_check.conf import DATABASES
#
#
# def get_ips(status):
#     """
#     向数据库中获取数据
#     :param status:
#     :return:
#     """
#     conn = pymysql.connect(
#         host=DATABASES['HOST'],
#         user=DATABASES['USER'],
#         password=DATABASES['PASSWORD'],
#         db=DATABASES['DB'],
#         charset = 'utf8'
#     )
#     cursor = conn.cursor()  # 创建游标
#     sql = 'select * from ip_check_ips where status="%s"'
#
#     try:
#         cursor.execute(sql, status)
#         conn.commit()
#         return cursor.fetchmany(300)
#     except:
#         conn.rollback()

# print(get_ips(2))


E = [1,2,4,4,5]


def x():
    for i in range(len(E)):
        print(i)
        E.pop()


def fun():
    x()
    print(E)

fun()