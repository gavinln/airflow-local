# airflow-local

* Source code - [Github][10]
* Author - Gavin Noronha - <gavinln@hotmail.com>

[10]: https://github.com/gavinln/airflow-local.git

## About

This project provides a [Ubuntu (16.04)][20] [Vagrant][30] Virtual Machine
(VM) with [Airflow][40], a data workflow management system from [Airbnb][50].

[20]: http://releases.ubuntu.com/14.04/
[30]: http://www.vagrantup.com/
[40]: https://github.com/airbnb/airflow
[50]: http://nerds.airbnb.com/airflow/

There are [Ansible][60] scripts that automatically install the software when
the VM is started.

[60]: https://www.ansible.com/

## 1. Run Airflow

### Connect to the VM

1. To start the virtual machine(VM) type

    ```
    vagrant up
    ```

2. Connect to the VM

    ```
    vagrant ssh
    ```

### Initialize Airflow

This process will setup Airflow in Standalone mode using Sequential Executor

1. Setup the home directory

    ```
    export AIRFLOW_HOME=~/airflow
    ```

2. Initialize the sqlite database

    ```
    airflow initdb
    ```

3. Start the web server

    ```
    airflow webserver -p 8080
    ```

4. Open a web browser to the UI at http://192.168.33.10:8080

### Run a task

1. List DAGS

    ```
    airflow list_dags
    ```

2. List tasks for `example_bash_operator` DAG

    ```
    airflow list_tasks example_bash_operator
    ```

3. List tasks for `example_bash_operator` in a tree view

    ```
    airflow list_tasks example_bash_operator -t
    ```

4. Run the `runme_0` task on the `example_bash_operator` DAG today

    ```
    airflow run example_bash_operator runme_0 `date +%Y-%m-%d`
    ```

5. Backfill a DAG

    ```
    export START_DATE=$(date -d "-2 days" "+%Y-%m-%d")
    airflow backfill -s $START_DATE example_bash_operator
    ```

6. Clear the history of DAG runs

    ```
    airflow clear example_bash_operator
    ```

### Add a new task

1. Go to the Airflow config directory

    ```
    cd ~/airflow
    ```

2. Set the airflow dags directory in airflow.cfg by change the line:

    ```
    dags_folder = /vagrant/airflow/dags
    ```

3. Remove example dags

    ```
    load_examples = False
    ```

3. Restart the web server

    ```
    airflow webserver -p 8080
    ```

### Run a task

1. Run the dynamic_dags task
airflow list_dags

2. Run the dag
airflow trigger_dag dynamic_dags

3. Run the scheduler to actually run the dag
airflow scheduler

### Disable logging

1. Change to the airflow directory

    ```
    cd /vagrant/airflow
    ```

2. Set airflow environment

    ```
    source set_airflow_env.sh
    ```

3. Run airflow without any logging messages

### Setup airflow dags directory

1. Edit file ~/airflow/airflow.cfg

2. Set the following:

    ```
    dags_folder = /vagrant/airflow/dags
    load_examples = False
    ```

3. Start the scheduler by running the following

    ```
    airflow scheduler
    ```

### Setup Airflow in Pseudo-distributed mode using Local Executor

