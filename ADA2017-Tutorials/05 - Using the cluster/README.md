# How to access the ADA cluster

### Important note:
* the cluster is accessible only from the EPFL network (therefore remember to use the EPFL VPN when you are outside of the campus!)

Run `ssh YOUR_GASPAR_ACCOUNT@iccluster060.iccluster.epfl.ch` on your favorite terminal, followed by your GASPAR password. To speed up the login process,
I recommend you to install your own SSH key right away.

Once logged in, you can inspect the datasets directory stored in the Hadoop Distributed File System just by running `hadoop fs -ls /datasets`.
Check the other options of the `hadoop fs` command to move data in and out HDFS.


# How to use the Spark cluster from your computer

### Important note:
* we tested this configuration on Ubuntu (14.x and 16.x) and OSX

Even though you can submit any kind of Spark job when you are logged in on the master node (`iccluster060`), or even use the Spark shell `pyspark`, we prepared
a guide for those of you who prefer to launch the Spark jobs directly from their computers.

## Step by step:

1) Download Spark 1.6.3 with hadoop 2.6: https://spark.apache.org/downloads.html

First, you need a local copy of Apache Spark.
```sh
wget http://mirror.switch.ch/mirror/apache/dist/spark/spark-1.6.3/spark-1.6.3-bin-hadoop2.6.tgz
tar -zxvf spark-1.6.3-bin-hadoop2.6.tgz
```
Note: Spark is written in Scala and depends on the JVM. (sudo apt-get install default-jdk)
- - - -
2) Download the YARN configuration for the ADA cluster

YARN is the resources manager introduced with Hadoop 2.0. It takes care of the scalability of your Spark jobs and optimizes the usage of the cluster.
[Download the archive](ADA_YARN.zip) with the configuration, and unpack it in a local directory.

- - - -

3) Set the env variables YARN_CONF_DIR and YARN_CONF_DIR.

```sh
export YARN_CONF_DIR=<YARN_config_directory>
export HADOOP_USER_NAME=username
```
Where *<YARN_config_directory>* is the full path of the directory where you have the configuration files and *username* is your Gaspar Account.

Note: this is temporary. If you want to avoid to type this setup every time you reboot you computer, update your shell config (i.e. $HOME/.bashrc)

- - - -
4) Create a new file called *spark-defaults.conf* in the config directory of Spark *(<spark_directory>/conf/spark-defaults.conf)* and add the the following lines:
```sh
spark.driver.extraJavaOptions -Dhdp.version=2.7.3
spark.yarn.am.extraJavaOptions -Dhdp.version=2.7.3
```
This specifies the version of Hadoop that the ADA cluster is using.
- - - -
5) Enjoy (*responsibly*)! Now you can launch *pyspark* or *spark-submit* from your computer using the parameter --master yarn
```sh
<spark_directory>/bin/pyspark --master yarn
<spark_directory>/bin/spark-submit --master yarn yourjob.py
```

# Random useful information
* if you have to store an intermediate result, please save it directly on the Hadoop file system (using prefix *hdfs://...*) and possibily in [Parquet format](https://spark.apache.org/docs/1.6.3/sql-programming-guide.html#parquet-files)
* If you store anything in parquet, it's a good practice to save the dataset with a compressed format. Snappy is a great choice to balance compression and performance:
```python
sqlContext.setConf("spark.sql.parquet.compression.codec","snappy")
```
* DO NOT try to push the usage of the cluster to its limit without asking. The resources are shared and you could block other groups
