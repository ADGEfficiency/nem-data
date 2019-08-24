from flask import Config, Flask


class DevConfig(Config):
    """Development configuration."""
    ENV = 'development'
    DEBUG = True


class TestConfig(Config):
    """Development configuration."""
    ENV = 'test'
    TESTING = True
    DEBUG = True


def make_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(generator.blueprint)
