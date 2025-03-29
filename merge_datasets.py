from datasets import load_dataset, concatenate_datasets, Sequence, Value

## FIXME: this whole thing is a bit hacky and clunky at the moment, will be revisited later on
## NOTE: we need to recast spike_counts to the same data type (uint8) before we can concatenate the datasets

# # vbn
# vbn = load_dataset("eminorhan/vbn", split='train', download_mode='force_redownload')
# vbn = vbn.add_column("source_dataset", ["vbn"] * len(vbn))
# print(len(vbn))

# # ibl
# ibl = load_dataset("eminorhan/ibl", split='train', download_mode='force_redownload')
# ibl = ibl.add_column("source_dataset", ["ibl"] * len(ibl))
# print(len(ibl))

# # shield
# shield = load_dataset("eminorhan/shield", split='train', download_mode='force_redownload')
# shield = shield.add_column("source_dataset", ["shield"] * len(shield))
# print(len(shield))

# # vcn
# vcn = load_dataset("eminorhan/vcn", split='train', download_mode='force_redownload')
# vcn = vcn.add_column("source_dataset", ["vcn"] * len(vcn))
# print(len(vcn))

# vcn-2
vcn_2 = load_dataset("eminorhan/vcn-2", split='train', download_mode='force_redownload')
vcn_2 = vcn_2.add_column("source_dataset", ["vcn_2"] * len(vcn_2))
print(len(vcn_2))

# # petersen
# petersen = load_dataset("eminorhan/petersen", split='train', download_mode='force_redownload')
# petersen = petersen.add_column("source_dataset", ["petersen"] * len(petersen))
# print(len(petersen))

# # concatenate all and push to hub
# neural_bench = concatenate_datasets([willett, h1, h2, m1a, m1b, m2, area2_bump, dmfc_rsg, xiao, churchland, perich, makin, lanzarini, neupane_ppc, neupane_entorhinal, papale, rajalingham])
# neural_bench.push_to_hub("eminorhan/neural-bench-rodent", token=True)