from omegaconf import OmegaConf

from src.appication.containers import Container
from src.appication import customization

container = Container()
cfg = OmegaConf.load('../config/config.yml')
container.config.from_dict(cfg)
container.wire([customization])

