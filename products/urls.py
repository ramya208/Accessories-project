
# from django.urls import path
# from . import views

# urlpatterns = [
#     # path("", views.signup_view, name="signup"),
#     path("", views.signup, name="signup"),

#     path("login/", views.login_view, name="login"),

#     path("products/", views.product_list, name="products"),
#     path("api/products/", views.ProductAPI.as_view(), name="product-api"),
#     path(
#     "add-product/",
#     views.add_product,
#     name="add-product"
# ),
# path(
#     "edit-product/<int:id>/",
#     views.edit_product,
#     name="edit-product"
# ),

#     # path('', views.home, name='home'),
# ]
from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.signup,
        name="signup"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "products/",
        views.product_list,
        name="products"
    ),

    path(
        "add-product/",
        views.add_product,
        name="add-product"
    ),

    path(
        "edit-product/<int:id>/",
        views.edit_product,
        name="edit-product"
    ),

    path(
        "api/products/",
        views.ProductAPI.as_view(),
        name="product-api"
    ),

    path(
        "api/products/<int:id>/",
        views.ProductDetailAPI.as_view(),
        name="product-detail-api"
    ),

     path(
        'token-login/',
        views.token_login,
        name='token-login'
    ),

]