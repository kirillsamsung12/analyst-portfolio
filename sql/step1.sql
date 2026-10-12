select 
    tx_id,
    tx_date,
    amount,
    round(sum(amount) over (order by tx_date asc), 2) as накопленная_сумма,
    LAG(tx_date) over (order by tx_date asc) as прошлая_дата,
    ROUND(julianday(tx_date) - julianday(LAG(tx_date) over (order by tx_date asc)), 1) as прошло_дней

from transactions
where user_id = 2 and status = 'success';