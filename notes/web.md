# Web interface for relations

## Database

Uses [Prisma](https://prisma.io) and PostgreSQL.

Create a postgres database, e.g.

```bash
createdb maltaekni-lokaverkefni
```

Create a user and grant privileges, e.g.

```bash
psql maltaekni-lokaverkefni
# Execute queries from inside psql
DROP ROLE IF EXISTS "maltaekni-user";
CREATE USER "maltaekni-user" WITH ENCRYPTED PASSWORD 'maltaekni';
GRANT ALL PRIVILEGES ON DATABASE maltaekni-lokaverkefni TO "maltaekni-user";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "maltaekni-user";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "maltaekni-user";
```

Add the database connection string to `.env`, e.g.:

```env
DATABASE_URL="postgresql://maltaekni-user:maltaekni@localhost:5432/maltaekni-lokaverkefni?schema=public"
```

### Updates to the database

Update schema in `schema.prisma` and run

```bash
npx prisma db push
```

If changing schema, run

```bash
npx prisma migrate reset
```

This will hose the current data, so make sure to back it up first.

## Seeding the database

## Interface
