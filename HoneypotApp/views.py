from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os


def DownloadFileDataRequest(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        flag = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'only4MySQL', database = 'HoneypotAppDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM files where filename='"+name+"' and filepassword='"+password+"'")
            rows = cur.fetchall()
            for row in rows:
                flag = 1
                break
        print("======================="+str(flag))    
        if flag == 1:
            with open('static/files/'+name, 'rb') as fh:
                response = HttpResponse(fh.read(),content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename='+name
                return response
        else:
            with open('static/files/second.pdf', 'rb') as fh:
                response = HttpResponse(fh.read(),content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename=second.pdf'
                return response
    
def DownloadFile(request):
    if request.method == 'GET':
        name = request.GET.get('id', False)
        output = '<tr><td><font size="" color="black">File&nbsp;Name</b></td><td><input type="text" name="t1" value="'+name+'" readonly>'
        output+='<tr><td><font size="" color="black">Password</b></td><td><input type="text" name="t2">'
        context= {'data':output}
        return render(request, 'DownloadFileData.html', context)           
    

def Download(request):
    if request.method == 'GET':
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>User Name</font></th>'
        output+='<th><font size=3 color=black>File Name</font></th>'
        output+='<th><font size=3 color=black>File Password</font></th>'
        output+='<th><font size=3 color=black>Download File</font></th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'only4MySQL', database = 'HoneypotAppDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM files")
            rows = cur.fetchall()
            for row in rows:
                usr = row[0]
                fn = row[1]
                fp = row[2]
                access = row[3].split(" ")
                if user in access:
                    output+='<tr><td><font color="black" size="3">'+usr+'</td>'
                    output+='<td><font color="black" size="3">'+fn+'</td>'
                    output+='<td><font color="black" size="3">'+fp+'</td>'
                    output+='<td><a href=\'DownloadFile?id='+fn+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
                else:
                    output+='<tr><td><font color="black" size="3">'+usr+'</td>'
                    output+='<td><font color="black" size="3">'+fn+'</td>'
                    output+='<td><font color="black" size="3">-</td>'
                    output+='<td><a href=\'DownloadFile?id='+fn+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        context= {'data':output}        
        return render(request, 'Download.html', context)


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
        return render(request, 'Login.html', {})

def Register(request):
    if request.method == 'GET':
        return render(request, 'Register.html', {})

def Upload(request):
    if request.method == 'GET':
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        output = '<tr><td><font size="" color="black">Choose&nbsp;Share&nbsp;Users</b></td><td><select name="t3" multiple>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'only4MySQL', database = 'HoneypotAppDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] != user:
                    output+='<option value='+row[0]+'>'+row[0]+'</option>'
        output+='</select></tr></td>'
        output+='<tr><td></td><td><input type="submit" value="Submit">'
        output+='</td></table><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/></div></div></body></html>'
        context= {'data':output}
        return render(request, 'Upload.html', context)    

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        status_data = ''
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'only4MySQL', database = 'HoneypotAppDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    status = 'success'
                    break
        if status == 'success':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            output = 'Welcome : '+username
            context= {'data':output}
            return render(request, 'UserScreen.html', context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)

def UploadFile(request):
    if request.method == 'POST':
        password = request.POST.get('t1', False)
        myfile = request.FILES['t2']
        name = request.FILES['t2'].name
        access_list = request.POST.getlist('t3')
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        shares = user+" "
        for i in range(len(access_list)):
            shares+=access_list[i]+" "
        shares = shares.strip()

        fs = FileSystemStorage()
        filename = fs.save('static/files/'+name, myfile)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'only4MySQL', database = 'HoneypotAppDB',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO files(username,filename,filepassword,shares) VALUES('"+user+"','"+name+"','"+password+"','"+shares+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data1':'File uploaded successfully'}
            return render(request, 'Upload.html', context)
        else:
            context= {'data1':'Error in uploading file'}
            return render(request, 'Upload.html', context)        
    

def Signup(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      address = request.POST.get('address', False)
      
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'only4MySQL', database = 'HoneypotAppDB',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Signup Process Completed'}
       return render(request, 'Register.html', context)
      else:
       context= {'data':'Error in signup process'}
       return render(request, 'Register.html', context)
    
