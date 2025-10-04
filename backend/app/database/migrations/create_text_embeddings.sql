CREATE TABLE IF NOT EXISTS text_embeddings (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    text TEXT,
    embedding FLOAT8[],       -- PostgreSQL array of floats for vector storage
    summary TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
