with помесячный_отчет as 
(

    select
        strftime('%Y-%m', tx_date) as месяц,
        round(sum(amount), 2) as выручка_за_месяц
    from transactions

    where status ='success'

    group by месяц  
)
select 
    месяц,
    выручка_за_месяц,
    round(sum(выручка_за_месяц) over (order by месяц asc), 2) as накопительный_итог

from помесячный_отчет
order by месяц asc;