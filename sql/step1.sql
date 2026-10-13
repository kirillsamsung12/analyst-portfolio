with таблица_по_рангам as(
    select 
        user_id,
        tx_id,
        amount,
        category,
        dense_rank() over (partition by user_id order by amount desc) as ранг
    from transactions
    where status = 'success' and category is not null)
select 
    user_id,
    tx_id,
    amount,
    category
from таблица_по_рангам
where ранг = 1
order by amount desc
limit 15;