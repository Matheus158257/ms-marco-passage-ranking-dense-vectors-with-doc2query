'''Getting data from MS MARCO datsets'''
import collections
import functools
import traceback
import sys
import os


#-------------------- Funcios to read tsv as dicts
def load_qrels(path,encoding="cp1252"):
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


def load_queries(path,encoding="cp1252"):
  """Loads queries into a dict of key: query id, value: query text."""
  queries = {}
  with open(path) as f:
    for i, line in enumerate(f):
      query_id, query = line.rstrip().split('\t')
      queries[query_id] = query
      if i % 100000 == 0:
        print('Loading queries {}'.format(i))
  return queries


def load_collection(path,encoding="cp1252"):
  """Loads tsv collection into a dict of key: doc id, value: doc text."""
  collection = {}
  with open(path,encoding=encoding, newline='') as f:
    for i, line in enumerate(f):
      doc_id, doc_text = line.rstrip().split('\t')
      collection[doc_id] = doc_text.replace('\n', ' ').replace('"', '')
      if i % 1000000 == 0:
        print('Loading collection, doc {}'.format(i))

  return collection

def load_doc2query(path,encoding="cp1252"):
  """Loads txt queries from doc2query into a dict of key: doc id, value: doc query."""
  collection = {}
  with open(path, encoding=encoding, newline='') as f:
    for i, line in enumerate(f):
      doc_id, doc_text = line.rstrip().split('\t')
      collection[str(i)] = doc_text.replace('\n', ' ').replace('"', '')
      if i % 1000000 == 0:
        print('Loading doc2query, doc {}'.format(i))

  return collection


def load_triple(path,encoding="cp1252", max_i=None):
    """Load triple tsv into python dict."""
    triples = {}
    with open(path, encoding=encoding, newline='') as f:
        for i, line in enumerate(f):
            qid, pid, nid = line.rstrip().split('\t')
            triples[str(i)] = qid.replace('"', ''), pid.replace('"', ''), nid.replace('"', '')
            if i % 100000 == 0:
                print('Loading triple {}'.format(i))
            if max_i != None and i > max_i:
                break
    return triples
    
#-------------------- Funcion to get the passages as top docTTTTTqueries
def load_txts_topk(folder,k=1,n=18,encoding="cp1252"):
    k = k if k<=80 else 80
    n = n if n<=18 else 18
    nsamples = [i for i in range(0,k)] #[0] ou [0,1,2,3...]
    nparts = [i for i in range(0,n)] #cada bloco é de 17
    extension_template2 = '-1004000'

    txts = []
    for sample in nsamples:
        rows = []
        for part in nparts:
            name_template = 'predicted_queries_topk_sample0' if sample>9 else 'predicted_queries_topk_sample00'
            extension_template1 = '.txt0' if part>9 else '.txt00'
            
            file_name = f"{name_template}{str(sample)}{extension_template1}{str(part)}{extension_template2}"
            path = os.path.join( folder,file_name)
            txt_reader = open(path,mode = "r",encoding = encoding,errors='ignore')
            for row in txt_reader:
                rows.append([(elem.replace("\n","")) for elem in row])
                            
        txts.append(rows)

    return txts
    
    
   
 #-------------------- Funcion work with dicts as train, valid, test datasets
def take_part(d,n_elements):
    elements =  [str(x) for x in range(n_elements + 1)]
    newdict = {key:d[key] for key in elements}
    return newdict
  
def reset_dict_keys(original_dict): 	
    new_dict = {} 	
    for i, (k, v) in enumerate(original_dict.items()):
      new_dict[str(i)] = v
    return new_dict
 
def train_val_test(d, tr, vl, ts):
    elements =  [str(x) for x in range(tr)]
    train = {key:d[key] for key in elements}
    elements =  [str((x + tr)) for x in range(vl)]
    val = {key:d[key] for key in elements}
    val = reset_dict_keys(val)
    elements =  [str((x + tr + vl)) for x in range(ts)]
    test = {key:d[key] for key in elements}
    test = reset_dict_keys(test)
    return train, val, test