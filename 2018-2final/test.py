
from pymongo import MongoClient
from elasticsearch import Elasticsearch
import traceback

# 创建连接
_db = MongoClient('mongodb://127.0.0.1:27017')['201802final']
es = Elasticsearch('127.0.0.1:9200')
# _db.update({}, {"$set": {"src": "20130408120000"}})
# 初始化索引的Mappings设置
_index_mappings = {
    "settings": {
        "number_of_shards": "1",
        "analysis": {
            "analyzer": {
                "ik": {
                    "tokenizer": "ik_smart"
                }
            }
        }
    },
  "mappings": {
        "listen1": {
              "properties": {
                "file_name":    { "type": "text"  },
                "src":     { "type": "text"  },
              }
        }
    },

}
# 创建索引
if es.indices.exists(index='listen1_index') is not True:
  es.indices.create(index='listen1_index', body=_index_mappings)

# 从MongoDB中查询数据，由于在Elasticsearch使用自动生成_id，因此从MongoDB查询
# 返回的结果中将_id去掉。
# data_cursor = _db.data_link.find({}, projection={'_id': False})
data_cursor = _db.data_link.find({}, projection={'_id': False})
data_docs = [x for x in data_cursor]
# 批量导入
processed = 0
for _doc in data_docs:
    try:
        processed += 1
        es.index(index='listen1_index',doc_type='listen1',body=_doc,id=str(processed))
        print('Processed:'+str(processed),flush=True)
    except:
        traceback.print_exc()

print('Search all...',  flush=True)
_query_all = {
  'query': {
    'match_all': {}
  }
}

_searched = es.search(index='listen1_index', doc_type='data_link', body=_query_all)
print(_searched, flush=True)

# 输出查询到的结果
for hit in _searched['hits']['hits']:
    print(hit['_source'], flush=True)

# #查询姓名中包含jerry的记录
# print('Search name contains jerry.', flush=True)
# _query_name_contains = {
#     'query': {
#         'match': {
#             'file_name': '世界精神日'
#         }
#     }
# }
# _searched = es.search(index='listen_index', doc_type='data_link', body=_query_name_contains)
# print(_searched, flush=True)
#
# for hit in _searched['hits']['hits']:
#     print(hit['_source'], flush=True)
