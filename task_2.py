import pandas as pd

from config import path_sources, path_results, colors


# Загружаем данные из файла 
app2 = pd.read_excel(path_sources / 'Приложение 2 к тестовому заданию.xlsx')
app3 = pd.read_excel(path_sources / 'Приложение 3 к тестовому заданию.xlsx')

# Создаем множество уникальных пар (owner_inn, address) из Приложения 3
permissions = set(zip(app3['owner_inn'], app3['address']))

# Функция для проверки наличия разрешения
def check_permission(row):
    return 'есть разрешение' if (row['owner_inn'], row['Адрес']) in permissions else 'нет разрешения'

# Добавляем новый столбец с признаком наличия разрешения
app2['Разрешение'] = app2.apply(check_permission, axis=1)

# Сохраняем результат
app2.to_excel(path_results / 'Задание 2 результат.xlsx', index=False)

print(f"{colors['green']}Обработка завершена. Результат сохранён в файле 'Задание 2 результат.xlsx'{colors['end']}")