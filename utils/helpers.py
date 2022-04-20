from typing import Optional

from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator


def get_paginated_objects(paginator: Paginator, page: int) -> Optional[Page]:
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = []

    return objects
