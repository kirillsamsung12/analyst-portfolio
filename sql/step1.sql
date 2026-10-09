select
    case 
        when amount <1000 then 'Микро'
        when amount >=1000 and amount <10000 then 'Стандарт'
        when amount >=10000 then 'Премиум'
        end as 'категория',
    count(tx_id) as колличество_покупок,
    round(sum(amount), 2) as Суммарная_выручка,
    round(avg(amount), 2) as Средний_чек
from transactions
where status = 'success'
group by категория
order by Суммарная_выручка desc;
