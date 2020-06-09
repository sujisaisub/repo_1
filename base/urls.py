from django.urls import path
from . import views

urlpatterns = [path("",views.base),
			   path("home/",views.home),
				path("portfolio/",views.portfolio),
				path("Feedback/",views.Feedback_view),
				path("<int:id>",views.index),
				path("create/", views.create),]