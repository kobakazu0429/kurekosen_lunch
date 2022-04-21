import os
import re
import datetime
import itertools
import locale
import dotenv
import tabula
import numpy as np
import tweepy


def prepare():
    dotenv.load_dotenv()
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")


def get_menu():
    pdf_path = "https://www.kure-nct.ac.jp/campuslife/pdf/menu.pdf"

    dfs = tabula.read_pdf(pdf_path, area=[
        [100, 55, 380, 205],
        [100, 210, 380, 360],
        [100, 370, 380, 520],
        [100, 525, 380, 675],
        [100, 680, 380, 830]
    ], lattice=True, pages="all", pandas_options={"header": None, "index": None})

    ignore_lists = [
        "エネルギー",
        "たんぱく質",
        "脂質",
        "炭水化物",
        "食塩相当量",
        "g",
        "kcal",
        "アレルゲン",
        "小麦卵乳そば",
        "●",
    ]
    ignore_pattern = "|".join(ignore_lists)

    def ignore_by_lists(v):
        if type(v) is not str:
            return v

        if re.search(ignore_pattern, v):
            return np.nan
        else:
            return v

    def normalize(df):
        df = df.applymap(ignore_by_lists)
        df = df.dropna(how="all")
        df = df.dropna(axis="columns")
        df = df.applymap(lambda x: x.replace("\r", ""))

        return df

    menus = list(filter(lambda df: not df.empty, map(normalize, dfs)))

    now = datetime.datetime.now()
    today = now.strftime("%-m月%-d日(%a)")

    today_menu = list(filter(lambda menu: menu.iat[0, 0] == today, menus))

    if len(today_menu) != 1:
        print(today_menu)
        raise Exception

    today_menu_str = "\n".join(
        list(itertools.chain.from_iterable(today_menu[0].values.tolist()))
    )
    return today_menu_str


def tweet(text: str):
    client = tweepy.Client(
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_KEY_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
    )
    client.create_tweet(text=text)


def main():
    try:
        prepare()
        menu = get_menu()
        print(menu)
        tweet(menu)
    except:
        tweet("メニューがないか、問題が発生しました。\ncc: @kobakazu0429")


if __name__ == "__main__":
    main()
