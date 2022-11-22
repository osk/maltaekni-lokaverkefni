import dotenv from 'dotenv';
import express from 'express';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { router } from './routes.js';

dotenv.config();

const { PORT: port = 3000 } = process.env;

const app = express();

app.use(express.urlencoded({ extended: true }));

const path = dirname(fileURLToPath(import.meta.url));

app.use(express.static(join(path, './public')));
app.set('views', join(path, './views'));
app.set('view engine', 'ejs');

app.use(router);

app.use((req, res) => {
  console.warn('Not found', req.originalUrl);
  res.status(404).send('not found');
});

// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  console.error(err);
  return res.status(500).send('Internal server error');
});

app.listen(port, () => {
  console.info(`Server running at http://localhost:${port}/`);
});
