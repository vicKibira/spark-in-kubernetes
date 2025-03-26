# Builder step: Download and configure Spark environment
FROM openjdk:11.0.11-jre-slim-buster AS builder

# Install dependencies for PySpark
RUN apt-get update -y && apt-get install -y \
    curl vim wget software-properties-common ssh net-tools ca-certificates \
    python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python environment
ENV PYTHON="/usr/bin/python3"

# Fix the value of PYTHONHASHSEED
ENV SPARK_VERSION=3.4.0 \
    HADOOP_VERSION=3 \
    SPARK_HOME=/opt/spark \
    PYTHONHASHSEED=1

# Download and extract Apache Spark
RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
    && mkdir -p /opt/spark \
    && tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
    && rm -f apache-spark.tgz

# Apache Spark Environment
FROM builder AS apache-spark

WORKDIR /opt/spark

# Set environment variables for Spark
ENV SPARK_MASTER_PORT=7077 \
    SPARK_MASTER_WEBUI_PORT=8080 \
    SPARK_LOG_DIR=/opt/spark/logs \
    SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
    SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
    SPARK_WORKER_WEBUI_PORT=8080 \
    SPARK_WORKER_PORT=7000 \
    SPARK_MASTER="spark://spark-master:7077" \
    SPARK_WORKLOAD="master"

# Expose necessary ports
EXPOSE 8080 7077 6066

# Create log directory and redirect logs to stdout
RUN mkdir -p $SPARK_LOG_DIR \
    && touch $SPARK_MASTER_LOG \
    && touch $SPARK_WORKER_LOG \
    && ln -sf /dev/stdout $SPARK_MASTER_LOG \
    && ln -sf /dev/stdout $SPARK_WORKER_LOG

# Copy startup script
COPY start-spark.sh /
RUN chmod +x /start-spark.sh

CMD ["/bin/bash", "/start-spark.sh"]
