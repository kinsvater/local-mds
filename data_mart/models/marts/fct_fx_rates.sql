select
    year,
    case
        when currency_name = 'Euro' then 'EUR'
        when currency_name = 'Pound Sterling' then 'GBP'
        else null
    end as currency_code,
    to_usd_rate
from {{ ref('stg_fx_rates') }}
