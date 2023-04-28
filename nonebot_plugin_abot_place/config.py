import sys
from typing import Optional, Union, Set, Tuple

from nonebot import get_driver
from pydantic import BaseModel

# get package version
if sys.version_info < (3, 10):
    from importlib_metadata import version
else:
    from importlib.metadata import version

try:
    __version__ = version("nonebot_plugin_bilichat")
except Exception:
    __version__ = None


class Config(BaseModel):
    place_view_aliases: Optional[Set[Union[str, Tuple[str, ...]]]]
    color_view_aliases: Optional[Set[Union[str, Tuple[str, ...]]]]
    place_draw_aliases: Optional[Set[Union[str, Tuple[str, ...]]]]


plugin_config = Config.parse_obj(get_driver().config)
