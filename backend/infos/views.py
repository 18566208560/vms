import datetime
import time,json
from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse,JsonResponse,HttpResponseBadRequest
from .models import InterviewInfo
from users.models import UserInfo
from utils.constant import TIME_BUKET,INTERVIEW_TIME_BUKET
from users.views import checklogin
from django.utils.decorators import method_decorator
import re,json,time
import logging
logger = logging.getLogger('django')

# Create your views here.


@method_decorator(checklogin, name='dispatch')
class Interview(View):
    def get(self,request):

        req_date = request.GET.get('date')
        date = datetime.date(*[int(i) for i in req_date.split("-")])
        interviews = InterviewInfo.objects.filter(date__gte=date)
        data = {}
        for interview in interviews:
            users = interview.user.values("realname","username")
            c_date = interview.date.strftime("%Y-%m-%d")
            info = {"users":list(users),"tb_id":interview.tb_id,"remaining":interview.num-len(users),"time_bucket": INTERVIEW_TIME_BUKET[interview.tb_id],"date":c_date}
            if data.get(c_date):
                data[c_date].append(info)
            else:
                data[c_date] = [info]
        print(data)
        return JsonResponse(list(data.values()), safe=False)


    def post(self,request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)

        date = req_data.get('date')
        tb_id = str(req_data.get('tb_id'))
        user_id = req_data.get('userid')
        print(date,type(tb_id),type(user_id))
        date = date if date and re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', date) else ""
        tb_id = tb_id if tb_id and re.match(r'^\d{1,2}$', tb_id) else ""
        user_id = user_id if user_id and re.match(r'^\d{1,5}$', user_id) else ""

        if not all([date, tb_id, user_id]):
            return JsonResponse({"msg": '参数不匹配'}, status=400)

        try:
            user = UserInfo.objects.get(id=user_id)
            info = InterviewInfo.objects.get(date=date,tb_id=tb_id)
            if info.user.count() >= info.num:
                return JsonResponse({"msg":'人数已达上限'},status=400)
            if user in info.user.all():
                return JsonResponse({"msg": '你已预约过此时段'}, status=400)
            info.user.add(user)
            return JsonResponse({"msg":"预约成功"})
        except Exception as e:
            logger.error(e)
            return JsonResponse({"msg":"参数错误"})


@method_decorator(checklogin, name='dispatch')
class MyInterview(View):
    def get(self,request):
        # 查询实验预约表
        user = UserInfo.objects.get(id=request.userid)
        # 通过用户表查询关联的interviewinfo（面试预约表），返回查询集
        intv_query = user.interviewinfo_set.all()
        # 通过用户表查询关联的中间表，返回中间表的数据

        intvList = []
        for q in intv_query:
            # 查询该时段共有多少个人预约
            data = {
                'date':datetime.date.strftime(q.date, '%Y-%m-%d'),
                'tb_id':q.tb_id,
                'time_bucket': INTERVIEW_TIME_BUKET[q.tb_id],
                'count':q.user.count(),
                'msg':q.comment
            }
            intvList.append(data)
        return JsonResponse(intvList,safe=False)

    def post(self,request):
        params = json.loads(request.body)
        date = params.get("date")
        tb_id = str(params.get("tb_id"))

        date = date if date and re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', date) else ""
        tb_id = tb_id if tb_id and re.match(r'^\d{1,2}$', tb_id) else ""

        if not all([date,tb_id]):
            return JsonResponse({"status":"nok","msg":"格式不正确！"},status=401)

        try:
            interview = InterviewInfo.objects.get(date=date,tb_id=tb_id)
            user = UserInfo.objects.get(id=request.userid)
            interview.user.remove(user)
            return JsonResponse({"status":"ok","msg":"取消面试成功"},status=200)
        except Exception as e:
            logger.error("取消面试预约操作失败：%s"%e)
            return JsonResponse({"status":"nok","msg":"取消面试失败"}, status=400)
