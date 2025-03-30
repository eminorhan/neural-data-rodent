IBL dataset. Dataset URL: https://dandiarchive.org/dandiset/000409

To download:
```python
dandi ls -r DANDI:000409 > log.txt
grep 'path:' log.txt | awk '{print $2}' | grep 'processed-only' > processed_paths.txt
sh download_ibl.sh
```

Token count: 69,147,814,139

HF repo: https://huggingface.co/datasets/eminorhan/ibl
