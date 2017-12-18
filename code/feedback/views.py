# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from issue import *
from etc import *
import os

ERR_NO_SESSION_ID = 0x10; ERR_ROOT_ACCESSING = 0x20;
ERR_SECURITY_BREACH = 0x30;

@csrf_exempt
def feedback(request):
	fileType = []
	folderName = ''
	issue = []
	etc = []
        operation = request.POST.get('operation', '')
        directoryName = request.POST.get('dirName', '')

        if directoryName ==      '':
                directoryName = './'

        # __ NORMALIZE DIRECTORY PATH & PREVENT ERROR  __START__#
        (directoryName, status) = normalize_directory_path(request, directoryName)
        if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
                token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
                return render(request, 'coding/templates/error.html', token)

	# __ REDIRECT BETWEEN DIRECTORIES __START__#
        if operation == 'ReDirect':
                folderName = request.POST.get('folder', '')
                directoryName += folderName

        # __ GO TO PARENT DIRECTORY __START__#
        elif operation == 'GoBack':
                index = len(directoryName) - 2
                while index > 0: # Find a parent path until meeting '/' character
                        if directoryName[index] == '/':
                                break
                        index = index - 1
                directoryName = directoryName[:index]

        # __ ROOT DIRECTORY RESTRICTION __START__#
        (directoryName, status)= block_top_directory(request, directoryName)
        if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
                token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
                return render(request, 'coding/templates/error.html', token)

        # __ -L OPTION FOR FILE TYPE __START__#
        command = 'ls -l ' + "'" + directoryName + "'"
        result = os.popen(command).read().split('\n')[1:-1] # except first line(due to total info for ls command) & split by '\n'
        for _type in result:
                fileType.append(_type[0])

	# __ -1 OPTION FOR FILE NAME __START__#
        command = 'ls -1 ' + "'" + directoryName + "'"
        fileName = os.popen(command).read().split('\n')[:-1]

        # __ FOR FILE DATE __START__ #
        command = "ls -l " + "'" + directoryName + "'"  + " | awk '{print $6, $7, $8}'"
        fileDate = os.popen(command).read().split('\n')[1:-1]

        fileInfo = make_file_info(fileType, fileName, fileDate, 'NULL')

        rootDirectory = "./userDirectory/" + request.session['Directory'] + '/'
        isTopDirectory = 'false'
        if directoryName == rootDirectory:
                isTopDirectory = 'true'
	else:
		fileInfo = []
		for i in printIssue(folderName):
                        issue.append((i[0],i[1],i[2]))
                etc = get_single_item_data(get_index(folderName))

        token = {'fileInfo': fileInfo, 'dirName': directoryName, 'isTop': isTopDirectory,'folder':folderName,'issue':issue,'etc':etc}
	return render(request, 'feedback/templates/record.html', token)

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
			success = 'fail'
                        token = {'code': code, 'result':result, 'success':success, 'issue':issue, 'etc':etc}
                        return render(request, 'feedback/templates/feedbackEdit.html',token)
		os.popen('touch sonar-project.properties')
		os.popen('echo sonar.projectKey=testForFeedback>> sonar-project.properties')
		os.popen('echo sonar.projectName=testForFeedback>> sonar-project.properties')
		os.popen('echo sonar.projectVersion=2.0 >> sonar-project.properties')
		os.popen('echo sonar.sources=./test.java >> sonar-project.properties').close()
		os.popen('sonar-scanner')
		os.popen("rm test.java test.class error sonar-project.properties")
		result ='compile is finished'
		for i in printIssue('testForFeedback'):
			issue.append((i[0],i[1],i[2]))
		etc = get_single_item_data(get_index('testForFeedback'))
		success='ok'
        token = {'code': code, 'result':result, 'success':success,'issue':issue,'etc':etc}
        return render(request, 'feedback/templates/feedbackEdit.html',token)

def normalize_directory_path(request, _dirName):
        if _dirName == '' or _dirName == '.': # PREVENT __EMPTY SET ERROR__
                try:
                        _dirName = "./userDirectory/" + request.session['Directory'] # Relative Path must be used.
                except:
                        request.session.flush()
                        return (_dirName, ERR_NO_SESSION_ID)

        if _dirName[0] == '/': # PREVENT __ ROOT ACCESSING __ FOR SECURITY
                return (_dirName, ERR_ROOT_ACCESSING)

        if _dirName[-1] != '/': # PREVENT __DUPLICATED SLASH ERROR__
                _dirName += '/'
        _dirName = _dirName.replace('\n', '') # PRVENT __ENCODING ERROR__
        _dirName = _dirName.replace('\r', '')
        return (_dirName, 'Normal')

def block_top_directory(request, _currentDirectory):
        try:
                if request.session['Directory'] == '': # Session itself exists, but there is no contents.
                        return (_currentDirectory, ERR_NO_SESSION_ID)
        except:  # when there is no session['Directory'] value.
                return (_currentDirectory, ERR_NO_SESSION_ID)

        rootDirectory = "./userDirectory/" + request.session['Directory'] + '/'

        curLen = len(_currentDirectory)
        rootLen = len(rootDirectory)
        if curLen <= rootLen:
                return (rootDirectory, 'Normal')

        return (_currentDirectory, 'Normal')

def make_file_info(_fileType, _fileName, _fileDate, _filter):
        row = [] # [filetype, filename]
        output = [] # it would be 2D array --- [ [filetype_1, filename_1], [filetype_2, filename_2] ]

        # Exception Handler
        if _fileType == '' or _fileName == '' or _fileDate == '':
                print '[#ERR] __make_file_info()__: filetype or filename or fileDate is NULL'
                return "ERR:NULL"
        if len(_fileType) != len(_fileName) != len(_fileDate):
                print '[#ERR] __make_file_info()__: length of array of filetype and filename is not equal'
                return "ERR:LENGTH"

        # __ MAKE 2D LIST __START__#
        MAX = len(_fileType)
        for i in range(0, MAX):
                if _fileType[i] == '-': # case of file
                        extension = os.path.splitext(_fileName[i])[1].lower()
                        if extension == '.class':
                                continue
                        row.append(extension)
                else: # case of directory or other things
                        row.append(_fileType[i])
                row.append(_fileName[i])
                row.append(_fileDate[i])
                output.append(row)
                row = []

        # __ EXTENSION FILTER __START__#
        tempOut = []
        FILTER = []
        if _filter != 'NULL':
                if _filter == 'C':
                        FILTER.append('.c')
                        FILTER.append('.h')
                elif _filter == 'CPP':
                        FILTER.append('.cpp')
                        FILTER.append('.h')
                elif _filter == 'JAVA':
                        FILTER.append('.java')
                elif _filter == 'PYTHON':
                        FILTER.append('.py')
                        FILTER.append('.pyc')
                for _row in output:
                        if _row[0] == FILTER[0] or _row[0] == FILTER[1]:
                                tempOut.append(_row)
                output = tempOut

        return output
