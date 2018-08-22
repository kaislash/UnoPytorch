""" 
    File Name:          UnoPytorch/label_encoding.py
    Author:             Xiaotian Duan (xduan7)
    Email:              xduan7@uchicago.edu
    Date:               8/13/18
    Python Version:     3.6.6
    File Description:   
        This file includes helper functions that are re
"""

import errno
import json
import logging
import pandas as pd


logger = logging.getLogger(__name__)


def get_labels(dict_path: str):
    """label_list = get_labels(label_encoding_dict)

    Get the list of labels from a encoding dictionary

    Args:
        dict_path (str): Path to store the dictionary for label encoding.

    Returns:
        (list): list of labels.
    """
    with open(dict_path, 'r') as f:
        label_encoding_dict = json.load(f)

    return [l for l in label_encoding_dict.keys() if not l.isdigit()]


def get_label_encoding_dict(dict_path: str, labels: iter):
    """le_dict = get_label_encoding_dict('./dict.pkl', ['some', 'labels'])

    This function takes all the labels and a path, constructs a dictionary of
    label mapping. The dictionary contains forward and backward mapping from
    keys to values.
    For example, the label encoding dictionary for ['A', 'B', 'C'] is
    {0: 'A', 1: 'B', 2: 'C', 'A': 0, 'B': 1, 'C': 2}.

    Note that due to JSON formatting, the keys cannot be integers,
    which means that the actual storage

    Args:
        dict_path (str): Path to store the dictionary for label encoding.
        labels (iter): a iterable structure of all the labels to be encoded.

    Returns:
        (dict): dictionary for forward/backward label encoding.
    """
    label_encoding_dict = None

    # Directly read the dict if it exists already
    try:
        with open(dict_path, 'r') as f:
            label_encoding_dict = json.load(f)

        if labels is not None:

            # Check if the labels in dict are indeed the labels to be encoded
            old_labels = get_labels(dict_path)

            if len(set(labels) - set(old_labels)) != 0:

                # If not, extend the label encoding dict
                old_idx = len(old_labels)
                for idx, l in enumerate(set(labels) - set(old_labels)):
                    label_encoding_dict[idx + old_idx] = l
                    label_encoding_dict[l] = idx + old_idx

                with open(dict_path, 'w') as f:
                    json.dump(label_encoding_dict, f, indent=4)

    except OSError as e:

        # If the dict does not exist, create one based on labels
        if e.errno == errno.ENOENT:
            label_encoding_dict = {}

            # Forward and backward encoding k-v pairs
            for idx, src in enumerate(labels):
                label_encoding_dict[idx] = src
                label_encoding_dict[src] = idx

            with open(dict_path, 'w') as f:
                json.dump(label_encoding_dict, f, indent=4)
        else:
            logger.error('Error loading %s.' % dict_path, exc_info=True)

    if label_encoding_dict is None:
        logger.error('Unknown error getting labels from %s.' % dict_path,
                     exc_info=True)
        raise Exception('Unable to get label dict.')

    return label_encoding_dict


def encode_label_to_int(labels: pd.Series or list,
                        dict_path: str,
                        dtype: type=int):
    """dataframe['A'] = label_encoding(dataframe['A'], './path/')

    This function encodes a series into numeric and return as a list. In the
    meanwhile, the dictionary for encoding is stored for future usage.

    Args:
        labels (pd.Series or list): Pandas series or list object for encoding.
        dict_path (str): Path to store the dictionary for label encoding.

    Returns:
        (list): list of encoded items.
        (dict): label encoding dictionary.
    """
    if type(labels) is list:
        label_list = list(set(labels))
    else:
        label_list = labels.tolist()

    label_encoding_dict: dict \
        = get_label_encoding_dict(dict_path, list(set(label_list)))
    encoded_list = [dtype(label_encoding_dict[s]) for s in label_list]

    return encoded_list, label_encoding_dict


def encode_int_to_onehot(labels: pd.Series or list,
                         num_classes: int,
                         dtype: type):

    if type(labels) is list:
        label_list = list(set(labels))
    else:
        label_list = labels.tolist()

    encoded_list = []

    for l in label_list:
        encoded = [0] * num_classes
        encoded[l] = 1
        encoded = list(map(dtype, encoded))
        encoded_list.append(encoded)

    return encoded_list








