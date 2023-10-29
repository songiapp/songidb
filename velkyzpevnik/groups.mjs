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
  const resp = await fetch(
    `https://www.velkyzpevnik.cz/interpreti/1/abecedne-vzestupne?letter=${char.toLowerCase()}`
  );
  const text = await resp.text();
  const matches = [
    ...text.matchAll(
      /\<a\s+class\=\"interpret\"\s+href\=\"[^"]+\">[^<]+<small/gs
    ),
  ].map((x) => x[0]);
  for (const anchor of matches) {
    const m = anchor.match(/href\=\"([^"]+)\">([^<]+)<small/s);
    const link = m[1];
    const name = m[2].trim();
    const id = link.substring(1);
    groupsById[id] = {
      id,
      name,
      link,
    };
  }
}

await fs.writeFile(
  "groups.json",
  JSON.stringify(Object.values(groupsById), undefined, 2)
);
