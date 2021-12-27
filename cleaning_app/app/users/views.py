from fastapi import APIRouter, Depends, HTTPException, Request, status

from fastapi_users.manager import InvalidPasswordException, UserAlreadyExists
from fastapi_users.router.common import ErrorCode

from app.users.depends import get_current_active_user
from app.users.manager import UserManager, get_user_manager
from app.users.serializers import User, UserDB, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/api/me", response_model=User)
async def me(
    user: UserDB = Depends(get_current_active_user),
):
    return user


@router.patch(
    "/api/me",
    response_model=User,
    dependencies=[Depends(get_current_active_user)],
)
async def update_me(
    request: Request,
    user_update: UserUpdate,
    user: UserDB = Depends(get_current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        return await user_manager.update(
            user_update, user, safe=True, request=request
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )
