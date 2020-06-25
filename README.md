# Dense Vector passage re-ranking with doc2query 
### Developed by Matheus Gustavo Alves Sasso and Graziella Cardoso Bonadia

This project uses doc2query algorithm to train a neural network using passages as artificial queries with the following loss function and the gold passages strategy cited on the paper **Dense Passage Retrieval for Open-Domain Question Answering**, that can be found [here](https://arxiv.org/abs/2004.04906)

We used the files from [TREC 2020 competition](https://microsoft.github.io/TREC-2020-Deep-Learning/) .

For the training we used the other positive artificial queries from the batch as the negative queries. To develop this a dataloader with that information we used the file [qidpidtriples.train.full.2.tsv.gz	](https://msmarco.blob.core.windows.net/msmarcoranking/qidpidtriples.train.full.2.tsv.gz) combined with the queries and the [artificial queries](https://storage.googleapis.com/doctttttquery_git/predicted_queries_topk_sampling.zip.) . All this organization was possible with the package [FAISS](https://ai.facebook.com/tools/faiss/), that simplifies the query - passage(artificial query) scoring.

For the inference step we just used FAISS with the trained model to re-rank the passages and find and MRR@10 score.



## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the requirements
```bash
pip install ftfy
pip install transformers
pip install pytorch-lightning
pip install mkl
```
And specially for the FAISS package:
```bash
!wget  https://anaconda.org/pytorch/faiss-cpu/1.2.1/download/linux-64/faiss-cpu-1.2.1-py36_cuda9.0.176_1.tar.bz2
!tar xvjf faiss-cpu-1.2.1-py36_cuda9.0.176_1.tar.bz2
```


## Usage

For the usage, its necessary to run the pipeline on number suggested order, linking the file generated from the previous step from the pipeline as the input of the current one. Next, we can see the pipeline order:

* 1_ReadDoc2Query.ipynb
* 2_ReadTriplesIds.ipynb
* 3_ReadInferenceDatasetDataframe.ipynb
* 5_1_DOIS_MOD_TwoTowerPassageRanking_GoldPassages



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.