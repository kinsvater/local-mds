import altair as alt
import streamlit as st
from metricflow import MetricFlowClient

client = MetricFlowClient.from_config()


@st.cache_data
def load_data(granularity: str = 'month'):
    data = client.query(metrics=['order_revenue_usd'],
                        dimensions=['site_id__site_region', f'metric_time__{granularity}'],
                        order=[f'metric_time__{granularity}']).result_df

    data.columns = ['Period', 'Region', 'Revenue']
    return data


st.markdown('# Query data using a semantic layer')

choice = st.radio('Granularity', ('Month', 'Quarter', 'Year'))

df = load_data(granularity=choice.lower())

chart = alt.Chart(df).mark_line().encode(x='Period', y='Revenue', color='Region')
st.altair_chart(chart, use_container_width=True)

st.write(df)
