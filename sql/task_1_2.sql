-- Спринт 1, Задача 1.2: Поиск «спящих» клиентов без транзакций
-- Результат: 25 клиентов с нулевой активностью

SELECT
    u.user_id,
    u.city,
    u.age,
    u.signup_date
FROM users u
LEFT JOIN transactions t ON u.user_id = t.user_id
WHERE t.tx_id IS NULL;
