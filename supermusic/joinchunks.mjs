import fs from "fs/promises";
import { buildArtistMap } from "../utils/artistmap.mjs";

const allSongs = [];

for (const file of await fs.readdir("texts")) {
  if (!file.endsWith(".json")) {
    continue;
  }
  const songs = JSON.parse(
    await fs.readFile(`texts/${file}`, { encoding: "utf-8" })
  );
  allSongs.push(...songs);
}

const [artistMap, artists] = buildArtistMap(
  allSongs.map((song) => song.artist)
);

console.log(`Writing ${allSongs.length} songs`);
await fs.writeFile(
  "yellowdb.json",
  JSON.stringify(
    {
      artists,
      songs: allSongs.map((song) => ({
        ...song,
        artist: undefined,
        artistId: artistMap[song.artist],
      })),
    },
    undefined,
    2
  )
);
