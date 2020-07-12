from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect 
from base.models import Item, ToDoList, Feedback
from base.forms import CreateNewList, FeedbackForm
from django.core.mail import send_mail
from django.conf import settings
import requests
from bs4 import BeautifulSoup as BSoup
from base.models import Headline
from newsapi import NewsApiClient

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
       
        send_mail('ContactFormFrommywebsite',message,settings.EMAIL_HOST_USER,['sujitha.rasalingam91@gmail.com'],fail_silently=True)
        return render(request,'base/feedback.html',{'c_name':c_name})
    else:
    	return render(request,'base/feedback.html')

#news aggregation
def proj_news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "base/projects_list.html", context) 

def scrape(request):
  session = request.Session()
  session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
  url = "https://www.theonion.com/"
  content = session.get(url, verify=False).content
  soup = BSoup(content, "html.parser")
  News = soup.find_all('div', {"class":"curation-module__item"})
  for artcile in News:
    main = artcile.find_all('a')[0]
    link = main['href']
    image_src = str(main.find('img')['srcset']).split(" ")[-4]
    title = main['title']
    new_headline = Headline()
    new_headline.title = title
    new_headline.url = link
    new_headline.image = image_src
    new_headline.save()
  return redirect("../")

def news_aggregator(request):
    return render(request, 'base/news_aggregator.html')  


# GEtting news from Times of India

toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BSoup(toi_r.content, 'html5lib')

toi_headings = toi_soup.find_all('h2')

toi_headings = toi_headings[0:-13] # removing footers

toi_news = []

for th in toi_headings:
    toi_news.append(th.text)



#Getting news from Hindustan times

ht_r = requests.get("https://www.hindustantimes.com/india-news/")
ht_soup = BSoup(ht_r.content, 'html5lib')
ht_headings = ht_soup.findAll("div", {"class": "headingfour"})
ht_headings = ht_headings[2:]
ht_news = []

for hth in ht_headings:
    ht_news.append(hth.text)


def news_aggregator(req):
    return render(req, 'base/news_aggregator.html', {'toi_news':toi_news, 'ht_news': ht_news})    

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