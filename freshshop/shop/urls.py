from django.conf.urls import url
from django.views.static import serve

from freshshop import settings
from shop import views

urlpatterns=[
url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    url(r'^index/$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^info/$',views.info,name='info'),
    url(r'^site/$',views.site,name='site'),
    url(r'^order/$',views.order,name='order'),
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^placeorder/$',views.placeorder,name='placeorder'),
    url(r'^list/$',views.list,name='list'),
    url(r'^detail/(?P<goodid>\d+)$',views.detail,name='detail'),
    url(r'^select/$',views.select,name='select'),
    url(r'^addcart/$',views.addcart,name='addcart'),
    url(r'^addgoods/$',views.addgoods,name='addgoods'),
    url(r'^subgoods/$',views.subgoods,name='subgoods'),
#购物车删除商品
    url(r'^delgoods/$',views.delgoods,name='delgoods'),
    #生成订单
    url(r'^neworder/$',views.neworder,name='neworder'),
    #立即购买
    url(r'^bug/$',views.bug,name='bug'),
    url(r'^appnotifyurl/$', views.appnotifyurl, name='appnotifyurl'),  # 支付成功后，订单的处理
    url(r'^pay/$', views.pay, name='pay'),  # 支付


]