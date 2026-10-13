import duckdb

DATA = "data/yellow_tripdata_2024-01.parquet"

wynik = duckdb.sql(f"""
    SELECT
        -- Wolumen
        count(*) as liczba_rekordow,

        -- Braki danych (a)
        count(*) - count(passenger_count) as null_passenger_count,
        count(*) - count(RatecodeID)      as null_ratecodeid,
        count(*) - count(store_and_fwd_flag)   as null_store_and_fwd_flag,
        count(*) - count(congestion_surcharge) as null_congestion_surcharge,
        count(*) - count(Airport_fee)          as null_airport_fee,

        

        -- Zakresy
        min(trip_distance) as shortest_trip,
        max(trip_distance) as longest_trip,
        min(fare_amount)   as min_fare_amount,
        max(fare_amount)   as max_fare_amount,
        min(tpep_pickup_datetime) as najwczesniejszy_odbior,   
        max(tpep_pickup_datetime) as najpozniejszy_odbior,   
        
        -- Anomalie
        count(*) FILTER(WHERE trip_distance = 0)   as dystans_zero,
        count(*) FILTER(WHERE trip_distance < 0)   as ujemny_dystans,
        count(*) FILTER(WHERE trip_distance > 100) as dystans_za_duzy,
        count(*) FILTER(WHERE total_amount = 0)    as total_amount_zero,
                count(*) FILTER(WHERE tpep_pickup_datetime < '2024-01-01'
                           OR tpep_pickup_datetime >= '2024-02-01') as poza_styczniem,
        count(*) FILTER(WHERE tpep_dropoff_datetime < tpep_pickup_datetime) as koniec_przed_startem

        
    FROM '{DATA}'
""")

wiersz = wynik.fetchone()

for nazwa, wartosc in zip(wynik.columns, wiersz):
    print(f"{nazwa:35} {wartosc}")
