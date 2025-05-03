from dialogs.user_dialogs import working_dialog, settings_dialog
from dialogs.default_mode import router as default_router
from dialogs.inline_mode import router as inline_router

routers = [default_router, inline_router]

__all__ = ["working_dialog", "routers", "settings_dialog"]
