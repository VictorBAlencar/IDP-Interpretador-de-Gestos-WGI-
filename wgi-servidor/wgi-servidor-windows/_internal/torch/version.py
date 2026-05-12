from typing import Optional

__all__ = ['__version__', 'debug', 'cuda', 'git_version', 'hip', 'rocm', 'xpu']
__version__ = '2.11.0+cpu'
debug = False
cuda: Optional[str] = None
git_version = '70d99e998b4955e0049d13a98d77ae1b14db1f45'
hip: Optional[str] = None
rocm: Optional[str] = None
xpu: Optional[str] = None
