Visual Behavior - Neuropixels dataset from Allen Institute. Dataset URL: https://dandiarchive.org/dandiset/000713

To download the latest version of the dataset:
```python
dandi download DANDI:000713
```

To process the data and push it to HF hub as a separate dataset repository:
```python
python create_vbn.py
```

Long sessions (>10M tokens) are divided into equal-sized chunks of 10M tokens at most. For a 1000-channel recording, this is roughly equivalent to 200-second long chunks. For a 100-channel recording, it is roughly equivalent to 2000-second long chunks.

Session count: 153

Token count: 153,877,057,200

HF repo: https://huggingface.co/datasets/eminorhan/vbn
