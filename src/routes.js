import crypto from 'crypto';
import express from 'express';
import { randomSentenceWithEntities, allPredefinedRelations, createRelation } from './db.js';

export const router = express.Router();

async function save(req, res) {
  console.log('req.body :>> ', req.body);
  const { entityRelationId, relation, relation_string, flagged, reversed, from } = req.body;
  const ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
  const creator = ip + req.headers['user-agent'];
  const creatorHash = crypto.createHash('sha256').update(creator).digest('hex');

  console.log(
    'Saving',
    entityRelationId,
    relation,
    relation_string,
    flagged,
    reversed,
    from,
    creatorHash,
  );

  const result = await createRelation(
    entityRelationId,
    creatorHash,
    relation,
    flagged === 'true',
    reversed === 'true',
  );

  console.log('result :>> ', result);

  if (req.headers['x-fetch'] == '1') {
    // It came from client-side js fetch POST
    let sentences = await getSentences();
    let error = false;

    if (!sentences) {
      error = true;
      sentences = {};
    }

    res.json({
      error,
      sentence_one: sentences.sentence_one,
      sentence_two: sentences.sentence_two,
      id: sentences.id,
    });
  } else {
    // It came from a POST
    res.redirect(`/${from ?? ''}`);
  }
}

function translateLabel(label) {
  switch (label) {
    case 'Person':
      return 'Manneskja';
    case 'Location':
      return 'Staðsetning';
    case 'Organization':
      return 'Fyrirtæki/stofnun';
    case 'Miscellaneous':
      return 'Annað';
    default:
      return label;
  }
}

function readySentenceForDisplay(sentence) {
  if (!sentence) {
    return null;
  }

  const { sentence: s, a_name: a, b_name: b } = sentence;
  sentence.sentence = s
    .replace(a, `<mark class="a">${a}</mark>`)
    .replace(b, `<mark class="b">${b}</mark>`);

  sentence.a_label = translateLabel(sentence.a_label);
  sentence.b_label = translateLabel(sentence.b_label);

  return sentence;
}

async function renderClassificationTemplate(req, res, page, title) {
  const sentence = await randomSentenceWithEntities();
  const relations = await allPredefinedRelations();

  return res.render(page, {
    title,
    page,
    error: !sentence || !relations,
    sentence: readySentenceForDisplay(sentence),
    relations,
  });
}

function catchErrors(fn) {
  return (req, res, next) => fn(req, res, next).catch(next);
}

router.get('/', (req, res) => res.render('index', { title: 'Forsíða', page: 'index' }));
router.get('/instructions', (req, res) =>
  res.render('instructions', { title: 'Leiðbeiningar', page: 'instructions' }),
);
router.get('/about', (req, res) => res.render('about', { title: 'Um verkefni', page: 'about' }));
router.get('/v1', (req, res) =>
  catchErrors(renderClassificationTemplate(req, res, 'v1', 'Útgáfa 1 af flokkunarviðmóti')),
);
router.get('/v2', (req, res) =>
  catchErrors(renderClassificationTemplate(req, res, 'v2', 'Útgáfa 2 af flokkunarviðmóti')),
);

router.post('/save', (req, res) => catchErrors(save(req, res)));
