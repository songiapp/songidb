import fs from "fs/promises";

const groups = JSON.parse(
  await fs.readFile("groups.json", { encoding: "utf-8" })
);

let processed = 0;
const yellowGroups = groups.filter((x) => x.isYellow);
for (const group of yellowGroups) {
  processed += 1;
  console.log(
    `Processing group ${processed}/${yellowGroups.length}: ${group.name}`
  );
  const resp = await fetch(`https://supermusic.cz/${group.link}`);
  const text = await resp.text();

  const matches = [
    ...text.matchAll(/\"skupina.php\?idpiesne=[^\"]+\"\&sid=\>[^<]+\<img/g),
  ].map((x) => x[0]);

  group.songs = [];

  for (const anchor of matches) {
    const link = anchor.match(/\"skupina.php\?idpiesne=[^\"]+\"/)[0];
    const name = anchor.match(/\>([^\<]+)\</)[1];
    const m = link.match(/idpiesne=([\d]+)/);
    const id = m[1];

    group.songs.push({
      id,
      link: link.slice(1, -1),
      name: name.trim(),
    });
  }
}

await fs.writeFile("group-songs.json", JSON.stringify(groups, undefined, 2));
