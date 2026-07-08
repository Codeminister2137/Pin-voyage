from pin_voyage.config import Config, get_config


def test_config_builds_database_url_from_postgres_settings():
    config = Config(
        POSTGRES_HOST="db.example",
        POSTGRES_PORT=5433,
        POSTGRES_DB="voyage",
        POSTGRES_USER="app",
        POSTGRES_PASSWORD="secret",
    )

    assert (
        config.DATABASE_URL
        == "postgresql+psycopg2://app:secret@db.example:5433/voyage"
    )


def test_get_config_reads_environment(monkeypatch):
    monkeypatch.setenv("POSTGRES_HOST", "db")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("POSTGRES_DB", "pin_voyage")
    monkeypatch.setenv("POSTGRES_USER", "user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "password")

    config = get_config()

    assert config.POSTGRES_HOST == "db"
    assert config.POSTGRES_PORT == 5432
    assert (
        config.DATABASE_URL
        == "postgresql+psycopg2://user:password@db:5432/pin_voyage"
    )
