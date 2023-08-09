
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import *

from django.http import JsonResponse
from django.template.loader import render_to_string

from django.core.mail import send_mail
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import authenticate, get_user_model, login, logout

from .models import *


# Create your views here.
def home(request):
	return render (request,'index.html')

def blog(request):
	posts=Post.objects.all()
	featured_post = FeaturedPost.objects.all()
	recent = RecentWork.objects.all()
	return render(request, 'blog.html',{'posts':posts, 'featured_post':featured_post, 'recent':recent})

def blog_details(request,posts_id):
	post_detail = Post.objects.filter(sno=posts_id).first()
	return render(request, 'blog-details.html',{'post_details': post_detail })

def comments(request):
	if request.method=='POST':
		comment=request.POST.get('comment')
		obj=Comment(comment1=comment,user=request.user)
		obj.save() 
		# print("cvhvhbjnknkhbhkjbkjv")
	return render(request,'blog.html')


def blog_post(request, post_id):
	if(request.method == 'POST'):
		# name = request.POST.get('name')
		# email = request.POST.get('email')
		print(request.POST.get('csrfmiddlewaretoken'))
		user = request.user
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		post = Post.objects.filter(sno = post_id).first()
		obj=Comment(user = user, message = message, subject=subject, post=post, timestamp = datetime.datetime.strptime('2021-09-09 00:00:00','%Y-%m-%d %H:%M:%S'))
		obj.save()
		email = user.email
		send_mail(
			'Someone Commented'+subject,
		    'from:' +email +'\nmessage:\n'+message,
		    'rk7305758@gmail.com',
		    ['paliwalap7@gmail.com'],
		    fail_silently=True,
			)

		comments = Comment.objects.filter(post = post, parent = None)
		replies = Comment.objects.filter(post = post).exclude(parent = None)

		repliesdict  = {}
		for i in replies:
			if i.parent not in repliesdict.keys():
				repliesdict[i.parent] = [i]
			else:
				repliesdict[i.parent].append(i)
		print(repliesdict)
		context = {'comments':comments, 'repliesdict':repliesdict,'post':post}

		html = render_to_string('comment.html', context, request=request)
		return JsonResponse({'html':html})


	post = Post.objects.filter(sno = post_id).first()
	recent_posts = Post.objects.all()[:4:-1]
	recent = RecentWork.objects.all()

	
	tags = Tags.objects.filter(post=post)
	comments = Comment.objects.filter(post = post, parent=None)
	replies = Comment.objects.filter(post = post).exclude(parent = None)

	repliesdict  = {}
	for i in replies:
		if i.parent not in repliesdict.keys():
			repliesdict[i.parent] = [i]
		else:
			repliesdict[i.parent].append(i)

	print(repliesdict)
	return render(request, 'blog-details.html', {'post_details':post, 'recent_posts':recent_posts, 'recent':recent, 'comments':comments, 'repliesdict':repliesdict, 'tags':tags})


def search_tag(request):
	query = request.GET.get('search')
	posts = Post.objects.filter(title__contains = query)
	page = request.GET.get('page', 1)
	paginator = Paginator(posts, 2)
	# categories = Category.objects.all()
	try:
	    post_obj = paginator.page(page)
	except PageNotAnInteger:
	    post_obj = paginator.page(1)
	except EmptyPage:
	    post_obj = paginator.page(paginator.num_pages)
	
	return render(request, 'search-blog.html', {'post_obj':post_obj, 'results_count':posts.count(), 'query':query})
