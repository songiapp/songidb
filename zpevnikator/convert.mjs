import { XMLParser } from "fast-xml-parser";
import fs from "fs/promises";
import { buildArtistMap } from "../utils/artistmap.mjs";

const XMLdata = await fs.readFile("zp.xml", { encoding: "utf-8" });

const parser = new XMLParser();
let json = parser.parse(XMLdata);

const [artistMap, artists] = buildArtistMap(
  json.InetSongDb.song.map((song) => song.groupname)
);

const converted = {
  artists,
  songs: json.InetSongDb.song.map((song) => ({
    id: song.ID,
    title: song.title,
    artistId: artistMap[song.groupname],
    author: song.author || undefined,
    remark: song.remark || undefined,
    lang: song.lang,
    text: song.songtext,
  })),
};

await fs.writeFile("zpevnikator.json", JSON.stringify(converted, undefined, 2));
