# Local Modern Data Stack

## Configure local environment

Commands below assume that the current working directory is the root of this repository.

1. Install the conda environment using the environment.yml:

```bash
conda env create -f environment.yml
```

2. Activate the environment with `conda activate local-mds`.
3. Add the following lines to ~/.dbt/profiles.yml:

```yaml
data_mart:
  outputs:
   dev:
     type: duckdb
     path: <path-to-data-mart.duckdb>
  target: dev
```

4. Run [src/generate-raw-data.py](src/generate-raw-data.py) to create storage and ingest raw data.
5. Run `dbt run --project-dir data_mart/` to build the data mart.
6. Add the following lines to ~/.metricflow/config.yml:

```yaml
model_path: <path-to-the-metrics-directory>
dwh_schema: main_marts
dwh_dialect: duckdb
dwh_database: <path-to-data-mart.duckdb>
```

and verify connection with `mf health-check`.

## Try metricflow using its CLI

Start with `mf validate-configs` to verify that everything is ok with the setup in [metrics](metrics).
The command helps debug in case it is not and thus should be used before any changes are committed to
the repository.

```bash
mf query --metrics order_revenue_usd --dimensions metric_time__year,order_type --order metric_time__year
```

```bash
mf query --metrics order_revenue_usd --dimensions metric_time__year,site_id__site_region --order metric_time__year
```

```bash
mf query --metrics order_revenue_usd --dimensions metric_time__year,site_id__account_id__account_region --order metric_time__year
```

## Try metricflow Python API inside a streamlit app

```bash
streamlit run src/app.py
```
