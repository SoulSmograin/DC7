import utils
import re
import config
import os



# Подключение к MySQL
try:
    # Создание настроек для подключения, если они отсутствуют
    utils.making_settings()
    # Создание подключения к MySQL
    connection = config.get_connect_mysql()
    cursor = connection.cursor()
    # Глобальный cписок баз данных
    database_list = []
except:
    # В случае проблем с подключеним утилита прекращет работу
    print("Проблема с подключением")
    exit()


# Часть кода с выполнением запросов
def exec_sql_file(vFile):
    global connection
    global cursor
    global database_list

    # Строка в которой будет формироваться запрос
    statement = ""
    for line in vFile:
        # игнорируем комментарии
        if re.match(r'--', line):
            continue
        # Поиск конца запроса
        if not re.search(r';', line):
            statement = statement + line
        # когда вы получаете строку, оканчивающуюся на ';' затем оператор exec и сброс для следующего оператора
        else:
            statement = statement + line
            statement_x = statement.split(" ")
            # Временное решение
            if statement_x[0] + " " + statement_x[1] == "CREATE DATABASE":
               # Выполнение запроса на создание БД
                try:
                    cursor.execute(statement)
                except Exception as err:
                    print(err)
                # Переподключение к созданной БД
                try:
                    # Выбираем БД с которой будем работать
                    utils.use_database(cursor, statement_x[2])
                    database_list.append(statement_x[2].replace(";", ""))
                except Exception as err:
                    print(err)
            elif statement_x[0] + " " + statement_x[1] == "insert into" or statement_x[0] == "update":
                try:
                    cursor.execute(statement)
                    connection.commit()
                except Exception as err:
                    print(err)
            else:
                try:
                    cursor.execute(statement)
                except Exception as err:
                    print(err)
            statement = ""


# Получение всех файлов из папки scripts
for root, dirs, files in os.walk(os.getcwd() + "\scripts"):
    print(files)
    for file in files:
        # Путь к файлу
        PATH_TO_FILE = os.getcwd() + "\scripts\\" + file
        # Открываем файл
        file = open(PATH_TO_FILE, 'r')
        # Сплитим файл
        vFile = file.read().split("\n")
        # Информируем о чтении файла
        print("\n[INFO] Выполнение файла SQL script : '%s'" % (PATH_TO_FILE))
        # Вызываем функцию для выполнения запрсоов из файла
        # Передаем файл в виде массива элементов
        exec_sql_file(vFile)

# Вывод результатов работы
utils.export_to_file(connection, cursor, database_list)
connection.close()