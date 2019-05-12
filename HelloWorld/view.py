from django.shortcuts import render
import os
from . import ninja
from hello import models
import json

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
    if request.method == 'POST':
        funcname = request.POST.get('name')
    if 'funcname' in dir():
        node = models.CallGraphNode.objects.get(name=funcname)
        node1 = {}
        node2 = []
        node1['num'] = node.num
        node1['name'] = node.name
        node2.append(json.dumps(node1, ensure_ascii=False))
        funcid = node.num
        edge = models.CallGraphEdge.objects.filter(start=funcid)
        edge1 = {}
        edge2 = []
        for e in edge:
            edge1['start'] = e.start
            edge1['end'] = e.end
            edge2.append(json.dumps(edge1, ensure_ascii=False))
            node = models.CallGraphNode.objects.get(num=e.end)
            node1['num'] = node.num
            node1['name'] = node.name
            node2.append(json.dumps(node1, ensure_ascii=False))
        context['callfunctionedge'] = edge2
        context['callfunctionnode'] = node2
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
            return HttpResponse("no files for upload!")  
        destination = open(os.path.join("F:\\HelloWorld\\upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()

        path = os.path.join("F:\\HelloWorld\\upload",myFile.name)
        bv = ninja.load_binary(path)
        ninja.get_func(bv)
        ninja.get_CG(bv)

        context['main'] = 'upload over!'
    return render(request, 'main.html', context)