"""tests for vak.config.parse module"""
import copy

import pytest

import vak.config
import vak.transforms.transforms
import vak.split
import vak.models
import vak.spect


@pytest.mark.parametrize(
    "section_name",
    [
        "DATALOADER",
        "EVAL" "LEARNCURVE",
        "PREDICT",
        "PREP",
        "SPECT_PARAMS",
        "TRAIN",
    ],
)
def test_parse_config_section_returns_attrs_class(
    section_name,
    all_generated_configs_toml_path_pairs,
    default_model,
):
    """test that ``vak.config.parse.parse_config_section``
    returns an instance of ``vak.config.learncurve.LearncurveConfig``"""
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        if default_model not in str(toml_path):
            continue  # only need to check configs for one model
            # also avoids FileNotFoundError on CI
        if section_name in config_toml:
            config_section_obj = vak.config.parse.parse_config_section(
                config_toml=config_toml,
                section_name=section_name,
                toml_path=toml_path,
            )
            assert isinstance(
                config_section_obj, vak.config.parse.SECTION_CLASSES[section_name]
            )


@pytest.mark.parametrize(
    "section_name",
    [
        "DATALOADER",
        "EVAL",
        "LEARNCURVE",
        "PREDICT",
        "PREP",
        "SPECT_PARAMS",
        "TRAIN",
    ],
)
def test_parse_config_section_missing_options_raises(
    section_name,
    all_generated_configs_toml_path_pairs,
    default_model,
):
    """test that configs without the required options in a section raise KeyError"""
    if vak.config.parse.REQUIRED_OPTIONS[section_name] is None:
        pytest.skip(f"no required options to test for section: {section_name}")

    # in comprehensions below, filter by default model
    # because we only need to check configs for one model
    # also avoids FileNotFoundError on CI
    if section_name == "PREP":
        configs_toml_path_pairs = (
            (config_toml, toml_path)
            for config_toml, toml_path in all_generated_configs_toml_path_pairs
            if default_model in str(toml_path)
        )
    else:
        configs_toml_path_pairs = (
            (config_toml, toml_path)
            for config_toml, toml_path in all_generated_configs_toml_path_pairs
            if section_name.lower() in toml_path.name
            and default_model in str(toml_path)
        )

    for config_toml, toml_path in configs_toml_path_pairs:
        if section_name in config_toml:
            for option in vak.config.parse.REQUIRED_OPTIONS[section_name]:
                config_copy = copy.deepcopy(config_toml)
                config_copy[section_name].pop(option)
                with pytest.raises(KeyError):
                    config = vak.config.parse.parse_config_section(
                        config_toml=config_copy,
                        section_name=section_name,
                        toml_path=toml_path,
                    )


@pytest.mark.parametrize("section_name", ["EVAL", "LEARNCURVE", "PREDICT", "TRAIN"])
def test_parse_config_section_model_not_installed_raises(
    section_name, all_generated_configs_toml_path_pairs
):
    """test that a ValueError is raised when the ``models`` option
    in the section specifies names of models that are not installed"""
    # we only need one toml, path pair
    # so we just call next on the ``zipped`` iterator that our fixture gives us
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        if section_name.lower() in toml_path.name:
            break  # use these

    config_toml[section_name]["models"] = "NotInstalledNet, OtherNotInstalledNet"
    with pytest.raises(ValueError):
        vak.config.parse.parse_config_section(
            config_toml=config_toml, section_name=section_name, toml_path=toml_path
        )


@pytest.mark.parametrize(
    "section_name",
    [
        "EVAL",
        "PREDICT",
    ],
)
def test_parse_config_section_nonexistent_checkpoint_path_raises(
    section_name, all_generated_configs_toml_path_pairs
):
    """test that a FileNotFoundError is raised when checkpoint_path does not exist"""
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        if section_name.lower() in toml_path.name:
            break  # use these

    config_toml[section_name]["checkpoint_path"] = "obviously/non/existent/dir/check.pt"
    with pytest.raises(FileNotFoundError):
        vak.config.parse.parse_config_section(
            config_toml=config_toml, section_name=section_name, toml_path=toml_path
        )


@pytest.mark.parametrize("section_name", ["LEARNCURVE", "TRAIN"])
def test_parse_config_section_nonexistent_root_results_dir_raises(
    section_name, all_generated_configs_toml_path_pairs
):
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        if section_name.lower() in toml_path.name:
            break  # use these

    config_toml[section_name]["root_results_dir"] = "obviously/non/existent/dir"
    with pytest.raises(NotADirectoryError):
        vak.config.parse.parse_config_section(config_toml, section_name, toml_path)


@pytest.mark.parametrize("section_name", ["EVAL", "LEARNCURVE", "PREDICT", "TRAIN"])
def test_nonexistent_csv_path_raises(
    section_name, all_generated_configs_toml_path_pairs
):
    """test that a FileNotFoundError is raised when csv_path does not exist"""
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        if section_name.lower() in toml_path.name:
            break  # use these

    config_toml[section_name]["csv_path"] = "obviously/non/existent/dir/predict.csv"
    with pytest.raises(FileNotFoundError):
        vak.config.parse.parse_config_section(
            config_toml=config_toml, section_name=section_name, toml_path=toml_path
        )


def test_parse_prep_section_nonexistent_data_dir_raises_error(
    all_generated_configs_toml_path_pairs,
):
    config_toml, toml_path = next(all_generated_configs_toml_path_pairs)
    config_toml["PREP"]["data_dir"] = "theres/no/way/this/is/a/dir"
    with pytest.raises(NotADirectoryError):
        vak.config.parse.parse_config_section(config_toml, "PREP", toml_path)


