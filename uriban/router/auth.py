from enum import Enum

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.requests import Request

from uriban.api import api

__all__ = ("router",)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


class OauthTypeEnum(str, Enum):
    google = "google"


@router.get("/login")
async def login_list():
    res = []
    for i in OauthTypeEnum:
        res.append(f"/auth/login/{i}")
    return res


@router.get("/login/{oauth_type}")
async def login(oauth_type: OauthTypeEnum, request: Request):
    if oauth_type == OauthTypeEnum.google:
        return await api.oauth.google\
            .authorize_redirect(request, f"{str(request.url)[: -1 * len(request.url.path)]}/auth/callback/google")


@router.get("/callback/{oauth_type}")
async def callback(oauth_type: OauthTypeEnum, request: Request):
    if oauth_type == OauthTypeEnum.google:
        try:
            token = await api.oauth.google.authorize_access_token(request)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        user_data = await api.oauth.google.parse_id_token(request, token)
        user_data = dict(user_data)
        request.session["user"] = user_data

    return RedirectResponse(url="/")
