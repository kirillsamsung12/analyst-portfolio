# ==============================================================================
# ПРОЕКТ 1: КОГОРТНЫЙ АНАЛИЗ УДЕРЖАНИЯ КЛИЕНТОВ (COHORT RETENTION ANALYSIS)
# ==============================================================================

# ШАГ 1: Импорт библиотек и подключение к базе данных
# Подключи библиотеки для работы с таблицами, базой данных и графиками
# Установи соединение с data/fintech_sandbox.db
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('data/fintech_sandbox.db')
df_data = pd.read_sql ("select user_id, tx_date from transactions where status = 'success'" ,conn)
df_data['tx_date'] = pd.to_datetime(df_data['tx_date'])
df_data['tx_month'] = df_data['tx_date'].dt.to_period('M')
df_data['cohort'] = df_data.groupby('user_id')['tx_month'].transform('min')
df_data['lifetime'] = (df_data['tx_month'] - df_data['cohort']).apply(lambda x: x.n)
cohort_counts = df_data.groupby(['cohort', 'lifetime'])['user_id'].nunique().reset_index()
cohort_pivot = cohort_counts.pivot(index='cohort', columns = 'lifetime', values = 'user_id')
retention_matrix = cohort_pivot.divide(cohort_pivot[0], axis=0)
print((retention_matrix * 100).round(1))
plt.figure(figsize=(14, 8))
sns.heatmap(retention_matrix, annot=True, fmt='.1%', cmap='Blues', vmin=0.5, vmax=1.0)
plt.title('Когортный анализ удержания клиентов банка (Monthly Retention Rate)', fontsize=14, pad=15)
plt.xlabel('Месяц жизни клиента (Lifetime)')
plt.ylabel('Когорта (Месяц первой покупки)')

plt.savefig('dashboards/cohort_retention_heatmap.png', dpi=300, bbox_inches='tight')
print("График успешно сохранен в dashboards/cohort_retention_heatmap.png")




# ШАГ 2: Выгрузка данных и подготовка дат
# Забери успешные транзакции (клиент и дата операции)
# Преобразуй даты в формат временных меток и выдели календарный месяц операции



# ШАГ 3: Определение когорты и месяца жизни (Lifetime)
# Найди для каждого клиента месяц его самой первой покупки (его когорту)
# Посчитай разницу в месяцах между текущей покупкой и первой покупкой (0, 1, 2...)



# ШАГ 4: Построение когортной матрицы (Retention Matrix)
# Сгруппируй данные по когорте и месяцу жизни, подсчитав уникальных клиентов
# Разверни в сводную таблицу (когорта по строкам, месяцы жизни по колонкам)
# Переведи абсолютные значения в проценты удержания (доля от месяца 0)



# ШАГ 5: Визуализация тепловой карты (Heatmap) и сохранение отчёта
# Построй график с процентами удержания
# Сохрани готовую картинку в папку dashboards/

