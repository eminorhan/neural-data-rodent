## rodent ephys data

~417B raw tokens of ephys data recorded from rodents (raw=uncompressed, tokens=units x time bins). Unless otherwise noted, the data consist of spike counts within 20 ms time bins recorded from each unit.

Token counts per dataset:

1. **VBN:** 153,877,057,200 tokens ([dandi:000713](https://dandiarchive.org/dandiset/000713)); rows = 153
2. **IBL:** 69,147,814,139 tokens ([dandi:000409](https://dandiarchive.org/dandiset/000409)); rows = 347
3. **SHIELD:** 61,890,305,241 tokens ([dandi:001051](https://dandiarchive.org/dandiset/001051)); rows = 99
4. **VCN:** 36,681,686,005 tokens ([dandi:000021](https://dandiarchive.org/dandiset/000021)); rows = 32
5. **VCN-2:** 30,600,253,445 tokens ([dandi:000022](https://dandiarchive.org/dandiset/000022)); rows = 26
6. **Petersen:** 15,510,368,376 tokens ([dandi:000059](https://dandiarchive.org/dandiset/000059)); rows = 24
7. **Oddball:** 14,653,641,118 tokens ([dandi:000253](https://dandiarchive.org/dandiset/000253)); rows = 14
8. **Illusion:** 13,246,412,456 tokens ([dandi:000248](https://dandiarchive.org/dandiset/000248)); rows = 12
9. **Huszar:** 8,812,474,629 tokens ([dandi:000552](https://dandiarchive.org/dandiset/000552)); rows = 65
10. **Steinmetz:** 7,881,422,592 tokens ([dandi:000017](https://dandiarchive.org/dandiset/000017)); rows = 39
11. **Finkelstein:** 1,313,786,316 tokens ([dandi:000060](https://dandiarchive.org/dandiset/000060)); rows = 98
12. **Giocomo:** 1,083,328,404 tokens ([dandi:000053](https://dandiarchive.org/dandiset/000053)); rows = 349
13. **Mehrotra:** 465,402,824 tokens ([dandi:000987](https://dandiarchive.org/dandiset/000987)); rows = 14
14. **Iurilli:** 388,791,426 tokens ([dandi:000931](https://dandiarchive.org/dandiset/000931)); rows = 2
15. **Gonzalez:** 366,962,209 tokens ([dandi:000405](https://dandiarchive.org/dandiset/000405)); rows = 276
16. **Li:** 260,807,325 tokens ([dandi:000010](https://dandiarchive.org/dandiset/000010)); rows = 99

Total number of tokens: 416,541,213,101. The combined dataset can be accessed from [this](https://huggingface.co/datasets/eminorhan/neural-bench-rodent) public HF repository.

### Note:
In my experience, running `merge_datasets.py` requires a patch in the `huggingface_hub` library. The HF `datasets` library doesn't do retries while loading datasets from the hub (`load_dataset`) or when pushing them to the hub (`push_to_hub`). This almost always results in connection errors for large datasets, aborting the loading or pushing of the dataset. The patch involves adding a "retry" functionality to `huggingface_hub`'s default session backend factory. Specifically, you need to update the `_default_backend_factory()` function in `huggingface_hub/utils/_http.py` with:
```python
from requests.adapters import HTTPAdapter, Retry

...

def _default_backend_factory() -> requests.Session:
    session = requests.Session()
    retries = Retry(total=20, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    if constants.HF_HUB_OFFLINE:
        session.mount("http://", OfflineAdapter(max_retries=retries))
        session.mount("https://", OfflineAdapter(max_retries=retries))
    else:
        session.mount("http://", UniqueRequestIdAdapter(max_retries=retries))
        session.mount("https://", UniqueRequestIdAdapter(max_retries=retries))
    return session
```  
or something similar (you can play with the `Retry` settings). This will prevent the premature termination of the job when faced with connection issues. 