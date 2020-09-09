from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [path("",views.base),
			   path("home/",views.home),
				path("portfolio/",views.portfolio),
				path("Feedback/",views.Feedback_view),
				path("<int:id>",views.index),
				path("create/", views.create),
				path("contact/",views.contact),
				path('news_agg/', views.news_agg, name='news_agg'),
				path('news_agg/',views.news_agg),
				path('chatting/',views.bot_response, name='chatting'),
				path('get_chatting/',views.chat, name='get_chatting'),
				]