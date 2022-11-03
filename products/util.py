import random
from pages.models import Notification
from products.models import (Product, Provider, ProductPackaging, ProductMoveType, Client, WhLocation,
                             ProductMove, ProductUnit, LogisticUnitCode)
from accounts.models import AppUser
from pages.util import rstri


PACKAGE_UNIT = "Unit"
PACKAGE_BOX = "Box"
PACKAGE_PALLET = "Pallet"
PACKAGE_OTHER = "Other"

MOVE_IN = "IN_BUY"
MOVE_IN_DESC = "Increase stock by Buy"
MOVE_IN_RFID = "IN_BUY_RFID"
MOVE_IN_RFID_DESC = "Increase stock by Buy with RFID tag"
MOVE_OUT = "OUT_SELL"
MOVE_OUT_DESC = "Decrease stock by Sell"
MOVE_OUT_USE = "OUT_USE"
MOVE_OUT_USE_DESC = "Decrease stock to internal usage"
MOVE_CHANGE = "CHANGE"
MOVE_CHANGE_DESC = "Change"
MOVE_CHANGE_ERROR = "CHANGE_ERROR"
MOVE_CHANGE_ERROR_DESC = "Change by Error"
MOVE_QUALITY = "QUALITY"
MOVE_QUALITY_DESC = "Quality Check"
MOVE_CHANGE_VALUATION = "CHANGE_VALUATION"
MOVE_CHANGE_VALUATION_DESC = "Change Valuation"
MOVE_CHANGE_GROUPING = "CHANGE_GROUPING"
MOVE_CHANGE_GROUPING_DESC = "Change Grouping"
MOVE_CHANGE_LOCATION = "CHANGE_LOCATION"
MOVE_CHANGE_LOCATION_DESC = "Change Location"
MOVE_RFID_FIND_ONE = "RFID_FIND_ONE"
MOVE_RFID_FIND_ONE_DESC = "RFID Find One Handheld reader"
MOVE_RFID_FIND_ALL = "RFID_FIND_ALL"
MOVE_RFID_FIND_ALL_DESC = "RFID Find All by Handheld reader"
MOVE_RFID_LECTURE = "RFID_LECTURE"
MOVE_RFID_LECTURE_DESC = "RFID Lecture by Fixed Antenna"

LOG_UNIT_TYPE_PRODUCT = "Product"
LOG_UNIT_TYPE_PRODUCT_UNIT = "ProductUnit"

def create_demo_data() -> str:
    # create package types
    pack1 = ProductPackaging(name = PACKAGE_UNIT)
    pack1.save()
    pack2 = ProductPackaging(name = PACKAGE_BOX)
    pack2.save()
    pack3 = ProductPackaging(name = PACKAGE_PALLET)
    pack3.save()

    # create product moves
    move_type1 = ProductMoveType(name = MOVE_IN, description = MOVE_IN_DESC)
    move_type1.save()
    move_type1b = ProductMoveType(name = MOVE_IN_RFID, description = MOVE_IN_RFID_DESC)
    move_type1b.save()
    move_type2 = ProductMoveType(name = MOVE_OUT, description = MOVE_OUT_DESC)
    move_type2.save()
    move_type2b = ProductMoveType(name = MOVE_OUT_USE, description = MOVE_OUT_USE_DESC)
    move_type2b.save()
    move_type3 = ProductMoveType(name = MOVE_CHANGE, description = MOVE_CHANGE_DESC)
    move_type3.save()
    move_type4 = ProductMoveType(name = MOVE_CHANGE_ERROR, description = MOVE_CHANGE_ERROR_DESC)
    move_type4.save()
    move_type5 = ProductMoveType(name = MOVE_QUALITY, description = MOVE_QUALITY_DESC)
    move_type5.save()
    move_type7 = ProductMoveType(name = MOVE_CHANGE_VALUATION, description = MOVE_CHANGE_VALUATION_DESC)
    move_type7.save()
    move_type7b = ProductMoveType(name = MOVE_CHANGE_GROUPING, description = MOVE_CHANGE_GROUPING_DESC)
    move_type7b.save()
    move_type9 = ProductMoveType(name = MOVE_CHANGE_LOCATION, description = MOVE_CHANGE_LOCATION_DESC)
    move_type9.save()
    move_type10 = ProductMoveType(name = MOVE_RFID_FIND_ONE, description = MOVE_RFID_FIND_ONE_DESC)
    move_type10.save()
    move_type11 = ProductMoveType(name = MOVE_RFID_FIND_ALL, description = MOVE_RFID_FIND_ALL_DESC)
    move_type11.save()
    move_type12 = ProductMoveType(name = MOVE_RFID_LECTURE, description = MOVE_RFID_LECTURE_DESC)
    move_type12.save()

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


def generate_rfid_code() -> str:
    return "123456789"


def proccess_product_move(product_move: ProductMove):
    assert product_move
    assert product_move.move_type
    if product_move.move_type.name == MOVE_IN:
        product_unit = ProductUnit(
            product = product_move.product,
            provider = product_move.provider,
            quantity = product_move.quantity,
            wh_location = product_move.wh_location_to,
            product_packaging = product_move.product_packaging,
            user = product_move.user,
            lot = product_move.lot,
            unit_valuation = product_move.unit_price,
            expiration_date = product_move.expiration_date,
            related_moves = product_move.pk
        )
        product_unit.save()
        # TODO check if qr required & generate
    elif product_move.move_type.name == MOVE_IN_RFID:
        product_unit = ProductUnit(
            product = product_move.product,
            provider = product_move.provider,
            quantity = product_move.quantity,
            wh_location = product_move.wh_location_to,
            product_packaging = product_move.product_packaging,
            user = product_move.user,
            lot = product_move.lot,
            unit_valuation = product_move.unit_price,
            expiration_date = product_move.expiration_date,
            related_moves = product_move.pk
        )
        product_unit.save()
        # TODO check if qr required & generate
        # create base object
        log_unit_code = LogisticUnitCode(
            entity=LOG_UNIT_TYPE_PRODUCT_UNIT, entity_id=product_unit.id,
            description=f"ProductUnit {product_unit.id}",
            rfid_code=product_move.rfid_code,
            entity_url=product_unit.get_absolute_url(), entity_api_url=product_unit.get_api_url()
        )
        log_unit_code.save()
    elif product_move.move_type.name == MOVE_OUT:
        product_unit = product_move.product_unit
        product_unit.quantity = product_unit.quantity - product_move.quantity
        product_unit.save()
    elif product_move.move_type.name == MOVE_OUT_USE:
        product_unit = product_move.product_unit
        product_unit.quantity = product_unit.quantity - product_move.quantity
        product_unit.save()
    elif product_move.move_type.name == MOVE_CHANGE_LOCATION:
        product_unit = product_move.product_unit
        product_unit.wh_location = product_move.wh_location_to
        product_unit.save()
    elif product_move.move_type.name == MOVE_CHANGE_GROUPING:
        product_unit = product_move.product_unit
        product_unit.product_packaging = product_move.product_packaging
        product_unit.save()
