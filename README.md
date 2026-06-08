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

---

## What is Apache Spark?

**Apache Spark** is an open-source, distributed computing engine built for processing large-scale data fast. It can run batch jobs, streaming, SQL queries, machine learning, and graph processing — all within a single unified framework.

### What problem did it solve?

Before Spark, the dominant tool for big data processing was **Hadoop MapReduce**. It worked, but it had a fundamental flaw: **it wrote intermediate results to disk after every step**.

For a multi-stage job (filter → join → aggregate → output), that meant constant disk I/O between each stage — extremely slow for iterative workloads like machine learning, where you need to pass over the same data dozens of times.

Spark solved this by keeping data **in memory (RAM)** between stages. Instead of reading and writing to disk at every step, Spark builds up a pipeline of transformations and executes them in one pass through the data. The result: Spark is typically **10–100x faster than Hadoop MapReduce** for most workloads.

### How does it work? The architecture

Spark runs on a **master/worker architecture** with three core components:

#### Driver
The **Driver** is the brain of a Spark job. It's the process that runs your code, builds the execution plan, and coordinates everything. When you write a Spark script, the Driver:
1. Parses your transformations into a **DAG (Directed Acyclic Graph)** — a logical map of all steps
2. Optimises the DAG using the **Catalyst query optimiser**
3. Splits the work into **Tasks** and sends them to workers

#### Cluster Manager
The **Cluster Manager** allocates resources across the cluster. Spark supports several: YARN, Kubernetes, Mesos, or Spark's own standalone manager. Databricks manages this for you automatically.

#### Executors (Workers)
**Executors** are the processes running on worker nodes that actually do the computation. Each executor:
- Receives tasks from the Driver
- Processes its **partition** of the data in memory
- Returns results back to the Driver

#### RDDs, DataFrames, and partitions
Spark splits data into **partitions** — chunks distributed across the cluster. Each executor works on its own partition in parallel.

Data can be represented as:
- **RDD (Resilient Distributed Dataset)** — the low-level building block, fault-tolerant and distributed
- **DataFrame** — higher-level, tabular (like a SQL table), optimised by Catalyst — this is what you use day-to-day in PySpark

#### Lazy evaluation
Spark doesn't execute anything when you define a transformation. It builds up a plan and only runs it when you call an **action** (like `.show()`, `.count()`, or `.write()`). This allows Spark to optimise the full pipeline before touching any data.

### Why did it become popular?

- **Speed** — In-memory processing made it dramatically faster than Hadoop for most workloads
- **Unified engine** — Batch, streaming, SQL, ML, and graph in one framework — no need to stitch together separate tools
- **Easy APIs** — Python (PySpark), Scala, Java, R — accessible to data scientists, not just engineers
- **Fault tolerance** — If a worker fails, Spark automatically recomputes lost partitions from the lineage graph
- **Open source** — Free to use, massive community, runs anywhere (on-prem, cloud, Databricks)
- **Databricks adoption** — The creators of Spark founded Databricks, which made Spark the default engine for cloud data work

---

## What is PySpark? Why do we tend to use that?

**PySpark** is the Python API for Apache Spark. It lets you write Spark jobs in Python rather than Spark's native language, Scala.

Under the hood, PySpark doesn't run Python on the cluster — it translates your Python code into JVM (Java Virtual Machine) instructions that Spark's engine executes. You get the full power of distributed Spark processing with the familiarity of Python syntax.

### Why do we tend to use PySpark?

