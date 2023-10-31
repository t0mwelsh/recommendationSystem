# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:36:49 2023

@author: Lillemoen
"""

import pandas as pd
office_df = pd.read_csv('Office_Products.csv', names=["item","user","rating","timestamp"])
book_df = pd.read_csv('Books.csv', names=["item","user","rating","timestamp"], nrows=25000000)

ratings_per_user = office_df.groupby('user')['rating'].count()
average_ratings_per_user = ratings_per_user.mean()

unique_items_count = office_df['item'].nunique()

def most_significant_rows(df, column, kept_rows):
    column_ratings_count = df[column].value_counts()
    sorted_ratings = column_ratings_count.sort_values(ascending=False)
    most_significant_rows = sorted_ratings.head(kept_rows).index
    
    return most_significant_rows

# significant_items = most_significant_rows(df, 'item', 10000)
# items_df = df[df['item'].isin(significant_items)]

significant_users = most_significant_rows(book_df, 'user', 10000)
users_df = book_df[book_df['user'].isin(significant_users)]


# # items_df = df[df['item'].isin(significant_items)]
# # users_df = df[df['user'].isin(significant_users)]
    
# significant_df = df[(df['item'].isin(significant_items)) & 
#                     (df['user'].isin(significant_users))]

def filter_dataframe(df, user_min, item_min, max_iter=10):
    count = 0
    while(df['item'].value_counts().min() < item_min or 
          df['user'].value_counts().min() < user_min):
        
        # Filter rows to keep only items with >= item_min ratings
        item_ratings_count = df['item'].value_counts()
        popular_items = item_ratings_count[item_ratings_count >= item_min].index
        df = df[df['item'].isin(popular_items)]

        # Filter rows to keep only users with >= user_min ratings
        user_ratings_count = df['user'].value_counts()
        active_users = user_ratings_count[user_ratings_count >= user_min].index
        df = df[df['user'].isin(active_users)]
        
        count += 1
        #if count >= max_iter:
            #break

    return df

filtered_office_df = filter_dataframe(office_df, 5, 50)
filtered_book_df = filter_dataframe(book_df, 8, 50)
filtered_book_df = filter_dataframe(book_df, 10, 50)

filtered_book_df.to_csv('filtered_book_df.csv', index=False)

user_ratings_count = filtered_book_df.groupby('user').size()
valid_users = user_ratings_count[user_ratings_count >= 100].index
xtra_filtered_df = filtered_book_df[filtered_book_df['user'].isin(valid_users)]

item_ratings_count = xtra_filtered_df.groupby('item').size()
valid_items = item_ratings_count[item_ratings_count >= 100].index
xtra_filtered_df = xtra_filtered_df[xtra_filtered_df['item'].isin(valid_items)]

xtra_filtered_df.to_csv('xtra_filtered_book_df.csv', index=False)

# To look up an item type https://www.amazon.co.uk/gp/aw/cr/ and then add the item