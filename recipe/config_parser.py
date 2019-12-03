import os, sys
from ConfigParser import SafeConfigParser

def read_config(ini_path):
    if not os.path.exists(ini_path):
        print 'No selfuch config file %s' % (ini_path)
        sys.exit(1)
    cfg = SafeConfigParser()
    cfg.read(ini_path)
    cfg_ini_dict = config_as_dict(cfg)
    return cfg_ini_dict


def config_as_dict(cfg):
    """
    """
    cfg_dict = {}
    for section in cfg.sections():
        cfg_dict[section] = {}
        for k, v in cfg.items(section):
            cfg_dict[section][k] = v
    return cfg_dict
