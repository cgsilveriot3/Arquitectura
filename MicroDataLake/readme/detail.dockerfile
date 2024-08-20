

[ec2-user@ip-172-31-85-158 ~]$ }
-bash: syntax error near unexpected token `}'


[ec2-user@ip-172-31-85-158 ~]$ start-worker.sh spark://100.26.186.172:7077
starting org.apache.spark.deploy.worker.Worker, logging to /usr/local/spark/logs/spark-ec2-user-org.apache.spark.deploy.worker.Worker-1-ip-172-31-85-158.ec2.internal.out

----------------------
  Tengo estos dos errores en cada log:
  2024-08-05 21:13:54,619 ERROR org.apache.hadoop.hdfs.server.namenode.NameNode: RECEIVED SIGNAL 15: SIGTERM

  -a01b-848b4e26d7f5) service to ip-172-31-85-158.ec2.internal/172.31.85.158:9000. Exiting.
2024-08-05 21:13:55,913 ERROR org.apache.hadoop.hdfs.server.datanode.DataNode: RECEIVED SIGNAL 15: SIGTERM
[ec2-user@ip-172-31-85-158 ~]$

cat $HADOOP_HOME/logs/hadoop-ec2-user-namenode-$(hostname).log | grep -i 'error'

cat $HADOOP_HOME/logs/hadoop-ec2-user-datanode-$(hostname).log | grep -i 'error'
------------------------------------------------------
 127.0.0.1   localhost
  172.31.85.158 ip-172-31-85-158.ec2.internal ip-172-31-85-158

./usr/local/spark/sbin/start-master.sh

ERROR: flask-caching 2.1.0 has requirement cachelib<0.10.0,>=0.9.0, but you'll have cachelib 0.10.2 which is incompatible.


arl-1.9.4 zipp-3.15.0
WARNING: You are using pip version 20.1.1; however, version 24.0 is available.
You should consider upgrading via the '/home/ec2-user/new_airflow_env/bin/python3.7 -m pip install --upgrade pip' command.


  --------------------------------
    vi /usr/local/hadoop/etc/hadoop/core-site.xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://ip-172-31-85-158.ec2.internal:9000</value>
    </property>
</configuration>

---------------------------------
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>

------------------------------------
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost6 localhost6.localdomain6
172.31.85.158 ip-172-31-85-158.ec2.internal

--------------------------------

<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://172.31.85.158:9000</value>
    </property>
</configuration>

--------------- clave fernet ----
9kQpY7L5KsTfG2YgeIH1vWj8uAw84Ga_GjC8a7dGJV0=
mQOFQEyfC28IP5ipi--PJF1f1UHVEqwIL8keubsg3R0=
-----------------------------------------------------------------------------------
docker-compose down
docker-compose up --build -d

FvWY_j0mH-vFJwQ4T_l1QdducaqUFIS7oI_bpD0jGQU=

docker exec -it 157e3bade84d python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"


docker exec -it 32ff7f146ea7 /bin/bash

docker exec -u root -it 157e3bade84d bash

docker exec -it -u root 157e3bade84d /bin/bash



docker cp 157e3bade84d:/usr/local/airflow/airflow.cfg ./airflow.cfg

docker cp <container_id>:/path/to/airflow.cfg /path/to/local/airflow.cfg
docker cp /path/to/local/airflow.cfg <container_id>:/path/to/airflow.cfg

docker cp airflow.cfg 157e3bade84d:/usr/local/airflow/airflow.cfg
chown airflow:airflow airflow.cfg
chmod 644 airflow.cfg
-------------------------------------------------------------------------
  docker exec -it 5f9903488590 airflow scheduler -D
  docker inspect 5f9903488590 | grep Mounts -A 10

  docker exec -it 5f9903488590 ls /usr/local/airflow/dags



/mnt/c/Users/cgsilveriot/Engineer/MicroDataLake/AirFlow_Dags:/usr/local/airflow/dags
                                                            /usr/local/airflow/dags

docker logs 6d3e8a2ce94f | grep "error"



docker exec -it 6d3e8a2ce94f bash
echo "
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

dag = DAG('test_dag', description='Simple test DAG', schedule_interval='@daily', start_date=datetime(2023, 1, 1), catchup=False)
task = DummyOperator(task_id='dummy_task', dag=dag)
" > /usr/local/airflow/dags/test_dag.py

6d3e8a2ce94f
6d3e8a2ce94f

docker cp postgres_to_hdfs_dag.py 6ef31e2f7229:/usr/local/airflow/dags/postgres_to_hdfs_dag.py

docker exec -it 6ef31e2f7229 /bin/bash


c/Users/cgsilveriot/Engineer/MicroDataLake/Dags

:9870

---------------------------------------------------------------------------------------------------
  Establecer un tuner ssh para poder alcanzar HDFS en la instancia AWS, esto debido a restricciones en la redis

  ssh -N -L 9870:localhost:9870 -i /path/to/your/key.pem ec2-user@<AWS-INSTANCE-IP>

  ---------------------------
    Asignarle la misma red al docker

    docker run --network="host" <your-airflow-docker-image>

addr:127.0.0.1
addr:172.20.104.17
addr:172.31.0.1
--------------------------------
hdfs desde docker: curl http://172.20.104.17:9870

bashCopiar código
hdfs dfs -put -f /tmp/empleados.csv hdfs://<IP-publica-de-AWS>:9000/user/airflow/empleados/


-------------------

  ssh -L 5432:localhost:5432 -N -f -i <tu-clave-pem> ec2-user@<ip-instancia>

  curl http://localhost:9870