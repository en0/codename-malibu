from os import stat


class FileWatcher:
    def __init__(self, file_path: str):
        self._path = file_path
        self._last = stat(self._path).st_mtime

    def has_changed(self) -> bool:
        _last = stat(self._path).st_mtime
        if _last > self._last:
            self._last = _last
            return True
        return False
