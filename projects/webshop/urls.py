from django.urls import path
from . import views

app_name = "webshop"

urlpatterns = [
    path('', views.homepage, name="home"),

    #category and products list
    path('category/<slug:category_slug>/', views.homepage, name="product_list_by_category"),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('all-products/', views.product_all, name="product_all"),
    path('products-by-user/<int:id>/', views.product_by_user, name="product_by_user"),

    #product add, update and delete
    path('add-product/', views.product_add, name='product_add'),
    path('edit-product/<int:id>/<slug:slug>/', views.product_update, name='product_update'),
    path('delete-product/<int:product_id>/', views.product_delete, name='product_delete'),


    #contact
    path('support/', views.contactpage, name="contact"),

    #user section
    path('register-user/', views.register, name="register"),
    path('login-user/', views.login, name="login"),
    path('logout-user/', views.logout, name="logout"),

    #user profile
    path('profile-user/<int:id>/', views.view_profile, name="view_profile"),
    path('profile-user/<int:id>/edit', views.edit_profile, name="edit_profile"),
    path('profile-user/<int:id>/delete', views.delete_profile, name="delete_profile"),

    #cart
    path('cart/', views.cart_detail, name="cart_detail"),
    path('add/<int:product_id>/', views.cart_add, name="cart_add"),
    path('remove/<int:product_id>/', views.cart_remove, name="cart_remove"),
]