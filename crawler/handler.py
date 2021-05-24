import json
import requests as req
from bs4 import BeautifulSoup
import datetime
import logging
import os
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run(event, context):
    
    s3 = boto3.client('s3')

    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    logger.info("crawling is running at " + str(current_time))

    bucket = "jy-crawling"
    filename = current_time + ".json"
    filepath = "/tmp/" + filename

    s3_path = current_time + "/" + filename

    url = "https://www.daangn.com/hot_articles"
    
    with open(filepath, "w") as json_file:
        crawled = crawler(url)
        logger.info(crawled)

        json.dump(crawled, json_file)

        s3.upload_file(filepath, bucket, s3_path)

    os.remove(filepath)


def crawler(url):
    r = req.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    output = soup.p.string
    return output
