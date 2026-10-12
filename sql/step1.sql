select
    case 
        when u.age <=25 then 'Молодые'
        when u.age <=45 then 'Взрослые'
        when u.age >45 then 'Зрелые'
        end as возрастная_группа,
    count(distinct u.user_id) as колличество_клиентов,
    round(sum(t.amount), 2) as revenue,
    round(avg(t.amount), 2) as avg_revenue
    from users u
    join transactions t on t.user_id = u.user_id
    where t.status = 'success' and u.age is not null and t.amount is not null and u.status = 'active'
    group by возрастная_группа
    order by revenue desc;

    