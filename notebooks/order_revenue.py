# Databricks notebook source
spark.sql("""
    SELECT
        current_catalog() AS catalog,
        current_schema() AS schema
""").show(truncate=False)

spark.sql("SHOW CATALOGS").show(truncate=False)

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.retail_dev")

# COMMAND ----------

from decimal import Decimal
from pyspark.sql import functions as F

orders = spark.createDataFrame(
    [
        (1001, 2, Decimal("100.00"), Decimal("20.00")),
        (1002, 3, Decimal("50.00"), Decimal("0.00")),
        (1003, 1, Decimal("80.00"), Decimal("80.00")),
    ],
    schema="""
        order_id INT,
        quantity INT,
        unit_price DECIMAL(12,2),
        discount DECIMAL(12,2)
    """,
)

order_revenue = orders.withColumn(
    "revenue",
    (
        F.col("quantity") * F.col("unit_price") - F.col("discount")
    ).cast("decimal(14,2)"),
)

display(order_revenue)

# COMMAND ----------

order_revenue.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.retail_dev.order_revenue")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.retail_dev.order_revenue
# MAGIC ORDER BY order_id;