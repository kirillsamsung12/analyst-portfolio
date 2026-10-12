select
    category,
    count(tx_id) as amount_operation,
    round(sum(amount), 2) as revenue,
    round(avg(amount), 2) as avg_revenue
from transactions
where status = 'success'
group by category
having avg_revenue >8000 and revenue >1500000
order by revenue desc;