import scrapy
import re

from utils import range_char


class Spider(scrapy.Spider):
    name = "ech"
    allowed_domains = ["m.e-chords.com"]
    start_urls = ['https://m.e-chords.com/top-artists.htm']

    def parse(self, response):
        for artist in response.xpath("//h3[@class='list-group-item-heading artista-nome']/a"):
            yield response.follow(
                artist.css('::attr(href)').get(),
                self.parse_group,
                cb_kwargs={
                    'artistName': artist.css('::text').get().strip(),
                    'artistHref': artist.css('::attr(href)').get(),
                }
            )

    def parse_group(self, response, **kwargs):
        yield {
            'type': 'artist',
            **kwargs,
        }

        for song in response.xpath("//a[@class='list-group-item']"):
            yield response.follow(
                song.css('::attr(href)').get(),
                self.parse_song,
                cb_kwargs={
                    **kwargs,
                    'songTitle': song.css('::text').get().strip(),
                    'songHref': song.css('::attr(href)').get()
                }
            )

    def parse_song(self, response, **kwargs):
        for song in response.xpath("//pre[@id='core']"):
            text = song.extract()
            text = re.sub(r'<u>([^<]+)</u>', r'[\1]', text)
            text = re.sub(r'<[^>]+>', '', text)
            yield {
                'type': 'song',
                **kwargs,
                'songText': text
            }
