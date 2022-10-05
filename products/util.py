import random
from pages.models import Notification
from products.models import Product, Provider, ProductPackaging, ProductMoveType, Client, WhLocation
from accounts.models import AppUser
from pages.util import rstri


PACKAGE_UNIT = "Unit"
PACKAGE_BOX = "Box"
PACKAGE_PALLET = "Pallet"

MOVE_ADD = "Increase by Buy"
MOVE_MINUS = "Decrease by Sell"
MOVE_CHANGE = "Change"
MOVE_CHANGE_ERROR = "Change by Error"
MOVE_LECTURE = "Lecture"
MOVE_QUALITY = "Quality Check"
MOVE_VALUATION = "Change Valuation"
MOVE_FIND = "Find"
MOVE_VALUATION = "Change Grouping"

def create_demo_data() -> str:
    # create package types
    pack1 = ProductPackaging(name = PACKAGE_UNIT)
    pack1.save()
    pack2 = ProductPackaging(name = PACKAGE_BOX)
    pack2.save()
    pack3 = ProductPackaging(name = PACKAGE_PALLET)
    pack3.save()

    # create product moves
    move_type1 = ProductMoveType(name = MOVE_ADD)
    move_type1.save()
    move_type2 = ProductMoveType(name = MOVE_MINUS)
    move_type2.save()
    move_type3 = ProductMoveType(name = MOVE_CHANGE)
    move_type3.save()
    move_type4 = ProductMoveType(name = MOVE_CHANGE_ERROR)
    move_type4.save()
    move_type5 = ProductMoveType(name = MOVE_LECTURE)
    move_type5.save()
    move_type6 = ProductMoveType(name = MOVE_QUALITY)
    move_type6.save()
    move_type7 = ProductMoveType(name = MOVE_VALUATION)
    move_type7.save()
    move_type8 = ProductMoveType(name = MOVE_FIND)
    move_type8.save()
    move_type9 = ProductMoveType(name = MOVE_VALUATION)
    move_type9.save()

    # create 20 providers with 10 products
    for i in range(1, 21):
        provider = Provider(
            cuit = rstri(13),
            name = f"TheProvider{i}-{rstri(3)}",
            contact = f"Phone: {rstri(3)}-{rstri(8)}"
        )
        provider.save()
        for j in range(1, 11):
            product = Product(
                name = f"SomeProduct{j}-{rstri(3)}",
                short_description = f"This is a product usefulf for some situations: {rstri(3)}, {rstri(4)} and {rstri(2)}",
                description = "This is a product",
                price = random.uniform(10.00, 110.00)
            )
            product.save()
            provider.products.add(product)
    # create 20 clients
    for i in range(1, 21):
        client = Client(
            cuit = rstri(13),
            name = f"TheClient{i}-{rstri(3)}",
            contact = f"Phone: {rstri(3)}-{rstri(8)}"
        )
        client.save()
    # create 3 locations
    for i in range(1, 4):
        location = WhLocation(
            name = f"Location{i}-{rstri(3)}",
            description = f"This is a sample location at gps: {rstri(3)}-{rstri(8)}"
        )
        location.save()
    users = AppUser.objects.all()
    for user in users:
        not1 = Notification(
            user = user,
            title = "Login Error",
            content = "Several errors on trying to login.",
            status = 'error',
        )
        not1.save()
        not2 = Notification(
            user = user,
            title = "Update completed",
            content = "Restart server 12 to complete the update.",
            status = 'event',
        )
        not2.save()
        not3 = Notification(
            user = user,
            title = "Job executed",
            content = "Job executed normally.",
            status = 'log',
        )
        not3.save()
        not4 = Notification(
            user = user,
            title = "Mail sended to client",
            content = "Mail sended related to product XXX.",
            status = 'mail',
        )
        not4.save()
        not5 = Notification(
            user = user,
            title = "Call to client",
            content = "Call to product XXX.",
            status = 'call',
            read=True
        )
        not5.save()
        not6 = Notification(
            user = user,
            title = "File added to product XXX",
            content = "File added to product XXX.",
            status = 'upload',
            read=True
        )
        not6.save()
    return "Create Demo Data created OK"
