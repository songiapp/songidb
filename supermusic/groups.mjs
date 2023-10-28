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
  const matches = [
    ...text.matchAll(
      /\<a\s*(class\=interpretzoznam)?\s*id\="\d+"\s+href\=\"skupina.php\?idskupiny=[^\"]+\"/g
    ),
  ].map((x) => x[0]);
  for (const anchor of matches) {
    const link = anchor.match(/\"skupina.php\?idskupiny=[^\"]+\"/)[0];
    const m = link.match(/idskupiny=([\d]+)\&name=([^\"]+)/);
    const id = m[1];
    const name = m[2];
    const isYellow = !anchor.includes("class=interpretzoznam");
    if (groupsById[id]) {
      continue;
    }
    groupsById[id] = {
      id,
      name,
      link: link.slice(1, -1),
      isYellow,
    };
  }
}

await fs.writeFile(
  "groups.json",
  JSON.stringify(Object.values(groupsById), undefined, 2)
);
