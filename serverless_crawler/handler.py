import json
import datetime
import logging
import os
import boto3
import lxml

# for scraping
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests as req

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Company Code
stock_code = int("005930")

# target url
url = f"https://finance.naver.com/item/sise_day.nhn?code=005930"

def run(event, context):
    
    s3 = boto3.client('s3')

    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    logger.info("crawling is running at " + str(current_time))

    bucket = "jy-crawling"
    filename = current_time + ".json"
    filepath = "/tmp/" + filename

    s3_path = current_time + "/" + filename

    
    with open(filepath, "w") as json_file:
        crawled = crawler(url)
        logger.info(crawled)

        json.dump(crawled, json_file)

        s3.upload_file(filepath, bucket, s3_path)

    os.remove(filepath)


def crawler(url):
    headers = {'User-agent': 'Mozilla/5.0'}
    r = req.get(url, verify = False, headers = headers)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


def test_run():
    
    crawled = crawler(url)

    return crawled


# test
if __name__ == "__main__":
    print(crawler(url))
