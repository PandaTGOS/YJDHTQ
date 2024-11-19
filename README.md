# YJDHTQ

MacOS
> zookeeper-server-start /System/Volumes/Data/opt/homebrew/etc/kafka/zookeeper.properties
> kafka-server-start /System/Volumes/Data/opt/homebrew/etc/kafka/server.properties


> kafka-topics --create --topic seller_product_data_tp --bootstrap-server localhost:9092 --partitions 10 --replication-factor 1
> kafka-topics --delete --topic seller_product_data_tp --bootstrap-server localhost:9092
