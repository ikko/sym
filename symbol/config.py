"""This module provides configuration management for the Symbol project using TOML files.

It defines a Config class for loading, saving, and managing application settings.
"""
import os
from pathlib import Path
import toml
from typing import Any, Dict, Optional, Union


class Config:
    """Manages application configuration loaded from and saved to TOML files."""

    def __init__(self, file_path: Optional[Union[str, Path]] = None):
        self._data: Dict[str, Any] = {}
        self.file_path = Path(file_path) if file_path else self._default_config_path()
        self.load()

    def _default_config_path(self) -> Path:
        """Determines the default configuration file path based on OS standards."""
        if os.name == 'posix':  # Linux, macOS, etc.
            config_dir = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
        else:  # Windows
            config_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
        return config_dir / 'symbol' / 'config.toml'

    def load(self) -> None:
        """Loads configuration from the TOML file."""
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                self._data = toml.load(f)

    def save(self) -> None:
        """Saves the current configuration to the TOML file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w') as f:
            toml.dump(self._data, f)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a configuration value by key, with an optional default."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets a configuration value."""
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __repr__(self) -> str:
        return f"Config(file_path='{self.file_path}', data={self._data})"
