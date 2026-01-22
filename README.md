# NetworkSecurity-project For Phishing Data

# MongoDB with Python (PyMongo) – Complete Guide

This document provides a practical overview of **MongoDB** and how to **query it using Python with PyMongo**, suitable for ETL pipelines, data engineering, and backend development.

---

## What is MongoDB?

**MongoDB** is a NoSQL, document-oriented database that stores data in **JSON-like documents (BSON)** instead of rows and tables.

### Key Characteristics
- Schema-flexible (no fixed table structure)
- Document-based storage
- Horizontally scalable
- High performance for read/write operations
- Native support for nested objects and arrays

### Core Concepts
| MongoDB | Relational DB |
|------|--------------|
| Database | Database |
| Collection | Table |
| Document | Row |
| Field | Column |
| `_id` | Primary Key |

---

## Installing PyMongo

```bash
pip install pymongo
````

---

## Connecting to MongoDB

### Local MongoDB

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["my_database"]
collection = db["my_collection"]
```

### MongoDB Atlas

```python
client = MongoClient(
    "mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
)

db = client["my_database"]
collection = db["my_collection"]
```

---

## Basic Queries

### Find All Documents

```python
documents = collection.find()
for doc in documents:
    print(doc)
```

### Find One Document

```python
doc = collection.find_one({"email": "user@email.com"})
```

---

## Filtering (WHERE)

### Simple Filter

```python
collection.find({"status": "ACTIVE"})
```

### Multiple Conditions (AND)

```python
collection.find({
    "status": "ACTIVE",
    "country": "CO"
})
```

### OR Condition

```python
collection.find({
    "$or": [
        {"status": "ACTIVE"},
        {"status": "PENDING"}
    ]
})
```

---

## Comparison Operators

```python
collection.find({"age": {"$gt": 18}})
collection.find({"age": {"$gte": 18, "$lte": 30}})
collection.find({"price": {"$lt": 100}})
```

| Operator | Meaning          |
| -------- | ---------------- |
| `$gt`    | Greater than     |
| `$gte`   | Greater or equal |
| `$lt`    | Less than        |
| `$lte`   | Less or equal    |
| `$ne`    | Not equal        |
| `$in`    | In list          |

---

## Selecting Fields (Projection)

```python
collection.find(
    {"status": "ACTIVE"},
    {"_id": 0, "name": 1, "email": 1}
)
```

---

## Sorting Results

```python
collection.find().sort("age", 1)    # Ascending
collection.find().sort("age", -1)   # Descending
```

---

## Pagination (LIMIT / OFFSET)

```python
collection.find().limit(10)
collection.find().skip(20).limit(10)
```

---

## Counting Documents

```python
collection.count_documents({"status": "ACTIVE"})
```

---

## Querying Nested Fields

```python
collection.find({"address.city": "Bogotá"})
```

---

## Querying Arrays

```python
collection.find({"tags": "python"})
```

Array with multiple conditions:

```python
collection.find({"tags": {"$all": ["python", "etl"]}})
```

---

## Regex / Text Search

```python
collection.find({
    "name": {"$regex": "^Seb", "$options": "i"}
})
```

---

## Aggregation Framework (GROUP BY)

```python
pipeline = [
    {"$match": {"status": "ACTIVE"}},
    {"$group": {
        "_id": "$country",
        "count": {"$sum": 1}
    }}
]

results = collection.aggregate(pipeline)
for r in results:
    print(r)
```

---

## Insert Operations

### Insert One

```python
collection.insert_one({
    "name": "Juan",
    "age": 30,
    "status": "ACTIVE"
})
```

### Insert Many

```python
collection.insert_many([
    {"name": "Ana", "age": 25},
    {"name": "Luis", "age": 28}
])
```

---

## Update Operations

### Update One

```python
collection.update_one(
    {"email": "user@email.com"},
    {"$set": {"status": "INACTIVE"}}
)
```

### Update Many

```python
collection.update_many(
    {"status": "PENDING"},
    {"$set": {"status": "ACTIVE"}}
)
```

---

## Delete Operations

```python
collection.delete_one({"email": "user@email.com"})
collection.delete_many({"status": "INACTIVE"})
```

---

## Indexes (Performance)

```python
collection.create_index("email", unique=True)
collection.create_index([("status", 1), ("country", 1)])
```

---

## MongoDB to Pandas DataFrame

```python
import pandas as pd

docs = list(collection.find())
df = pd.DataFrame(docs)
```

---

## SQL vs MongoDB Cheat Sheet

| SQL      | MongoDB                  |
| -------- | ------------------------ |
| SELECT   | find                     |
| WHERE    | filter                   |
| LIMIT    | limit                    |
| OFFSET   | skip                     |
| ORDER BY | sort                     |
| GROUP BY | aggregate                |
| INSERT   | insert_one / insert_many |
| UPDATE   | update_one / update_many |
| DELETE   | delete_one / delete_many |

---

## Common Use Cases

* ETL pipelines
* Event storage
* Logs and audit trails
* Semi-structured data
* Microservices backends
* Data ingestion before Kafka / Spark

---

## Best Practices

* Always index frequently queried fields
* Avoid large unbounded documents
* Use projections to reduce network usage
* Prefer aggregation pipeline for heavy transformations
* Use connection pooling (default in PyMongo)

---

## References

* [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/)
* [https://pymongo.readthedocs.io/](https://pymongo.readthedocs.io/)


