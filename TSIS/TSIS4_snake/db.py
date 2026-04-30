
import psycopg2
from config import DB_CONFIG

def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def create_tables():
    """Create tables if they don't exist"""
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        conn.close()

def get_or_create_player(username):
    """Get player id or create a new one"""
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        # Try to find existing player
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        row = cur.fetchone()
        if row:
            return row[0]
        # Create new player
        cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return player_id
    except Exception as e:
        print(f"Error working with player: {e}")
        return None
    finally:
        conn.close()

def save_game_result(username, score, level_reached):
    """Save game result"""
    conn = get_connection()
    if not conn:
        return
    try:
        player_id = get_or_create_player(username)
        if not player_id:
            return
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s)
        """, (player_id, score, level_reached))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error saving game result: {e}")
    finally:
        conn.close()

def get_top10():
    """Get top 10 results"""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, gs.score, gs.level_reached,
                   TO_CHAR(gs.played_at, 'DD.MM.YYYY') as date
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC
            LIMIT 10
        """)
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print(f"Error getting top 10: {e}")
        return []
    finally:
        conn.close()

def get_personal_best(username):
    """Get player's personal best score"""
    conn = get_connection()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT MAX(gs.score)
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            WHERE p.username = %s
        """, (username,))
        row = cur.fetchone()
        cur.close()
        if row and row[0] is not None:
            return row[0]
        return 0
    except Exception as e:
        print(f"Error getting personal best: {e}")
        return 0
    finally:
        conn.close()