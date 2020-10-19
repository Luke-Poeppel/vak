from pathlib import Path

import vak

HERE = Path(__file__).parent
# convention is that all the config.ini files in setup_scripts/ that should be
# run when setting up for development have filenames of the form `setup_*_config.ini'
# e.g., 'setup_learncurve_config.ini'
TEST_DATA_ROOT = HERE.joinpath('..', 'test_data')
TEST_CONFIGS_ROOT = TEST_DATA_ROOT.joinpath('configs')
TEST_CONFIGS_TO_RUN = TEST_CONFIGS_ROOT.glob('test*toml')


def main():
    for test_toml_path in TEST_CONFIGS_TO_RUN:
        if 'train' in test_toml_path.name:
            command = 'train'
        elif 'predict' in test_toml_path.name:
            command = 'predict'
        elif 'learncurve' in test_toml_path.name:
            command = 'learncurve'
        else:
            raise ValueError(
                f'unable to determine command to run from config name:\n{test_toml_path}'
            )

        print(
            f"re-running vak {command} to set up for tests, using config: {test_toml_path.name}"
        )

        if command == 'train':
            vak.cli.train(toml_path=test_toml_path)
        elif command == 'predict':
            vak.cli.predict(toml_path=test_toml_path)
        elif command == 'learncurve':
            vak.cli.learncurve.learning_curve(toml_path=test_toml_path)


if __name__ == '__main__':
    main()
