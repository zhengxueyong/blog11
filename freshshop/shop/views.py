import hashlib
import random
import time
from urllib.parse import parse_qs

from django.core.cache import cache
from django.core.paginator import Paginator

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from shop.alipay import alipay
from shop.models import User, UserAddress, GoodsCategory, Goods, ShoppingCart, OrderInfo, OrderGoods


def index(request):#主页
    token=request.session.get('token')
    userid=cache.get(token)
    response_data={
        # 'user':None
    }
    if userid:
        user=User.objects.get(pk=userid)
        response_data['user']=user
        shopcarts=ShoppingCart.objects.filter(user=user)
        print(len(shopcarts))
        response_data['num']=len(shopcarts)


    goodcates=GoodsCategory.objects.all()
    # goodcate=goodcates.first()
    # goods=goodcate.goods_set.first()
    # print(goodcate.category_type,goods.name)
    response_data['goodcates']=goodcates
    # print(goodcates.first().get_category_type_foo())
    response_data['goods']=goodcates.first().goods_set.all()
    # print(goodcates.first().goods_set.all())
    return render(request,'index.html',context=response_data)


def generate_token():
    temp = str(time.time()) + str(random.random())
    md5 = hashlib.md5()
    md5.update(temp.encode('utf-8'))
    return md5.hexdigest()


def generate_password(param):
    md5 = hashlib.md5()
    md5.update(param.encode('utf-8'))
    return md5.hexdigest()

def register(request):
    if request.method=='GET':

        return render(request,'register.html')

    elif request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('pwd')
        cpassword=request.POST.get('cpwd')
        email=request.POST.get('email')
        if not(password==cpassword):#两次密码不正确
            return render(request,'register.html')
       #如果没有异常存入数据库中
        try:
            user=User()
            user.username=username
            user.password=generate_password(cpassword)
            user.email=email
            user.save()
            token=generate_token()
            cache.set(token,user.id,60*60*24*20)
            request.session['token']=token
            return redirect('shop:index')
        except:
            return render(request,'register.html')


def login(request):
    if request.method=='GET':
        return render(request,'login.html')

    elif request.method=='POST':
        username=request.POST.get('username')
        password=generate_password(request.POST.get('pwd'))
        users=User.objects.filter(username=username).filter(password=password)

        if users.exists():
            user=users.first()
            token=generate_token()
            cache.set(token,user.id,60*6000*24*3)
            request.session['token']=token

            return redirect('shop:index')
        else:
            return render(request,'login.html',context={'error':'用户名或密码错误'})


def logout(request):

    request.session.flush()
    return redirect('shop:index')


def info(request):#用户中心
    token = request.session.get('token')
    userid = cache.get(token)
    response_data = {
        # 'user':None
    }
    if userid:
        user = User.objects.get(pk=userid)
        response_data['user'] = user


        site=user.useraddress_set.last()
        response_data['site']=site


    return render(request,'user_center_info.html',context=response_data)


def site(request):#地址模板
    if request.method=='GET':
        token = request.session.get('token')
        userid = cache.get(token)

        response_data = {
            # 'user':None
        }
        if userid:
            user = User.objects.get(pk=userid)
            response_data['user'] = user
            site=user.useraddress_set.last()
            response_data['site']=site
        return render(request,'user_center_site.html',context=response_data)
    elif request.method=='POST':
        shouname=request.POST.get('shouname')
        site=request.POST.get('site')
        email=request.POST.get('email')
        phone=request.POST.get('phone')


        token = request.session.get('token')
        userid = cache.get(token)

        response_data = {
            # 'user':None
        }
        if userid:
            user = User.objects.get(pk=userid)
            response_data['user'] = user

        else:
            return redirect('shop:login')



        if not(shouname and site and email and phone):
            response_data['error']='请填写完整'
            return render(request,'user_center_site.html',context=response_data)

        useradress= UserAddress()
        useradress.user=user
        useradress.address=site
        useradress.signer_name=shouname
        useradress.signer_mobile=phone
        useradress.save()


        return redirect('shop:info')


def order(request):#订单模板
    token = request.session.get('token')
    userid = cache.get(token)

    response_data = {
        # 'user':None
    }
    if userid:
        user = User.objects.get(pk=userid)
        response_data['user'] = user
        page=int(request.GET.get('page',1))
        orders=user.orderinfo_set.all()
        p=Paginator(orders,3)
        orders=p.page(page)

        response_data['orders']=orders

    return render(request,'user_center_order.html',context=response_data)


def cart(request):#购物车
    token = request.session.get('token')
    userid = cache.get(token)

    response_data = {
        # 'user':None
    }
    if userid:
        print(userid)
        user = User.objects.get(pk=userid)
        response_data['user'] = user
        shocarts=ShoppingCart.objects.filter(user=user)
        # print(shocarts.first().goods.name)

        response_data['shopcarts']=shocarts
        sum = 0
        num=0
        for shopcart in shocarts:
            num=num+1
            sum=sum+(shopcart.nums*shopcart.goods.shop_price)
        response_data['sum']=sum
        response_data['num']=num

        return render(request,'cart.html',context=response_data)

    return redirect('shop:login')


