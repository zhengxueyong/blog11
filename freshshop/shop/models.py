from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=20,unique=True,null=True,blank=True,verbose_name='姓名')
    password=models.CharField(max_length=255,verbose_name='密码')
    birthday=models.DateField(null=True,blank=True,verbose_name='出生年月日')
    GENDER=(
        ('male',u'男'),
        ('female','女')
    )
    gender=models.CharField(max_length=6,choices=GENDER,default='female',verbose_name='性别')
    mobile=models.CharField(null=True,blank=True,max_length=11,verbose_name='电话')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        db_table = 'f_user'

class UserAddress(models.Model):

    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    province = models.CharField(max_length=100, default='', verbose_name='省份')
    city = models.CharField(max_length=100, default='', verbose_name='城市')
    district = models.CharField(max_length=100, default='', verbose_name='区域')
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='电话')
    signer_postcode = models.CharField(max_length=11, default='', verbose_name='邮编')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'f_user_address'


class GoodsCategory(models.Model):
    """
    Goods类别
    """
    CATEGORY_TYPE = (
        (1, '新鲜水果'),
        (2, '海鲜水产'),
        (3, '猪牛羊肉'),
        (4, '禽类蛋品'),
        (5, '新鲜蔬菜'),
        (6, '速冻食品'),
    )
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别')
    category_front_image = models.CharField(max_length=100, null=True, blank=True, verbose_name='封面图')

    class Meta:
        db_table = 'f_goods_category'

class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, verbose_name='商品类目', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='商品名')
    goods_sn = models.CharField(max_length=50, default='', verbose_name='商品唯一货号')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    sold_nums = models.IntegerField(default=0, verbose_name='销售量')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    goods_nums = models.IntegerField(default=0, verbose_name='商品库存')
    market_price = models.FloatField(default=0, verbose_name='市场价格')
    shop_price = models.FloatField(default=0, verbose_name='本店价格')
    goods_brief = models.CharField(max_length=500, verbose_name='商品简短描述')
    goods_desc = models.TextField(null=True)
    ship_free = models.BooleanField(default=True, verbose_name='是否承担运费')
    goods_front_image = models.ImageField(upload_to='static/images/', null=True, blank=True, verbose_name='封面图')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'f_goods'


        # -------------------------------------------------------------

class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name='数量')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'f_shopping_cart'



class OrderInfo(models.Model):
    """
    订单模型
    """
    ORDER_STATUS = {
        ('TRADE_SUCCESS', '成功'),
        ('TRADE_CLOSE', '交易关闭'),
        ('WAIT_BUYER_PAY', '交易创建'),
        ('TRADE_FINISHED', '交易结束'),
        ('paying', '待支付')
    }

    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='交易号')
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=20, verbose_name='交易状态')
    post_script = models.CharField(max_length=200, verbose_name='订单留言')
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    pay_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='支付时间')

    # 用户收货信息
    address = models.CharField(max_length=200, default='', verbose_name='收货地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='收货人')
    signer_mobile = models.CharField(max_length=11, verbose_name='联系电话')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')



class OrderGoods(models.Model):
    """
    订单详情商品信息模型
    """

    order = models.ForeignKey(OrderInfo, verbose_name='订单详情', related_name='goods', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    goods_nums = models.IntegerField(default=0, verbose_name='数量')


