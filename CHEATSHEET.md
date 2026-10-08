# 📌 Шпаргалка аналитика: День 1 (SQL & Python/Pandas)

> Сохраняй этот файл. Забыть буквы синтаксиса в первый день — абсолютно нормально. Главное — понимать логику шагов.

---

## 🗄️ 1. Логика объединения (JOIN / MERGE)

Когда связываем две таблицы по общему полю (например, `user_id`):
* **`LEFT JOIN`** оставляет **ВСЕХ** пользователей из первой таблицы.
* Если у пользователя нет записей во второй таблице — вместо данных подставляется пустота (**`NULL`** в SQL, **`NaN`** в Python).

---

## 🛠️ 2. В SQL

```sql
-- Поиск пользователей без транзакций:
SELECT u.user_id, u.city
FROM users u
LEFT JOIN transactions t ON u.user_id = t.user_id
WHERE t.tx_id IS NULL;
```

---

## 🐍 3. В Python (Pandas)

### Шаг 1: Подключение к базе
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/fintech_sandbox.db")
```

### Шаг 2: Выгрузка таблиц
```python
df_users = pd.read_sql("SELECT * FROM users", conn)
df_cards = pd.read_sql("SELECT * FROM cards", conn)
```

### Шаг 3: Склейка двух таблиц (`pd.merge`)
```python
df_all = pd.merge(df_users, df_cards, on="user_id", how="left")
```

### Шаг 4: Поиск тех, у кого нет данных (`.isna()`)
```python
# 1. Спросили, где пусто:
is_empty = df_all["card_id"].isna()

# 2. Оставили только эти строки в таблице:
df_no_cards = df_all[is_empty]
```

### Шаг 5: Подсчёт строк и процентов (`len`)
```python
count_no_cards = len(df_no_cards)  # сколько без карт (15)
total = len(df_users)              # всего клиентов (200)

percent = (count_no_cards / total) * 100  # 7.5%
```
