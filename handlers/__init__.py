from handlers import default_mode, inline_mode

routers = [default_mode.router, inline_mode.router]

__all__ = ["routers"]
