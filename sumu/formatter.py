from scrapy_formatter import ScrapyFormatter


class Formatter(ScrapyFormatter):
    def __init__(self, pkg):
        super().__init__(pkg)
        self.by_lang_list = ['cs', 'de', 'en', 'es', 'fr', 'it', 'sk']

    def process_song(self, **kwargs):
        self.add_song(
            kwargs['artistName'],
            kwargs['songTitle'],
            kwargs['songText'])

    def filter_loaded_song(self, song):
        # only song with chords
        return '[' in song['songText']
