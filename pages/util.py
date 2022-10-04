import random
import string
from typing import List, Optional
from .models import Notification
from accounts.models import AppUser


def user_notifications(user: Optional[AppUser]) -> List[Notification]:
    if user and user.is_authenticated:
        return Notification.objects.filter(user__exact=user, read__exact=False)[:10] # Get 10 notifications
    return []


def rstri(length) -> str:
    """
    get random digits string of length
    """
    return ''.join(random.choice(string.digits) for x in range(length))
