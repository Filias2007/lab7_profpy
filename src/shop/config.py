import os

def load_config() -> dict:
    env = os.getenv("SHOP_ENV", "development")
    debug_str = os.getenv("SHOP_DEBUG", "true").lower()
    debug = debug_str in ("true", "1", "yes")
    return {
        "env": env,
        "debug": debug,
    }