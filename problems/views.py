#coding: utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import Problems
from utils import IDGenerator

# Create your views here.

def showProblems(request):
	nickname = request.session['nickname']
	problems = Problems.objects()
	
	return render(request, 'showProblems.html', locals())

def addProblems(request):
	return render(request, 'addProblems.html')

def addProblemsCheck(request):
	try:
		rawProblem = request.POST['problem']
		rawOptions = request.POST['options']
		rawAnswer = request.POST['answer']
	except:
		return render(request, 'info.html', {'info': '提交内容不完整'})

	myID = IDGenerator().getRandomID()
	print myID
	problem = rawProblem.strip('\r\n')
	options = rawOptions.split('\n')
	answer = rawAnswer.strip('\r\n')
	problem = Problems(myID=myID, problem = problem, options = options, answer = answer)
	problem.save()

	return HttpResponseRedirect('/showProblems/')

def editProblem(request):
	try:
		myID = request.GET['myID']
	except:
		info = '错误的请求方式'
		return render(request, 'info.html', locals())
	problem = Problems.objects(myID = myID)
	if len(problem) == 0:
		info = '错误的请求ID'
		return render(request, 'info.html', locals())

	problem = problem[0]
	problem.options = '\n'.join(problem.options)
	print problem.options
	return render(request, 'editProblem.html', {'problem': problem})