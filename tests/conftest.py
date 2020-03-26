from pathlib import Path

import pytest
import toml

HERE = Path(__file__).parent


@pytest.fixture
def test_data_root():
    return HERE.joinpath('..', '..', 'test_data')

# ---- paths to config.toml files used in tests ----
@pytest.fixture
def test_configs_root(test_data_root):
    return test_data_root.joinpath('configs')


@pytest.fixture
def config_path_train_audio_cbin_annot_notmat(test_configs_root):
    return test_configs_root.joinpath('test_train_audio_cbin_annot_notmat.toml')


@pytest.fixture
def config_path_train_spect_mat_annot_yarden(test_configs_root):
    return test_configs_root.joinpath('test_train_spect_mat_annot_yarden.toml')


@pytest.fixture
def config_path_predict_audio_cbin_annot_notmat(test_configs_root):
    return test_configs_root.joinpath('test_predict_audio_cbin_annot_notmat.toml')


@pytest.fixture
def config_path_invalid_section(test_configs_root):
    return test_configs_root.joinpath('invalid_section_config.toml')


@pytest.fixture
def config_path_invalid_option(test_configs_root):
    return test_configs_root.joinpath('invalid_option_config.toml')


# ---- `config_toml` fixtures -- return config files loaded into dicts with toml library
# used to test functions that parse config sections, taking these dicts as inputs
@pytest.fixture
def config_toml_train_audio_cbin_annot_notmat(config_path_train_audio_cbin_annot_notmat):
    with config_path_train_audio_cbin_annot_notmat.open('r') as fp:
        config_toml = toml.load(fp)
    return config_toml


@pytest.fixture
def config_toml_train_spect_mat_annot_yarden(config_path_train_spect_mat_annot_yarden):
    with config_path_train_spect_mat_annot_yarden.open('r') as fp:
        config_toml = toml.load(fp)
    return config_toml


@pytest.fixture
def config_toml_predict_audio_cbin_annot_notmat(config_path_predict_audio_cbin_annot_notmat):
    with config_path_predict_audio_cbin_annot_notmat.open('r') as fp:
        config_toml = toml.load(fp)
    return config_toml


@pytest.fixture
def config_toml_train_audio_cbin_annot_notmat(config_path_train_audio_cbin_annot_notmat):
    with config_path_train_audio_cbin_annot_notmat.open('r') as fp:
        config_toml = toml.load(fp)
    return config_toml
