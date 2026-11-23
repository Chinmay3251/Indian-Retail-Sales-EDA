# Benchmark methodology
Compare revenue by region, monthly revenue, and top products. Each implementation reads the same 100k CSV on each of five runs; report median elapsed time. DuckDB uses `read_csv_auto` plus SQL; Pandas uses `read_csv` plus vectorized/groupby operations. CSV parsing is included in both timings. Speedup = Pandas median / DuckDB median; >1 means DuckDB faster. Results vary by hardware, versions, disk cache, and system load.

DuckDB could not be installed in the artifact-building environment because package-index network access was unavailable. No timing values are fabricated. Run `python src/benchmark.py` locally after installing requirements to generate `reports/benchmark_results.csv`.
