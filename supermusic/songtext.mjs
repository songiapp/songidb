import fs from "fs/promises";
import path from "path";
import _ from "lodash";

// const SLICE_ARGS = [0, 1];
const SLICE_ARGS = [0];

const groups = JSON.parse(
  await fs.readFile("group-songs.json", { encoding: "utf-8" })
);

let groupIndex = 0;

for (const group of groups) {
  groupIndex += 1;
  const chunkFile = `texts/${group.id}.json`;
  try {
    await fs.stat(chunkFile);
    // file exists
    continue;
  } catch (err) {
    console.log(
      `Processing group ${groupIndex}/${groups.length} ${group.name}`
    );
  }

  const songs = [];

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

  if (songs.length > 0) {
    await fs.writeFile(chunkFile, JSON.stringify(songs, undefined, 2));
    console.log(`Written group ${group.name} with ${songs.length} songs`);
  } else {
    console.log(`Chunk ${group.name} has no songs`);
  }
}
