
from elasticsearch import Elasticsearch

# 此方法为搜索关键词时调用
def do_search(key_word):
    # 连ElasticSearch
    es = Elasticsearch('127.0.0.1:9200')
    # 关键字信息
    print('Search name contains '+key_word, flush=True)
    # 查询规则
    _query_name_contains = {
        'query': {
            'match': {
                'file_name': key_word
            }
        }
    }
    # 进行搜索,索引为entry_level_index,doc_type为entry_level,
    _searched = es.search(index='listen1_index', doc_type='listen1', body=_query_name_contains)
    # print(_searched, flush=True)
    #
    # for hit in _searched['hits']['hits']:
    #     print(hit['_source'], flush=True)

    # 返回dict字典 提取主要信息
    return _searched['hits']['hits']