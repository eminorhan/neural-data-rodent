import os
import math
import argparse
import numpy as np
from scipy.io import loadmat
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
            if filename.endswith(".mat"):
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


def create_spike_count_matrix(x, bin_size=0.02):
    """
    Processes a list of lists containing spike times and cluster indices, 
    differentiating clusters across probes, to create a spike count matrix.

    Args:
        x: A list of 8 sublists, where each sublist contains spike times and cluster indices.
           x[probe_idx][0] -> spike times (t, 1) numpy array
           x[probe_idx][1] -> cluster indices (t, 1) numpy array
        bin_size: The size of each time bin in seconds (default: 0.02 seconds).

    Returns:
        A numpy array of shape (n_clusters, n_timebins) representing spike counts per cluster and time bin.
    """

    all_spike_times = []
    all_cluster_indices = []
    
    # offset the cluster indices so that they are unique across probes.
    cluster_offset = 0
    for probe_idx, probe in enumerate(x):
        
        print(f"(Probe {probe_idx}) Spike times     min/max/dtype: {probe[0].min()}, {probe[0].max()}, {probe[0].dtype}")
        print(f"(Probe {probe_idx}) Cluster indices min/max/dtype: {probe[1].min()}, {probe[1].max()}, {probe[1].dtype}")

        spike_times, cluster_indices = probe[0], probe[1].astype(np.uint16)
        all_spike_times.extend(spike_times.flatten().tolist())
        all_cluster_indices.extend((cluster_indices.flatten() + cluster_offset).tolist())
        cluster_offset += np.max(cluster_indices) # set the offset to be larger than the max cluster index in the current probe.

    all_spike_times = np.array(all_spike_times)
    all_cluster_indices = np.array(all_cluster_indices)

    # find the maximum time across all probes to determine the number of time bins
    max_time = np.max(all_spike_times)
    n_timebins = int(np.ceil(max_time / bin_size))

    # find the maximum cluster index to determine the number of clusters
    max_cluster = int(np.max(all_cluster_indices))
    n_clusters = max_cluster

    # initialize the spike time matrix with zeros
    spike_time_matrix = np.zeros((n_clusters, n_timebins), dtype=np.uint8)

    # populate the spike time matrix
    for spike_time, cluster_index in zip(all_spike_times, all_cluster_indices):
        time_bin = int(spike_time / bin_size)
        spike_time_matrix[int(cluster_index)-1, time_bin] += 1

    return spike_time_matrix


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

        data = loadmat(file_path)['spks'][0]
        spike_counts = create_spike_count_matrix(data)

        # subject, session identifiers
        subject_id, session_id = extract_subject_session_id(file_path)

        # append sessions
        spike_counts_list.append(spike_counts)
        subject_list.append(subject_id)
        session_list.append(session_id)

        print(f"Spike count dtype / shape / max: {spike_counts.dtype} / {spike_counts.shape} / {spike_counts.max()}")
        n_tokens += np.prod(spike_counts.shape)

    def gen_data():
        for a, b, c in zip(spike_counts_list, subject_list, session_list):
            yield {
                "spike_counts": a,
                "subject_id": b,
                "session_id": c
                }

    ds = Dataset.from_generator(gen_data, writer_batch_size=1)
    ds = ds.train_test_split(test_size=math.ceil(len(ds)/100), shuffle=False)
    print(f"Number of tokens in dataset: {n_tokens} tokens")
    print(f"Number of rows in train: {len(ds["train"])}")
    print(f"Number of rows in test: {len(ds["test"])}")

    # push all data to hub (we set num_shards=len(ds), otherwise we get list index overflow error in loading arrow file)
    ds.push_to_hub("eminorhan/steinmetz-2", num_shards={'train': len(ds["train"]), 'test': len(ds["test"])}, token=True)