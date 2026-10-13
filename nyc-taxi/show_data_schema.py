import duckdb

DATA = "data/yellow_tripdata_2024-01.parquet"


duckdb.sql(f"DESCRIBE SELECT * FROM '{DATA}'").show()


duckdb.sql(f"SELECT * FROM '{DATA}' LIMIT 5").show()
