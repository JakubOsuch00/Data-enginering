import statistics
import time

import duckdb
import matplotlib.pyplot as plt
import polars as pl

FLAT = "'data/lakehouse/flat/trips.parquet'"
PARTITIONED = "read_parquet('data/lakehouse/partitioned/**/*.parquet', hive_partitioning = true)"
POWTORZENIA = 10
DOSTAWCY = [1, 2, 6]

con = duckdb.connect()


def zapytanie(zrodlo, vendor_id):
    return f"""
        SELECT
            pickup_hour,
            AVG(trip_distance) AS sredni_dystans,
            AVG(tip_amount)    AS sredni_napiwek
        FROM {zrodlo}
        WHERE VendorID = {vendor_id}
        GROUP BY pickup_hour
        ORDER BY pickup_hour
    """


def zmierz(sql):
    con.sql(sql).fetchall()
    czasy = []
    for _ in range(POWTORZENIA):
        start = time.perf_counter()
        con.sql(sql).fetchall()
        czasy.append((time.perf_counter() - start) * 1000)
    return statistics.mean(czasy), statistics.stdev(czasy)


wyniki = []
for vendor_id in DOSTAWCY:
    sredni_a, odch_a = zmierz(zapytanie(FLAT, vendor_id))
    sredni_b, odch_b = zmierz(zapytanie(PARTITIONED, vendor_id))
    wyniki.append({
        "VendorID": vendor_id,
        "A_plaski_ms": round(sredni_a, 1),
        "A_odch_ms": round(odch_a, 1),
        "B_partycje_ms": round(sredni_b, 1),
        "B_odch_ms": round(odch_b, 1),
        "zysk_proc": round((sredni_a - sredni_b) / sredni_a * 100, 1),
    })

tabela = pl.DataFrame(wyniki)
print(tabela)

plan = con.sql("EXPLAIN ANALYZE " + zapytanie(PARTITIONED, 1)).fetchall()[0][1]
print(plan)

x = list(range(len(DOSTAWCY)))
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar([i - 0.2 for i in x], tabela["A_plaski_ms"], width=0.38, yerr=tabela["A_odch_ms"],
       color="#2a78d6", label="A: plik płaski (full scan)")
ax.bar([i + 0.2 for i in x], tabela["B_partycje_ms"], width=0.38, yerr=tabela["B_odch_ms"],
       color="#eb6834", label="B: partycje (partition pruning)")
ax.set_xticks(x, [f"VendorID = {v}" for v in DOSTAWCY])
ax.set_ylabel("Średni czas zapytania [ms]")
ax.set_title(f"Benchmark A/B: średnia z {POWTORZENIA} pomiarów")
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("benchmark.png", dpi=150)
print("Zapisano wykres: benchmark.png")
