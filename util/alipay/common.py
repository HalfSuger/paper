
from datetime import datetime

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes
import json
# 定义资源
class Pay(Resource):
    def post(self):
        # 获取订单号，根据订单生成 支付订单
        # 支付订单包括: 订单号、支付金额、订单名称

        # 传递参数执行支付类里的direct_pay方法，返回签名后的支付参数，
        url = alipay.direct_pay(
            subject="测试订单",  # 订单名称
            # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
            out_trade_no="201810021221",  # 订单号
            total_amount=100,  # 支付金额
            return_url="http://localhost:5000/paym/"
        )

        # 将前面后的支付参数，拼接到支付网关
        # 注意：下面支付网关是沙箱环境，最终进行签名后组合成支付宝的url请求
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        # 返回的是支付宝的支付地址
        return {'re_url': re_url}


# 添加资源
api.add_resource(Pay, '/paytest/')  # 支付接口