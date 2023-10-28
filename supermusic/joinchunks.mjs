import fs from "fs/promises";

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

console.log(`Writing ${allSongs.length} songs`);
await fs.writeFile("yellowdb.json", JSON.stringify(allSongs, undefined, 2));
