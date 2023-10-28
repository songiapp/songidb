import fs from "fs/promises";
import path from "path";
import _ from "lodash";

// const SLICE_ARGS = [0, 1];
const SLICE_ARGS = [0];

const groups = JSON.parse(
  await fs.readFile("group-songs.json", { encoding: "utf-8" })
);

let chunkIndex = 0;
for (const chunk of _.chunk(groups, 10).slice(...SLICE_ARGS)) {
  chunkIndex += 1;
  const chunkFile = `texts/${chunkIndex}.json`;
  try {
    await fs.stat(chunkFile);
    // file exists
    continue;
  } catch (err) {
    console.log(`Processing chunk ${chunkIndex}`);
  }

  const songs = [];

  for (const group of chunk) {
    let lastSong = "";
    for (const song of (group.songs || []).slice(...SLICE_ARGS)) {
      if (song.name == lastSong) {
        continue;
      }
      const resp = await fetch(`https://supermusic.cz/${song.link}`);
      const text = await resp.text();
      const textMatch = text.match(/\<\/SCRIPT\>(.*?)\<script\s+LANGUAGE=/s);
      if (textMatch) {
        const sonngText = textMatch[1]
          .replace(
            /<sup>([^.]+?)<\/sup>/gs,
            (m) => `[${m.replace(/<[^>]+?>/g, "")}]`
          )
          .replace(/<br\/>/g, "\n")
          .replace(/\n\s*\n/gs, "\n")
          .replace(/\r/g, "")
          .trim();
        //.replace(/<sup><a[^>]+>([^<]+)<\/a><\/sup>/g, (m) => `[${m[1]}]`)
        songs.push({
          id: song.id,
          artist: group.name,
          text: sonngText,
          title: song.name,
        });
        lastSong = song.name;
      }
    }
  }

  if (songs.length > 0) {
    await fs.writeFile(chunkFile, JSON.stringify(songs, undefined, 2));
    console.log(`Written chunk ${chunkIndex} with ${songs.length} songs`);
  } else {
    console.log(`Chunk ${chunkIndex} has no songs`);
  }
}
