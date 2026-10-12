select
    user_id as Идентификатор_клиента,
    tx_id as Идентификатор_операции,
    tx_date as поле_даты,
    amount as поле_суммы,
    row_number() over (partition by user_id order by tx_date ASC) as номер_покупки

from transactions

where status ='success'
order by user_id, tx_date
LIMIT 15;
