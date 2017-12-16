# -*- coding: cp936 -*-

# use pip install futures to install
from concurrent.futures import ThreadPoolExecutor as Pool
import requests
import os
import time
import re
import logging
import sys

# because chinese path and the web site is encoding by gbk
reload(sys)
sys.setdefaultencoding('gbk')

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(message)s')
# format='[line:%(lineno)d]%(levelname)s %(message)s')
logger = logging.getLogger(__name__)

BASE_PATH = os.path.dirname(__file__)
logger.info("BASE_PATH: %s", BASE_PATH)


class JishuDownload(object):

    def __init__(self, thread_num=20, retry_num=5):
        self.retry_num = retry_num

        self.client = requests.Session()
        # for connection poll full error
        self.adapter = requests.adapters.HTTPAdapter(
            max_retries=retry_num, pool_connections=thread_num,
            pool_maxsize=thread_num * 2)
        self.client.headers["User-Agent"] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.client.mount('http://', self.adapter)
        self.client.mount('https://', self.adapter)

        self.pool = Pool(max_workers=thread_num)

        self.timeout = 60
        self.main_timeout = 2
        self.url_pattern = re.compile("<img src='(.+?)'")
        self.title_pattern = re.compile('<h4>(.+?)</h4>', re.I)
        self.path = None

    def downloadAll(self, url):
        urls = self.praseUrl(url)
        logger.info("try to down img to :%s", self.path)
        results = self.pool.map(self.downloadJpg, urls)
        success = 0
        fail = 0
        for result in results:
            if result:
                success += 1
            else:
                fail += 1
        logger.info("success: %s, fail: %s", success, fail)

    def praseUrl(self, url):
        res = self.client.get(url, timeout=self.main_timeout)
        datas = re.sub('______', '.', res.content.decode('gbk'))
        urls = self.url_pattern.findall(datas)
        try:
            title = self.title_pattern.search(datas)
            title = title.group(1)
            self.path = os.path.join(BASE_PATH, title)
        except Exception as e:
            logger.warn("get title fail: %s", e)
            self.path = BASE_PATH
        logger.info("path: %s", self.path)
        os.mkdir(self.path)
        for url in urls[::-1]:
            if url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.gif'):
                pass
            else:
                urls.remove(url)
        # try:
            # os.mkdir(self.path)
        # except Exception as e:
            # logger.warn("mkdir %s fail: %s", self.path, e)
        return urls

    def downloadJpg(self, url):
        error_num = 0
        res = ''
        # retry many times: retry_num * 2, because requests also retry
        while error_num < self.retry_num:
            try:
                res = self.client.get(url, timeout=self.timeout)
                break
            except Exception as e:
                logger.warn("----- %s fail for %s time", url, error_num)
                error_num += 1

        if not res:
            logger.warn("%s fail", url)
            return False
        filename = url.split('/')[-1]
        with open(os.path.join(self.path, filename), 'wb') as f:
            f.write(res.content)
        logger.info("%s success", filename)
        return True


if __name__ == '__main__':

    mainurl = raw_input('input url:')
    time_start = time.time()
    jd = JishuDownload()
    jd.downloadAll(mainurl)
    logger.info("download cost time: %ss", time.time() - time_start)
