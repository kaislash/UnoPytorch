""" 
    File Name:          UnoPytorch/df_dataset.py
    Author:             Xiaotian Duan (xduan7)
    Email:              xduan7@uchicago.edu
    Date:               8/16/18
    Python Version:     3.6.6
    File Description:   

"""

import numpy as np
import pandas as pd
import torch.utils.data as data


class DFDataset(data.Dataset):

    def __init__(
            self,
            dataframe: pd.DataFrame,
            dtype: type = np.float32, ):

        self.__dataframe = dataframe
        self.__len = len(dataframe)
        self.__dtype = dtype

    def __len__(self):
        return self.__len

    def __getitem__(self, index):
        return self.__dataframe.iloc[index].values.astype(self.__dtype)
