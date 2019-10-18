import atexit
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnectNoSSL, Disconnect



class VMS(object):
    __instance = []
    def __new__(cls,*args,**kwargs):
        for obj in cls.__instance:
            if obj.host == kwargs["host"]:
                return obj
        else:
            cls.__instance.append(super().__new__(cls))
            return cls.__instance[-1]
        
    def __init__(self,host=None,port=443,user="root",pwd=None):
        self.host = host # "192.168.100.100"
        self.user = user # "root"
        self.pwd = pwd   # "BNcisco123"
        self.port = port # 443
        try:
            self.si = SmartConnectNoSSL(host=host, user=user, pwd=pwd, port=port)
            atexit.register(Disconnect, self.si)
            self.content = self.si.RetrieveContent()
            # self.content = self.si.content   # 跟上面作用一样
            self.vmList = self.get_vmlist()

        except vmodl.MethodFault as error:
            print("Caught vmodl fault : " + error.msg)



    def get_vmlist(self):#获取所有虚拟机列表
        obj = self.content.viewManager.CreateContainerView(self.content.rootFolder, [vim.VirtualMachine], True)
        return obj.view


    def wait_for_tasks(self, tasks):
        """Given the service instance si and tasks, it returns after all the
       tasks are complete
       """
        property_collector = self.si.content.propertyCollector
        task_list = [str(task) for task in tasks]
        # Create filter
        obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                     for task in tasks]
        property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,pathSet=[],all=True)
        filter_spec = vmodl.query.PropertyCollector.FilterSpec()
        filter_spec.objectSet = obj_specs
        filter_spec.propSet = [property_spec]
        pcfilter = property_collector.CreateFilter(filter_spec, True)
        try:
            version, state = None, None
            # Loop looking for updates till the state moves to a completed state.
            while len(task_list):
                update = property_collector.WaitForUpdates(version)
                for filter_set in update.filterSet:
                    for obj_set in filter_set.objectSet:
                        task = obj_set.obj
                        for change in obj_set.changeSet:
                            if change.name == 'info':
                                state = change.val.state
                            elif change.name == 'info.state':
                                state = change.val
                            else:
                                continue

                            if not str(task) in task_list:
                                continue

                            if state == vim.TaskInfo.State.success:
                                # Remove task from taskList
                                task_list.remove(str(task))
                            elif state == vim.TaskInfo.State.error:
                                raise task.info.error
                # Move to next version
                version = update.version
        finally:
            if pcfilter:
                pcfilter.Destroy()

    def getstate(self,vm_name):
        """
        获取虚拟机开机状态
        :param vm_name: list,要获取虚拟机列表 ["DR","jump-pc"]
        :return: dict {"jump-pc":"poweredOn","kali":"poweredOff"}
        

        """

        return [{"lab_name":vm.name,"lab_status":vm.runtime.powerState} for vm in self.vmList if vm.name in vm_name]



    def poweronvm(self,vm_name):  # 打开虚拟机
        """
        :param vm_name: list,要打开虚拟机列表 ["DR","jump-pc"]
        :return: true or false
        """

        try:
            tasks = [vm.PowerOn() for vm in self.vmList if vm.name in vm_name]
            print(tasks,vm_name)

            self.wait_for_tasks(tasks)
            print("打开完成")
            return True
        except Exception as e:

            return False


    def re_snapshot(self,vm_names):##恢复快照
        """
        恢复快照
        :param vm_name: ["虚拟机名称"，"虚拟机名称"]  # 改为不指定快照名称 以 ### 开头 在这里快照名称 没有什么作用， 待需求明确，再作代码 修改
        :return: true or false
        """
        snap_objs = []
        for vm in self.vmList:
            if vm.name in vm_names:
                snapshots = vm.snapshot.rootSnapshotList
                snap_obj = get_snapshot(snapshots)
                snap_objs.append(snap_obj)
        print(snap_objs)
        try:
            task = [snap_obj.RevertToSnapshot_Task() for snap_obj in snap_objs]
            self.wait_for_tasks(task)
            print("恢复完成")
            return True
        except Exception as e:

            return False


def get_snapshot(root):
    for i in root:

        if i.name.startswith("###"):   # 改为不指定快照名称 ，创建 快照时指定名称 以 ### 开头
            return i.snapshot
        if hasattr(i,"childSnapshotList") and i.childSnapshotList:
            res = get_snapshot(i.childSnapshotList)
            if res:
                return res
    return False


if __name__ == "__main__":
    host = "192.168.127.101"
    user = "root"
    pwd = "0.0010.0"
    port = 443
    vm = VMS(host=host,port=port,user=user,pwd=pwd)
    obj = vm.get_vmlist()
    for v in obj:
        print("-"*30)
        print(dir(v))
        print("-*-:",v.name)
        print("-*-:",v.runtime.powerState)
        print("-*-:",v.snapshot)
        print("-*-:",v.snapshot.rootSnapshotList)
        print("-*-:",v.snapshot.rootSnapshotList[0].snapshot)
        print("-*-:",type(v.snapshot.rootSnapshotList[0].snapshot))
        print("-*-:",v.summary.quickStats)
    print("*"*30)
    vm.re_snapshot(["Tiny Core Linux"])
    # vm.poweronvm(["DR","jump-pc"])
    # vm.re_snapshot({"DR":"test","jump-pc":"test"})

