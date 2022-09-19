from asyncore import read
import random
import string
from products.models import Product, Provider, Notification
from accounts.models import AppUser


def create_demo_data() -> str:
    # create 20 providers with 10 products
    for i in range(1, 20):
        provider = Provider(
            cuit = rstri(13),
            name = f"TheProvider{i}-{rstri(3)}",
            contact = f"Phone: {rstri(3)}-{rstri(8)}"
        )
        provider.save()
        for j in range(1, 10):
            product = Product(
                name = f"SomeProduct{j}-{rstri(3)}",
                short_description = f"This is a product usefulf for some situations: {rstri(3)}, {rstri(4)} and {rstri(2)}",
                description = "This is a product",
                price = random.uniform(10.00, 110.00),
                provider = provider
            )
            product.save()
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


def rstri(length) -> str:
    """
    get random digits string of length
    """
    return ''.join(random.choice(string.digits) for x in range(length))
