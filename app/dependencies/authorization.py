from typing import Union
from fastapi import (
    Cookie,
    Query,
    Path,
    status,
    WebSocket,
    WebSocketException
)
from app.settings import settings


async def authorize(
    websocket: WebSocket,
    session: Union[str, None] = Cookie(default=None),
    organization_id: Union[int, None] = Query(),
    user_id: Union[int, None] = Query(), # TODO: Should be to validate access token
    channel: str = Path()

):
    '''Dependency to validate if the User is authorized to establish a connection'''
    if organization_id is None or channel not in settings.TOPICS.keys():
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return organization_id