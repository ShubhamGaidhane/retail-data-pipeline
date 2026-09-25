# Databricks notebook source
dbutils.widgets.text("target_schema", "retail_dev")
target_schema = dbutils.widgets.get("target_schema")

if target_schema not in {"retail_dev", "retail_ci"}:
    raise ValueError(f"Unexpected target schema: {target_schema}")

table_name = f"workspace.{target_schema}.order_revenue"
print(f"Writing to: {table_name}")



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


expected = [
    (1001, Decimal("180.00")),
    (1002, Decimal("150.00")),
    (1003, Decimal("0.00")),
]

actual = [
    (row.order_id, row.revenue)
    for row in order_revenue.select("order_id", "revenue")
    .orderBy("order_id")
    .collect()
]

if actual != expected:
    raise ValueError(
        f"Revenue validation failed: expected {expected}, got {actual}"
    )

print("Revenue validation passed for all 3 sample orders.")



order_revenue.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(table_name)


# COMMAND ----------

display(spark.table(table_name).orderBy("order_id"))