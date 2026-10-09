select
    u.city,
    count(t.tx_id) as колличество_платежей,
    round(sum(t.amount), 2) as выручка_по_городу,
    round(avg(t.amount), 2) as средний_чек

from users u
join transactions t on u.user_id = t.user_id
where u.status = 'active' and t.status = 'success' and u.city is not null
group by u.city
having выручка_по_городу >2000000
order by выручка_по_городу desc;