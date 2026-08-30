from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SITES_DIR = DATA_DIR / "sites"
MEMPALACE_DIR = DATA_DIR / "mempalace"

DATA_DIR.mkdir(exist_ok=True)
SITES_DIR.mkdir(exist_ok=True)
MEMPALACE_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    app_name: str = "AI Website Builder"
    db_path: str = str(DATA_DIR / "app.db")
    mempalace_data_dir: str = str(MEMPALACE_DIR)
    sites_dir: str = str(SITES_DIR)
    max_agent_loops: int = 10
    default_temperature: float = 0.4
    github_personal_access_token: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
