import fs from "fs/promises";

const groups = JSON.parse(
  await fs.readFile("groups.json", { encoding: "utf-8" })
);

let processed = 0;

for (const group of groups) {
  processed += 1;
  console.log(`Processing group ${processed}/${groups.length}: ${group.name}`);
  const resp = await fetch(`https://www.velkyzpevnik.cz/${group.link}`);
  const text = await resp.text();

  const matches = [
    ...text.matchAll(/href=\"[^"]+">\s*<p\s+class=\"song-title\">[^<]+<\/p>/gs),
  ].map((x) => x[0]);

  group.songs = [];

  for (const anchor of matches) {
    const m = anchor.match(
      /href=\"([^"]+)">\s*<p\s+class=\"song-title\">([^<]+)<\/p>/s
    );
    const link = m[1];
    const name = m[2];

    group.songs.push({
      link,
      name: name.trim(),
    });
  }
}

await fs.writeFile("group-songs.json", JSON.stringify(groups, undefined, 2));
