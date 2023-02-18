with sites as (
    select
        Id as site_id,
        SiteOwnerId as owner_account_id,
        Region as site_region
    from raw.sites
)

select * from sites
