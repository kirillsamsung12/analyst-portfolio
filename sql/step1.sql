with пронумерованные_покупки AS (
    select
        user_id,
        tx_id,
        tx_date,
        amount,
        row_number() over (partition by user_id order by tx_date ASC) as номер_покупки

    from transactions

    where status ='success'
)

select 
    user_id,
    tx_id,
    tx_date,
    amount
from пронумерованные_покупки
where номер_покупки = 1
ORDER BY amount DESC
LIMIT 10;