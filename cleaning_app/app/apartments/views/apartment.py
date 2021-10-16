from fastapi import APIRouter, Depends

from fastapi_pagination import LimitOffsetPage, LimitOffsetParams
from fastapi_pagination.ext.ormar import paginate

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.apartments.models import Apartment as ApartmentModel
from app.apartments.serializers.apartment import (
    Apartment,
    CreateApartment,
    UpdateApartment,
)
from app.apartments.depends.apartment import (
    get_apartment as get_apartment_depends,
)


apartments_router = APIRouter(prefix="/api/apartments", tags=["apartments"])


@apartments_router.get(
    "",
    response_model=LimitOffsetPage[Apartment],
    dependencies=[Depends(LimitOffsetParams)],
)
async def get_all_apartments(user: User = Depends(get_current_user_obj)):
    return await paginate(
        user.apartments.select_related(["users", "rooms"]).queryset
    )


@apartments_router.post("", response_model=Apartment)
async def create_apartment(
    data: CreateApartment, user: User = Depends(get_current_user_obj)
):
    apartment = await ApartmentModel.objects.create(**data.dict())
    await apartment.users.add(user)
    return apartment


@apartments_router.get("/{apartment_id}", response_model=Apartment)
async def get_apartment(
    apartment: ApartmentModel = Depends(get_apartment_depends),
):
    return apartment


@apartments_router.put("/{apartment_id}", response_model=Apartment)
async def update_apartment(
    data: UpdateApartment,
    apartment: ApartmentModel = Depends(get_apartment_depends),
):
    return await apartment.update_from_dict(data.dict()).update()


@apartments_router.delete("/{apartemnt_id}", response_model=Apartment)
async def delete_apartment(
    apartment: ApartmentModel = Depends(get_apartment_depends),
):
    await apartment.delete()

    return apartment
