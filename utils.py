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