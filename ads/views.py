from django.shortcuts import render, redirect
import json
from django.core import serializers
from ads.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Q



# Create your views here.
def home(request):
	return render(request,'ads/index.html',{})

def get_ads(request):
	ads = Ad.objects.all().order_by('?')
	for field in request.GET:
		if(field=='I' or field=='II' or field=='III' or field=='IV'):
			y = Year.objects.get(year=field)
			ads = ads & Ad.objects.filter(yr=y)
		else:
			try:
				ads = ads & Ad.objects.filter(br=Branch.objects.get(branch=field))
			except:
				pass
	return ads
def adapi(request):
	ads = get_ads(request)
	'''
	TODO:
	Ad.objects.filter(
    Q(br = Branch.objects.filter(branch = 'SE')),
    Q(yr = Year.objects.filter(year = 'I')) | Q(yr = Year.objects.filter(year = 'II'))
	)
	'''
	data = serializers.serialize('json',ads)
	data = json.loads(data)
	if(not request.user.is_authenticated()):
		for i in range(len(data)):
			data[i]['fields']['phone'] = ""
	return JsonResponse(data, safe=False)

@login_required
def postad(request):
	if(request.method=='GET'):
		return render(request,'ads/post.html',{})
	elif(request.method=='POST'):
		usr = request.user
		ad = Ad(by=usr)
		ad.save()
		flag = 1
		inp_obj = request.POST

		for field in request.POST:
			if(field=='I' or field=='II' or field=='III' or field=='IV'):
				ad.yr.add(Year.objects.get(year=field))
			elif(field=='title' or field=='desc' or field=='price' or field=='phone'):
				try:
					setattr(ad, field, request.POST.get(field))
				except:
					ad.delete()
					error = 'error'
					return render(request,'ads/post.html',{'error':error})
			else:
				try:
					ad.br.add(Branch.objects.get(branch=field))
				except:
					pass
		ad.save()
		return redirect('/myads')
	else:
		return HttpResponse("Something went wrong. Couldn't submit your post")


@login_required
def myads(request):
	if(request.method=='GET'):
		usr = request.user
		ads = usr.ad_set.all()
		return render(request,'ads/myads.html',{'ads':ads})
	elif(request.method=='POST'):
		ad_id = request.POST.get('ad_id')
		ad = Ad.objects.get(id=ad_id)
		ad.delete()
		messages.add_message(request, messages.INFO, 'deleted')
		return redirect('/myads')
	else:
		return HttpRequest("Something went wrong. Couldn't delete the ad.")

def loginpage(request):
	unauth = None
	if(request.user.username):
		return redirect('/')
	if(request.GET.get('unauth')):
		unauth = True
	return render(request,'ads/loginpage.html',{'unauth':unauth})

def login(request):
	return redirect('/accounts/facebook/login')

def success_login(request):
	usr = request.user
	nm= usr.socialaccount_set.all().filter(provider='facebook')[0].extra_data['name'].split()
	if(not usr.first_name or len(usr.first_name)==0):
		if(len(nm)>0):
			usr.first_name = nm[0]
		if(len(nm)>1):
			usr.last_name = nm[1]
	usr.save()

	return redirect('/')

def myadsapi(request):
	usr = User.objects.get(id = request.user.id)
	ads = usr.ad_set.all()
	data = serializers.serialize('json',ads)
	return HttpResponse(data, content_type='application/json')


def contact(request):
	if(request.method == 'GET'):
		return render(request,'ads/contact.html',{})
	elif(request.method == 'POST'):
		success = 'true'
		try:
			content = request.POST.get('content')
			user = request.user
			by=""
			fn=""
			ln=""
			by = user.email
			fn=user.first_name
			ln=user.last_name
		except:
			pass
		content = by+" "+fn+" "+ln+"		"+content
		email = EmailMessage("From: "+by,content,to=['jeequery@gmail.com'])
		email.send()
		return render(request,'ads/contact.html',{'success':success})

def logout_view(request):
	logout(request)
	return redirect('/')

def login_cancelled(request):
	return redirect('/')

def account_inactive(request):
	return render(request,'ads/inactive.html',{})

def handler404(request):
	return render(request,'ads/404.html',{})

@csrf_exempt
def soldapi(request):
	data = {'sold_items':'error'}
	if(request.method=="GET"):
		try:
			f = open('ads/soldapi.txt','r')
			sold = f.read()
			data['sold_items']=sold
		except:
			pass
		return HttpResponse(json.dumps(data), content_type="application/json")
	elif(request.method=="PUT"):
		try:
			f = open('ads/soldapi.txt','r')
			j = 0
			try:
				i = int(f.read())
				j = i
			except:
				pass
			y = j + 1
			f = open('ads/soldapi.txt','w')
			f.write(str(y))
			f.close()
		except:
			pass
		return HttpResponse('done')
