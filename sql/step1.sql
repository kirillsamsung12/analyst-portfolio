select 
    tx_id,
    tx_date,
    amount,
    round(sum(amount) over (order by tx_date asc), 2) as накопленная_сумма

from transactions
where user_id = 2 and status = 'success';