import asyncpg
from ..config import DATABASE_CONFIG

# ------------------ Database Connection ------------------

async def get_connection():
    """
    Creates and returns a new asyncpg connection using DATABASE_CONFIG.
    """
    return await asyncpg.connect(**DATABASE_CONFIG)

# ------------------ Embeddings CRUD ------------------

async def save_embedding(record: dict):
    """
    Saves text, embedding vector, summary, and user_id to the database.
    The 'embedding' is expected to be a NumPy array or list of floats.
    """
    conn = await get_connection()
    try:
        query = """
        INSERT INTO text_embeddings (user_id, text, embedding, summary)
        VALUES ($1, $2, $3, $4)
        RETURNING id;
        """
        embedding_list = record["embedding"].tolist() if not isinstance(record["embedding"], list) else record["embedding"]
        result = await conn.fetchval(
            query,
            record["user_id"],
            record["text"],
            embedding_list,
            record["summary"],
        )
        return result
    finally:
        await conn.close()


async def get_embedding_by_id(embedding_id: int):
    """
    Fetches an embedding record by ID.
    """
    conn = await get_connection()
    try:
        query = "SELECT * FROM text_embeddings WHERE id = $1;"
        record = await conn.fetchrow(query, embedding_id)
        return dict(record) if record else None
    finally:
        await conn.close()


async def get_user_embeddings(user_id: str):
    """
    Fetches all embeddings for a specific user.
    """
    conn = await get_connection()
    try:
        query = "SELECT id, text, summary, embedding FROM text_embeddings WHERE user_id = $1;"
        records = await conn.fetch(query, user_id)
        return [dict(r) for r in records]
    finally:
        await conn.close()
