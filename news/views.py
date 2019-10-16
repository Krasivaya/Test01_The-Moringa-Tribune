from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import datetime as dt
from .models import Article
from .forms import NewsLetterForm

#News view for particular day
#Form view
def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            print('valid')
    else:
        form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date": date,"news":news,"letterForm":form})

#Passt days News View
def past_days_news(request, past_date):
    try:
        #convert data from url
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()
    except ValueError:
        #raise 404 error when valueError is thrown
        raise Http404()
        assert False
    
    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html',{"date":date, "news":news})

#Search result view
def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

#A single article view

def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})
