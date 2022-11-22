-- TODO this is not the ideal setup

CREATE TYPE relation_type AS ENUM
  ('PREDEFINED', 'USER');

CREATE TYPE entities_relation_type AS ENUM
  ('UNKNOWN', 'MARKED', 'FLAGGED');

-- Possible relations between two entities.
CREATE TABLE relation (
  id SERIAL PRIMARY KEY,
  name VARCHAR(128),
  display VARCHAR(128),
  type relation_type,

  -- something unique for the user creating this
  -- TODO should be a foreign key
  creator VARCHAR(128),
  created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT current_timestamp,
  updated TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT current_timestamp
);

CREATE TABLE sentence (
  id SERIAL PRIMARY KEY,
  sentence_id VARCHAR(128) UNIQUE NOT NULL,
  section VARCHAR(128) NOT NULL,
  sentence TEXT NOT NULL
);

CREATE TABLE entity (
  id SERIAL PRIMARY KEY,
  name VARCHAR(128) NOT NULL,
  label VARCHAR(128) NOT NULL,
  index VARCHAR(128) NOT NULL,
  sentence_id INTEGER NOT NULL, -- Should not be here but in the relation table

  CONSTRAINT fk_entity_sentence FOREIGN KEY
    (sentence_id) REFERENCES sentence (id)
    ON DELETE CASCADE
);

-- Relation between two entities, i.e. it's been marked by a person.
-- TODO this should be a one-to-many relation :/
CREATE TABLE entities_relation (
  id SERIAL PRIMARY KEY,
  relation_type entities_relation_type DEFAULT 'UNKNOWN',
  relation_id INTEGER,
  a_id INTEGER NOT NULL,
  b_id INTEGER NOT NULL,

  -- Is the relation reversed? lol typo
  -- E.g. B works_for A since we might not have A is_worker_at B.
  reveresed BOOLEAN DEFAULT FALSE,

  -- something unique for the user creating this
  -- TODO should be a foreign key
  creator VARCHAR(128),

  created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT current_timestamp,
  updated TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT current_timestamp,

  CONSTRAINT fk_entitiesrelation_relation FOREIGN KEY
    (relation_id) REFERENCES relation (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_entitiesrelation_a FOREIGN KEY
    (a_id) REFERENCES entity (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_entitiesrelation_b FOREIGN KEY
    (b_id) REFERENCES entity (id)
    ON DELETE CASCADE
);

-- TODO This should be in a separate file
INSERT INTO relation (name, display, type) VALUES ('works_for', 'vinnur fyrir', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('attended', 'gekk í', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('founded', 'stofnaði', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('studied_at', 'lærði hjá', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('teached_at', 'kenndi hjá', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('child_of', 'barn', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('parent_of', 'foreldri', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('partner_of', 'maki', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('author_of', 'höfundur', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('associate', 'samstarfsmaður', 'PREDEFINED'); -- TODO non gendered?
INSERT INTO relation (name, display, type) VALUES ('member_of', 'meðlimur í', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('political_affiliation', 'stjórnmálatengsl', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('created', 'bjó til', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('competitors', 'keppinautar', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('siblings', 'systkini', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('visited', 'heimsótti', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('located_in', 'staðsett í', 'PREDEFINED');
INSERT INTO relation (name, display, type) VALUES ('located_at', 'staðsett hjá', 'PREDEFINED');
