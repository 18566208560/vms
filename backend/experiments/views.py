import requests
from django.views import View
from django.http.response import JsonResponse,HttpResponse
from users.models import UserInfo
from users.views import checklogin
from django.utils.decorators import method_decorator
from experiments.models import Rack,Lab,LabModel,ReservationInfo
from django.db.models import Count
import json,re,time,datetime
from utils.snapshot import VMS
import logging
logger = logging.getLogger('django')
# Create your views here.

@method_decorator(checklogin, name='dispatch')
class GetRack(View):
    def get(self,request):
        """"获取rack列表"""
        data = Rack.objects.filter(rack_show=1)

        res = [{"id":i.id,"rack_name":i.rack_name} for i in data]

        return JsonResponse(res,safe=False)

@method_decorator(checklogin, name='dispatch')
class GetLab(View):
    def get(self,request,rack_id):

        # 获取 所有实验 列表
        data = LabModel.objects.filter(lab_m__lab_rack_id=rack_id).annotate(count=Count('lab_m'))
        print(data)
        res = [{"lab_name":i.lab_name,"count":i.count,"lab_tb":json.loads(i.lab_tb)} for i in data]
        print(res)

        return JsonResponse(res,safe=False)

@method_decorator(checklogin, name='dispatch')
class Reservation(View):
    def get(self,request,rack_id,lab_date):
        """获取 预约表展示信息 指定rack 和 日期的信息"""
        # 获取 日期
        lab_dates = datetime.date(*[int(i) for i in lab_date.split("-")])
        # 获取 预约实验 列表
        data = ReservationInfo.objects.filter(rack=rack_id,date=lab_dates)

        res = [{"lab":i.lab.lab_id.lab_name,"tb_id":i.tb_id,"user":i.user.realname,"date":lab_date} for i in data]
        return JsonResponse(res,safe=False)

    def post(self,request):
        """提交预约"""
        # {date: this.c_date, tb_id: tb_id, userid: this.userid, "rackid": this.rackid, "labname": lab_name},
        # {date: 2019-9-9, tb_id: 1/6:30-9:30, userid: 3, "rackid": 4, "labname": 攻防},
        # {date: this.c_date, tb_id: tb_id, userid: this.userid, "rackid": this.rackid, "labname": lab_name},
        # 》验证数据合法性  》tb_id提交时间(包括日期)就小于时间段时间开始前一分钟  》labname实验资源数量应在范围内
        # 》同一时段同一用户只能约一次  》用户同一时段不同实验 只能预约一个实验
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        datestr =req_data.get("date")
        tb_id =req_data.get("tb_id")
        userid =req_data.get("userid")
        rackid =req_data.get("rackid")
        labname =req_data.get("labname")

        date = datetime.date(*[int(i) for i in datestr.split("-")]) if re.match(r"\d{4}-\d{1,2}-\d{1,2}",datestr) else None
        if not all([date,tb_id,userid,rackid,labname]):
            logger.info("提交预约参数不完整：%s" % ([date, tb_id, userid, rackid, labname]))
            return JsonResponse({"status":"nok","msg":"请求数据有误"})

        # tb_id提交时间(包括日期)就小于时间段时间开始前一分钟
        tb = time.mktime(time.strptime(datestr+" "+tb_id.split("/")[1].split("-")[0],"%Y-%m-%d %H:%M"))
        if time.time()>tb-60:
            return JsonResponse({"status": "nok", "msg": "已超过预约时间！"})


        # labname实验资源数量应在范围内
        lab_num = ReservationInfo.objects.filter(date=date,tb_id=tb_id,rack=rackid,lab__lab_id__lab_name=labname)
        count = Lab.objects.filter(lab_id__lab_name=labname).count()   # 实验表中指定名称同一模型的数量
        print(count,lab_num.count())
        if count<=lab_num.count():
            return JsonResponse({"status": "nok", "msg": "当前时段已满员，请选择其它时段！"})

        # 同一时段同一用户只能约一次
        for i in lab_num:
            # print(type(i.user.id),type(userid),i.user.id==userid,"------------")
            if i.user.id == int(userid):
                return JsonResponse({"status": "nok", "msg": "你已预约此时段，请选择其它时段！"})

        # 用户同一时段不同实验 只能预约一个实验
        lab_user = ReservationInfo.objects.filter(date=date,user=userid)  # 获取用户当天所有预约 与当前时段检测冲突
        tb = [time.mktime(time.strptime(datestr + " " + j, "%Y-%m-%d %H:%M")) for j in tb_id.split("/")[1].split("-")]
        status = False
        for i in lab_user:
            st = [time.mktime(time.strptime(datestr + " " + j, "%Y-%m-%d %H:%M")) for j in i.tb_id.split("/")[1].split("-")]
            if tb[0]>st[1]:
                continue
            elif tb[1]<st[0]:
                continue
            else:
                status=True
                break
        if status:
            return JsonResponse({"status": "nok", "msg": "与其它已预约时段冲突，请选择其它时段！"})


        try:
            rack = Rack.objects.get(pk=rackid)
            user = UserInfo.objects.get(pk=userid)
            labs = Lab.objects.filter(lab_id__lab_name=labname)

            lab = [i for i in labs if i not in [j.lab for j in lab_num]]

            res = ReservationInfo.objects.create(
                date=date,
                tb_id=tb_id,
                rack=rack,
                lab=lab[0],
                user=user,
            )
        except (Rack.DoesNotExist,UserInfo.DoesNotExist) as e:
            logger.error("rack与userifno没有查询到数据%s"%e)
            return JsonResponse({"status": "nok", "msg": "数据错误！"})
        except Exception as e:
            logger.error("保存数据其它异常%s"%e)
            return JsonResponse({"status": "nok", "msg": "保存失败！"})
        else:
            return JsonResponse({"status": "ok", "msg": "预约成功！"})

