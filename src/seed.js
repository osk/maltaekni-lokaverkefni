import { readFile } from 'fs/promises';
import { end, query } from './db.js';

async function loadJson(dir) {
  return JSON.parse(await readFile(dir));
}

async function insertSentence(sentence) {
  const q = `
    INSERT INTO sentence
      (sentence_id, section, sentence)
    VALUES
      ($1, $2, $3)
    RETURNING id`;
  const values = [sentence.id.id, sentence.id.section, sentence.sentence];

  // TODO error handling
  const result = await query(q, values);
  return result.rows[0].id;
}

async function insertEntity(entity, sentenceId) {
  const q = `
    INSERT INTO entity
      (name, label, index, sentence_id)
    VALUES
      ($1, $2, $3, $4)
    RETURNING id`;
  const values = [entity.name, entity.label, entity.index, sentenceId];

  // TODO error handling
  const result = await query(q, values);
  return result.rows[0].id;
}

async function insertEntitiesRelation(aId, bId) {
  const q = `
    INSERT INTO entities_relation
      (a_id, b_id)
    VALUES
      ($1, $2)
    RETURNING id`;
  const values = [aId, bId];

  // TODO error handling
  const result = await query(q, values);
  return result.rows[0].id;
}

async function main() {
  const data = await loadJson('./data/output/pairs/pairs.json');
  console.log(`Loaded ${data.length} sentences from json`);
  let count = 0;

  for (const item of data) {
    const sentenceId = await insertSentence(item);

    // map, index => id
    const entities = {};

    for (const pair of item.pairs) {
      const a_id =
        pair.a.index in entities ? entities[pair.a.index] : await insertEntity(pair.a, sentenceId);
      entities[pair.a.index] = a_id;
      const b_id =
        pair.b.index in entities ? entities[pair.b.index] : await insertEntity(pair.b, sentenceId);
      entities[pair.b.index] = b_id;
      await insertEntitiesRelation(a_id, b_id);
    }

    count = count + 1;
    if (count % 500 === 0) {
      console.log(`${count} sentences inserted...`);
    }
  }

  console.log('done');
  await end();
}

main().catch(async (e) => {
  console.error('error running seed', e);
  process.exit(1);
});
