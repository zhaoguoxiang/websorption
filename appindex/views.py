import os
import time
from multiprocessing import Process
from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from myscripts.main import run
# Create your views here.


def recive_data(request:HttpRequest):
    username = request.POST.get('user')
    projectdir = '/'.join(['uploaddata',username,time.strftime('%y-%m-%d-%H-%M-%S')])
    os.makedirs(projectdir)
    file_object = request.FILES.get("cif")
    with open('/'.join([projectdir,file_object.name]),'wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)    
    return projectdir

def index(request:HttpRequest):
    if request.method == 'GET':
        return render(request,'index.html')
    
    workdir = recive_data(request)
    p = Process(target=run,args=(workdir,request.POST.get("molecule"),request.POST.get("email")))
    p.start()
    return HttpResponse('submit success!')