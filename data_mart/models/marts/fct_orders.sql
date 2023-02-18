with orders as (
    select *,
        extract('year' from booked_date)::integer as booked_year
    from {{ ref('stg_orders') }}
), rates as (
    select * from {{ ref('fct_fx_rates') }}
)

select
    orders.order_id,
    orders.deliver_to_site_id,
    orders.order_type,
    orders.currency_code,
    orders.order_price_lcu,
    orders.order_cost_lcu,
    orders.order_price_lcu * rates.to_usd_rate as order_price_usd,
    orders.order_cost_lcu * rates.to_usd_rate as order_cost_usd,
    orders.booked_date
from orders
left join rates
    on orders.booked_year = rates.year and orders.currency_code = rates.currency_code
