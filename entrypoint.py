try:
    from app import create_app
except ImportError:
    from .app import create_app
    
apk = create_app("config.py")
