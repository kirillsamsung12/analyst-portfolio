select 
    strftime('%Y-%m', tx_date) as месяц,
    count(*) as количество_операций,
    round(sum(amount), 2) as объем_денег,
    round(avg(amount), 2) as средний_чек
from transactions
where status = 'success'
group by месяц 
order by месяц;
