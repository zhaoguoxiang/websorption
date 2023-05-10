import os
import time
from multiprocessing import Process
from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

from mlscripts.feature import runzeo,get_data
from myscripts.sendemail import sendresult
from myscripts.run_cif import cleanciffile

# Create your views here.
def receive_data(request:HttpRequest):
    username = request.POST.get('user')
    projectdir = '/'.join(['uploaddata',username,time.strftime('%y-%m-%d-%H-%M-%S')])
    os.makedirs(projectdir)
    file_object = request.FILES.get("cif")
    with open('/'.join([projectdir,file_object.name]),'wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)    
    return projectdir

def dojob(workdir,email):
    cleanciffile(workdir)
    runzeo(workdir)
    data=get_data(workdir)
    sendresult(str(data),email)    

def ml(request:HttpRequest):
    if request.method == 'GET':
        return render(request,'ml.html')
    
    projectdir = receive_data(request)
    #dojob(projectdir,request.POST.get('email'))
    p = Process(target=dojob,args=(projectdir,request.POST.get("email")))
    p.start()
    return HttpResponse('submit success!')
