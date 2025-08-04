CREATE TABLE builds (
  id SERIAL PRIMARY KEY,
  run_id BIGINT,
  status TEXT,
  duration_minutes FLOAT,
  commit_hash TEXT,
  author TEXT,
  timestamp TIMESTAMP
);
