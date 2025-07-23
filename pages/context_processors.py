# your_app_name/context_processors.py

from .models import Category

def categories_for_search(request):
    """
    Context processor to make top-level categories and their subcategories
    available globally in templates, typically for navigation or search filters.
    """
    # Fetch top-level categories and prefetch their subcategories
    # This minimizes database queries when rendering the hierarchy
    top_level_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories').order_by('name')
    
    return {
        'top_level_categories': top_level_categories
    }
