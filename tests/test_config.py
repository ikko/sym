import os
from pathlib import Path
import toml
from symb.config import Config

def test_config_default_path(tmp_path):
    # Temporarily set XDG_CONFIG_HOME for testing default path on POSIX
    original_xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
    os.environ['XDG_CONFIG_HOME'] = str(tmp_path)

    config = Config(file_path=None) # Test with default path
    expected_path = tmp_path / 'symb' / 'config.toml'
    assert config.file_path == expected_path

    # Restore original XDG_CONFIG_HOME
    if original_xdg_config_home is not None:
        os.environ['XDG_CONFIG_HOME'] = original_xdg_config_home
    else:
        del os.environ['XDG_CONFIG_HOME']

def test_config_load_save(tmp_path):
    config_file = tmp_path / "test_config.toml"
    config = Config(file_path=config_file)

    # Test setting and saving
    config['test_key'] = 'test_value'
    config.set('another_key', 123)
    config.save()

    assert config_file.exists()
    loaded_data = toml.load(config_file)
    assert loaded_data['test_key'] == 'test_value'
    assert loaded_data['another_key'] == 123

    # Test loading
    new_config = Config(file_path=config_file)
    assert new_config['test_key'] == 'test_value'
    assert new_config.get('another_key') == 123
    assert 'test_key' in new_config
    assert 'non_existent_key' not in new_config

def test_config_get_set_methods():
    config = Config(file_path=None) # Use default, won't save/load for this test

    config.set('my_setting', 'value1')
    assert config.get('my_setting') == 'value1'
    assert config['my_setting'] == 'value1'

    config['my_setting'] = 'value2'
    assert config.get('my_setting') == 'value2'
    assert config['my_setting'] == 'value2'

    assert config.get('non_existent', 'default_val') == 'default_val'
