import fs from "fs/promises";

const groups = JSON.parse(
  await fs.readFile("groups.json", { encoding: "utf-8" })
);

const songsById = {};

let processed = 0;
for (const group of groups) {
  processed += 1;
  console.log(`Processing group ${processed}/${groups.length}: ${group.name}`);
  const resp = await fetch(`https://supermusic.cz/${group.link}`);
  const text = await resp.text();

  const matches = [...text.matchAll(/\"skupina.php\?idpiesne=[^\"]+\"/g)].map(
    (x) => x[0]
  );

  for (const link of matches) {
    const m = link.match(/idpiesne=([\d]+)/);
    const id = m[1];
    if (songsById[id]) {
      continue;
    }
    songsById[id] = {
      id,
      link: link.slice(1, -1),
      group: group.name,
      groupId: group.id,
    };
  }
}

await fs.writeFile(
  "songs.json",
  JSON.stringify(Object.values(songsById), undefined, 2)
);
