select
    Year::integer as year,
    Currency as currency_name,
    Rate as to_usd_rate
from raw.fx_rates
