import shutil
import os
import sys

# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(current_dir)

import vzp
import zp8
import sumu
import gzip
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def getPackage(name):
    match name:
        case 'vzp':
            return vzp
        case 'zp8':
            return zp8
        case 'sumu':
            return sumu


pkg = sys.argv[1]
cmd = sys.argv[2]

match cmd:
    case 'crawl':
        settings = get_project_settings()
        settings[
            'USER_AGENT'] = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
        settings['COOKIES_ENABLED'] = False
        settings['JOBDIR'] = f'.tmp/{pkg}'
        settings['FEEDS'] = {
            f'{pkg}/crawled.jsonl': {'format': 'jsonlines', 'overwrite': False}
        }
        process = CrawlerProcess(settings)
        spider = getPackage(pkg).Spider
        process.crawl(spider)
        process.start()
    case 'format':
        formatter = getPackage(pkg).Formatter(pkg)
        formatter.run()
    case 'compress':
        with open(f'{pkg}/crawled.jsonl', 'rb') as f_in:
            with gzip.open(f'{pkg}/crawled.jsonl.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    case 'reset':
        shutil.rmtree(f'.tmp/{pkg}', True)
        try:
            os.remove(f'{pkg}/crawled.jsonl')
        except FileNotFoundError:
            pass
        try:
            os.remove(f'{pkg}/db.json')
        except FileNotFoundError:
            pass
