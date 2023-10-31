# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 15:06:20 2023

@author: Lillemoen
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv('xtra_filtered_book_df.csv')

average_value = df['rating'].mean()

pivot_table = df.pivot_table(index='user', columns='item',
                            values='rating', fill_value=average_value)

pivot_table.to_csv('filtered_pivot_table.csv')

knn = NearestNeighbors(n_neighbors=6)
knn.fit(pivot_table)

# for i in range(10):
#     print(knn.kneighbors([pivot_table.iloc[i]], return_distance=False))


