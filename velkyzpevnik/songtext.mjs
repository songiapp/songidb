import fs from "fs/promises";
import path from "path";
import _ from "lodash";

// const SLICE_ARGS = [0, 1];
const SLICE_ARGS = [0];

const groups = JSON.parse(
  await fs.readFile("group-songs.json", { encoding: "utf-8" })
);

let groupIndex = 0;

for (const group of groups.slice(...SLICE_ARGS)) {
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

  for (const song of (group.songs || []).slice(...SLICE_ARGS)) {
    const resp = await fetch(`https://www.velkyzpevnik.cz/${song.link}`);
    const text = await resp.text();
    const textMatch = text.match(/<pre[^>]+>(.*?)<\/pre/s);

    if (textMatch) {
      const sonngText = textMatch[1]
        .replace(/<span class='chord'[^>]*>([^<]+)<\/span>/gs, (m) => `[${m}]`)
        .replace(/<[^>]+?>/g, "")
        .trim();
      songs.push({
        id: song.link,
        artistId: group.id,
        text: sonngText,
        title: song.name,
      });
    }
  }

  await fs.writeFile(chunkFile, JSON.stringify(songs, undefined, 2));
  console.log(`Written group ${group.name} with ${songs.length} songs`);
}
