import pymysql
from utils import get_settings_con
from pymysql.cursors import DictCursor



# Подключение к стандартной базе данных MySQL (В случае если первым запросом в файле не CREATE TADABASE)
def get_connect_mysql():
    dict = get_settings_con()
    connection = pymysql.connect(
        host = dict['HOST'],
        user = dict['USER'],
        password = dict['PASSWORD'],
        charset = 'utf8mb4',
        cursorclass = DictCursor,
        port = int(dict['PORT'])
    )
    return connection