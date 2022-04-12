## Querymagic
Use querymagic to write Splunk and Kusto queries in your Jupyter notebooks.

It needs following environment variables:

- SPLUNK_TOKEN
- SPLUNK_SEARCH_URL
- KUSTO_CLIENT_ID
- KUSTO_CLIENT_SECRET
- KUSTO_TENANT_ID

The package queries `Insights` database for kusto queries. This detail is hardcoded.