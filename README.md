## OnionStats
A web application to query Tor nodes information and make statistics.
More will come.

## Install
Software stack involved:

- mongodb
- elasticsearch
- tornado
- semantic-ui + jquery

### mongodb
* `apt-get install mongodb`

* enable replica: 
`mongod --bind_ip 127.0.0.1 --port 27017 --dbpath /var/lib/mongodb --replSet rs0 --logpath /var/log/mongodb/mongodb.log --fork`
    (be sure that your hostname is listed under 127.0.0.1 in /etc/hosts)
    
* `> rs.initialite()` (mongodb shell)

### elasticsearch
* `apt-get install default-jdk`
* `wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.3/elasticsearch-2.3.3.deb`
* `dpkg -i elasticsearch`
* `systemctl enable elasticsearch.service`
* `service elasticsearch start`

Few recommendation:
- by default ES uses 256m as heap size. You want most likely change that. Edit the parameter _ES_HEAP_SIZE_ in _/etc/default/elasticsearch_ and set it to 1g (1g as minimum and maximum heap size)

## install the mapping
In order to optimize the search engine, we need to specify the type of data we're going to use:
* `curl -XPUT http://localhost:9200/_template/template_name -d '<mapping here>'` (the actually mapping is at the end of this file)

## mongodb-connector
* `pip install mongo-connector`
* `pip install elastic2-doc-manager`
* `mongo-connector -m localhost:27017 -t localhost:9200 -d elastic2_doc_manager --auto-commit-interval=0 &>/dev/null &` (it will log to mongo-connector.log)

## make it run
* `pip install -r requirements.txt`
* `python manage.py` (it will download the data from Onionoo and insert into mongodb
* `python onionstats.py` (open http://localhost:8080)


### Links
https://github.com/mongodb-labs/mongo-connector/wiki/Usage%20with%20ElasticSearch

### Mapping

```
{
   "mappings" : {
      "bridges" : {
         "properties" : {
            "first_seen" : {
               "type" : "date",
               "format" : "YYYY-MM-dd HH:mm:ss"
            },
            "geo" : {
               "type" : "string"
            },
            "last_restarted" : {
               "format" : "YYYY-MM-dd HH:mm:ss",
               "type" : "date"
            },
            "last_seen" : {
               "format" : "YYYY-MM-dd HH:mm:ss",
               "type" : "date"
            },
            "flags" : {
               "type" : "string"
            }
         }
      },
      "relays" : {
         "properties" : {
            "last_seen" : {
               "format" : "YYYY-MM-dd HH:mm:ss",
               "type" : "date"
            },
            "flags" : {
               "type" : "string"
            },
            "last_changed_address_or_port" : {
               "type" : "date",
               "format" : "YYYY-MM-dd HH:mm:ss"
            },
            "first_seen" : {
               "format" : "YYYY-MM-dd HH:mm:ss",
               "type" : "date"
            },
            "geo" : {
               "type" : "string"
            },
            "last_restarted" : {
               "type" : "date",
               "format" : "YYYY-MM-dd HH:mm:ss"
            }
         }
      }
   },
   "template" : "onion*"
}
```
