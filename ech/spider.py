import scrapy
import re

from utils import range_char


class Spider(scrapy.Spider):
    name = "ech"
    allowed_domains = ["m.e-chords.com"]
    start_urls = ['https://m.e-chords.com/top-artists.htm']

    def parse(self, response):
        for artist in response.css('.interpret'):
            yield response.follow(
                artist.css('::attr(href)').get(),
                self.parse_group,
                cb_kwargs={
                    'artistName': artist.css('::text').get().strip(),
                    'artistHref': artist.css('::attr(href)').get(),
                }
            )
        # for artist in response.css('.interpret'):
        #     yield {
        #         'name': artist.css('::text').get().strip(),
        #         'href': artist.css('::attr(href)').get(),
        #         }

    def parse_group(self, response, **kwargs):
        yield {
            'type': 'artist',
            **kwargs,
        }

        for song in response.xpath("//p[@class='song-title']/.."):
            yield response.follow(
                song.css('::attr(href)').get(),
                self.parse_song,
                cb_kwargs={
                    **kwargs,
                    'songTitle': song.css('.song-title::text').get().strip(),
                    'songHref': song.css('::attr(href)').get()
                }
            )

        # for song in response.xpath("//p[@class='song-title']/.."):
        #     yield {
        #         **kwargs,
        #         'name': song.css('.song-title::text').get().strip(),
        #         'href': song.css('::attr(href)').get(),
        #         }

    def parse_song(self, response, **kwargs):
        for song in response.xpath("//pre[@class='format']"):
            yield {
                'type': 'song',
                **kwargs,
                'songText': re.sub(
                    r'<[^>]+>',
                    '',
                    re.sub(r'<span class="chord"[^>]*>([^<]+)</span>', r'[\1]', song.extract())
                )
            }
