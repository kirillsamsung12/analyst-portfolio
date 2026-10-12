with order_date_number as
    (
        select
            user_id,
            tx_id,
            tx_date,
            row_number() over(partition by user_id order by tx_date) as номер_покупки,
            lag(tx_date) over(partition by user_id order by tx_date) as прошлая_дата_покупки
        from transactions
        where status = 'success'
    )
select
    user_id,
    round(julianday(tx_date) - julianday(прошлая_дата_покупки), 1) as дней_между_покупками
from order_date_number
where номер_покупки =2
ORDER BY user_id
limit 15;