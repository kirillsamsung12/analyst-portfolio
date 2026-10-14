select 
    u.city,
    count(distinct u.user_id) as уникальных_пользователей,
    count(t.tx_id) as колличество_транзакций,
    round(sum(t.amount), 2) as сумма_выручки,
    round(avg(t.amount), 2) as средний_чек_покупки
from users u
join transactions t on u.user_id = t.user_id
where u.status = 'active' and  t.status = 'success'
group by u.city
having сумма_выручки >2000000
order by сумма_выручки desc;
