import openai
import os
import re
import requests
import sys
from num2words import num2words
import os
import pandas as pd
import numpy as np
import matplotlib
import plotly
import scipy
import sklearn
from openai.cli import display
from openai.embeddings_utils import get_embedding, cosine_similarity
import tiktoken
import openpyxl
from json import loads, dumps

openai.api_key = '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'


def preprocessing_post(db):
    df_posts = db[['text']]

    pd.options.mode.chained_assignment = None

    tokenizer = tiktoken.get_encoding("cl100k_base")
    df_posts['n_tokens'] = df_posts["text"].apply(lambda x: len(tokenizer.encode(str(x))))
    df_posts = df_posts[df_posts.n_tokens < 8192]

    print('check_1')

    df_posts['ada_v2'] = df_posts["text"].apply(lambda x: get_embedding(str(x), engine='text-embedding-ada-002'))
    df_posts.to_json('temp.json', orient='records')
    return df_posts


# search through the reviews for a specific product
def search_docs(df, user_query, top_n=3):
    embedding = get_embedding(
        user_query,
        engine="text-embedding-ada-002"
        # engine should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
    )
    df["similarities"] = df.ada_v2.apply(lambda x: cosine_similarity(x, embedding))

    res = (df.sort_values("similarities", ascending=False).head(top_n))

    res = res.reset_index()

    res = res.drop(columns=['index'])

    return res


print('check_3')
