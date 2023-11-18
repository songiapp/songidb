from scrapy_formatter import ScrapyFormatter


class Formatter(ScrapyFormatter):
    def process_artist(self, **kwargs):
        self.add_artist(kwargs['artistName'], kwargs['artistHref'].replace('https://m.e-chords.com/', ''))

    def process_song(self, **kwargs):
        self.add_song(
            kwargs['songHref'].replace('https://m.e-chords.com/chords/', '').replace('/', '-'),
            kwargs['artistHref'].replace('https://m.e-chords.com/', ''),
            kwargs['songTitle'],
            self.fix_chord_lines(kwargs['songText']))

    def filter_loaded_song(self, song):
        # only song from chords folder
        return song['songHref'].startswith('https://m.e-chords.com/chords/')
