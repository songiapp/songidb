from scrapy_formatter import ScrapyFormatter
import re

class Formatter(ScrapyFormatter):
    def process_artist(self, **kwargs):
        m = re.match(r'.*idskupiny=(\d+)', kwargs['artistHref'])
        self.add_artist(kwargs['artistName'], m[1])

    def process_song(self, **kwargs):
        ma = re.match(r'.*idskupiny=(\d+)', kwargs['artistHref'])
        ms = re.match(r'.*idpiesne=(\d+)', kwargs['songHref'])
        self.add_song(
            ms[1],
            ma[1],
            kwargs['songTitle'],
            kwargs['songText'])

    def filter_loaded_song(self, song):
        # only song with chords
        return '[' in song['songText']
