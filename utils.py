from omegaconf import OmegaConf
from wrman.config_classes.config import *

def open_config(file_path):
    try:
        with open(file_path, 'r') as file:
            omega_cfg = OmegaConf.structured(OmegaConf.load(file))
            cfg = Config(**omega_cfg)
            cfg.continuity_cfg = TestConfig(**cfg.continuity_cfg)
            cfg.leakage_cfg = TestConfig(**cfg.leakage_cfg)
            cfg.hipot_cfg = TestConfig(**cfg.hipot_cfg)
            cfg.isolation_cfg = TestConfig(**cfg.isolation_cfg)
            return cfg
    except ValueError as e:
        raise e

def fetch_wire_list_cfg(file_path=None):
    return open_config(file_path if file_path else "config.yaml")
    

def fetch_unused_list_cfg(file_path=None):
    return open_config(file_path if file_path else "config.yaml")

def fetch_grd_list_cfg(file_path=None):
    cfg: Config  = open_config(file_path if file_path else "config.yaml")
    cfg.continuity_cfg.update_block_name("GROUND_CONTINUITY_TESTS")
    return cfg