@method_decorator(checklogin, name='dispatch')
class MyReservation(View):

    def get(self,request,userid):
        now = datetime.date.today()
        data = ReservationInfo.objects.filter(date__gte=now,user=userid).order_by("date")
        res = {}
        for i in data:
            obj = {"date":i.date.strftime("%Y-%m-%d"),"rack":i.rack.rack_name,"lab":i.lab.lab_id.lab_name,"tb_id":i.tb_id,"user":i.user.id,"id":i.id}
            if obj["date"] in res:
                res[obj["date"]].append(obj)
            else:
                res[obj["date"]] = [obj]
        res = {k:sorted(v,key=lambda x:x["tb_id"].split("/")[0]) for k,v in res.items()}
        return JsonResponse(res,safe=False)

    def post(self,request):
        """取消预约"""
        # 》开始前五分钟不能取消
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        id =req_data.get("id")
        datestr =req_data.get("date")
        tb_id =req_data.get("tb_id")
        userid =req_data.get("user")
        rackid =req_data.get("rack")
        labname =req_data.get("lab")

        date = datetime.date(*[int(i) for i in datestr.split("-")]) if re.match(r"\d{4}-\d{1,2}-\d{1,2}",datestr) else None
        if not all([id,date,tb_id,userid,rackid,labname]):
            logger.info("取消预约参数不完整：%s"%([id,date,tb_id,userid,rackid,labname]))
            return JsonResponse({"status":"nok","msg":"请求数据有误"})

        # tb_id取消时间(包括日期)就小于时间段时间开始前五分钟
        tb = time.mktime(time.strptime(datestr+" "+tb_id.split("/")[1].split("-")[0],"%Y-%m-%d %H:%M"))
        if time.time()>tb-60*5:
            return JsonResponse({"status": "nok", "msg": "当前时间不能取消！"})

        try:
            reser = ReservationInfo.objects.get(id=id)
        except ReservationInfo.DoesNotExist as e:
            logger.error("没有查询 到相应数据")
            return JsonResponse({"status": "nok", "msg": "参数有误！"})
        else:
            reser.delete()
            return JsonResponse({"status": "ok", "msg": "取消成功！"})