- **Python is the data language** — The data science and data engineering ecosystem lives in Python: pandas, NumPy, scikit-learn, TensorFlow, Hugging Face. PySpark fits naturally into that world
- **Lower barrier to entry** — Scala (Spark's native language) has a steeper learning curve. Most data professionals already know Python
- **Same performance** — For DataFrame operations, PySpark performance is essentially identical to Scala Spark because both compile down to the same execution plan via Catalyst
- **Notebooks** — PySpark works seamlessly in Jupyter and Databricks notebooks, which is how most data work is done interactively
- **Pandas integration** — PySpark DataFrames can be converted to pandas with `.toPandas()`, and since Spark 3.2, you can use the **pandas API on Spark** (`pyspark.pandas`) to write familiar pandas code that runs distributed

### PySpark vs plain pandas

| | pandas | PySpark |
|---|---|---|
| Runs on | Single machine | Distributed cluster |
| Data size | Up to ~GBs | TBs to PBs |
| Execution | Eager (immediate) | Lazy (planned then executed) |
| Syntax | Familiar, simple | Similar, slightly more verbose |
| Speed at scale | Slow / crashes | Fast |

Use pandas for small data and local exploration. Use PySpark when the data outgrows a single machine.

---

## What is Databricks?

**Databricks** is a cloud-based data platform built on top of Apache Spark. It was founded in 2013 by the original creators of Spark and provides a managed environment for running Spark workloads — no cluster setup, no infrastructure management, just notebooks and data.

It sits at the centre of the modern data stack, combining data engineering, data science, SQL analytics, and ML in one unified platform — the **Databricks Lakehouse**.

### What problems did it solve?

Running Spark yourself was painful. Before Databricks, teams had to:

- **Provision and manage clusters manually** — configuring Hadoop, tuning memory, handling node failures
- **Handle infrastructure on their own** — setting up cloud VMs, networking, storage permissions
- **Stitch together separate tools** — one tool for ETL, another for SQL, another for ML
- **Deal with Hadoop complexity** — YARN, HDFS, and a sprawling ecosystem of brittle integrations

Databricks eliminated all of this. It made Spark accessible to data engineers and data scientists without needing a dedicated infrastructure team.

### How does it work?

Databricks runs on your cloud provider (AWS, Azure, or GCP) inside your own account. When you spin up a cluster, Databricks provisions VMs on your behalf, installs Spark, and manages the lifecycle automatically.

The core components:

- **Clusters** — Managed Spark clusters that auto-scale and auto-terminate. You choose the size and Databricks handles the rest
- **Notebooks** — Interactive notebooks (Python, SQL, Scala, R) attached to a live cluster. Code runs on the distributed cluster, results appear inline
- **DBFS (Databricks File System)** — An abstraction over cloud storage (S3, ADLS) that makes it feel like a local filesystem
- **Delta Lake** — Built-in as the default storage format, giving every table ACID compliance and time travel out of the box
- **Unity Catalog** — Centralised governance layer for managing access, lineage, and discovery across all data assets
- **Databricks Runtime** — An optimised version of Spark with performance improvements, pre-installed libraries, and GPU support

### Why has it become popular?

- **Managed Spark** — All the power of Spark, none of the infrastructure headache
- **Collaborative notebooks** — Multiple people can work in the same notebook simultaneously, like Google Docs for data
- **One platform for everything** — ETL, SQL analytics, ML model training, and serving all in one place
- **Delta Lake by default** — Reliable, versioned, ACID-compliant storage without extra setup
- **Auto-scaling clusters** — Clusters grow and shrink with the workload, keeping costs down
- **Enterprise adoption** — Used by thousands of companies (Microsoft, Comcast, Shell) — strong community and support
- **Tight cloud integration** — Native integrations with AWS, Azure, and GCP services

### Key features

| Feature | Description |
|---|---|
| **Managed Clusters** | Spin up Spark clusters in seconds, auto-scale, auto-terminate |
| **Notebooks** | Interactive, collaborative, multi-language (Python, SQL, Scala, R) |
| **Delta Lake** | ACID transactions, time travel, schema enforcement on all tables |
| **Unity Catalog** | Data governance, access control, and lineage across the platform |
| **Databricks SQL** | Run SQL queries on lakehouse data with a warehouse-like interface |
| **MLflow** | Built-in experiment tracking, model registry, and deployment |
| **Workflows** | Orchestrate multi-step data pipelines with scheduling and dependencies |
| **Auto Loader** | Incrementally ingest new files from cloud storage as they arrive |
