# YJDHTQ

MacOS
> START ZOOKEEPER : brew services start zookeeper
> START KAFKA : brew services start kafka

OR 

> START ZOOKEEPER : zookeeper-server-start /System/Volumes/Data/opt/homebrew/etc/kafka/zookeeper.properties\
> START KAFKA : kafka-server-start /System/Volumes/Data/opt/homebrew/etc/kafka/server.properties\

> CREATE TOPIC : kafka-topics --create --topic seller_product_data_tp --bootstrap-server localhost:9092 --partitions 10 --replication-factor 1\
> DELETE TOPIC : kafka-topics --delete --topic seller_product_data_tp --bootstrap-server localhost:9092\
> LIST ALL TOPICS : kafka-topics --list --bootstrap-server localhost:9092


Linux
> START ZOOKEEPER : sudo systemctl start kafka\
> START KAFKA : sudo systemctl stop kafka\
> CREATE TOPIC : ./kafka --topics.sh --create --topic seller_product_data_tp --bootstrap-server localhost:9092 --partitions 10 --replication-factor 1\
> DELETE TOPIC : /kafka --topics.sh --delete --topic seller_product_data_tp --bootstrap-server localhost:9092\
> LIST ALL TOPICS : 

Windows
Good Luck ! XD XD