def placeorder(request):
    token = request.session.get('token')
    userid = cache.get(token)

    response_data = {
        # 'user':None
    }
    if userid:
        print(userid)
        user = User.objects.get(pk=userid)
        response_data['user'] = user
        order=user.orderinfo_set.all().last()

        # print(order)
        response_data['order']=order
        allprice=0
        for ordergoods in order.goods.all():
            allprice=allprice+(ordergoods.goods_nums*ordergoods.goods.shop_price)
        response_data['allprice']=allprice
        response_data['nums']=len(order.goods.all())
    return render(request,'place_order.html',context=response_data)


def list(request):
    return  render(request,'list.html')


def detail(request,goodid):#商品细节
    token = request.session.get('token')
    userid = cache.get(token)

    response_data = {
        # 'user':None
    }
    if userid:
        print(userid)
        user = User.objects.get(pk=userid)
        response_data['user']=user
        shopcarts = ShoppingCart.objects.filter(user=user)
        print(len(shopcarts))
        response_data['num'] = len(shopcarts)
    good=Goods.objects.get(pk=goodid)


    response_data['good']=good

    return render(request,'detail.html',context=response_data)


def select(request):#查询商品
    keyword=request.POST.get('keyword')
    good=Goods.objects.filter(Q(name__contains=keyword) | Q(shop_price__contains=keyword)).first()
    if good==None:
        return HttpResponse('没有该商品')
    response_data = {}
    response_data['good'] = good


    return render(request,'detail.html',context=response_data)

#加入购物车
def addcart(request):
    token = request.session.get('token')
    userid = cache.get(token)

    response_data = {
        # 'user':None
    }
    if userid:#用户登陆后的情况
        print(userid)

        user = User.objects.get(pk=userid)

        goodid=request.GET.get('goodid')
        good = Goods.objects.get(pk=goodid)
        shopcarts=ShoppingCart.objects.filter(user=user).filter(goods=good)
        if shopcarts.exists():
            shopcart=shopcarts.first()
            shopcart.nums=shopcart.nums+int(request.GET.get('goodnum'))
            shopcart.save()



        else:
            shopcart=ShoppingCart()
            shopcart.goods=good
            shopcart.user=user
            goodnum=shopcart.nums+int(request.GET.get('goodnum'))
            shopcart.nums=goodnum
            shopcart.save()


        # print(goodid)

        shopcarts1 = ShoppingCart.objects.filter(user=user)  # 如果有登陆先获取用户购物车数量
        response_data['goodsnum'] = str(len(shopcarts1))


        response_data['msg']='success'
        response_data['statue']='1'
        response_data['good']=shopcart.user.username+'添加'+shopcart.goods.name+' 成功，数量为：'+str(shopcart.nums)+'当前购物车数量' + str(len(shopcarts1))
        return JsonResponse(response_data)

    # return redirect('shop:login')

#立即购买
def bug(request):
    token = request.session.get('token')
    userid = cache.get(token)

    response_data = {
        # 'user':None
    }
    if userid:#用户登陆后的情况
        print(userid)

        user = User.objects.get(pk=userid)
        goodid = request.GET.get('goodid')
        good = Goods.objects.get(pk=goodid)

        shopcart = ShoppingCart()
        shopcart.goods = good
        shopcart.user = user
        goodnum = int(request.GET.get('goodnum'))
        shopcart.nums = goodnum
        shopcart.save()
        response_data['msg'] = 'success'
        response_data['statue'] = '1'

        return JsonResponse(response_data)


###########################
#改变购物车的商品数量

def addgoods(request):
    goodid=request.GET.get('goodid')
    goodnums=request.GET.get('goodnums')
    token = request.session.get('token')
    userid = cache.get(token)

    response_data = {
        # 'user':None
    }
    if userid:  # 用户登陆后的情况
        print(userid)

        user = User.objects.get(pk=userid)

        good=Goods.objects.get(pk=goodid)


        shopcarts=ShoppingCart.objects.filter(user=user).filter(goods=good)
        shopcart=shopcarts.first()
        shopcart.nums=goodnums
        shopcart.save()
        newprice=int(shopcart.goods.shop_price)*int(goodnums)
        print(goodid,goodnums)
        allshopcarts=ShoppingCart.objects.filter(user=user)
        allsum=0
        for allshopcart in allshopcarts:
            allsum=allsum+(allshopcart.goods.shop_price*allshopcart.nums)

        response_data['allsum']=allsum
        response_data['status']=1
        response_data['message']='增加商品success'
        response_data['newprice']=str(newprice)



    return JsonResponse(response_data)


