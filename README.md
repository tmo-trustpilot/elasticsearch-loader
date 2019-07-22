# ElasticSearch Quick Ingest

This repo contains a `docker-compose` file that will create a local ElasticSearch instance and and Kibana to view it. The script `ingest-data.json` will scan any `*.json` or `*.json.gz` in the directory and load them into the ES instance.

* Start ES/Kibana: `docker-compose up`
* Install python ES library: `pip install -r requirements`
* Ingest data: `python ingest-data.py`
* Visit `http://localhost:5601`
* Create an index pattern in kibana
