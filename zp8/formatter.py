import xml.etree.ElementTree as ET
from scrapy_formatter import ScrapyFormatter
import re

def replace_labels(text):
    return re.sub(r'^\.([^\n]+)(\n|$)', r'# \1\n', text, flags=re.MULTILINE)

class Formatter(ScrapyFormatter):
    def __init__(self, pkg):
        super().__init__(pkg)

    def run(self):
        song = []
        tree = ET.parse('zp8/zp.xml')
        root = tree.getroot()
        for child in root:
            title = child.findtext('{http://zpevnik.net/InetSongDb.xsd}title')
            id = child.findtext('{http://zpevnik.net/InetSongDb.xsd}ID')
            text = child.findtext('{http://zpevnik.net/InetSongDb.xsd}songtext')
            groupname = child.findtext('{http://zpevnik.net/InetSongDb.xsd}groupname')
            lang = child.findtext('{http://zpevnik.net/InetSongDb.xsd}lang')
            author = child.findtext('{http://zpevnik.net/InetSongDb.xsd}author')
            remark = child.findtext('{http://zpevnik.net/InetSongDb.xsd}remark')

            self.add_song(groupname, title, replace_labels(text), lang, {'author': author, 'remark': remark})

        self.save_database()
