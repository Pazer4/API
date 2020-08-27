# Импортируем библиотеку, соответствующую типу нашей базы данных
import sqlite3

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
conn = sqlite3.connect('DB.db')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

# Делаем INSERT запрос к базе данных, используя обычный SQL-синтаксис
cursor.execute('SELECT "shoot" from shoots WHERE "primary ID MC"=555')

data=cursor.fetchone()
if data:
    print(data[0])

"""# Проверяем результат
cursor.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")
results = cursor.fetchall()
print(results)  # [('A Aagrh!',), ('A Cor Do Som',), ('Aaron Copland & London Symphony Orchestra',)]"""

# Не забываем закрыть соединение с базой данных
conn.close()
