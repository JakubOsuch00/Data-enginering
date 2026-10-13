import duckdb

DATA = "data/yellow_tripdata_2024-01.parquet"

duckdb.sql(f"""
    SELECT
        count(*) FILTER(WHERE passenger_count IS NULL
                          AND RatecodeID IS NULL AND store_and_fwd_flag IS NULL 
                          AND congestion_surcharge IS NULL AND Airport_fee IS NULL) as null_w_obu
    FROM '{DATA}'
""").show()

duckdb.sql(f"""
    SELECT
        VendorID,
        count(*) as liczba
    FROM '{DATA}'
    WHERE passenger_count IS NULL
    GROUP BY VendorID
    ORDER BY liczba DESC
""").show()

duckdb.sql(f"""
    SELECT
        payment_type,
        count(*) as liczba
    FROM '{DATA}'
    WHERE fare_amount < 0
    GROUP BY payment_type
    ORDER BY liczba DESC
""").show()