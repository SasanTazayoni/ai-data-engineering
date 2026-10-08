# Interview Questions & Answers

Interview-ready answers for the Big Data, lakehouse, and Databricks/PySpark topics in this repo. Kept punchy and memorable; the full detail behind each lives in the [README.md](README.md) and [pyspark-intro/databricks-and-pyspark-research.md](pyspark-intro/databricks-and-pyspark-research.md).

Each answer follows the same shape: a one-line framing summary, supporting points, and a **Remember:** hook to lock it in.

## Contents

**Big Data & Lakehouse**

- [What is a data lake, and what are its advantages vs a data warehouse?](#what-is-a-data-lake-and-what-are-its-advantages-vs-a-data-warehouse)
- [What is a data lakehouse?](#what-is-a-data-lakehouse)
- [What is Parquet, and why is it used?](#what-is-parquet-and-why-is-it-used)
- [What is Delta Lake?](#what-is-delta-lake)
- [What is the medallion architecture? (and what is data ingestion?)](#what-is-the-medallion-architecture-and-what-is-data-ingestion)
- [What is Apache Spark, and what problem does it solve?](#what-is-apache-spark-and-what-problem-does-it-solve)
- [What is Databricks, and why is it so popular among data professionals?](#what-is-databricks-and-why-is-it-so-popular-among-data-professionals)

---

## Big Data & Lakehouse

### What is a data lake, and what are its advantages vs a data warehouse?

**A data lake stores raw data of any type cheaply; a data warehouse stores structured, processed data optimised for fast, reliable querying. The modern lakehouse combines both.**

**Data lake** — a centralised repository storing data in its raw, native format (structured, semi-structured, and unstructured), typically on cheap object storage. _Examples: AWS S3_

- Stores anything regardless of format
- Extremely cheap storage
- Schema-on-read: you decide the structure when you query, not when you store — flexible
- Good for machine learning and exploration
- Downside: without governance it becomes a "data swamp" — hard to find or trust anything

**Data warehouse** — stores structured, processed data optimised for querying and reporting, with the schema defined upfront (schema-on-write) and data transformed before loading.

- Fast, reliable queries
- Enforced schema means higher data quality
- Purpose-built for BI and reporting
- Downside: rigid schema makes changes expensive, it typically only handles structured data, and storage costs more

> **Remember:** lake = cheap, raw, any format, schema-on-read (flexible, but risks a swamp); warehouse = structured, governed, fast queries (reliable, but rigid and pricier). The modern answer is the lakehouse, which puts warehouse-quality governance on top of cheap lake storage.

_Full detail: [README — Data Lakes](README.md#what-are-data-lakes-how-do-they-work) and [Data Warehouses](README.md#what-are-data-warehouses-how-do-they-work)._

### What is a data lakehouse?

**A modern architecture that combines the best of a data lake and a data warehouse in one system — cheap open storage with warehouse-quality reliability and governance.**

- Coined by Databricks, now widely adopted as the dominant enterprise data architecture
- The problem it solves: companies used to need both a data lake (for raw storage and ML) and a data warehouse (for reporting), copying data between them — creating cost, inconsistency, and two systems to maintain
- The lakehouse takes cheap lake storage (open formats like Parquet on S3) and adds warehouse-quality reliability: ACID transactions, schema enforcement, time travel, and unified governance
- One copy of the data instead of two — scientists and analysts read the same data, with no synchronisation lag or inconsistency
- Open formats mean no vendor lock-in — the files are yours, readable by any compatible tool
- A transaction layer is what enables the reliability (see the Delta Lake entry), and the medallion architecture organises the data within it, Bronze → Silver → Gold (see its own entry)
- Delta Lake, Apache Iceberg, and Apache Hudi are competing implementations of that transaction layer — the pattern is the standard regardless of which you use

> **Remember:** the lakehouse = cheap lake storage + warehouse reliability, on one copy of the data. It solves the "two separate systems" problem. Delta Lake makes it work under the hood, and the medallion pattern organises the data inside it.

_Full detail: [README — Data Lakehouses](README.md#what-are-data-lakehouses)._

### What is Parquet, and why is it used?

**Parquet is an open, columnar file format optimised for analytics — it's the underlying storage format for most lakehouses, and the foundation Delta Lake builds on.**

- **Columnar storage:** stores data by column rather than by row. Analytical queries usually read a few columns across many rows, so reading just those columns (instead of every full row) is far faster and touches far less data
- **Efficient compression:** because a column holds values of the same type, Parquet compresses it much better than row formats — less storage and less I/O
- **Open and language-agnostic:** readable by Spark, pandas, DuckDB, and most data tools — no vendor lock-in
- **Metadata built in:** stores the schema and per-column statistics (like min/max) with the data, so query engines can skip whole chunks that can't match a filter ("predicate pushdown")
- Contrast with row formats like CSV, which are better for writing or reading whole records one at a time, but slow for analytics

> **Remember:** Parquet = open columnar format built for analytics. Columnar layout + compression + metadata means you read less data and query faster. Delta Lake is essentially Parquet files plus a transaction log.

_Full detail: [research doc — Delta Lake vs raw Parquet on S3](pyspark-intro/databricks-and-pyspark-research.md#delta-lake-vs-raw-parquet-on-s3)._

### What is Delta Lake?

**An open-source storage layer that sits on top of object storage (like S3 or ADLS) and adds database-quality reliability to a data lake — most importantly ACID transactions, which raw object storage can't provide.**

- Adds ACID transactions to a data lake — something standard object storage cannot do on its own
- Uses a transaction log (the "delta log") that records every change made to the data
- **Time travel:** query the state of the data at any previous point using `VERSION AS OF` or `TIMESTAMP AS OF`
- **Schema enforcement:** bad data can't corrupt the table
- **MERGE operations:** upserts that update existing rows and insert new ones in a single operation
- Built on Parquet files (see the Parquet entry), so the data stays in an open format

> **Remember:** Delta Lake is what turns a data lake into a lakehouse — it adds ACID, time travel, schema enforcement, and MERGE on top of cheap object storage. It's Parquet + a transaction log. Apache Iceberg and Apache Hudi do the same job from other vendors, so the pattern matters more than the specific implementation.

_Full detail: [README — Delta Lakes](README.md#what-are-delta-lakes)._

### What is the medallion architecture? (and what is data ingestion?)

**A data design pattern that organises data into three progressive quality layers — Bronze, Silver, Gold — each refining the data further, so it moves from raw and messy to clean and business-ready while always staying traceable to its source.**

First, **data ingestion:** the step of bringing data into your system from its original sources — APIs, databases, files, or streaming systems like Kafka. It's the entry point of any pipeline: getting the raw data in before anything is done to it. In the medallion pattern, ingestion is exactly what lands data in the Bronze layer.

The three layers:

- **Bronze:** raw ingested data, stored exactly as it arrived with no changes. Preserves the original source for auditing, reprocessing, and full lineage
- **Silver:** cleaned and validated data: duplicates removed, nulls handled, types corrected, records conformed to a consistent structure ready for analysis
- **Gold:** fully processed, aggregated, business-ready data used for reporting, dashboards, and machine learning
- Each layer builds on the previous one, and everything stays traceable back to the raw source — so you can always audit how a number in a Gold dashboard was derived

> **Remember:** Bronze = raw (as-ingested), Silver = cleaned, Gold = business-ready. Sometimes called "multi-hop" architecture. Databricks coined the term, but it's a logical pattern you can implement on any lakehouse (Snowflake, Fabric, BigQuery) — each layer is a set of Delta tables with the same ACID guarantees.

### What is Apache Spark, and what problem does it solve?

**An open-source distributed computing engine for processing large volumes of data fast — the engine underneath Databricks. Its key innovation was keeping data in memory rather than writing to disk between steps.**

- **The problem it solves:** before Spark, Hadoop MapReduce wrote intermediate results to disk between every single step — and disk I/O is extremely slow. A ten-step pipeline meant ten disk reads and ten disk writes
- **Spark's solution:** keep intermediate results in RAM between steps (RAM is roughly 100× faster than disk for sequential reads). A ten-step pipeline reads once, processes all ten steps in memory, and writes once — benchmarks showed 10–100× speedups (real-world gains are often more modest, and Spark spills to disk when data doesn't fit in memory)
- **Master-worker architecture:** the Driver builds an execution plan (a DAG — Directed Acyclic Graph) and coordinates the work; Executors across many machines process chunks of data in parallel
- **Lazy evaluation:** transformations like `filter`, `select`, and `groupBy` don't run immediately — they build up a plan. Only an action like `show()` or `write()` triggers execution, which lets the Catalyst optimizer find the most efficient path
- **Fault tolerance via lineage:** Spark remembers the transformations that produced each partition, so if a node fails it recomputes just that partition rather than restarting the whole job
- **PySpark:** the Python interface — the dominant one for data engineers. The same code that processes 1GB in a notebook runs on 1TB in production with no changes

> **Remember:** Spark solved MapReduce's disk-I/O bottleneck by working in memory. It's distributed (Driver + Executors), lazy (builds a plan, optimises, then runs on an action), and fault-tolerant (recomputes lost partitions from lineage). PySpark is how data engineers use it.

_Full detail: [README — Apache Spark](README.md#what-is-apache-spark)._

### What is Databricks, and why is it so popular among data professionals?

**Databricks is a unified data analytics platform built on Apache Spark, delivered as a managed cloud service — its popularity comes from putting data engineering, data science, ML, and analytics in one place instead of stitching separate tools together.**

**What it is:**

- A unified analytics platform built on Apache Spark, by the team that originally created Spark
- A managed cloud service on AWS, Azure, and GCP — nothing to install, accessed through a browser (SaaS/PaaS: Databricks runs the infrastructure, you bring your code and data)
- Delta Lake is the native storage format, which is what makes it a lakehouse rather than just a data lake
- Core components: Clusters (compute), Notebooks (development), Delta Lake (storage), MLflow (machine learning), Unity Catalog (governance), Workflows (orchestration), and SQL Warehouse (analyst queries)

**Why it's so popular:**

- Unifies everything in one workspace — engineers build pipelines, scientists build models, analysts query, all on the same underlying data
- Built on Spark, so it processes data at massive scale (petabytes, in parallel) without you managing infrastructure
- Native Delta Lake brings ACID transactions, time travel, and schema enforcement to cheap object storage
- Collaborative notebooks support Python, SQL, Scala, and R in the same place
- Auto-scaling clusters provision and terminate compute automatically — no managing servers or over-provisioning
- Built-in MLflow, plus Unity Catalog for centralised governance (access control, lineage, auditing)
- Open formats (Parquet, Delta) mean no vendor lock-in at the data layer, even though the platform itself is managed
- Strong enterprise adoption makes it a common line item on data-engineering job specs — knowing it is directly employable

> **Remember:** Databricks = a managed, Spark-powered lakehouse platform that unifies engineering, science, ML, and analytics in one place. Its edge is the combination — massive-scale compute, native Delta Lake reliability, and collaboration across roles on one copy of the data, with open formats so you're not locked in.

_Full detail: [README — Databricks](README.md#what-is-databricks)._
