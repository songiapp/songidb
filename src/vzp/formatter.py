from scrapy_formatter import ScrapyFormatter

class Formatter(ScrapyFormatter):
    def process_artist(self, **kwargs):
        self.add_artist(kwargs['artistName'], kwargs['artistHref'][1:])

    def process_song(self, **kwargs):
        self.add_song(
            kwargs['songHref'][1:].replace('/', '-'),
            kwargs['artistHref'][1:],
            kwargs['songTitle'],
            kwargs['songText'])
