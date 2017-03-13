from mtass import settings
import boto.ec2
import automation
import time

'''
type of conf expected keys
region
ami_type
key_name
instance_type
security_groups
'''

class aws_instance_manager:
    def __init__(self,conf):
        self.conn = boto.ec2.connect_to_region(conf['region'], aws_access_key_id=settings.aws_accesskey_id,
                                          aws_secret_access_key=settings.aws_secretaccess_key)


    def create_instance(self,conf):
        ins = self.conn.run_instances(conf['ami_type'], key_name=conf['key_name'], instance_type=conf['instance_type'],
                           security_groups=conf['security_groups'])
        ip_a = ''
        ins_id = ins.instances[0].id
        xj = -1
        while xj<0:
            l=self.conn.get_all_instances()
            for i in l:
                for j in i.instances:
                    if j.id == ins_id:
                        if j.state == 'running':
                            ip_a = j.ip_address
                            xj=1
            time.sleep(2)
        print "launched"
        if self.load_instance(ip_a):
            return ins
        else:
            return False


    def give_aws_details(self):
        ins = []
        ins_list=self.conn.get_all_instances()
        for i in ins_list:
            for j in i.instances:
                ins.append(j)
        l = []
        for i in ins:
            l.append({'id':i.id, 'running_time':i.launch_time, 'state':i.state, 'ip':i.ip_address})
        return l

    def load_instance(self,ip_a):
        au=automation.cloud_automator(conf={'host':ip_a,
                                      'user':'ubuntu','key_path':'/home/musunuru/Desktop/tanya.pem'})
        try:
            if True:
                au.run_command('vncserver')
                return True
        except:
            return False
