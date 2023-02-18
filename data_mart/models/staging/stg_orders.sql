with orders as (
    select
        Id as order_id,
        SiteIdDelivery as deliver_to_site_id,
        Type as order_type,
        CurrencyCode as currency_code,
        Price as order_price_lcu,
        Cost as order_cost_lcu,
        DateBooked::date as booked_date
    from raw.orders
)

select * from orders
