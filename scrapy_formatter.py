import gzip
import json
import pathlib
import os
from unidecode import unidecode
import re
import langdetect


def kebab_case(s):
    return '-'.join(
        re.sub(r"(\s|_|-|\.)+", " ",
               re.sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                      lambda mo: ' ' + mo.group(0).lower(), re.sub(r'[^a-zA-Z0-9\-_\s.]', '', s))).split())


class ScrapyFormatter:
    def __init__(self, pkg, **kwargs):

        self.songs = []
        self.artists = []
        self.pkg = pkg
        self.by_lang = kwargs['by_lang']
        self.by_lang_list = kwargs['by_lang_list']

        self.artists_by_id = {}

    def process_artist(self, **kwargs):
        pass

    def process_song(self, **kwargs):
        pass

    def add_artist(self, name, id=None):
        artist_id = id if id else kebab_case(unidecode(name)) or 'no-artist'
        # if not id:
        #     # create id from name
        #     id = kebab_case(unidecode(name)) or 'no-artist'

        if artist_id in self.artists_by_id:
            return artist_id
        artist = {
            'id': artist_id,
            'name': name,
        }
        self.artists_by_id[artist_id] = artist
        self.artists.append(artist)
        return artist_id

    def add_song(self, id, artist_id, title, text, lang=None, args: dict = {}):
        song_obj = {
            'id': id,
            'title': title,
            'artistId': artist_id,
            'text': text,
            **{k: v for k, v in args.items() if v}
        }
        lang = None
        try:
            lang = lang or langdetect.detect(re.sub(r'\[.*?]', '', text)) or 'na'
        except:
            lang = 'na'

        if lang:
            song_obj['lang'] = lang

        self.songs.append(song_obj)

    def filter_loaded_song(self, song):
        return True

    def open_file(self):
        if os.path.isfile(f'{self.pkg}/crawled.jsonl'):
            return open(f'{self.pkg}/crawled.jsonl')
        if os.path.isfile(f'{self.pkg}/crawled.jsonl.gz'):
            return gzip.open(f'{self.pkg}/crawled.jsonl.gz', 'rt')

        raise Exception('Input file crawled.json not found')

    def run(self):
        loaded_songs = []

        with self.open_file() as f:
            for line in f:
                obj = json.loads(line)
                match obj['type']:
                    case 'artist':
                        self.process_artist(**obj)
                    case 'song':
                        if self.filter_loaded_song(obj):
                            loaded_songs.append(obj)

        for song in loaded_songs:
            self.process_song(**song)

        self.save_database()

    def do_save_file(self, file, songs):
        used_artists = set(s['artistId'] for s in songs)
        pathlib.Path(file).write_text(json.dumps({
            'artists': [a for a in self.artists if a['id'] in used_artists],
            'songs': songs,
        }, indent=2, ensure_ascii=False), encoding='utf-8')

    def save_database(self):
        if self.by_lang or self.by_lang_list:
            langs = self.by_lang_list.split(',') if self.by_lang_list else set(s['lang'] for s in self.songs)

            for lang in langs:
                self.do_save_file(f'{self.pkg}/db-{lang}.json', [s for s in self.songs if s['lang'] == lang])
        else:
            self.do_save_file(f'{self.pkg}/db.json', self.songs)

    def join_chord_line(self, chord_line, text_line):
        chord_pos = 0
        text_pos = 0
        res = ""
        while text_pos < len(text_line):
            if chord_pos < len(chord_line) and chord_line[chord_pos] == "[":
                res += "["
                chord_pos += 1
                chord_len = 0
                while chord_pos < len(chord_line) and chord_line[chord_pos] != "]":
                    res += chord_line[chord_pos]
                    chord_pos += 1
                    chord_len += 1
                res += "]"
                if chord_pos < len(chord_line) and chord_line[chord_pos] == "]":
                    chord_pos += 1

                while chord_len > 0 and text_pos < len(text_line):
                    res += text_line[text_pos]
                    text_pos += 1
                    chord_len -= 1

                continue
            res += text_line[text_pos]
            chord_pos += 1
            text_pos += 1

        if chord_pos < len(chord_line):
            res += chord_line[chord_pos:].replace(" ", "")
        return res

    def fix_chord_lines(self, text):
        res = ""
        lines = text.split("\n")
        i = 0
        while i < len(lines):
            if "[" in lines[i] and i + 1 < len(lines):
                res += self.join_chord_line(lines[i], lines[i + 1]) + "\n"
                i += 2
            else:
                res += lines[i] + "\n"
                i += 1
        return res
