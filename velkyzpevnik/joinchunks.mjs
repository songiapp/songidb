import fs from "fs/promises";

const allSongs = [];

function joinChordLine(chordLine, textLine) {
  let chordPos = 0;
  let textPos = 0;
  let res = "";

  while (textPos < textLine.length) {
    if (chordLine[chordPos] == "[") {
      res += "[";
      chordPos += 1;
      while (chordPos < chordLine.length && chordLine[chordPos] != "]") {
        res += chordLine[chordPos];
        chordPos += 1;
      }
      res += "]";
      if (chordLine[chordPos] == "]") {
        chordPos += 1;
      }
      continue;
    }

    res += textLine[textPos];
    chordPos += 1;
    textPos += 1;
  }

  res += chordLine.slice(chordPos).replace(/\s/g, "");
  return res;
}

function fixChordLines(text) {
  let res = "";
  const lines = text.split("\n");
  let i = 0;
  while (i < lines.length) {
    if (lines[i].includes("[") && i + 1 < lines.length) {
      res += joinChordLine(lines[i], lines[i + 1]) + "\n";
      i += 2;
    } else {
      res += lines[i] + "\n";
      i += 1;
    }
  }
  return res;
}

const groups = JSON.parse(
  await fs.readFile("groups.json", { encoding: "utf-8" })
);

for (const file of await fs.readdir("texts")) {
  if (!file.endsWith(".json")) {
    continue;
  }
  const songs = JSON.parse(
    await fs.readFile(`texts/${file}`, { encoding: "utf-8" })
  );
  allSongs.push(
    ...songs.map((song) => ({
      ...song,
      id: song.id.substring(1).replace("/", "-"),
      text: fixChordLines(song.text),
    }))
  );
}

console.log(`Writing ${allSongs.length} songs`);
await fs.writeFile(
  "db.json",
  JSON.stringify(
    {
      artists: groups.map((group) => ({
        id: group.id,
        name: group.name,
      })),
      songs: allSongs,
    },
    undefined,
    2
  )
);