@method_decorator(checklogin, name='dispatch')
class Experiment(View):

    def get(self,request):
        gua_user = request.GET.get("user")

        lab = Lab.objects.get(lab_gua_user__contains=gua_user)

        doc = lab.lab_id.lab_doc

        return HttpResponse(doc)

    def post(self,request):
        # 进入实验
        # 》根据当前日期时间 获取用户预约信息 rack lab  labModel ，
        # 》根据lab 分配获取guacamole用户
        # 》根据lab 获取vms信息 作恢复快照操作

        json_str = request.body.decode()
        req_data = json.loads(json_str)
        id =req_data.get("id")
        datestr =req_data.get("date")
        tb_id =req_data.get("tb_id")
        userid =req_data.get("user")
        rackid =req_data.get("rack")
        labname =req_data.get("lab")

        #   验证数据 完整性
        date = datetime.date(*[int(i) for i in datestr.split("-")]) if re.match(r"\d{4}-\d{1,2}-\d{1,2}",datestr) else None
        print([id,date,tb_id,userid,rackid,labname],"-------------")
        if not all([id,date,tb_id,userid,rackid,labname]):
            logger.error("参数完整性有误")
            return JsonResponse({"status":"nok","msg":"请求数据有误"})

        #   验证数据 有效性
        try:
            res_data = ReservationInfo.objects.get(id=id,date=date,tb_id=tb_id,rack__rack_name=rackid,user=userid)
        except ReservationInfo.DoesNotExist as e:
            logger.error("参数有效性有误%s"%e)
            return JsonResponse({"status":"nok","msg":"请求数据有误"})

        # 验证当前进入实验时间段 在范围内
        st = [time.mktime(time.strptime(datestr+" "+i,"%Y-%m-%d %H:%M")) for i in res_data.tb_id.split("/")[1].split("-")]
        print(st,time.time())
        if not st[0]<time.time()<st[1]:
            logger.error(" 不在有效时间内")
            return JsonResponse({"status": "nok", "msg": "不在有效时间内"})

        # 获取 lab 对应的 guacamole 用户名|密码（用|分割）
        gua_user = res_data.lab.lab_gua_user
        userinfo = {"username": gua_user, "password": "admin123"}  # guacamole注册文请求数据
        url = "http://172.99.0.3:8080/guacamole/api/tokens"
        # url = "http://183.6.116.44:18080/remote/api/tokens"  # guacamole 注册

        res = requests.post(url, data=userinfo)
        if res.status_code == 200:
            return JsonResponse({"status":"ok","msg":"实验环境ok","data":res.text},status=200)
        else:
            logger.error(" guacamole token获取失败")
            return JsonResponse({"status":"nok","msg":"实验环境nok"},status=200)


