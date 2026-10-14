select
    u.user_id,
    u.city,
    u.signup_date
    from users u left join transactions t on u.user_id = t.user_id
    where t.tx_id is null
    order by u.signup_date;

