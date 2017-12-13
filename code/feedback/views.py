# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from issue import *
from etc import *
import os

def feedback(request):
	return render(request, 'feedback/templates/record.html')

def test(request):
        return render(request, 'feedback/templates/test.html')

def feedbackEdit(request):
	code =''
	result = ''
	success = ''
	issue=[]
	etc = []
	if request.POST.get('operation','') == 'Write':
                code = request.POST.get('edit_data', '')
                f = open('test.java','w')
                f.write(code)
                f.close()
                compile_command = "javac test.java 2> error"
                os.popen(compile_command)
                result = os.popen("cat error").read()
                #have error
                if result.lower().find('error')>=0:
                	os.popen("rm test.java test.class error")
                        token = {'code': code, 'result':result}
                        return render(request, 'coding/templates/solveEdit.html',token)
		os.popen('touch sonar-project.properties')
		os.popen('echo sonar.projectKey=testForFeedback>> sonar-project.properties')
		os.popen('echo sonar.projectName=testForFeedback>> sonar-project.properties')
		os.popen('echo sonar.projectVersion=2.0 >> sonar-project.properties')
		os.popen('echo sonar.sources=. >> sonar-project.properties').close()
		os.popen('sonar-scanner')
		os.popen("rm test.java test.class error sonar-project.properties")
		result ='compile is finished'
		for i in printTestIssue():
			issue.append((i[0],i[1],i[2]))
		etc = get_single_item_data(get_index('testForFeedback'))
		success='ok'
        token = {'code': code, 'result':result, 'success':success,'issue':issue,'etc':etc}
        return render(request, 'feedback/templates/feedbackEdit.html',token)
