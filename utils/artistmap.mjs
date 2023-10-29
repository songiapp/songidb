import _ from "lodash";

export function removeDiacritics(s) {
  return String(s ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

export function buildArtistMap(artistArray) {
  const artistMap = {};
  const artists = [];
  const processedIds = new Set();

  for (const artist of artistArray) {
    const id = _.kebabCase(removeDiacritics(artist));
    artistMap[artist] = id;

    if (processedIds.has(id)) {
      continue;
    }

    processedIds.add(id);

    artists.push({
      id,
      name: artist,
    });
  }

  return [artistMap, artists];
}
