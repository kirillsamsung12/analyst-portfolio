select 
    u.user_id,
    u.age,
    case WHEN age IS NULL THEN 'Не указан' when age < 30 then 'Молодежь' else 'Взрослые' end as возрастная_группа
from users u
left join cards c on u.user_id = c.user_id
where u.city IS NOT NULL;



