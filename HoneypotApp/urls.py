from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('Upload.html', views.Upload, name="Upload"), 
	       path('UploadFile', views.UploadFile, name="UploadFile"),
	       path('Download.html', views.Download, name="Download"), 
	       path('DownloadFile', views.DownloadFile, name="DownloadFile"),
	       path('DownloadFileDataRequest', views.DownloadFileDataRequest, name="DownloadFileDataRequest"),
	           
]
