IBL dataset. 

**Dataset URL:** https://dandiarchive.org/dandiset/000409

To download:
```python
dandi ls -r DANDI:000409 > log.txt
grep 'path:' log.txt | awk '{print $2}' | grep 'processed-only' > processed_paths.txt
sh download_ibl.sh
```

**Token count:** 69,147,814,139

**HF repo:** https://huggingface.co/datasets/eminorhan/ibl

**Recorded area & stimulus, task, or behavior:** Brain-wide recordings from mice during a decision-making task with sensory, motor, and cognitive components.

**Paper URL:** https://www.biorxiv.org/content/10.1101/2023.07.04.547681v4

```
@article{ibl2023,
  title={A brain-wide map of neural activity during complex behaviour},
  author={International Brain Laboratory and Benson, Brandon and Benson, Julius and Birman, Daniel and Bonacchi, Niccol{\`o} and Bougrova, Kc{\'e}nia and Bruijns, Sebastian A and Carandini, Matteo and Catarino, Joana A and Chapuis, Gaelle A and others},
  journal={bioRxiv},
  pages={2023--07},
  year={2023},
  publisher={Cold Spring Harbor Laboratory}
}
```
