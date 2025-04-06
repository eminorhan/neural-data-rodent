from datasets import concatenate_datasets, load_dataset, DatasetDict


def concatenate_hf_datasets_and_push(repo_list, new_repo_name):
    """
    Concatenates Hugging Face datasets from a list of repositories and pushes to the Hugging Face Hub.
    Adds a 'source_dataset' column to each component dataset, using only the name after the backslash.

    Args:
        repo_list (list): A list of Hugging Face dataset repository names.
        new_repo_name (str): The name for the new concatenated dataset repository.
    """

    ds_list = []

    for repo_name in repo_list:
        ds = load_dataset(repo_name, split="train")
        source_name = repo_name.split("/")[-1] # Extract the name after the last backslash

        ds = ds.add_column("source_dataset", [source_name] * len(ds))

        ds_list.append(ds)
        print(f"Dataset {repo_name} has been added.")

    # concatenate component datasets
    ds = concatenate_datasets(ds_list)
    ds = ds.train_test_split(test_size=0.01, shuffle=True)

    # push to hub
    ds.push_to_hub(new_repo_name, max_shard_size="1GB", token=True)
    print(f"Concatenated dataset pushed to {new_repo_name} on the Hugging Face Hub. Train / test len: {len(ds["train"])} / {len(ds["test"])}")


if __name__ == '__main__':

    # list of component dataset repositories to be concatenated
    repo_list = [
        "eminorhan/vbn", "eminorhan/ibl", "eminorhan/shield", "eminorhan/vcn", "eminorhan/vcn-2", "eminorhan/v2h", "eminorhan/petersen",
        "eminorhan/oddball", "eminorhan/illusion", "eminorhan/huszar", "eminorhan/steinmetz", "eminorhan/steinmetz-2", "eminorhan/finkelstein",
        "eminorhan/giocomo", "eminorhan/mehrotra", "eminorhan/iurilli", "eminorhan/gonzalez", "eminorhan/li" 
    ]
    new_repo_name = "neural-bench-rodent"

    concatenate_hf_datasets_and_push(repo_list, new_repo_name)