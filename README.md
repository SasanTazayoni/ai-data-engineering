# AI Data Engineering - Databricks and PySpark Research

![Python](./tech/python.png) ![Apache Spark](./tech/apachespark.png) ![Databricks](./tech/databricks.png) ![VSCode](./tech/vscode.png)

---

## What can be considered "Big Data"?

**Big Data** refers to datasets that are too large, fast-moving, or complex to be processed by traditional database tools. It is commonly defined by the **three V's**:

- **Volume** — The sheer amount of data (terabytes, petabytes, or beyond). Think logs from millions of users, sensor readings, transaction records at scale.
- **Velocity** — The speed at which data is generated and needs to be processed. Social media feeds, financial trades, and IoT devices produce data in real time.
- **Variety** — The range of data types and sources: structured (tables), semi-structured (JSON, XML), and unstructured (images, video, text).

Some definitions extend this to **five V's**, adding:

- **Veracity** — The trustworthiness and quality of the data (noise, inconsistencies, missing values).
- **Value** — Whether the data actually yields useful insight after processing.

### In practice

There is no fixed size threshold — data is "big" when it outgrows the tools you're currently using. A dataset that breaks a single Postgres instance or takes days to query in Excel is effectively Big Data for that context. The real question is whether your infrastructure can handle it efficiently.

---

## What is OLTP?

**OLTP (Online Transaction Processing)** is a class of systems designed to handle large numbers of short, real-time transactions — things like inserting a new order, updating a user's balance, or logging a login event.

Key characteristics:
- Optimised for **writes and reads of individual rows**
- High volume of **concurrent transactions**
- Data is **current and operational** (not historical)
- Examples: banking systems, e-commerce checkouts, booking platforms

OLTP databases are typically relational (PostgreSQL, MySQL) and are the backbone of day-to-day application data.

### What is ACID?

ACID is a set of properties that guarantee database transactions are processed reliably — critical in OLTP systems where data integrity matters.

- **Atomicity** — A transaction is all-or-nothing. If any part fails, the whole thing is rolled back. You can't debit an account without crediting another.
- **Consistency** — A transaction brings the database from one valid state to another. Rules and constraints are never violated.
- **Isolation** — Concurrent transactions don't interfere with each other. Each transaction behaves as if it's running alone.
- **Durability** — Once a transaction is committed, it stays committed — even if the system crashes immediately after.

---

## What is OLAP?

**OLAP (Online Analytical Processing)** is a class of systems designed for querying and analysing large volumes of historical data rather than processing individual transactions.

Key characteristics:
- Optimised for **complex queries across many rows** (aggregations, groupings, trends)
- Data is typically **read-heavy** — writes are batch loads, not real-time inserts
- Queries span **large time ranges** and multiple dimensions
- Examples: sales reporting, business intelligence dashboards, data science workloads

Where OLTP asks *"what is the current state?"*, OLAP asks *"what patterns exist across all historical data?"*

| | OLTP | OLAP |
|---|---|---|
| Purpose | Record transactions | Analyse data |
| Query type | Simple, row-level | Complex, aggregate |
| Data volume | Current | Historical, large |
| Speed optimised for | Writes | Reads |
| Example | PostgreSQL app DB | Data warehouse |

---

## What are Data Warehouses? How do they work?

A **Data Warehouse** is a centralised repository designed to store large volumes of structured, historical data from multiple sources — built specifically for analysis and reporting, not for running an application.

Think of it as the single source of truth for business intelligence. Instead of querying your live production database (which would slow it down), you copy and transform data into the warehouse where analysts can query freely.

### How they work

Data flows into a warehouse through a process called **ETL (Extract, Transform, Load)**:

1. **Extract** — Pull raw data from source systems (databases, APIs, spreadsheets, logs)
2. **Transform** — Clean, standardise, and reshape the data into a consistent schema
3. **Load** — Write the transformed data into the warehouse

Once loaded, data is organised into a schema optimised for querying — typically a **star schema** or **snowflake schema**, where a central fact table (e.g. orders) links out to dimension tables (e.g. customers, products, dates).

### Key characteristics

- Stores **structured data only**
- Data is **read-optimised** — columnar storage means aggregations across millions of rows are fast
- Data is **immutable** — historical records aren't updated, new records are appended
- Queries run on **cold, batch-loaded data**, not live transactions

### Examples

| Tool | Type |
|---|---|
| Snowflake | Cloud data warehouse |
| Google BigQuery | Cloud data warehouse |
| Amazon Redshift | Cloud data warehouse |
| Databricks SQL | Lakehouse (warehouse-like) |

---

## What are Data Lakes? How do they work?

