'''Converts MS MARCO doc-query pairs to the OpenNMT format.'''
import collections
import functools
import traceback
import sys



def load_qrels(path):
  """Loads qrels into a dict of key: query id, value: set of relevant doc ids."""
  qrels = collections.defaultdict(set)
  with open(path) as f:
    for i, line in enumerate(f):
      query_id, _, doc_id, relevance = line.rstrip().split('\t')
      if int(relevance) >= 1:
        qrels[query_id].add(doc_id)
      if i % 100000 == 0:
        print('Loading qrels {}'.format(i))
  return qrels


def load_queries(path):
  """Loads queries into a dict of key: query id, value: query text."""
  queries = {}
  with open(path) as f:
    for i, line in enumerate(f):
      query_id, query = line.rstrip().split('\t')
      queries[query_id] = query
      if i % 100000 == 0:
        print('Loading queries {}'.format(i))
  return queries


def load_collection(path):
  """Loads tsv collection into a dict of key: doc id, value: doc text."""
  collection = {}
  with open(path) as f:
    for i, line in enumerate(f):
      doc_id, doc_text = line.rstrip().split('\t')
      collection[doc_id] = doc_text.replace('\n', ' ')
      if i % 1000000 == 0:
        print('Loading collection, doc {}'.format(i))

  return collection

def load_doc2query(path):
  """Loads txt queries from doc2query into a dict of key: doc id, value: doc query."""
  collection = {}
  with open(path) as f:
    for i, line in enumerate(f):
      doc_text = line.rstrip()
      collection[str(i)] = doc_text.replace('\n', ' ')
      if i % 1000000 == 0:
        print('Loading doc2query, doc {}'.format(i))

  return collection


def load_triple(path, max_i=None):
    """Load triple tsv into python dict."""
    triples = collections.defaultdict(set)
    with open(path) as f:
        for i, line in enumerate(f):
            qid, pid, nid = line.rstrip().split('\t')
            triples[i] = qid, pid, nid
            if i % 100000 == 0:
                print('Loading triple {}'.format(i))
            if max_i != None and i > max_i:
                break
    return triples