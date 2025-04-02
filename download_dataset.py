from datasets import load_dataset

ds = load_dataset("eminorhan/neural-bench-rodent", num_proc=32, trust_remote_code=True)
print(f"Done!")