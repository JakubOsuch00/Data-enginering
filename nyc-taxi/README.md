# NYC Taxi Lakehouse

Potok danych na zbiorze NYC Yellow Taxi (styczeń 2024, ~3 mln kursów):
profilowanie jakości danych, czyszczenie, partycjonowany Lakehouse w Parquet i model ML.

## Technologie
Python, DuckDB, Polars, Parquet

## Dane
Pobierz plik `yellow_tripdata_2024-01.parquet` ze strony
[NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
i umieść go w folderze `data/`.

## Uruchomienie
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python show_data_schema.py


