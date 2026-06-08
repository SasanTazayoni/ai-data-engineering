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
