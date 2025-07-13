
from django.urls import path
from .views import home,about,shop,singleProduct,cart,myAccount,page404, login, register, myProfile, wishList, page500, add_product, product_list, product_detail, brand_detail, brand_list, page503

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),
    path('singleProduct/', singleProduct, name='singleProduct'),
    path('cart/', cart, name='cart'),
    path('myAccount/', myAccount, name='myAccount'),
    path('page404/', page404, name='page404'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('myProfile/', myProfile, name='myProfile'),
    path('wishList/', wishList, name='wishList'),
    path('page500/', page500, name='page500'),
    path('page503/', page503, name='page503'),
    path('product/add/', add_product, name='add_product'),
    path('product/list/', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('brands/', brand_list, name='brand_list'),
    path('brands/<int:brand_id>/', brand_detail, name='brand_detail'),
    # path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    # path('wishlist/', wishlist_view, name='wishlist'),
    # path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),

    # path('brands/int:brand_id/', brand_detail, name='brand_detail'),
]

