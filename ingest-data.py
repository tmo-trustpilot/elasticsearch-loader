import gzip
import hashlib
import json
from glob import glob

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

HOST = "localhost:9200"
INDEX = "ingest"
client = Elasticsearch(HOST)

def read_records(filename):
    id_prefix = hashlib.md5(filename.encode("utf8")).hexdigest()
    record_id = 0

    with gzip.open(filename) if filename.endswith(".gz") else open(filename) as file:
        for line in file:
            record = json.loads(line)
            yield {
                "_id": f"{id_prefix}-{record_id:010d}",
                "_source": record,
            }
            record_id += 1

for filename in glob("*.json.gz") + glob("*.json"):
    print(f"Processing {filename}")
    file_progress = 0

    for ok, result in streaming_bulk(
        client, read_records(filename), index=INDEX, chunk_size=500
    ):
        action, result = result.popitem()
        doc_id = "%s %s" % (filename, result["_id"])

        if not ok:
            print("Failed to %s document %s: %r" % (action, doc_id, result))
        else:
            file_progress += 1
            if file_progress % 10000 == 0:
                print("Inserted %s" % doc_id)

    print(f"Finished {filename}")
