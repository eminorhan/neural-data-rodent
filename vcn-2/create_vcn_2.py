import os
import argparse
import numpy as np
from pynwb import NWBHDF5IO
from datasets import Dataset


def find_nwb_files(root_dir):
    """
    Crawls through a directory (including subdirectories), finds all files
    that end with ".nwb", and returns the full paths of all the found files in a list.

    Args:
        root_dir: The root directory to start the search from.

    Returns:
        A list of full paths to the found .nwb files, or an empty list if
        no files are found or if the root directory is invalid.
        Returns None if root_dir is not a valid directory.
    """

    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory.")
        return None

    nwb_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".nwb"):
                full_path = os.path.join(dirpath, filename)
                nwb_files.append(full_path)
    return nwb_files


def extract_subject_session_id(file_path):
    """
    Extracts subject and session identifier strings from a full file path.

    Args:
        file_path (str): The full file path.

    Returns:
        str: Subject identifier string.
        str: Session identifier string.
    """
    directory, filename = os.path.split(file_path)
    subdirectory = os.path.basename(directory)
    filename_without_extension, _ = os.path.splitext(filename)
    return f"{subdirectory}", f"{filename_without_extension}"


def get_args_parser():
    parser = argparse.ArgumentParser('Consolidate data in multiple files into a single file', add_help=False)
    parser.add_argument('--data_dir',default="data",type=str, help='Data directory')
    return parser


if __name__ == '__main__':

    args = get_args_parser()
    args = args.parse_args()
    print(args)

    # get all .nwb files in the sorted folder
    nwb_files = find_nwb_files(args.data_dir)
    print(f"Files: {nwb_files}")
    print(f"Total number of files: {len(nwb_files)}")

    # lists to store results for each session
    spike_counts_list, subject_list, session_list = [], [], []

    # token counter
    n_tokens = 0

    for file_path in sorted(nwb_files):
        print(f"Processing file: {file_path}")
        with NWBHDF5IO(file_path, "r") as io:
            nwbfile = io.read()

            # we will save just spike activity for now
            units = nwbfile.units.to_dataframe()
            max_time = max([u.max() if len(u)>0 else 0 for u in units['spike_times']])
            spike_counts = np.vstack([np.histogram(row, bins=np.arange(0, max_time + 0.02, 0.02))[0] for row in units['spike_times']]).astype(np.uint8)  # spike count matrix (nxt: n is #channels, t is time bins)

            # subject, session identifiers
            subject_id, session_id = extract_subject_session_id(file_path)

            # append sessions
            spike_counts_list.append(spike_counts)
            subject_list.append(subject_id)
            session_list.append(session_id)

            print(f"Spike count shape / max: {spike_counts.shape} / {spike_counts.max()}")
            n_tokens += np.prod(spike_counts.shape)

    def gen_data():
        for a, b, c in zip(spike_counts_list, subject_list, session_list):
            yield {
                "spike_counts": a,
                "subject_id": b,
                "session_id": c
                }

    ds = Dataset.from_generator(gen_data, writer_batch_size=1)
    print(f"Estimated size of dataset: {ds._estimate_nbytes()/1e9:.2f} GB")
    print(f"Number of tokens in dataset: {n_tokens} tokens")

    # push all data to hub
    ds.push_to_hub("eminorhan/vcn-2", num_shards=10, token=True)