import json

from users.models import UserInfo
from django.core.mail import send_mail
from django.views.generic import View
from django.http.response import HttpResponse,JsonResponse,HttpResponseBadRequest
from django.utils.decorators import method_decorator
from utils.captcha.captcha import captcha
import logging,re,hashlib
logger = logging.getLogger('django')
from django.conf import settings


def checklogin(func):
    def inner(request,*args,**kwargs):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = UserInfo.check_user_token(token[4:])
            if not user_id:
                logger.info("token错误")
                return JsonResponse({"status": -1, "msg": "请先登陆！"}, status=403)
            request.userid = user_id
        except KeyError as e:
            logger.error(e)
            return JsonResponse({"status": -1, "msg": "请先登陆！"}, status=403)
        except Exception as e:
            logger.error("请先登陆:%s"%e)
            return JsonResponse({"status": -1, "msg": "请先登陆！"}, status=403)

        return func(request,*args,**kwargs)

    return inner

class Captcha(View):
    """图片验证码"""

    def get(self, request, uuid):
        try:
            text, image = captcha.generate_captcha()
        except Exception as e:

            logger.error("验证码生成错误")
        else:
            request.session.set_expiry(60*60*2)
            request.session["captcha_%s" % uuid] = text

            return HttpResponse(image, content_type='images/jpg')

class Register(View):
    def post(self,request):

        params = json.loads(request.body)
        username = params.get("username")
        password = params.get("password")
        email = params.get("email")
        captcha = params.get("captcha")
        uuid = params.get("uuid")


        username = username if username and re.match(r'^\w{6,12}$',username) else ""
        password = password if password and re.match(r'^.{6,12}$',password) else ""
        email = email if email and re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email) else ""
        captcha = captcha if captcha and re.match(r'^[a-zA-Z0-9]{4}$',captcha) else ""
        uuid = uuid if uuid and re.match(r'^[a-z0-9-]{36}$',uuid) else ""

        if not(username and password and email and captcha and uuid):
            return JsonResponse({"status":-1,"msg":"格式不正确！"},status=401)
        elif self.request.session.get("captcha_%s" % uuid,"") and self.request.session.get("captcha_%s" % uuid).lower()!=captcha.lower():
            return JsonResponse({"status":-1,"msg":"验证码错误！"},status=401)
        try:
            password = hashlib.sha224(password.encode()).hexdigest()
            user = UserInfo.objects.create(
                username=username,
                password=password,
                email=email,
                )
        except Exception as e:

            return JsonResponse({"status":-1,"msg":"注册失败！"},status=401)

        token = user.genrate_user_token()
        data = {"username":user.username,"user_id":user.id,"token":token,"msg":"注册成功"}
        return JsonResponse(data,status=200)

class Login(View):
    def post(self,request):

        params = json.loads(request.body)
        username = params.get("username")
        password = params.get("password")
        captcha = params.get("captcha")
        uuid = params.get("uuid")

        username = username if username and re.match(r'^\w{6,12}$', username) else ""
        password = password if password and re.match(r'^.{6,12}$', password) else ""
        captcha = captcha if captcha and re.match(r'^[a-zA-Z0-9]{4}$', captcha) else ""
        uuid = uuid if uuid and re.match(r'^[a-z0-9-]{36}$', uuid) else ""

        if not(username and password and captcha and uuid):
            return JsonResponse({"status":-1,"msg":"格式不正确！"},status=401)
        elif self.request.session.get("captcha_%s" % uuid, "") and self.request.session.get(
            "captcha_%s" % uuid).lower() != captcha.lower():
            return JsonResponse({"status":-1,"msg":"验证码错误！"},status=401)

        try:
            password = hashlib.sha224(password.encode()).hexdigest()
            user = UserInfo.objects.get(username=username,password=password,)
        except UserInfo.DoesNotExist as e:
            return JsonResponse({"status":-1,"msg":"用户名或密码错误！"},status=401)
        token = user.genrate_user_token()
        data = {"username": user.username, "user_id": user.id, "token": token,"msg":"登陆成功"}
        return JsonResponse(data,status=200)

class Forgot(View):
    def get(self,request,uuid,email):
        text = captcha.generate_captcha(flag="text")[0]
        request.session["email_%s" % uuid] = text

        # 发送邮件
        try:
            send_mail('YesLab教务系统密码重置', '验证码：'+text, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            return JsonResponse({'msg': '邮件发送成功！'}, status=200)
        except Exception as e:
            logger.error("邮件发送失败：%s"%e)
            return JsonResponse({'msg': '邮件发送失败！'}, status=400)


    def post(self, request):

        params = json.loads(request.body)
        username = params.get("username")
        password = params.get("password")
        email = params.get('email')
        captcha = params.get("captcha")
        uuid = params.get("uuid")

        username = username if username and re.match(r'^\w{6,12}$', username) else ""
        password = password if password and re.match(r'^.{6,12}$', password) else ""
        email = email if email and re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email) else ""
        captcha = captcha if captcha and re.match(r'^[a-zA-Z0-9]{4}$', captcha) else ""
        uuid = uuid if uuid and re.match(r'^[a-z0-9-]{36}$', uuid) else ""

        if not(username and password and email and captcha and uuid):
            return JsonResponse({"status":-1,"msg":"格式不正确！"},status=401)
        elif self.request.session.get("email_%s" % uuid, "") and self.request.session.get(
            "email_%s" % uuid).lower() != captcha.lower():
            return JsonResponse({"status":-1,"msg":"验证码错误！"},status=401)

        # 对输入信息进行判断
        try:
            user = UserInfos.objects.get(username=username, email=email)
        except Exception as e:
            logger.info("用户不存在:%s"%e)
            return JsonResponse({'msg': '用户不存在或邮箱错误！'},status=400)

        password = hashlib.sha224(password.encode()).hexdigest()
        if user.password == password:
            logger.info("密码不能与旧密码相同")
            return JsonResponse({'msg': '密码不能与旧密码相同'},status=400)

        # 修改密码
        user.password = password
        user.save()

        return JsonResponse({'username': username, 'user_id': user.id, 'msg': 'successful'})


@method_decorator(checklogin, name='dispatch')
class UserInfos(View):
    def get(self, request, user_id):
        user = UserInfo.objects.get(id=user_id)
        name = user.realname
        email = user.email
        qq = user.qq
        phone = user.phone
        adress = user.adress
        if name and email and qq and phone and adress:
            dataList = {
                'name': name,
                'email': email,
                'qq': qq,
                'phone': phone,
                'adress': adress,
            }
            return JsonResponse(dataList)
        else:
            return HttpResponseBadRequest()

    def post(self, request, user_id):
        params = json.loads(request.body)
        name = params.get("name")
        phone = params.get("phone")
        qq = params.get('qq')
        adress = params.get("adress")

        name = name if name and re.match(r'^\w{1,12}$', name) else ""
        phone = phone if phone and re.match(r'^1[3456789]\d{9}$', phone) else ""
        qq = qq if qq and re.match(r'^\d{5,13}$',qq) else ""
        adress = adress if adress and re.match(r'^\w{1,20}$', adress) else ""

        if not(name and phone and qq and adress):
            return JsonResponse({"status":-1,"msg":"数据不完整或格式不正确！"},status=401)

        try:
            user = UserInfo.objects.get(id=user_id)
            user.realname = name
            user.phone = phone
            user.qq = qq
            user.adress = adress
            user.save()
            return JsonResponse({'msg': '保存成功'},status=200)
        except Exception as e:
            logger.error("个人信息保存失败%s"%e)
            return JsonResponse({'msg': '个人信息保存失败！'}, status=400)
