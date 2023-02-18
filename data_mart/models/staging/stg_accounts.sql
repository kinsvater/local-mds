with accounts as (
    select
        Id as account_id,
        CompanyName as company_name,
        BillingRegion as account_region
    from raw.accounts
)

select * from accounts
