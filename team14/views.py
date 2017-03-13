from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import csv
import aws_connect
import subprocess
import thread
import time
import sys
# Create your views here.
import billing

def my_dashboard(request):
	return render_to_response('dashboard.html')

def billing_api(request):
    x=billing.coustm_billing()
    x.caluculate_metrics()
    l=[]
    try:
        with open('billing.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                l.append([row['id'], row['NetworkOut'],row ['Diskusage'],row['NetworkIn'],row ['ramusage']
                    ,row['CPUUtilization'], 0.5*float(row['NetworkOut'])+0.6*float(row ['Diskusage'])+0.6*float(row['NetworkIn'])+0.7*float(row ['ramusage'])])
        return render_to_response('billing.html',{'stats':l})
    except:
        return HttpResponse("</p>NO data, launch instance<p>")
def home_page(request):
    di=give_metrics()
    print di
    return render_to_response('index.html',{'di':di})

def instance_details(request):
    a = aws_connect.aws_instance_manager(conf={'region':'us-east-1'})
    return render_to_response('inst.html',{'stats':a.give_aws_details()})
def no_ins():
    a = aws_connect.aws_instance_manager(conf={'region':'us-east-1'})
    return len(a.give_aws_details())

def find_bill(request):
    return render_to_response('bills.html')

def launch_instance(request):
    try:
        o = aws_connect.aws_instance_manager({'region':'us-east-1'})
        ins = 0
        for i in range(int(request.GET.get('no'))):
            ins = o.create_instance({'ami_type':'ami-34a8a35c','key_name':'tanya','instance_type':'t2.micro','security_groups':['default']})
        if ins:
            return HttpResponse('launched')
        else:
            return HttpResponse('problem launching')
    except Exception as e:
        print str(e)

def render_emulator(request):
    ip = request.GET.get('ip_ad')
    try:
        subprocess.call(['fuser', '-k', '6080/tcp'])
        thread.start_new_thread(run_vnc,(ip+':5901',))
        time.sleep(1)
    except:
        print "thread error"
    return HttpResponse("fine")


def run_vnc(ip):
    try:
        subprocess.call(['./plz.sh',ip])
    except Exception as e:
        print str(e)

def give_metrics():
    cpu=0.0
    mem=0.0
    disk=0.0
    count=0
    with open('billing.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cpu+=float(row['CPUUtilization'])
            disk+=float(row['Diskusage'])
            mem+=float(row['ramusage'])
    count = no_ins()
    cpu = cpu/count
    disk = disk*(10.0/count)
    mem =  mem*(100.0/(992*count))
    return {'count':no_ins(),'cpu':cpu,'mem':mem,'disk':disk/10.0}

