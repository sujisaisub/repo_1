from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect 
from base.models import Item, ToDoList, Feedback
from base.forms import CreateNewList, FeedbackForm
from django.core.mail import send_mail
from django.conf import settings
#from bs4 import BeautifulSoup as BSoup
from base.models import Headline
from newsapi.newsapi_client import NewsApiClient
from base.chatbot import chatbot
from base.rootchatbot import words, labels, training, output, model, data
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle



# Create your views here.
#def home(request):
	#return render(request,'base/home.html')

#def home(response, id):
#	ls = ToDoList.objects.get(id = id)
#	return HttpResponse("<h1>%s</h1>" %ls.name)

#def home(response, name):
#	ls = ToDoList.objects.get(name=name)
#	items = ls.item_set.get(id = 1)
#	return HttpResponse("<h1>%s</h1><br><p>%s</p>" %(ls.name,items.text))

def portfolio(request):
	return render(request,'base/portfolio.html')

def thanks(request):
	return render(request,'base/thanks.html')

def Feedback_view_backup(request):
    print(f"request.method : {request.method}")
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            #n = form.cleaned_data["name"]  
            #t = Feedback(name=n)     
            form.save()
            print("d2o")
            #return redirect('http://127.0.0.1:8000/basethanks.html' )
            return render(request,'base/thanks.html')
    else:
        form = FeedbackForm
    return render(request, 'base/feedback.html', {'form': form})

def Feedback_view(response):
    print(f"response.method : {response.method}")
    ls = Feedback.objects.all()    
    if response.method == 'POST':
        print(response.POST)    	
        if response.POST.get("save"): 
          nam = response.POST.get("name")     
          em = response.POST.get("email")
          txt = response.POST.get("text")      
          ls.create(name=nam,email=em,text=txt)          
          return render(response,'base/greetins.html',)    
    return render(response, 'base/feedback.html', {'ls':ls})

def base(request):
	return render(request,'base/basetemplate.html')


def home(request):
	return render(request,'base/home.html')


def index(response, id):
	ls = ToDoList.objects.get(id=id)
	if response.method=='POST':
		print(response.POST)
		if response.POST.get("save"):
			for item in ls.item_set.all():
				print(item.id)
				print("c"+str(item.id))

				if response.POST.get("c" +str(item.id)) == 'clicked':

					item.complete = True
				else:
					item.complete = False
				item.save()

		elif response.POST.get('newItem'):
			txt = response.POST.get("new")
			if len(txt) > 1:
				ls.item_set.create(text=txt,complete=False)
			else:
				print("invalid input for the textbox")

	
	return render(response,'base/list.html', {'ls':ls})

def create(response):
	if response.method=='POST':
		form = CreateNewList(response.POST)
		if form.is_valid():
			n = form.cleaned_data["name"]
			t = ToDoList(name=n)
			t.save()
			print(n)
			return HttpResponseRedirect("/%i" %t.id)	
	else:

		form = CreateNewList()
		return render(response,'base/createpage.html',{'form':form})

def contact(request):
    if request.method == 'POST':
        c_name = request.POST['name']
        c_em   = request.POST['email']
        message = "Name" + ":" + c_name + "\n" + "EmailID" + ":" + c_em + "\n" + "Message" + ":" + request.POST['text']
       
        send_mail('ContactFormFrommywebsite',message,settings.EMAIL_HOST_USER,['sujitha.rasalingam91@gmail.com'],fail_silently=False)
        return render(request,'base/feedback.html',{'c_name':c_name})
    else:
    	return render(request,'base/feedback.html')



def news_aggregator(request):
    return render(request, 'base/news_aggregator.html')  

   

#using NewsApiClient    
def news_agg(request):
  newsapi = NewsApiClient(api_key='3fe5b067769946879821f0ee5afdab83')
  top_news = newsapi.get_top_headlines(sources='recode')
  print(len(top_news))
  articles = top_news['articles']

  desc = []
  news = []
  img  = []
  url  = []

  for i in range(len(articles)):

    myarticles= articles[i]

    desc.append(myarticles['description'])
    url.append(myarticles['url'])
    img.append(myarticles['urlToImage'])
    news.append(myarticles['title'])

    mylist= zip(url, img, desc, news)

  return render(request, 'base/news_aggregator.html',context={'mylist':mylist})

#chatbot

def bot_response(request):
  # Creating ChatBot Instance
   return render(request, 'base/chatting.html')  


def get_bot_response(request):
    #ls = ChatBot.objects.get(name=chatbot)
    userText = request.GET.get('msg')
    print('views_sujitha')
    print(userText)
    print(chatbot.get_response(userText))
    return HttpResponse((chatbot.get_response(userText)))
    
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


def chat(request):
    userText = request.GET.get('msg')
    
    print(userText)

    results = model.predict([bag_of_words(userText, words)])
    
    results_index = numpy.argmax(results)

    print(results_index)

    tag = labels[results_index]

    if results[0][results_index] > 0.7:
      for tg in data["intents"]:
          if tg['tag'] == tag:
              responses = tg['responses']
      result = (random.choice(responses))
    else:
      result = "I dint get your question, try again!"

    print(result)
    
    return HttpResponse(result)
