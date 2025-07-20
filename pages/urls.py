from django.urls import path
from .views import (
    home, about, shop, singleProduct, myAccount, page404,
    login, register, myProfile, page500, add_product, product_list,
    product_detail, brand_detail, brand_list, page503, remove_from_cart,
    add_to_cart, cart, search, wishlist_view, add_to_wishlist,
    remove_from_wishlist, checkout, edit_product, delete_product, category_detail, view_cart  # 👈 Include these
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),
    path('singleProduct/', singleProduct, name='singleProduct'),
    path('myAccount/', myAccount, name='myAccount'),
    path('page404/', page404, name='page404'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('myProfile/', myProfile, name='myProfile'),
    path('page500/', page500, name='page500'),
    path('page503/', page503, name='page503'),

    path('category/<slug:slug>/', category_detail, name='category_detail'),

    path('product/add/', add_product, name='add_product'),
    path('product/list/', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),

    path('product/<slug:slug>/edit/', edit_product, name='edit_product'),
    path('product/<slug:slug>/delete/', delete_product, name='delete_product'),

    path('brands/', brand_list, name='brand_list'),
    path('brands/<int:brand_id>/', brand_detail, name='brand_detail'),

    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),

    path('search/', search, name='search'),

    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),

    path('checkout/', checkout, name='checkout'),
]
