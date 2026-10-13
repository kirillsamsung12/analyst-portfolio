with помесячный_отчет as (
    select
        strftime ('%Y-%m', signup_date) as месяц,
        count(distinct user_id) as новые_клиенты
    from users
    group by месяц
)
select 
    месяц,
    новые_клиенты,
    SUM(новые_клиенты) OVER (ORDER BY месяц ASC) AS общее_число_клиентов
from помесячный_отчет
order by месяц asc;
