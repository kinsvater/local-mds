from pathlib import Path

import pandas as pd
import numpy as np
from mimesis import Generic
import duckdb

if __name__ == '__main__':
    faker = Generic(seed=1)

    num_accounts = 30
    accounts = pd.DataFrame({'Id': [f'a{i:05d}' for i in range(num_accounts)],
                             'CompanyName': [faker.finance.company() for _ in range(num_accounts)],
                             'BillingRegion': [faker.address.continent() for _ in range(num_accounts)]})

    # Every customer should have at least one site, some have more:
    num_extra_sites = 20
    sites = pd.DataFrame({'Id': [f's{i:05d}' for i in range(num_accounts + num_extra_sites)]})
    sites['SiteOwnerId'] = list(accounts['Id']) + list(accounts['Id'].sample(num_extra_sites, replace=True))
    sites['Region'] = list(accounts['BillingRegion']) + list([faker.address.continent() for _ in range(num_extra_sites)])

    num_orders = 50000
    orders = pd.DataFrame({'Id': [f'o{i:05d}' for i in range(num_orders)]})
    orders['SiteIdDelivery'] = sites['Id'].sample(num_orders, replace=True).values
    orders['DateBooked'] = [faker.datetime.date(start=2020, end=2022) for _ in range(num_orders)]
    orders['CurrencyCode'] = np.random.choice(['USD', 'EUR', 'GBP'], num_orders, replace=True, p=[0.7, 0.2, 0.1])
    orders['Price'] = faker.numeric.floats(start=0, end=100, precision=2, n=num_orders)
    orders['_percent'] = faker.numeric.floats(start=0, end=0.95, n=num_orders)
    orders['Cost'] = orders['Price'].mul(orders['_percent']).round(2)
    orders['Type'] = np.random.choice(['Installation', 'Service', 'Parts'], num_orders, replace=True, p=[0.4, 0.3, 0.3])
    orders = orders.drop('_percent', axis=1)

    fx_rates = pd.DataFrame({'Year': [2020, 2021, 2022, 2020, 2021],
                             'Currency': ['Euro', 'Euro', 'Euro', 'Pound Sterling', 'Pound Sterling', 'Pound Sterling'],
                             'Rate': [1.1, 1.2, 1.15, 1.3, 1.4, 1.2]})

    path_duck_db = Path(__file__).parent / '../data/data-mart.duckdb'

    if not path_duck_db.parent.exists():
        path_duck_db.parent.mkdir()

    con = duckdb.connect(database=str(path_duck_db), read_only=False)

    con.query("CREATE SCHEMA IF NOT EXISTS raw")

    for table_name in ('accounts', 'sites', 'orders', 'fx_rates'):
        con.query(f"DROP TABLE IF EXISTS raw.{table_name}; CREATE TABLE raw.{table_name} AS SELECT * FROM {table_name}")
