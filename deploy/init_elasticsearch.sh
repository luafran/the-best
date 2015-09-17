curl -X DELETE 'http://localhost:9200/the-best-test/_mapping/item'; echo
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
}'; echo

curl -s -XPOST localhost:9200/_bulk --data-binary @sysconfig/elasticsearch/initial-data; echo
