# bioblend-ontology-api

This project generates different ontology graphs for a sample dataset using GOEnrichment running on a Galaxy instance. The data I used to test this API was from Trapnell et al. 2014 (https://pubmed.ncbi.nlm.nih.gov/22383036/), referenced in this tutorial: https://training.galaxyproject.org/training-material/topics/transcriptomics/tutorials/goenrichment/tutorial.html. The other ontology file I downloaded, `uberon.owl`, was downloaded from OBO Foundry (https://obofoundry.org/ontology/uberon.html).

The graphs are generated from an API written using Flask that runs GOEnrichment through Bioblend, a library that interfaces with Galaxy. Calling the API with `0` downloads the graph generated with `go.obo` and with a `1` downloads the graph generated with `uberon.owl` and can be extended for any `.owl` or `.obo` ontology file

![image](https://user-images.githubusercontent.com/57931772/215821224-c7776dec-7d4b-4771-9049-e2a5a72c3ea4.png)
![image](https://user-images.githubusercontent.com/57931772/215821697-80690242-d3da-4327-8d51-f0169900fc2e.png)
