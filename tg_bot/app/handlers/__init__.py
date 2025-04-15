from .common import common_router
from .morse import morse_router

routers = [
    common_router,
    morse_router
]

__all__ = ["routers"]
