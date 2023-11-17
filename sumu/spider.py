import scrapy
import re

from utils import range_char


class Spider(scrapy.Spider):
    name = "vzp"
    # allowed_domains = ["www.seznam.cz"]
    allowed_domains = ["supermusic.cz"]
    start_urls = ["https://supermusic.cz/skupiny.php?od=k"]

    # start_urls = (f'https://supermusic.cz/skupiny.php?od=${letter}' for letter in
    #               range_char('a', 'z'))

    # start_urls = ["https://www.velkyzpevnik.cz/"]
    # start_urls = ["https://www.seznam.cz/"]

    # custom_settings = {'JOBDIR': '.tmp.vzp'}

    def parse(self, response):
        count = 0
        for artist in response.xpath('//a'):
            if artist.css('::attr(class)').get() == 'interpretzoznam':
                continue

            href = artist.css('::attr(href)').get()

            if not href.startswith('skupina.php?idskupiny='):
                continue

            count += 1
            if count > 3:
                break

            # yield {
            #     'type': 'artist',
            #     'artistName': artist.css('::text').get().strip(),
            #     'artistHref': artist.css('::attr(href)').get(),
            # }

            yield response.follow(
                artist.css('::attr(href)').get(),
                self.parse_group,
                cb_kwargs={
                    'artistName': artist.css('::text').get().strip(),
                    'artistHref': artist.css('::attr(href)').get(),
                }
            )

    def parse_group(self, response, **kwargs):
        count = 0
        processed_songs = []

        yield {
            'type': 'artist',
            **kwargs,
        }

        for song in response.xpath('//a'):
            href = song.css('::attr(href)').get()

            if not href.startswith('skupina.php?idpiesne='):
                continue

            title = song.css('::text').get()
            if not title:
                continue

            title = title.strip()

            count += 1
            if count > 3:
                break

            if title.upper() in processed_songs:
                continue
            processed_songs.append(title.upper())

            yield response.follow(
                song.css('::attr(href)').get(),
                self.parse_song,
                cb_kwargs={
                    **kwargs,
                    'songTitle': title,
                    'songHref': song.css('::attr(href)').get()
                }
            )

        # for song in response.xpath("//p[@class='song-title']/.."):
        #     yield response.follow(
        #         song.css('::attr(href)').get(),
        #         self.parse_song,
        #         cb_kwargs={
        #             **kwargs,
        #             'songTitle': song.css('.song-title::text').get().strip(),
        #             'songHref': song.css('::attr(href)').get()
        #         }
        #     )

        # for song in response.xpath("//p[@class='song-title']/.."):
        #     yield {
        #         **kwargs,
        #         'name': song.css('.song-title::text').get().strip(),
        #         'href': song.css('::attr(href)').get(),
        #         }

    def parse_song(self, response, **kwargs):
        for song in response.xpath("//td[@class='piesen']/font[@color='black']"):
            text = song.extract()
            text = re.sub('<script language=.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL).strip()
            text = re.sub('<pre>.*?</pre>', '', text).strip()
            text = re.sub('<a class="sup[^>]+>([^<]*)</a>', r'[\1]', text).strip()
            text = re.sub('<br/>', '\n', text).strip()
            text = re.sub(r'<[^>]+>', '', text).strip()

            if not text:
                continue

            yield {
                'type': 'song',
                **kwargs,
                'songText': text
            }
