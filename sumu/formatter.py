from scrapy_formatter import ScrapyFormatter
import re

class Formatter(ScrapyFormatter):
    def __init__(self, pkg):
        super().__init__(pkg)
        self.by_lang_list = ['cs', 'de', 'en', 'es', 'fr', 'it', 'sk']

    def process_song(self, **kwargs):
        artist = re.sub(r'\s*\([\d]+\)\s*$', '', kwargs['artistName'])
        self.add_song(
            artist,
            kwargs['songTitle'],
            self.convert_labels(kwargs['songText']))

    def filter_loaded_song(self, song):
        # only song with chords
        return '[' in song['songText']
