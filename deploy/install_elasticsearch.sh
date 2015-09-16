!#/bin/bash

apt-get -y install curl

apt-get -y install ntp ntpdate
service ntp start
ntpdate 0.pool.ntp.org

add-apt-repository -y ppa:webupd8team/java
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | apt-key add -
echo "deb http://packages.elastic.co/elasticsearch/1.7/debian stable main" | tee -a /etc/apt/sources.list.d/elasticsearch-1.7.list
apt-get update
echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
apt-get -y install oracle-java8-installer
apt-get -y install elasticsearch
service elasticsearch restart
# systemctl daemon-reload
# systemctl enable elasticsearch.service
# systemctl start elasticsearch

sleep 10

curl 'http://localhost:9200/?pretty'

curl -X DELETE 'http://localhost:9200/the-best-test/_mapping/item'
curl -X PUT localhost:9200/the-best-test/item/_mapping -d '{
  "item" : {
        "properties" : {
            "category" : { "type" : "string" },
            "suggest" : { "type" : "completion",
                          "index_analyzer" : "simple",
                          "search_analyzer" : "simple",
                          "payloads" : true
            }
        }
    }
}'

curl -s -XPOST localhost:9200/_bulk --data-binary @sysconfig/elasticsearch/initial-data; echo
