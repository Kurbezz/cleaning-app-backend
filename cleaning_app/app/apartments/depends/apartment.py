from fastapi import Depends, HTTPException, status

from app.apartments.models import Apartment as ApartmentModel
from app.users.depends import get_current_user_obj
from app.users.models import User


async def get_apartment(
    apartment_id: int, user: User = Depends(get_current_user_obj)
):
    apartment: ApartmentModel = (
        await user.apartments.select_related(["rooms"])
        .prefetch_related(["users"])
        .get_or_none(id=apartment_id)
    )

    if not apartment:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return apartment
