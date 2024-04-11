import time

import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

print(pymilvus.__version__)

fmt = "\n=== {:30} ===\n"

print(fmt.format("start connecting to Milvus"))
connections.connect("default", host="localhost", port="19530")

print(fmt.format("Drop collection `hello_milvus`"))
utility.drop_collection("hello_milvus")