Follow the instructions [here](https://stlong0521.github.io/20161023%20-%20Airflow.html)

### Setup Airflow in distributed mode using Celery Executor

Follow the instructions [here](https://stlong0521.github.io/20161023%20-%20Airflow.html)


## 2. Run RabbitMQ

### Start RabbitMQ

1. Start the RabbitMQ in a Docker container

    ```
    export RMQ_IMG=rabbitmq:3.6.10-management
    docker run -d --rm --hostname airflow-rmq \
        --name airflow-rmq -p 192.168.33.10:15672:15672 -p 5672:5672 $RMQ_IMG
    ```

2. Display the list of running Docker instances

    ```
    docker ps
    ```

2. Go to the RabbitMQ dashboard at http://192.168.33.10:15672/

3. Login using guest/guest

### Stop RabbitMQ

1. Connect to the RabbitMQ Docker container

    ```
    export RMQ=$(docker ps -aq --filter name=airflow-rmq)
    ```

2. List queues

    ```
    docker exec -ti $RMQ rabbitmqctl list_queues
    ```

3. Stop RabbitMQ

    ```
    docker stop $RMQ
    ```

## 3. Connect to RabbitMQ using Python

### Connect to RabbitMQ only using Python (no Celery)

The RabbitMQ web site demonstrates how to connect using Python and the
[Pika][100] library.

[100]: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

1. List queues

    ```
    docker exec -ti $RMQ rabbitmqctl list_queues
    ```

2. Send a message to a RabbitMQ queue called hello

    ```
    python rmq-send.py
    ```

3. Receive a message from RabbitMQ queue called hello

    ```
    python rmq-receive.py
    ```

4. List queues displaying the hello queue

    ```
    docker exec -ti $RMQ rabbitmqctl list_queues
    ```

5. Stop the app

    ```
    docker exec -ti $RMQ rabbitmqctl stop_app
    ```

6. Start the app

    ```
    docker exec -ti $RMQ rabbitmqctl start_app
    ```

7. List queues and the hello queue is not displayed

    ```
    docker exec -ti $RMQ rabbitmqctl list_queues
    ```

### Connect to RabbitMQ using Celery

1. Start the Celery worker

    ```
    export PYTHONPATH=/vagrant/scripts
    celery -A tasks worker --loglevel=info
    ```

2. Call the task

    ```
    export PYTHONPATH=/vagrant/scripts
    python -c "from tasks import add; add.delay(2, 3)"
    ```

## 4. Run Postgres

### Start Postgres

1. Start the Postgres in the Docker container with the name

    ```
    export PG_IMG=postgres:9.6.3
    export PGPASSWORD=airflow_pg_pass
    docker run -d --rm --name airflow-pg -p 127.0.0.1:5432:5432 \
        -e POSTGRES_PASSWORD=$PGPASSWORD $PG_IMG
    export PG=$(docker ps -aq --filter name=airflow-pg)
    ```

### Stop Postgres

1. List the Docker container

    ```
    docker ps --filter id=$PG
    ```

2. Stop Postgres

    ```
    docker stop $PG
    ```

## 5. Connect to Postgres using Psycopg2 and SQLAlchemy

Start the Postres database before running these steps

1. Connect to the database using psql and create the database test

    ```
    docker exec -ti $PG psql -U postgres -c "create database test"
    ```

2. Create table test in database test only using Psycopg2

    ```
    export PGHOST=localhost
    python /vagrant/scripts/pg-psycopg2.py
    ```

3. Connect to database test using Psycopg2 and SQLAlchemy

    ```
    python pg-sqlalchemy-read.py
    ```

4. Connect to the postgres database again

    ```
    docker exec -ti $PG psql -U postgres
    ```

5. List the databases

    ```
    \l
    ```

6. Connect to the test database

    ```
    \c test
    ```

7. List objects in the test database

    ```
    \d
    ```

8. Select all rows from the test database

    ```
    select id, num, data from test;
    ```

9. Quit the psql utility

    ```
    \q
    ```

10. Drop database test

    ```
    docker exec -ti $PG psql -U postgres -c "drop database test"
    ```

## 6. Setup Airflow with Postgres

### 1. Using the LocalExecutor

1. Change the executor in ~/airflow.cfg file to the following values

    ```
    executor = LocalExecutor
    ```

2. Change the sql_alchemy_conn in ~/airflow.cfg file to the following values

    ```
    # Change the meta db configuration
    sql_alchemy_conn = postgresql+psycopg2://postgres:airflow_pg_pass@localhost/test
    ```

### 2. Using the CeleryExecutor with Redis

1. Change the executor in ~/airflow.cfg file to the following values

    ```
    executor = CeleryExecutor
    ```

2. Set the following two values in ~/airflow.cfg file

    ```
    broker_url = redis://localhost:6379/0
    celery_result_backend = redis://localhost:6379/0
    ```

## 7. Setup [netdata][110] for monitoring

[110]: https://github.com/firehol/netdata

1. Change to the netdata directory

    ```
    cd ~/netdata
    ```

2. Install netdata without starting it

    ```
    sudo ./netdata-installer.sh --dont-start-it
    ```

3. Show status of netdata

    ```
    sudo systemctl status netdata
    ```

4. Start netdata

    ```
    sudo systemctl start netdata
    ```

5. View the netdata at http://192.168.33.10:19999/

6. Stop netdata

    ```
    sudo systemctl stop netdata
    ```

7. Modify /etc/netdata/netdata.conf to change configuration

8. Netdata stores data in memory and updates every second. To store hours of
   data without using up memory add the following

    ```
    [global]
    update every = 10
    ```

## Documentation

1. Main documentation

    * https://pythonhosted.org/airflow/

2. Videos on Airflow

    * [Best practices with Airflow](https://www.youtube.com/watch?v=dgaoqOZlvEA)
    * [A Practical Introduction to Airflow](https://www.youtube.com/watch?v=cHATHSB_450)

2. Slides

    * http://www.slideshare.net/walterliu7/airflow-a-data-flow-engine
    * http://www.slideshare.net/Hadoop_Summit/airflow-an-open-source-platform-to-author-and-monitor-data-pipelines

4. Airflow reviews

    * http://bytepawn.com/airflow.html
    * https://www.pandastrike.com/posts/20150914-airflow

5. Airflow tips and tricks

    * https://medium.com/handy-tech/airflow-tips-tricks-and-pitfalls-9ba53fba14eb#.i2hu0syug
    * [Airflow with Postgres + RabbitMQ](https://stlong0521.github.io/20161023%20-%20Airflow.html)
    * [Three tips on using Celery](https://library.launchkit.io/three-quick-tips-from-two-years-with-celery-c05ff9d7f9eb)
    * [Building a Data Pipeline with Airflow](http://tech.marksblogg.com/airflow-postgres-redis-forex.html)
    * https://databricks.com/blog/2016/12/08/integrating-apache-airflow-databricks-building-etl-pipelines-apache-spark.html
    * http://site.clairvoyantsoft.com/installing-and-configuring-apache-airflow/
    * https://gtoonstra.github.io/etl-with-airflow/principles.html
    * https://cwiki.apache.org/confluence/display/AIRFLOW/Common+Pitfalls
    * http://michal.karzynski.pl/blog/2017/03/19/developing-workflows-with-apache-airflow/


## Requirements

The following software is needed to get the software from github and run
Vagrant to set up the Python development environment. The Git environment
also provides an [SSH  client][200] for Windows.

* [Oracle VM VirtualBox][210]
* [Vagrant][220] version 1.9 or higher
* [Git][230]

[200]: http://en.wikipedia.org/wiki/Secure_Shell
[210]: https://www.virtualbox.org/
[220]: http://vagrantup.com/
[230]: http://git-scm.com/

