import pg from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const { DATABASE_URL: connectionString, NODE_ENV: nodeEnv = 'development' } = process.env;

if (!connectionString) {
  console.error('missing DATABASE_URL in env');
  process.exit(1);
}

const ssl = nodeEnv === 'production' ? { rejectUnauthorized: false } : false;

const pool = new pg.Pool({ connectionString, ssl });

pool.on('error', (err) => {
  console.error('error in db', err);
  process.exit(-1);
});

export async function query(q, values = []) {
  let client;
  try {
    client = await pool.connect();
  } catch (e) {
    console.error('unable to get client from pool', e);
    return null;
  }

  try {
    const result = await client.query(q, values);
    return result;
  } catch (e) {
    console.error('unable to query', e);
    return null;
  } finally {
    client.release();
  }
}

export async function end() {
  await pool.end();
}

/**
 * All predefined relations.
 */
export async function allPredefinedRelations() {
  const q = `SELECT id, display FROM relation WHERE type = 'PREDEFINED' ORDER BY display`;
  const result = await query(q);

  return result?.rows ? result.rows : null;
}

/**
 * Return a random sentence with entities
 */
export async function randomSentenceWithEntities() {
  const q = `
    SELECT
      s.sentence AS sentence,
      a.name AS a_name, a.label AS a_label,
      b.name AS b_name, b.label AS b_label,
      er.id AS entity_relation_id
    FROM
      entities_relation AS er
    LEFT JOIN
      entity AS a ON er.a_id = a.id
    LEFT JOIN
      entity AS b ON er.b_id = b.id
    LEFT JOIN
      sentence AS s ON a.sentence_id = s.id
    WHERE
      er.relation_type = 'UNKNOWN'
    ORDER BY random()
    LIMIT 1`;
  const result = await query(q);

  return result?.rows ? result.rows[0] : null;
}

async function createNewRelation(relation, creator) {
  const q = `
    INSERT INTO relation
      (display, type, creator)
    VALUES
      ($1, $2, $3)
    RETURNING id`;
  const values = [relation, 'USER', creator];

  const result = await query(q, values);
  return result.rows[0].id;
}

/**
 * Create a new relation between two entities.
 * @param {number} entityRelationId ID of the relation between two entities
 * @param {string} creator Something that identifies the creator of the relation
 * @param {number | string} relationIdOrString Either the ID of the relation or the string of a new relation
 * @param {boolean} flagged Is the relation flagged? I.e. something is weird about it.
 * @param {*} reversed Is the relation flagged? I.e. the given relation works for B->A instead of A->B
 */
export async function createRelation(
  entityRelationId,
  creator,
  relationIdOrString,
  flagged = false,
  reversed = false,
) {
  let relationId;
  if (typeof relationIdOrString === 'string') {
    relationId = await createNewRelation(relationIdOrString, creator);
  } else {
    relationId = relationIdOrString;
  }

  const q = `
    UPDATE entities_relation
    SET
      relation_type = $1,
      reveresed = $2,
      creator = $3,
      relation_id = $4
    WHERE
      id = $5`;
  const values = [
    flagged ? 'FLAGGED' : 'MARKED',
    Boolean(reversed) ? 't' : 'f',
    creator,
    Number.parseInt(relationId),
    entityRelationId,
  ];
  const result = await query(q, values);
  return result;
}
