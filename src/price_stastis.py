import math
from bs4 import BeautifulSoup
from newspaper import Article
import re
from collections import defaultdict
import json
from tqdm import tqdm


def parse_ticker(ticker_data):
    components = ticker_data.split(",")
    market_map = {"10": "HOSE", "02": "HNX", "03": "UPCOME"}

    data = {"ticker": components[1], 
            "market": market_map[components[3]],
            "reference": components[4], 
            "ceiling": components[6],
            "floor": components[5],
            "foreign_buy_vol": components[22] if components[3] == "10" else components[50],
            "foreign_sell_vol": components[23] if components[3] == "10" else components[51],
            "vol": components[55] if components[3] != "10" else components[27]}
    data["BV/SV"] = float(data["foreign_buy_vol"]) / \
        float(data["foreign_sell_vol"]
              ) if data["foreign_sell_vol"] and data["foreign_buy_vol"] else math.inf
    return data


def get_data_cafef(date):
    markets = ["HOSE", "UPCOME", "HASTC"]
    # date = "29/01/2021"
    links = {"foreign": [(market, f"https://s.cafef.vn/TraCuuLichSu2/3/{market}/{date}.chn") for market in markets], 
             "domestic": [(market, f"https://s.cafef.vn/TraCuuLichSu2/1/{market}/{date}.chn") for market in markets]}
    
    result = {}
    for key, links in links.items():
        for market, link in tqdm(links):
            article = Article(link)
            article.download()
            article.parse()
            soup = BeautifulSoup(article.html, 'html.parser')
            rows = soup.findAll('tr', id=re.compile(
                '^ctl00_ContentPlaceHolder1_ctl01_rptData_ctl[\d]+_(alt)?itemTR$'))
            
            for row in rows:
                components = row.text.split("\n")
                components = [r.strip() for r in components]

                ticker = components[1]
                if ticker not in result:
                    result[ticker] = {}

                if key == "foreign":
                    result[ticker]["market"] = market
                    result[ticker]["foreign_buy_vol"] = float(
                        components[2].replace(",", ""))
                    result[ticker]["foreign_sell_vol"] = float(
                        components[4].replace(",", ""))
                else:
                    result[ticker]["reference"] = float(components[6])
                    result[ticker]["ceiling"] = float(components[8])
                    result[ticker]["floor"] = float(components[9])
                    result[ticker]["vol"] = float(components[10].replace(",", ""))
                    result[ticker]["change"] = components[4]
    return result


if __name__ == "__main__":
    # with open("historical_price/29012021.txt", "r") as f:
    #     lines = f.readlines()
    # lines = [line.strip() for line in lines if line.startswith("DATA")]

    # data = [parse_ticker(line) for line in lines]
    # ticker_show = [(ticker["ticker"], ticker["BV/SV"]) for ticker in data]
    # ticker_show = sorted(ticker_show, key=lambda x: x[1])
    # for ticker in ticker_show:
    #     if ticker[1] != math.inf:
    #         print(ticker)
    date = "27/07/2020"
    result = get_data_cafef(date)
    date = date.replace("/", "")
    with open(f"historical_price/{date}.json", "w") as f:
        json.dump(result, f)


