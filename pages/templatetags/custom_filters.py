# your_app_name/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(query_set, pk_value):
    """
    Attempts to retrieve an object from a Django QuerySet by its primary key (id).
    Returns the object if found, otherwise None.
    """
    try:
        # We try to filter by 'id' as 'pk_value' is expected to be an ID
        return query_set.filter(id=pk_value).first()
    except (AttributeError, TypeError):
        # Handle cases where query_set is not a QuerySet or pk_value is invalid
        return None