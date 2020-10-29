import os
import re
import pandas as pd



# Использование другой другой БД
def use_database(cursor, db_name):
    # Подключение после создани БД
    query = "USE " + str(db_name)
    cursor.execute(query)
    return 0

# Получение списка таблиц в БД
def get_list_table(cursor):
    list_table = []
    query = "SHOW TABLES"
    cursor.execute(query)
    for table in cursor:
        list_table.append(table)
    return list_table

# Получение данных из таблицы
def get_data_from_table(connection, name_table):
    df = pd.read_sql('SELECT * FROM ' + name_table, connection)
    return df

# Создание файла настроек подключения
def making_settings():
    if os.path.exists(os.getcwd() + r'\connect\adc.txt') == True:
        return
    else:
        new_file = open(os.getcwd() + r'\connect\adc.txt', 'w')
        new_file.write(r'HOST:' + input("Введиет host - ") + '\n'
                       r'PORT:' + input("Введиет port - ") + '\n'
                       r'USER:' + input("Введиет user - ") + '\n'
                       r'PASSWORD:' + input("Введиет password - ") + '\n'
                       )
        new_file.close()

# Получение данных из файла настроек в формете dict
def get_settings_con():
    string = ""
    abc = open(os.getcwd() + r'\connect\adc.txt');

    for line in abc:
        string += line

    string = re.sub(r'\n', ' ', string)
    string = (re.sub(r':', ' ', string)).split(' ')
    dict = {string[i]: string[i + 1] for i in range(0, len(string) - 1, 2)}
    return dict


# OS функции
def create_folder_database(file_format, db_name):
    os.mkdir(os.getcwd() + file_format + db_name)

# Экспорт результатов работы в csv
def export_to_file_csv(df, table_name, db_name):
    if os.path.exists('csv_export') == False:
        os.mkdir("csv_export")
    if os.path.exists(os.getcwd() + r'\csv_export\%s' % db_name) == False:
        create_folder_database('\\csv_export\\', db_name)
    df.to_csv(os.getcwd() + r'\csv_export\%s\%s.сsv' % (db_name, table_name), index=False)
    return 0

# Экспорт результатов работы в excel
def export_to_file_excel(df, table_name, db_name):
    if os.path.exists('excel_export') == False:
        os.mkdir("excel_export")
    if os.path.exists(os.getcwd() + r'\excel_export\%s' % db_name) == False:
        create_folder_database('\\excel_export\\', db_name)
    df.to_excel(os.getcwd() + r'\excel_export\%s\%s.xls' % (db_name, table_name), index=False)

# Главная функция экспорта
def export_to_file(connection, cursor, database_list):
    # Добавить выборку по БД
    for db in database_list:
        use_database(cursor, db)
        table_list = get_list_table(cursor) #connection
        for table in table_list:
            keys = table.keys()
            for key in keys:
                df = get_data_from_table(connection, table[key])
                # Вывод в csv
                export_to_file_csv(df, table[key], db)
                # Вывод в excel
                # нужно чтобы был этот модуль  - pip install xlwt
                export_to_file_excel(df, table[key], db)


