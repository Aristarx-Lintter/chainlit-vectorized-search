from omegaconf import OmegaConf

from src.application.containers import Container
from src.application import customization

container = Container()
cfg = OmegaConf.load('config/config.yml')
container.config.from_dict(cfg)
container.wire([customization])
