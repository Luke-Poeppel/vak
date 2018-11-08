"""parses [TRAIN] section of config"""
from collections import namedtuple


TrainConfig = namedtuple('TrainConfig', ['train_data_dict_path',
                                         'train_set_durs',
                                         'num_replicates',
                                         'val_data_dict_path',
                                         'val_error_step',
                                         'checkpoint_step',
                                         'save_only_single_checkpoint_file',
                                         'n_max_iter',
                                         'patience',
                                         'normalize_spectrograms',
                                         'use_train_subsets_from_previous_run',
                                         'previous_run_path',
                                         ])


def parse_train_config(config, config_file):
    """parse [TRAIN] section of config.ini file

    Parameters
    ----------
    config : ConfigParser
        containing config.ini file already loaded by parse function

    Returns
    -------
    train_config : namedtuple
        with fields:
            train_data_dict_path :
            train_set_durs :
            num_replicates :
            val_data_dict_path :
            val_error_step :
            checkpoint_step :
            save_only_single_checkpoint_file :
            n_max_iter :
            patience :
            use_train_subsets_from_previous_run :
            previous_run_path :
    """
    train_data_dict_path = config['TRAIN']['train_data_path']

    if config.has_option('TRAIN', 'train_set_durs'):
        train_set_durs = [int(element)
                          for element in
                          config['TRAIN']['train_set_durs'].split(',')]
    else:
        # set to None when training on entire dataset
        train_set_durs = None

    if config.has_option('TRAIN', 'replicates'):
        num_replicates = int(config['TRAIN']['replicates'])
    else:
        # set to None when training on entire dataset
        num_replicates = None

    if config.has_option('TRAIN', 'val_data_path'):
        val_data_dict_path = config['TRAIN']['val_data_path']
    else:
        val_data_dict_path = None

    if config.has_option('TRAIN', 'val_error_step'):
        val_error_step = int(config['TRAIN']['val_error_step'])
    else:
        val_error_step = None

    if config.has_option('TRAIN', 'checkpoint_step'):
        checkpoint_step = int(config['TRAIN']['checkpoint_step'])
    else:
        checkpoint_step = None

    if config.has_option('TRAIN', 'save_only_single_checkpoint_file'):
        save_only_single_checkpoint_file = config.getboolean('TRAIN',
                                                             'save_only_single_checkpoint_file')
    else:
        save_only_single_checkpoint_file = True

    if config.has_option('TRAIN', 'n_max_iter'):
        n_max_iter = int(config['TRAIN']['n_max_iter'])
    else:
        n_max_iter = 18000

    if config.has_option('TRAIN', 'patience'):
        patience = config['TRAIN']['patience']
        try:
            patience = int(patience)
        except ValueError:
            if patience == 'None':
                patience = None
            else:
                raise TypeError('patience must be an int or None, but'
                                'is {} and parsed as type {}'
                                .format(patience, type(patience)))
    else:
        patience = None

    if config.has_option('TRAIN', 'normalize_spectrograms'):
        normalize_spectrograms = config.getboolean('TRAIN',
                                                   'normalize_spectrograms')
    else:
        normalize_spectrograms = False

    if config.has_option('TRAIN', 'use_train_subsets_from_previous_run'):
        use_train_subsets_from_previous_run = config.getboolean(
            'TRAIN', 'use_train_subsets_from_previous_run')
        try:
            previous_run_path = config['TRAIN']['previous_run_path']
        except KeyError:
            raise KeyError('In config.file {}, '
                           'use_train_subsets_from_previous_run = Yes, but'
                           'no previous_run_path option was found.\n'
                           'Please add previous_run_path to config file.'
                           .format(config_file))
    else:
        use_train_subsets_from_previous_run = False
        if config.has_option('TRAIN', 'previous_run_path'):
            raise ValueError('In config.file {}, '
                             'use_train_subsets_from_previous_run = No, but '
                             'previous_run_path option was specified as {}.\n'
                             'Please fix argument or remove/comment out '
                             'previous_run_path.'
                             .format(config_file,
                                     config['TRAIN']['previous_run_path'])
                             )
        else:

            previous_run_path = None

    return TrainConfig(train_data_dict_path=train_data_dict_path,
                       train_set_durs=train_set_durs,
                       num_replicates=num_replicates,
                       val_data_dict_path=val_data_dict_path,
                       val_error_step=val_error_step,
                       checkpoint_step=checkpoint_step,
                       save_only_single_checkpoint_file=save_only_single_checkpoint_file,
                       n_max_iter=n_max_iter,
                       patience=patience,
                       normalize_spectrograms=normalize_spectrograms,
                       use_train_subsets_from_previous_run=use_train_subsets_from_previous_run,
                       previous_run_path=previous_run_path)