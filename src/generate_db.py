import sqlite3
import random
from datetime import datetime, timedelta
import os

def create_database():
    db_path = os.path.join("data", "fintech_sandbox.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    random.seed(42)

    # 1. Таблица users
    cur.execute("""
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        signup_date TEXT NOT NULL,
        city TEXT,
        age INTEGER,
        status TEXT NOT NULL
    );
    """)

    # 2. Таблица cards
    cur.execute("""
    CREATE TABLE cards (
        card_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL,
        card_type TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    # 3. Таблица transactions
    cur.execute("""
    CREATE TABLE transactions (
        tx_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        tx_date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    # Генерация пользователей (200 чел)
    cities = ['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Самара', 'Краснодар']
    user_statuses = ['active'] * 170 + ['blocked'] * 15 + ['inactive'] * 15
    random.shuffle(user_statuses)

    start_date = datetime(2025, 10, 1)
    end_date = datetime(2026, 9, 30)
    total_days = (end_date - start_date).days

    users_data = []
    user_signup_map = {}

    for u_id in range(1, 201):
        # Дата регистрации: за последние 1.5 года
        u_days_offset = random.randint(0, total_days)
        signup_dt = start_date + timedelta(days=u_days_offset)
        signup_str = signup_dt.strftime("%Y-%m-%d")
        user_signup_map[u_id] = signup_dt

        # Пропуски в городах (~6%)
        city = random.choice(cities) if random.random() > 0.06 else None

        # Пропуски в возрасте (~8%)
        age = random.randint(18, 65) if random.random() > 0.08 else None

        status = user_statuses[u_id - 1]
        users_data.append((u_id, signup_str, city, age, status))

    cur.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?);", users_data)

    # Генерация карт (300 карт)
    # Распределяем карты: у кого-то 0 карт (15 чел), у кого-то 1-3 карты
    card_types = ['debit_standard', 'debit_premium', 'virtual', 'credit_standard']
    cards_data = []
    card_id_counter = 1001

    # Выберем 185 пользователей, у которых есть карты
    users_with_cards = list(range(1, 186))
    for u_id in users_with_cards:
        # минимум 1 карта
        num_cards = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        for _ in range(num_cards):
            if card_id_counter > 1300:
                break
            signup_dt = user_signup_map[u_id]
            max_days = max(1, (end_date - signup_dt).days)
            card_issue_dt = signup_dt + timedelta(days=random.randint(0, min(max_days, 30)), hours=random.randint(0, 23))
            c_type = random.choice(card_types)
            cards_data.append((card_id_counter, u_id, card_issue_dt.strftime("%Y-%m-%d"), c_type))
            card_id_counter += 1

    # Добиваем до 300 карт, если не хватило
    while card_id_counter <= 1300:
        u_id = random.choice(users_with_cards)
        signup_dt = user_signup_map[u_id]
        card_issue_dt = signup_dt + timedelta(days=random.randint(0, 15))
        cards_data.append((card_id_counter, u_id, card_issue_dt.strftime("%Y-%m-%d"), random.choice(card_types)))
        card_id_counter += 1

    cur.executemany("INSERT INTO cards VALUES (?, ?, ?, ?);", cards_data)

    # Генерация транзакций (3000 транзакций)
    # ~25 пользователей без транзакций (для проверки LEFT JOIN и конверсий)
    active_transacting_users = list(range(1, 176))
    categories = ['супермаркеты', 'рестораны и кафе', 'транспорт', 'коммунальные услуги', 'развлечения', 'одежда и обувь', 'электроника', 'переводы']
    tx_statuses = ['success', 'failed', 'refunded']

    transactions_data = []
    for tx_id in range(50001, 53001):
        u_id = random.choice(active_transacting_users)
        signup_dt = user_signup_map[u_id]

        # Транзакция происходит после регистрации
        remaining_days = max(1, (end_date - signup_dt).days)
        tx_dt = signup_dt + timedelta(
            days=random.randint(0, remaining_days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        # Категория (3% пропусков)
        category = random.choice(categories) if random.random() > 0.03 else None

        # Суммы: большинство мелкие/средние (100 - 4500), часть крупные (5000 - 65000)
        if random.random() < 0.85:
            amount = round(random.uniform(50.0, 4800.0), 2)
        else:
            amount = round(random.uniform(5000.0, 75000.0), 2)

        # Статусы: ~82% success, ~11% failed, ~7% refunded
        status = random.choices(tx_statuses, weights=[0.82, 0.11, 0.07])[0]

        transactions_data.append((tx_id, u_id, tx_dt.strftime("%Y-%m-%d %H:%M:%S"), amount, category, status))

    # Сортируем транзакции по дате для реалистичности
    transactions_data.sort(key=lambda x: x[2])
    # Переприсваиваем tx_id по порядку хронологии
    reindexed_tx = []
    for idx, row in enumerate(transactions_data, start=50001):
        reindexed_tx.append((idx, row[1], row[2], row[3], row[4], row[5]))

    cur.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?);", reindexed_tx)

    conn.commit()
    conn.close()
    print("Database successfully created and populated.")

if __name__ == "__main__":
    create_database()
