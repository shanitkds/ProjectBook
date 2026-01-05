from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name='home'),
    path("viewbook/",views.viewBook,name='viewbook'),
    path("createbook/",views.create_book,name='createbook'),
    path("updatebook/<int:id>",views.update,name='updatebook'),
    path("delete/<int:id>",views.delete,name='delete'),
    path("regi/",views.register_view,name='regi'),
    path("login/",views.login_view,name='login'),
    path("logout/",views.logout_view,name='logout'),
    path("add/<int:book_id>",views.add_cart,name='add'),
    path("viewcart/",views.view_cart,name='viewcart'),
    path("remove/<int:re_id>/",views.cart_remove,name='remove'),
    path("buy/<int:book_id>/",views.buy_now,name='buy'),
    path("success/",views.success,name='success'),
    path("cancel/",views.cancel,name='cancel'),
    
]