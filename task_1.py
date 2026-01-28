import pandas as pd
from config import path_sources, path_results, colors


# Загружаем данные из файла 
df = pd.read_excel(path_sources / 'Приложение 1 к тестовому заданию.xlsx')

df = df.rename(columns={
    'Рыночная цена актива в момент совершения сделки (за 1 шт)': 'market_price',
    'Цена сделки (за 1 шт)': 'deal_price'
})

# Рассчитываем отклонения от рынка
# Для покупки когда цена сделки выше рыночной 
# Для продажи когда цена сделки ниже рыночной 
df['price_deviation'] = df.apply(
    lambda x: x['deal_price'] - x['market_price']
    if x['Покупка/Продажа'] == 'B'
    else x['market_price'] - x['deal_price'],
    axis=1
)

# Посчитаем 
# avg_deviation - среднее отклонение, 
# total_deviation - суммарный эффект сделок, 
# deals_count - количество сделок,
# negative_share - процент невыгодных сделок
counterparty_stats = (
    df.groupby('Контрагент')
      .agg(
          avg_deviation=('price_deviation', 'mean'),
          total_deviation=('price_deviation', 'sum'),
          deals_count=('price_deviation', 'count'),
          negative_percent=('price_deviation', lambda x: (x > 0).mean() * 100)
      ).reset_index()
)

# Фильтруем подозрительных контрагентов
suspicious_counterparties = counterparty_stats[
    (counterparty_stats['avg_deviation'] > 0) &
    (counterparty_stats['negative_percent'] > 60) &
    (counterparty_stats['deals_count'] >= 5)
].sort_values('avg_deviation', ascending=False)

suspicious_counterparties = suspicious_counterparties.rename(columns={
    'avg_deviation': 'Среднее отклонение', 
    'total_deviation': 'Суммарный эффект',
    'deals_count': 'Количество сделок',
    'negative_percent': 'Процент невыгодных сделок'
})

suspicious_counterparties.to_excel(path_results / 'Задание 1 результат.xlsx', index=False)

print(f"{colors['green']}Обработка завершена. Результат сохранён в файле 'Задание 1 результат.xlsx'{colors['end']}")
