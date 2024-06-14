from entities.user import User
from entities.inventory import InventoryLine
from functional.phrases import Phrases

from typing import List


def represent_user(user: User, inventory: List[InventoryLine], phrase: Phrases) -> str:
    tg_id, name, phone, email, is_admin, district =\
        user.tg_id, user.name, user.phone, user.email, user.is_admin, user.district
    if not email:
        email = phrase["main"]["not_specified"]
    role = phrase["main"]["admin"] if is_admin else phrase["main"]["volunteer"]
    if not district:
        district = phrase["main"]["not_specified"]
    string = phrase["main"]["info"].format(id=tg_id, name=name, phone=phone,
                                           email=email, role=role, district=district)
    if inventory:
        string += phrase["main"]["inventory"]["text"]
        for item in inventory:
            string += phrase["main"]["inventory"]["line"].format(tags_line=" ".join(item.tags),
                                                                 volume=item.volume)
    return string
