-- Спринт 1, Задача 1.1: Финансовый отчёт по топ-категориям с оборотом > 2 млн руб.
-- Статус: Выполнено успешно

SELECT
    category,
    COUNT(*) as tx_count,
    ROUND(SUM(amount), 2) as total_spent,
    ROUND(AVG(amount), 2) as avg_check
FROM transactions
WHERE status = 'success' AND category IS NOT NULL
GROUP BY category
HAVING SUM(amount) > 2000000
ORDER BY total_spent DESC;
