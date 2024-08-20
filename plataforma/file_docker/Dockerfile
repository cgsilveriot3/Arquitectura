FROM ubuntu:20.04

# Configurar variables de entorno y prevenir interacciones durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar actualizaciones y dependencias necesarias
RUN apt-get update && \
    apt-get install -y --fix-missing \
    openjdk-8-jdk \
    wget \
    curl \
    net-tools \
    python3-pip \
    postgresql postgresql-contrib \
    sudo \
    vim \
    locales \
    && apt-get clean

# Configurar locales
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8




# Descargar e instalar Hadoop
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz && \
    tar -xzvf hadoop-3.2.1.tar.gz -C /usr/local/ && \
    ln -s /usr/local/hadoop-3.2.1 /usr/local/hadoop

# Configurar variables de entorno para Hadoop
ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Configurar core-site.xml
RUN echo '<configuration>' > $HADOOP_CONF_DIR/core-site.xml && \
    echo '  <property>' >> $HADOOP_CONF_DIR/core-site.xml && \
    echo '    <name>fs.defaultFS</name>' >> $HADOOP_CONF_DIR/core-site.xml && \
    echo '    <value>hdfs://localhost:9000</value>' >> $HADOOP_CONF_DIR/core-site.xml && \
    echo '  </property>' >> $HADOOP_CONF_DIR/core-site.xml && \
    echo '</configuration>' >> $HADOOP_CONF_DIR/core-site.xml

# Configurar hdfs-site.xml con persistencia
RUN echo '<configuration>' > $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '  <property>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '    <name>dfs.replication</name>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '    <value>1</value>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '  </property>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '  <property>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '    <name>dfs.namenode.name.dir</name>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '    <value>/hadoop/dfs/name</value>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '  </property>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '  <property>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '    <name>dfs.datanode.data.dir</name>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '    <value>/hadoop/dfs/data</value>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '  </property>' >> $HADOOP_CONF_DIR/hdfs-site.xml && \
    echo '</configuration>' >> $HADOOP_CONF_DIR/hdfs-site.xml

# Crear directorios de datos para HDFS
RUN mkdir -p /hadoop/dfs/name && \
    mkdir -p /hadoop/dfs/data && \
    $HADOOP_HOME/bin/hdfs namenode -format

# Iniciar y configurar PostgreSQL
RUN service postgresql start && \
    sudo -u postgres psql -c "CREATE USER airflow WITH PASSWORD 'airflow';" && \
    sudo -u postgres psql -c "CREATE DATABASE airflow;" && \
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;"

# Instalar Airflow
RUN pip3 install apache-airflow==2.6.2

# Configurar Airflow
ENV AIRFLOW_HOME=/usr/local/airflow
RUN mkdir -p $AIRFLOW_HOME/dags
COPY airflow.cfg $AIRFLOW_HOME/airflow.cfg

# Configuración adicional de Airflow para usar PostgreSQL
RUN sed -i "s|sqlite:////usr/local/airflow/airflow.db|postgresql+psycopg2://airflow:airflow@localhost:5432/airflow|g" $AIRFLOW_HOME/airflow.cfg

# Iniciar la base de datos de Airflow
RUN airflow db init

# Crear puntos de montaje para persistencia
VOLUME /hadoop/dfs/name
VOLUME /hadoop/dfs/data
VOLUME /usr/local/airflow/dags

# Comando de inicio del contenedor
CMD ["sh", "-c", "service postgresql start && start-dfs.sh && airflow db upgrade && airflow webserver -p 8080 & airflow scheduler"]
