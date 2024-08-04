from __future__ import annotations

from typing import Annotated

from authlib.integrations.starlette_client import OAuth
from fastapi import Depends
from starlette.config import Config

from app.service.random_generator import RandomNumberGenerator
from app.service.websocket_manager import WebSocketManager

_oauth_config: Config | None = None
_oauth: OAuth | None = None
_websocket_manager: WebSocketManager | None = None
_number_generator: RandomNumberGenerator | None = None


def get_oauth_config() -> Config:
    global _oauth_config
    if not _oauth_config:
        _oauth_config = Config(env_prefix="GITHUB_", env_file="app/.env.github")
    return _oauth_config


def register_oauth_client(config: OauthConfigDependency) -> OAuth:
    global _oauth
    if not _oauth:
        _oauth = OAuth(config)
        _oauth.register(
            name="github",
            client_id=config("CLIENT_ID"),
            client_secret=config("CLIENT_SECRET"),
            authorize_url="https://github.com/login/oauth/authorize",
            access_token_url="https://github.com/login/oauth/access_token",
            userinfo_endpoint="https://api.github.com/user",
            api_base_url="https://api.github.com",
            client_kwargs={"scope": "user:email"},
        )
    return _oauth


def get_websocket_manager() -> WebSocketManager:
    global _websocket_manager

    if not _websocket_manager:
        _websocket_manager = WebSocketManager()

    return _websocket_manager


def get_number_generator(
    ws_manager: WebSocketManagerDependency,
) -> RandomNumberGenerator:
    global _number_generator

    if not _number_generator:
        _number_generator = RandomNumberGenerator(ws_manager)

    return _number_generator


OauthConfigDependency = Annotated[Config, Depends(get_oauth_config)]
OauthClientDependency = Annotated[OAuth, Depends(register_oauth_client)]
WebSocketManagerDependency = Annotated[WebSocketManager, Depends(get_websocket_manager)]
NumberGeneratorDependency = Annotated[
    RandomNumberGenerator, Depends(get_number_generator)
]
