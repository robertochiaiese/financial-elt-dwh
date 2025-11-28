from scripts.dbConnect import connect_to_db

def test_connect_to_db_string():
    engine = connect_to_db("localhost", "testdb", "user", "pwd", 5432)
    assert "postgresql" in str(engine.url), "Engine URL must be a PostgreSQL URL"
