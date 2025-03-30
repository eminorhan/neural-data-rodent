from datasets import concatenate_datasets, load_dataset, DatasetDict

def concatenate_hf_datasets_and_push(repo_list, new_repo_name):
    """
    Concatenates Hugging Face datasets from a list of repositories and pushes to the Hugging Face Hub.
    Adds a 'source_dataset' column to each component dataset, using only the name after the backslash.

    Args:
        repo_list (list): A list of Hugging Face dataset repository names.
        new_repo_name (str): The name for the new concatenated dataset repository.
        private (bool, optional): Whether to create a private repository. Defaults to False.
    """

    train_datasets = []
    test_datasets = []

    for repo_name in repo_list:
        dataset = load_dataset(repo_name, download_mode='force_redownload')
        source_name = repo_name.split("/")[-1] # Extract the name after the last backslash

        train_data = dataset["train"].add_column("source_dataset", [source_name] * len(dataset["train"]))
        test_data = dataset["test"].add_column("source_dataset", [source_name] * len(dataset["test"]))

        train_datasets.append(train_data)
        test_datasets.append(test_data)
        print(f"Dataset {repo_name} has been added.")

    # concatenate component datasets
    concatenated_train = concatenate_datasets(train_datasets)
    concatenated_test = concatenate_datasets(test_datasets)
    concatenated_dataset = DatasetDict({"train": concatenated_train, "test": concatenated_test})

    # push to hub
    concatenated_dataset.push_to_hub(new_repo_name, num_shards={'train': len(concatenated_train), 'test': len(concatenated_test)}, token=True)
    print(f"Concatenated dataset pushed to {new_repo_name} on the Hugging Face Hub.")


if __name__ == '__main__':

    # list of component dataset repositories to be concatenated
    repo_list = [
        "eminorhan/vbn", "eminorhan/ibl", "eminorhan/shield", "eminorhan/vcn", "eminorhan/vcn-2", "eminorhan/petersen",
        "eminorhan/oddball", "eminorhan/illusion", "eminorhan/huszar", "eminorhan/steinmetz", "eminorhan/finkelstein",
        "eminorhan/giocomo", "eminorhan/mehrotra", "eminorhan/iurilli", "eminorhan/gonzalez", "eminorhan/li" 
    ]
    new_repo_name = "neural-bench-rodent"

    concatenate_hf_datasets_and_push(repo_list, new_repo_name)