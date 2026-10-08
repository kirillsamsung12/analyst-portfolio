select 
    u.city as город,
    count(distinct u.user_id) as всего_клиентов,
    count(distinct c.user_id) as клиент_с_картой,
    count(distinct u.user_id) - count(distinct c.user_id) as клиенты_без_карт
    from users u
left join cards c on u.user_id = c.user_id
where u.city IS NOT NULL
group by u.city
order by клиенты_без_карт desc;



