from app import create_app
from config import get_config

config = get_config()
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host=config.get("HOST"), port=int(config.get("PORT")))
