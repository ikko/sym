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
        """
        what: Initializes the Config instance.
        why: To set up configuration management for the application.
        how: Initializes internal data, sets file path, and loads existing config.
        when: Upon Config instantiation.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Setting up a preferences manager.
        how, what, why and when to improve: N/A.
        """
        self._data: Dict[str, Any] = {}
        self.file_path = Path(file_path) if file_path else self._default_config_path()
        self.load()

    def _default_config_path(self) -> Path:
        """
        what: Determines the default configuration file path.
        why: To ensure cross-platform compatibility for config location.
        how: Uses OS-specific environment variables (XDG_CONFIG_HOME, APPDATA).
        when: During Config initialization if no file path is provided.
        by (caller(s)): Config.__init__.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Finding a standard location.
        how, what, why and when to improve: Handle more OS-specific paths.
        """
        if os.name == 'posix':  # Linux, macOS, etc.
            config_dir = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
        else:  # Windows
            config_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
        return config_dir / 'symbol' / 'config.toml'

    def load(self) -> None:
        """
        what: Loads configuration from the TOML file.
        why: To retrieve saved application settings.
        how: Reads the TOML file and populates internal data.
        when: Upon Config initialization or explicit load request.
        by (caller(s)): Config.__init__, external code.
        how often: Infrequently.
        how much: Depends on config file size.
        what is it like: Loading saved game data.
        how, what, why and when to improve: Handle file not found gracefully.
        """
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                self._data = toml.load(f)

    def save(self) -> None:
        """
        what: Saves the current configuration to the TOML file.
        why: To persist application settings.
        how: Creates parent directories, dumps internal data to TOML file.
        when: After configuration changes.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on config data size.
        what is it like: Saving game progress.
        how, what, why and when to improve: Handle file write errors.
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w') as f:
            toml.dump(self._data, f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        what: Retrieves a configuration value by key.
        why: To access specific settings from the configuration.
        how: Uses dictionary `get` method with optional default.
        when: When a specific configuration setting is needed.
        by (caller(s)): External code, Config.__getitem__.
        how often: Frequently.
        how much: Minimal.
        what is it like: Looking up a value in a dictionary.
        how, what, why and when to improve: N/A.
        """
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        what: Sets a configuration value.
        why: To modify application settings.
        how: Updates the internal dictionary with the new key-value pair.
        when: When a configuration setting needs to be changed.
        by (caller(s)): External code, Config.__setitem__.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Changing a setting.
        how, what, why and when to improve: N/A.
        """
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        """
        what: Allows accessing configuration values using item syntax.
        why: To provide a convenient way to retrieve settings.
        how: Delegates to the `get` method.
        when: When accessing config values like a dictionary.
        by (caller(s)): Python's item access mechanism.
        how often: Frequently.
        how much: Minimal.
        what is it like: Accessing a dictionary value.
        how, what, why and when to improve: N/A.
        """
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        what: Allows setting configuration values using item syntax.
        why: To provide a convenient way to modify settings.
        how: Delegates to the `set` method.
        when: When modifying config values like a dictionary.
        by (caller(s)): Python's item assignment mechanism.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Setting a dictionary value.
        how, what, why and when to improve: N/A.
        """
        self.set(key, value)

    def __contains__(self, key: str) -> bool:
        """
        what: Checks if a key exists in the configuration.
        why: To determine if a setting is present.
        how: Delegates to the internal dictionary's `__contains__`.
        when: When checking for the existence of a configuration key.
        by (caller(s)): Python's `in` operator.
        how often: Frequently.
        how much: Minimal.
        what is it like: Checking for a key in a dictionary.
        how, what, why and when to improve: N/A.
        """
        return key in self._data

    def __repr__(self) -> str:
        """
        what: Returns a developer-friendly string representation.
        why: For debugging and introspection.
        how: Formats file path and internal data.
        when: When Config object is printed in a debugger or console.
        by (caller(s)): Python's `repr()` function.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A technical summary.
        how, what, why and when to improve: Include more details if needed.
        """
        return f"Config(file_path='{self.file_path}', data={self._data})"
