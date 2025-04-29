Visual Behavior - Neuropixels dataset from Allen Institute. 

**Dataset URL:** https://dandiarchive.org/dandiset/000713

To download the latest version of the dataset:
```python
dandi download DANDI:000713
```

To process the data and push it to HF hub as a separate dataset repository:
```python
python create_vbn.py
```

Long sessions (>10M tokens) are divided into equal-sized chunks of 10M tokens at most. For a 1000-channel recording, this is roughly equivalent to 200-second long chunks. For a 100-channel recording, it is roughly equivalent to 2000-second long chunks.

**Session count:** 153

**Token count:** 153,877,057,200

**HF repo:** https://huggingface.co/datasets/eminorhan/vbn

**Recorded area & stimulus, task, or behavior:** Recordings from mouse visual cortical areas including VISp, VISl, VISal, VISrl, VISam, and VISpm (up to 6 probes at a time). Multiple subcortical areas are also typically recorded, including visual thalamic areas LGd and LP as well as units in the hippocampus and midbrain. The task is a visual change detection task.

**Paper URL:** https://portal.brain-map.org/circuits-behavior/visual-behavior-neuropixels

```
@techreport{allen2022,
  author      = {{Allen Institute for Brain Science}},
  title       = {Allen Brain Observatory: Visual Behavior Neuropixels - Technical Whitepaper},
  institution = {Allen Institute for Brain Science},
  year        = {2022},
  url         = {https://portal.brain-map.org/circuits-behavior/visual-behavior-neuropixels},
  note        = {Accessed: 2025-04-28} 
}
```