@method_decorator(checklogin, name='dispatch')
class GetLabDoc(View):
    """获取 实验文档"""
    def post(self,request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        lab_name =req_data.get("lab_name")
        gua_name =req_data.get("gua_user")  # 通过guacamole 用户获取到对应的实验
        if not gua_name:
            logger.error("参数错误，没有获取到虚拟机名称")
            return JsonResponse({"status": "nok", "msg": "没有获取到虚拟机名称"}, status=400)

        try:
            lab = Lab.objects.get(lab_gua_user=gua_name)
            doc = lab.lab_id.lab_doc
            return JsonResponse({"status": "ok", "msg": "文档获取成功", "data": doc}, status=200)
        except Lab.DoesNotExist as e:
            logger.error("没有查询到虚拟机_%s"%e)
            return JsonResponse({"status": "nok", "msg": "文档获取失败"}, status=400)
        except Exception as e:
            logger.error("获取lab文档失败_%s" % e)
            return JsonResponse({"status": "nok", "msg": "文档获取失败"}, status=400)


@method_decorator(checklogin, name='dispatch')
class PowerOn(View):
    """开机"""
    def post(self,request):
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        lab_name =req_data.get("lab_name")
        gua_name =req_data.get("gua_user")  # 通过guacamole 用户获取到对应的实验
        if not gua_name and lab_name:
            logger.error("参数错误，没有获取到虚拟机名称")
            return JsonResponse({"status": "nok", "msg": "没有获取到虚拟机名称"}, status=400)
        try:
            lab = Lab.objects.get(lab_gua_user=gua_name)
            rack = lab.lab_rack_id
            vm = VMS(host=rack.rack_host,port=rack.rack_port,user=rack.rack_user,pwd=rack.rack_pwd)
            status = vm.poweronvm([lab_name])
            if status:
                return JsonResponse({"status": "ok", "msg": "开机成功"}, status=200)
            else:
                logger.error("开机 操作 失败")
                return JsonResponse({"status": "nok", "msg": "开机失败"}, status=200)
			
        except Lab.DoesNotExist as e:
            logger.error("gua帐户不存在：%s"%e)
            return JsonResponse({"status": "nok", "msg": "gua帐户不存在"}, status=400)
        except Exception as e:
            logger.error("其它错误 %s" % e)
            return JsonResponse({"status": "nok", "msg": "开机失败"}, status=400)


@method_decorator(checklogin, name='dispatch')
class Snapshot(View):
    """恢复快照"""
    def post(self,request):
        """
        恢复快照
        通过虚拟机名称 以及以###开头的快照名称(这里没有这个参数，创建虚拟时指定)恢复快照
        """
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        lab_name =req_data.get("lab_name")
        gua_name =req_data.get("gua_user")  # 通过guacamole 用户获取到对应的实验
        if not gua_name and lab_name:
            logger.error("参数错误，没有获取到虚拟机名称")
            return JsonResponse({"status": "nok", "msg": "没有获取到虚拟机名称"}, status=400)
        try:
            lab = Lab.objects.get(lab_gua_user=gua_name)
            rack = lab.lab_rack_id
            vm = VMS(host=rack.rack_host,port=rack.rack_port,user=rack.rack_user,pwd=rack.rack_pwd)
            status = vm.re_snapshot([lab_name])
            if status:
                return JsonResponse({"status": "ok", "msg": "恢复快照成功"}, status=200)
            else:
                logger.error("恢复快照 操作 失败")
                return JsonResponse({"status": "nok", "msg": "恢复快照失败"}, status=200)
			
        except Lab.DoesNotExist as e:
            logger.error("gua帐户不存在：%s"%e)
            return JsonResponse({"status": "nok", "msg": "gua帐户不存在"}, status=400)
        except Exception as e:
            logger.error("其它错误 %s" % e)
            return JsonResponse({"status": "nok", "msg": "恢复快照失败"}, status=400)


@method_decorator(checklogin, name='dispatch')
class Vmstate(View):
    """获取状态"""
    def post(self,request):
        """
        获取状态
        """
        json_str = request.body.decode()
        req_data = json.loads(json_str)
        lab_name =req_data.get("lab_name")
        gua_name =req_data.get("gua_user")  # 通过guacamole 用户获取到对应的实验
        if not gua_name and lab_name:
            logger.error("参数错误，没有获取到虚拟机名称")
            return JsonResponse({"status": "nok", "msg": "没有获取到虚拟机名称"}, status=400)
        try:
            lab = Lab.objects.get(lab_gua_user=gua_name)
            rack = lab.lab_rack_id
            vm = VMS(host=rack.rack_host,port=rack.rack_port,user=rack.rack_user,pwd=rack.rack_pwd)
            res = vm.getstate([lab_name])
            if res:
                return JsonResponse({"status": "ok", "msg": "获取状态成功","data":res}, status=200)
            else:
                logger.error("恢复快照 操作 失败  %s"%res)
                return JsonResponse({"status": "nok", "msg": "获取状态失败"}, status=200)	
        except Lab.DoesNotExist as e:
            logger.error("gua帐户不存在：%s"%e)
            return JsonResponse({"status": "nok", "msg": "gua帐户不存在"}, status=400)
        except Exception as e:
            logger.error("其它错误 %s" % e)
            return JsonResponse({"status": "nok", "msg": "获取状态失败"}, status=400)