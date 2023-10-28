import fs from "fs/promises";

const alphabet = [
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "I",
  "J",
  "K",
  "L",
  "M",
  "N",
  "O",
  "P",
  "Q",
  "R",
  "S",
  "T",
  "U",
  "V",
  "W",
  "X",
  "Y",
  "Z",
];

const groupsById = {};

for (const char of alphabet) {
  console.log("Processing groups from:", char);
  const resp = await fetch(`https://supermusic.cz/skupiny.php?od=${char}`);
  const text = await resp.text();
  const matches = [...text.matchAll(/\"skupina.php\?idskupiny=[^\"]+\"/g)].map(
    (x) => x[0]
  );
  for (const link of matches) {
    const m = link.match(/idskupiny=([\d]+)\&name=([^\"]+)/);
    const id = m[1];
    const name = m[2];
    if (groupsById[id]) {
      continue;
    }
    groupsById[id] = {
      id,
      name,
      link: link.slice(1, -1),
    };
  }
}

await fs.writeFile(
  "groups.json",
  JSON.stringify(Object.values(groupsById), undefined, 2)
);
