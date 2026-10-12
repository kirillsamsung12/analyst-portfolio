with крупные_покупки as (
    select
        user_id,
        tx_id,
        amount,
        dense_rank() over (partition by user_id order by amount desc) as ранг
    from transactions
    where status = 'success'
)

select 
    user_id,
    tx_id,
    amount,
    ранг
from крупные_покупки
where ранг <=3
order by user_id, ранг
LIMIT 15;
