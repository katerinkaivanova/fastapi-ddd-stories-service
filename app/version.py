import json
from pathlib import Path

from app.config import settings


version_file_path = settings.ROOT_DIR / 'version.json'


def get_version(path: Path | str) -> str:
    if (path := Path(path)).is_file():
        with path.open() as version_file:
            return json.load(version_file)['hash']

    return 'unstable'  # pragma: no cover


VERSION = get_version(version_file_path)
