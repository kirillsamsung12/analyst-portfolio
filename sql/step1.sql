select
    u.user_id,
    u.city,
    case
        when count(t.tx_id) >15 then 'VIP-покупатель'
        when count(t.tx_id) <5 then 'Новичок / Спящий'
        else '«Постоянный»'
    end as сегмент,
    count(t.tx_id) as число_покупок
from users u
left join transactions t
    on u.user_id = t.user_id
group by u.user_id
order by число_покупок desc;

