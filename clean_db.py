import pandas as pd
import re
from io import StringIO
from html.parser import HTMLParser
import janitor

df = pd.read_excel('new_db.xlsx')

df = df.dropna()

df = df.reset_index()

df = df.drop(columns=['Unnamed: 0', 'index', 'id', 'jsonb_view'])

df = df.change_type("text", dtype=str)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


for i in range(len(df)):
    df['text'][i] = strip_tags(df['text'][i])


for i in range(len(df)):
    post = str(df['text'][i])

    post = re.sub("""[^A-Za-zА-Яа-я0-9.,:;!?()/'"«» ]""", "", post)
    post = " ".join(post.split())
    df['text'][i] = post

df.replace('', None, inplace=True)

df = df.dropna()

df = df[df['text'].map(len) > 40]

df = df.drop_duplicates(subset=['text'])

df = df.reset_index()

df = df.drop(columns=['index'])

df.to_excel('upd_db.xlsx')
