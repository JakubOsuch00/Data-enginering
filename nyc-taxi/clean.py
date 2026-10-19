from datetime import datetime
from pathlib import Path

import polars as pl

DATA = "data/yellow_tripdata_2024-01.parquet"

df = pl.read_parquet(DATA)

print(df.shape)
print(df.head())

df = df.with_columns(
    (
        (pl.col("tpep_dropoff_datetime") - pl.col("tpep_pickup_datetime"))
        .dt.total_seconds() / 60
    ).alias("trip_duration_minutes")
)

print(df.select("tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_duration_minutes").head())

czyste = df.filter(
    pl.col("tip_amount") >= 0,
    pl.col("fare_amount") > 0,
    pl.col("total_amount") >= 0,
    pl.col("trip_duration_minutes") >= 1,
    pl.col("trip_duration_minutes") <= 300,
    pl.col("trip_distance") > 0,
    pl.col("trip_distance") <= 100,
    pl.col("tpep_pickup_datetime") >= datetime(2024, 1, 1),
    pl.col("tpep_pickup_datetime") < datetime(2024, 2, 1),
    pl.col("passenger_count").is_null() | (pl.col("passenger_count") <= 6),
)

przed = df.shape[0]
po = czyste.shape[0]
odrzucone = przed - po

print(f"Przed czyszczeniem: {przed:>10,}")
print(f"Po czyszczeniu:     {po:>10,}")
print(f"Odrzucono:          {odrzucone:>10,} ({odrzucone / przed * 100:.2f}%)")

czyste = czyste.with_columns(
    pl.col("tpep_pickup_datetime").dt.hour().alias("pickup_hour"),
    pl.col("tpep_pickup_datetime").dt.weekday().alias("pickup_day_of_week"),
    (pl.col("tpep_pickup_datetime").dt.weekday() >= 6).alias("is_weekend"),
    (pl.col("trip_distance") / (pl.col("trip_duration_minutes") / 60)).alias("avg_speed_mph"),
)

print(czyste.select("tpep_pickup_datetime", "pickup_hour", "pickup_day_of_week", "is_weekend", "avg_speed_mph").head())

Path("data/lakehouse/flat").mkdir(parents=True, exist_ok=True)

czyste.write_parquet("data/lakehouse/flat/trips.parquet", compression="snappy")

czyste.write_parquet("data/lakehouse/partitioned", partition_by="VendorID", compression="snappy")

print("Zapisano wariant A (płaski) i B (partycje)")