def test_parse_prep_section_both_audio_and_spect_format_raises(
    all_generated_configs_toml_path_pairs,
):
    """test that a config with both an audio and a spect format raises a ValueError"""
    # iterate through configs til we find one with an `audio_format` option
    # and then we'll add a `spect_format` option to it
    found_config_to_use = False
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        if "audio_format" in config_toml["PREP"]:
            found_config_to_use = True
            break
    assert found_config_to_use  # sanity check

    config_toml["PREP"]["spect_format"] = "mat"
    with pytest.raises(ValueError):
        vak.config.parse.parse_config_section(config_toml, "PREP", toml_path)


def test_parse_prep_section_neither_audio_nor_spect_format_raises(
    all_generated_configs_toml_path_pairs,
):
    """test that a config without either an audio or a spect format raises a ValueError"""
    # iterate through configs til we find one with an `audio_format` option
    # and then we'll add a `spect_format` option to it
    found_config_to_use = False
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        if "audio_format" in config_toml["PREP"]:
            found_config_to_use = True
            break
    assert found_config_to_use  # sanity check

    config_toml["PREP"].pop("audio_format")
    if "spect_format" in config_toml["PREP"]:
        # shouldn't be but humor me
        config_toml["PREP"].pop("spect_format")

    with pytest.raises(ValueError):
        vak.config.parse.parse_config_section(config_toml, "PREP", toml_path)


def test_load_from_toml_path(all_generated_configs):
    for toml_path in all_generated_configs:
        config_toml = vak.config.parse._load_toml_from_path(toml_path)
        assert isinstance(config_toml, dict)


def test_load_from_toml_path_raises_when_config_doesnt_exist(config_that_doesnt_exist):
    with pytest.raises(FileNotFoundError):
        vak.config.parse._load_toml_from_path(config_that_doesnt_exist)


def test_from_toml_path_returns_instance_of_config(
    all_generated_configs, default_model
):
    for toml_path in all_generated_configs:
        if default_model not in str(toml_path):
            continue  # only need to check configs for one model
            # also avoids FileNotFoundError on CI
        config_obj = vak.config.parse.from_toml_path(toml_path)
        assert isinstance(config_obj, vak.config.parse.Config)


def test_from_toml_path_raises_when_config_doesnt_exist(config_that_doesnt_exist):
    with pytest.raises(FileNotFoundError):
        vak.config.parse.from_toml_path(config_that_doesnt_exist)


def test_from_toml(all_generated_configs_toml_path_pairs, default_model):
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        if default_model not in str(toml_path):
            continue  # only need to check configs for one model
            # also avoids FileNotFoundError on CI
        config_obj = vak.config.parse.from_toml(config_toml, toml_path)
        assert isinstance(config_obj, vak.config.parse.Config)


def test_from_toml_parse_prep_with_sections_not_none(
    all_generated_configs_toml_path_pairs,
):
    """test that we get only the sections we want when we pass in a sections list to
    ``from_toml``. Specifically test ``PREP`` since that's what this will be used for."""
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        config_obj = vak.config.parse.from_toml(
            config_toml, toml_path, sections=["PREP", "SPECT_PARAMS"]
        )
        assert isinstance(config_obj, vak.config.parse.Config)
        for should_have in ("prep", "spect_params"):
            assert hasattr(config_obj, should_have)
        for should_be_none in ("eval", "learncurve", "train", "predict"):
            assert getattr(config_obj, should_be_none) is None
        assert (
            getattr(config_obj, "dataloader")
            == vak.config.dataloader.DataLoaderConfig()
        )


@pytest.mark.parametrize("section_name", ["EVAL", "LEARNCURVE", "PREDICT", "TRAIN"])
def test_from_toml_parse_prep_with_sections_not_none_does_not_raise(
    section_name, all_generated_configs_toml_path_pairs, random_path_factory
):
    """test that invalid values in other sections are ignored when we pass in a sections list
    specifying that we only want to parse ``PREP`` and ``SPECT_PARAMS``, e.g., ignore non-existent
    csv_path or checkpoint_path"""
    for config_toml, toml_path in all_generated_configs_toml_path_pairs:
        if section_name.lower() in toml_path.name:
            break  # use these

    purpose = vak.cli.prep.purpose_from_toml(config_toml, toml_path)
    section_name = purpose.upper()
    required_options = vak.config.parse.REQUIRED_OPTIONS[section_name]
    for required_option in required_options:
        # set option to values that **would** cause an error if we parse them
        if "path" in required_option:
            badval = random_path_factory(f"_{required_option}.exe")
        elif "dir" in required_option:
            badval = random_path_factory("nonexistent_dir")
        else:
            continue
        config_toml[section_name][required_option] = badval
    config_obj = vak.config.parse.from_toml(
        config_toml, toml_path, sections=["PREP", "SPECT_PARAMS"]
    )
    with pytest.raises((FileNotFoundError, NotADirectoryError)):
        vak.config.parse.from_toml(config_toml, toml_path, sections=section_name)


def test_invalid_section_raises(invalid_section_config_path):
    with pytest.raises(ValueError):
        vak.config.parse.from_toml_path(invalid_section_config_path)


def test_invalid_option_raises(invalid_option_config_path):
    with pytest.raises(ValueError):
        vak.config.parse.from_toml_path(invalid_option_config_path)


@pytest.fixture
def invalid_train_and_learncurve_config_toml(test_configs_root):
    return test_configs_root.joinpath("invalid_train_and_learncurve_config.toml")


def test_train_and_learncurve_defined_raises(invalid_train_and_learncurve_config_toml):
    """test that a .toml config with both a TRAIN and a LEARNCURVE section raises a ValueError"""
    with pytest.raises(ValueError):
        vak.config.parse.from_toml_path(invalid_train_and_learncurve_config_toml)
