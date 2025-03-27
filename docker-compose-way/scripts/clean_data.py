from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Data Cleaning Job") \
    .getOrCreate()

# Load data
df = spark.read.csv("hdfs://namenode:9000/raw_data.csv", header=True, inferSchema=True)

# Data cleaning steps
df_cleaned = df.dropDuplicates()  # Remove duplicates
df_cleaned = df_cleaned.na.drop()  # Drop rows with null values
df_cleaned = df_cleaned.withColumnRenamed("old_col_name", "new_col_name")  # Rename column

# Save cleaned data
df_cleaned.write.csv("hdfs://namenode:9000/cleaned_data.csv", header=True, mode="overwrite")

print("Data cleaning completed!")

# Stop Spark session
spark.stop()
git