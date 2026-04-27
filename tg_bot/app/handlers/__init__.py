from .common import common_router
from .morse import morse_router
from .audio import audio_router


routers = [
    common_router,
    morse_router,
    audio_router
]

__all__ = ["routers"]
