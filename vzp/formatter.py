import re
from scrapy_formatter import ScrapyFormatter

class Formatter(ScrapyFormatter):
    def process_song(self, **kwargs):
        self.add_song(
            kwargs['artistName'],
            kwargs['songTitle'],
            self.fix_chord_lines(kwargs['songText']))