A **Data Lake** is a centralised storage system that holds vast amounts of raw data in its native format until it's needed — structured, semi-structured, and unstructured all in one place.

Where a data warehouse demands clean, structured data upfront, a data lake takes the opposite approach: **store everything now, figure out the schema later**. This is sometimes called **ELT (Extract, Load, Transform)** — you load first, transform on the way out.

### How they work

1. **Ingest** — Raw data is dumped in from any source: databases, logs, images, video, JSON, CSV, Parquet, etc.
2. **Store** — Data sits in cheap, scalable object storage (e.g. AWS S3, Azure Data Lake Storage) with no enforced schema
3. **Process** — When needed, a compute engine (like Spark) reads the data and applies a schema at query time — known as **schema-on-read**
4. **Serve** — Processed results are passed to BI tools, ML models, or downstream pipelines

### Key characteristics

- Stores **any data type** — structured, semi-structured, unstructured
- **Schema-on-read** — no transformation required before storage
- Extremely **cheap at scale** (object storage is far cheaper than warehouse storage)
- Requires more work to query — raw data needs processing before it's useful

### Data Lake vs Data Warehouse

| | Data Lake | Data Warehouse |
|---|---|---|
| Data type | Any (raw) | Structured only |
| Schema | On read | On write |
| Cost | Low | Higher |
| Query speed | Slower (needs processing) | Fast |
| Best for | ML, data science, raw storage | BI, reporting, dashboards |

### Examples

- **AWS S3** + Athena
- **Azure Data Lake Storage**
- **Google Cloud Storage**
- **Hadoop HDFS** (older, on-premise)

---

## What are Data Lakehouses?

A **Data Lakehouse** is a modern architecture that combines the best of both worlds — the low-cost, flexible storage of a data lake with the structure, reliability, and query performance of a data warehouse.

It emerged because organisations kept running into the same problem: data lakes became messy and unreliable over time ("data swamps"), but data warehouses were too rigid and expensive to store everything. The lakehouse solves both.

### How it works

A lakehouse sits on top of cheap object storage (like a data lake) but adds a **metadata and transaction layer** on top that enforces:

- **Schema** — data has structure and types
- **ACID transactions** — safe concurrent reads and writes
- **Indexing and caching** — fast query performance like a warehouse

This means you can run BI queries, SQL analytics, and ML workloads all against the same data store — no need to copy data between systems.

### Key characteristics

- Built on **open file formats** (Parquet, ORC) — no vendor lock-in
- Supports **both SQL analytics and machine learning** workloads
- **ACID compliance** on top of a data lake
- **Single source of truth** — no duplication between lake and warehouse

### Lakehouse vs the others

| | Data Lake | Data Warehouse | Data Lakehouse |
|---|---|---|---|
| Storage cost | Low | High | Low |
| Data types | Any | Structured | Any |
| ACID support | No | Yes | Yes |
| ML workloads | Yes | Limited | Yes |
| Query performance | Slow | Fast | Fast |

### Examples

- **Databricks Lakehouse** (built on Delta Lake)
- **Apache Iceberg** + cloud storage
- **Apache Hudi**

---

## What are Delta Lakes?

**Delta Lake** is an open-source storage layer that brings ACID transactions, versioning, and reliability to data lakes. It was created by Databricks and is the foundation of the Databricks Lakehouse platform.

In plain terms: Delta Lake is what turns a messy data lake into a trustworthy, queryable lakehouse. It doesn't replace your storage — it sits on top of it (S3, ADLS, GCS) and adds a layer of control.

### How it works

Delta Lake stores data as **Parquet files** but adds a **transaction log** (the `_delta_log` folder) alongside them. Every change to the table — inserts, updates, deletes — is recorded as a JSON entry in that log.

This gives you:

- **ACID transactions** — concurrent reads and writes are safe
- **Time travel** — query any previous version of a table using `VERSION AS OF` or `TIMESTAMP AS OF`
- **Schema enforcement** — bad data is rejected at write time
- **Schema evolution** — controlled changes to table structure over time
- **Upserts (MERGE)** — update existing rows or insert new ones in a single operation

### Why it matters

Traditional data lakes had no concept of updates or deletes — once data was written, it was difficult to change. Delta Lake fixes this, making it possible to:

- Correct bad data after the fact
- Handle late-arriving records
- Comply with GDPR (right to be forgotten — you can delete specific rows)
- Recover from accidental writes by rolling back to a previous version

### Delta Lake vs a plain data lake

| | Plain Data Lake | Delta Lake |
|---|---|---|
| ACID transactions | No | Yes |
| Update/delete rows | No | Yes |
| Time travel | No | Yes |
| Schema enforcement | No | Yes |
| Audit history | No | Yes (transaction log) |