def subgoods(request):
    goodid = request.GET.get('goodid')
    goodnums = request.GET.get('goodnums')
    token = request.session.get('token')
    userid = cache.get(token)

    response_data = {
        # 'user':None
    }
    if userid:  # 用户登陆后的情况
        print(userid)

        user = User.objects.get(pk=userid)

        good = Goods.objects.get(pk=goodid)

        shopcarts = ShoppingCart.objects.filter(user=user).filter(goods=good)
        shopcart = shopcarts.first()
        shopcart.nums = goodnums
        shopcart.save()
        print(goodid, goodnums)
        allshopcarts = ShoppingCart.objects.filter(user=user)
        allsum = 0
        for allshopcart in allshopcarts:
            allsum = allsum + (allshopcart.goods.shop_price * allshopcart.nums)

        response_data['allsum'] = allsum

        newprice = int(shopcart.goods.shop_price) * int(goodnums)
        response_data['newprice'] = str(newprice)
        response_data['status'] = 1
        response_data['message'] = '减少商品success'

    return JsonResponse(response_data)

#删除购物车商品
def delgoods(request):
    token = request.session.get('token')
    userid = cache.get(token)
    goodid=request.GET.get('goodid')
    response_data = {
        # 'user':None
    }
    if userid:  # 用户登陆后的情况
        print(userid)

        user = User.objects.get(pk=userid)

        good = Goods.objects.get(pk=goodid)
        shopcart=ShoppingCart.objects.filter(user=user).filter(goods=good).first()
        shopcart.delete()
        response_data['status']=1
        response_data['message']='删除商品成功'
        shopcarts=ShoppingCart.objects.filter(user=user)
        response_data['newsum']=str(len(shopcarts))
        allshopcarts = ShoppingCart.objects.filter(user=user)
        allsum = 0
        for allshopcart in allshopcarts:
            allsum = allsum + (allshopcart.goods.shop_price * allshopcart.nums)

        response_data['allsum'] = allsum

    return JsonResponse(response_data)
#生成订单号
def generate_identifier():
    temp = str(time.time()) + str(random.randrange(1000,10000))
    return temp
#生成订单
def neworder(request):
    token = request.session.get('token')
    userid = cache.get(token)

    response_data = {
        # 'user':None
    }
    if userid:  # 用户登陆后的情况
        print(userid)

        user = User.objects.get(pk=userid)
        response_data['user'] = user
        shopcarts=user.shoppingcart_set.all()#用户购物车
        #遍历 取出商品总价
        # print(shopcarts.first()is None)
        if shopcarts.first() ==None:
            return redirect('shop:cart')

        allprice=0
        for shopcart in shopcarts:
            allprice=allprice+(shopcart.nums*shopcart.goods.shop_price)

    #用户地址表
        print(allprice)
        # useraddress=user.useraddress_set.all()
        # useraddres=useraddress.first()
        try:
            useraddress = user.useraddress_set.all()
            useraddres = useraddress.first()
            print(useraddres.address)
            #订单
            orderInfo=OrderInfo()
            orderInfo.user=user
            orderInfo.order_sn=generate_identifier()
            orderInfo.address=useraddres.address
            orderInfo.signer_name=useraddres.signer_name
            orderInfo.signer_mobile=useraddres.signer_mobile
            orderInfo.order_mount=allprice
            orderInfo.save()
            shopcarts = user.shoppingcart_set.all()


        except:
            return redirect('shop:site')
        # 生成订单详情表
        for shopcart in shopcarts:
            ordergoods = OrderGoods()
            ordergoods.order = orderInfo
            ordergoods.goods=shopcart.goods
            ordergoods.goods_nums=shopcart.nums
            ordergoods.save()
            shopcart.delete()

        return redirect('shop:placeorder')
    return redirect('shop:login')

def returnurl(request):
    return redirect('shop:index')


# 支付宝异步回调是post请求
@csrf_exempt
def appnotifyurl(request):
    if request.method == 'POST':
        # 获取到参数
        body_str = request.body.decode('utf-8')
        print(123123123)
        # 通过parse_qs函数
        post_data = parse_qs(body_str)

        # 转换为字典
        post_dic = {}
        for k,v in post_data.items():
            post_dic[k] = v[0]

        # 获取订单号
        out_trade_no = post_dic['out_trade_no']

        # 更新状态
        OrderInfo.objects.filter(order_sn=out_trade_no).update(status=1)


    return JsonResponse({'msg':'success'})


def pay(request):
    # print(request.GET.get('orderid'))

    orderid = request.GET.get('orderid')
    order = OrderInfo.objects.get(pk=orderid)

    sum = 0
    for orderGoods in order.ordergoods_set.all():
        sum += orderGoods.goods.shop_price * orderGoods.goods_nums

    # 支付地址信息
    data = alipay.direct_pay(
        subject='MackBookPro [256G 8G 灰色]', # 显示标题
        out_trade_no=order.order_sn,    # 爱鲜蜂 订单号
        total_amount=str(sum),   # 支付金额
        return_url='http://127.0.0.1:8000/shop/returnurl/'
    )

    # 支付地址
    alipay_url = 'https://openapi.alipaydev.com/gateway.do?{data}'.format(data=data)

    response_data = {
        'msg': '调用支付接口',
        'alipayurl': alipay_url,
        'status': 1
    }

    return JsonResponse(response_data)








