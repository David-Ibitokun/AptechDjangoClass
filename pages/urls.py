# from django.urls import path
# from .views import (
#     home, about, shop, myAccount, page404,
#     login, register, myProfile, page500, add_product, product_list,
#     product_detail, brand_detail, brand_list, page503, remove_from_cart,
#     add_to_cart, search, wishlist_view, add_to_wishlist,
#     remove_from_wishlist, checkout, edit_product, delete_product, category_detail, view_cart, vendor_orders, contact,
#     recent_order, update_cart_quantity,order_detail,
# )

# urlpatterns = [
#     path('', home, name='home'),
#     path('about/', about, name='about'),
#     path('shop/', shop, name='shop'),
#     path('myAccount/', myAccount, name='myAccount'),
#     path('page404/', page404, name='page404'),
#     path('login/', login, name='login'),
#     path('register/', register, name='register'),
#     path('myProfile/', myProfile, name='myProfile'),
#     path('page500/', page500, name='page500'),
#     path('page503/', page503, name='page503'),

#     path('category/<slug:slug>/', category_detail, name='category_detail'),

#     path('product/add/', add_product, name='add_product'),
#     path('product/list/', product_list, name='product_list'),
#     path('product/<slug:slug>/', product_detail, name='product_detail'),

#     path('products/<slug:slug>/', singleProduct, name='singleProduct'),

#     path('product/<slug:slug>/edit/', edit_product, name='edit_product'),
#     path('product/<slug:slug>/delete/', delete_product, name='delete_product'),

#     path('brands/', brand_list, name='brand_list'),
    
#     path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
#     path('cart/', view_cart, name='cart'),
#     path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
#     path('cart/update/<int:item_id>/', update_cart_quantity, name='update_cart_quantity'), 

#     path('search/', search, name='search'),

#     path('wishlist/', wishlist_view, name='wishlist'),
#     path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
#     path('wishlist/remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),

#     path('checkout/', checkout, name='checkout'),
    
#     path('vendor/orders/', vendor_orders, name='vendor_orders'),
    
#     path('contact/', contact, name='contact'),
#     path('brands/<slug:slug>/', brand_detail, name='brand_detail'),
#     path('brands/<int:pk>/', brand_detail, name='brand_detail_by_id'), 

#     path('my-orders/', recent_order, name='recent_order'),
#     path('my-orders/<int:order_id>/', order_detail, name='order_detail'),
# ]



# your_app_name/urls.py

from django.urls import path
from .views import (
    home, about, shop, singleProduct, myAccount, page404,
    login, register, myProfile, page500, page503,
    add_product, product_list, product_detail, edit_product, delete_product,
    brand_detail, brand_list,
    remove_from_cart, add_to_cart, cart, view_cart, update_cart_quantity,
    search,
    wishlist_view, add_to_wishlist, remove_from_wishlist,
    checkout, # Ensure checkout_complete is imported
    vendor_orders, vendor_order_detail, # Ensure vendor_order_detail is imported
    category_detail,
    contact,
    recent_order, order_detail,
    user_dashboard,
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),
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
    path('products/<slug:slug>/', singleProduct, name='singleProduct'), # Ensure this is correct and not conflicting
    path('product/<slug:slug>/edit/', edit_product, name='edit_product'),
    path('product/<slug:slug>/delete/', delete_product, name='delete_product'),

    path('brands/', brand_list, name='brand_list'),
    path('brands/<slug:slug>/', brand_detail, name='brand_detail'),
    path('brands/<int:pk>/', brand_detail, name='brand_detail_by_id'), # For accessing brand by ID if needed

    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart_quantity, name='update_cart_quantity'),

    path('checkout/', checkout, name='checkout'),

    path('search/', search, name='search'),

    path('wishlist/', wishlist_view, name='wishlist'), # Changed name from 'wishlist' to 'wishlist_view' for consistency
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),

    path('vendor/orders/', vendor_orders, name='vendor_orders'),
    path('vendor/orders/<str:order_number>/', vendor_order_detail, name='vendor_order_detail'), # Vendor specific order detail

    path('contact/', contact, name='contact'),

    path('my-orders/', recent_order, name='recent_order'),
    path('my-orders/<str:order_number>/', order_detail, name='order_detail'), # User specific order detail

    path('user-dashboard/', user_dashboard, name='user_dashboard'), # User dashboard page
]
