from django.shortcuts import render
import os
from . import ninja
from hello import models
 
context = {}

def hello(request):
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def welcome(request):
    context['welcome'] = 'Welcome!'
    return render(request, 'welcome.html', context)

def function(request):
    context['function'] = 'Function!'
    if context['main'] == 'upload over!':
        func_list = models.FuncInfo.objects.all()
        context['function'] = func_list
    return render(request, 'function.html', context)

def instruction(request):
    context['instruction'] = 'Instruction!'
    return render(request, 'instruction.html', context)

def callfunction(request):
    context['callfunction'] = 'CallFunction!'
    return render(request, 'callfunction.html', context)

def path(request):
    context['path'] = 'Path!'
    return render(request, 'path.html', context)

def funchange(request):
    context['funchange'] = 'FunChange!'
    return render(request, 'funchange.html', context)

def main(request):
    context['main'] = 'Main!'
    if request.method == "POST":    # 请求方法为POST时，进
        myFile =request.FILES.get("file-input", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            returnHttpResponse("no files for upload!")  
        destination = open(os.path.join("F:\\HelloWorld\\upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()

        path = os.path.join("F:\\HelloWorld\\upload",myFile.name)
        bv = ninja.load_binary(path)
        ninja.get_func(bv)

        context['main'] = 'upload over!'
    return render(request, 'main.html', context)