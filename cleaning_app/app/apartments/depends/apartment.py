from fastapi import Depends, HTTPException, status

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.apartments.models import Apartment as ApartmentModel


async def get_apartment(apartment_id: int, user: User = Depends(get_current_user_obj)):
    apartment: ApartmentModel = await user.apartments.select_related(
        ["users", "rooms"]
    ).get_or_none(id=apartment_id)

    if not apartment:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return apartment
