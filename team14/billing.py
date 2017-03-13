import boto.ec2.cloudwatch
from mtass import settings
import datetime
import csv
import paramiko

class coustm_billing:

    def __init__(self):
        self.main_conn = boto.ec2.connect_to_region("us-east-1",aws_access_key_id=settings.aws_accesskey_id,
                                                    aws_secret_access_key=settings.aws_secretaccess_key)
        self.conn = boto.ec2.cloudwatch.CloudWatchConnection(
            aws_access_key_id = settings.aws_accesskey_id,
            aws_secret_access_key = settings.aws_secretaccess_key)
        self.metrics = ['NetworkOut', 'DiskReadBytes', 'NetworkIn', 'DiskWriteBytes', 'CPUUtilization', 'Diskusage','ramusage']
        self.instance_list = self.main_conn.get_all_instances()
        self.instance_id=[]
        self.ip = {}
        for i in self.instance_list:
            for j in i.instances:
                if j.state == 'running':
                    self.instance_id.append(j.id)
                    self.ip[j.id] = j.ip_address



    def caluculate_metrics(self):
        metric_dict = {}
        di = { 'NetworkOut':0.0, 'DiskReadBytes':0.0, 'NetworkIn':0.0, 'DiskWriteBytes':0.0, 'CPUUtilization':0.0,
               'Diskusage':0.0,'ramusage':0.0 }
        try:
            with open('billing.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    di['NetworkOut'] = row['NetworkOut']
                    di['DiskReadBytes'] = row ['DiskReadBytes']
                    di['NetworkIn'] = row['NetworkIn']
                    di['DiskWriteBytes'] = row ['DiskWriteBytes']
                    di['CPUUtilization'] = row['CPUUtilization']
                    di['Diskusage']=0
                    di['ramusage']=0
                    metric_dict[row['id']] = di
                csvfile.truncate()
        except:
            for i in self.instance_id:
                metric_dict[i]=di
        with open('billing.csv', 'w') as csvfile:
            fieldnames = ['id','NetworkOut', 'DiskReadBytes', 'NetworkIn', 'DiskWriteBytes', 'CPUUtilization','Diskusage','ramusage']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader(),
            for inst in self.instance_id:
                for i in di.keys():
                    if i=='Diskusage':
                        metric_dict[inst][i] = self.disk_usage(inst)
                        continue
                    if i=='ramusage':
                        metric_dict[inst][i] = self.ram_usage(inst)
                        continue

                    metric_dict[inst][i] = float(metric_dict[inst][i]) + self.find_metrics(i,inst)


                writer.writerow({'id':inst, 'NetworkOut':metric_dict[inst]['NetworkOut'],
                                 'DiskReadBytes':metric_dict[inst]['DiskReadBytes'],
                                 'NetworkIn':metric_dict[inst]['NetworkIn'],
                                 'DiskWriteBytes':metric_dict[inst]['DiskWriteBytes'],
                                 'CPUUtilization':metric_dict[inst]['CPUUtilization'],
                                 'Diskusage':metric_dict[inst]['Diskusage'],
                                 'ramusage':metric_dict[inst]['ramusage']})


    def find_metrics(self,metric_type,ins_id):
        flag=0
        l=self.conn.get_metric_statistics(
                300,
                datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
                datetime.datetime.utcnow(),
                metric_type,
                'AWS/EC2',
                'Average',
                dimensions={'InstanceId':[ins_id]})
        count=0.0
        for i in l:
            if metric_type not in ['CPUUtilization']:
                count=count+5*i['Average']
                flag=1

            else:
                count = count+i['Average']
        if flag==1:
            return count/1024.0
        else:
            return count/12


    def disk_usage(self,id):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip[id], username='ubuntu', key_filename='/home/musunuru/Desktop/tanya.pem')
        stdin, stdout, stderr = ssh.exec_command('df')
        x=stdout.readlines()
        return x[1].split()[4][:2]

    def ram_usage(self,id):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip[id], username='ubuntu', key_filename='/home/musunuru/Desktop/tanya.pem')
        stdin, stdout, stderr = ssh.exec_command('free -m')
        x=stdout.readlines()
        x=x[1].split()
        print x[2]
        print x[1]
        x=float(x[2])/float(x[1])
        print x
        return (x*100)
