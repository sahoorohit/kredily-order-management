from datetime import datetime
from typing import Optional

from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.utils import timezone


def get_paginated_objects(paginator: Paginator, page: int) -> Optional[Page]:
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = []

    return objects


def get_local_datetime(_datetime: datetime) -> str:
    return datetime.strftime(timezone.localtime(_datetime), "%d-%m-%Y %H:%M:%S")
