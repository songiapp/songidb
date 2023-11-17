import json
from unidecode import unidecode
import re


def kebab_case(s):
    return '-'.join(
        re.sub(r"(\s|_|-)+", " ",
               re.sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                      lambda mo: ' ' + mo.group(0).lower(), s)).split())


class ScrapyFormatter:
    def __init__(self, pkg):

        self.songs = []
        self.artists = []
        self.pkg = pkg

        self.artists_by_id = {}

    def process_artist(self, **kwargs):
        pass

    def process_song(self, **kwargs):
        pass

    def add_artist(self, name, id):
        if not id:
            # create id from name
            id = kebab_case(unidecode(name)) or 'no-artist'

        if id in self.artists_by_id:
            return id
        artist = {
            'id': id,
            'name': name,
        }
        self.artists_by_id = artist
        self.artists.append(artist)
        return id

    def add_song(self, id, artist_id, title, text):
        self.songs.append({
            'id': id,
            'artistId': artist_id,
            'title': title,
            'text': text
        })

    def run(self):
        loaded_songs = []

        with open(f'{self.pkg}/crawled.jsonl') as f:
            for line in f:
                obj = json.loads(line)
                match obj['type']:
                    case 'artist':
                        self.process_artist(**obj)
                    case 'song':
                        loaded_songs.append(obj)

        for song in loaded_songs:
            self.process_song(**song)

        with open(f'{self.pkg}/db.json', "w") as f:
            f.write(json.dumps({
                'artists': self.artists,
                'songs': self.songs,
            }, indent=2))

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