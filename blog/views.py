from django.shortcuts import render,redirect, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

from django.contrib.auth.models import User
# Home
def home(request):
 posts = Post.objects.all()
 return render(request, 'blog/home.html', {'posts':posts})

# About
def about(request):
 return render(request, 'blog/about.html')

# Contact
def contact(request):
 return render(request, 'blog/contact.html')

# Dashboard
def dashboard(request):
 if request.user.is_authenticated:
  posts = Post.objects.all().order_by('-pk')
  user = request.user
  full_name = user.get_full_name()
  gps = user.groups.all()
  # print(gps)
  return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps})
 else:
  return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
 logout(request)
 return HttpResponseRedirect('/')

# Sigup
def user_signup(request):
 if request.method == "POST":
  form = SignUpForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! You have become an Staff.')
   user = form.save()
   group = Group.objects.get(name='Staff')
   user.groups.add(group)
   return  redirect('login')
 else:
  form = SignUpForm()
 return render(request, 'blog/signup.html', {'form':form})

# Login
def user_login(request):
 if not request.user.is_authenticated:
  if request.method == "POST":
   form = LoginForm(request=request, data=request.POST)
   if form.is_valid():
    uname = form.cleaned_data['username']
    upass = form.cleaned_data['password']
    user = authenticate(username=uname, password=upass)
    if user is not None:
     login(request, user)
     messages.success(request, 'Logged in Successfully !!')
     return redirect('dashboard')
  else:
   form = LoginForm()
  return render(request, 'blog/login.html', {'form':form})
 else:
  return HttpResponseRedirect('/dashboard/')

# Add New Post
def add_post(request):
 
  if request.user.is_authenticated:
    user = request.user
    grps = user.groups.all()
    # print(grps)
    if grps[0].name in ('Staff', 'Admin'):
      if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
          title = form.cleaned_data['title']
          desc = form.cleaned_data['desc']
          pst = Post(title=title, desc=desc)
          pst.save()
          messages.success(request, f"Congrats {user} blogs successfully created")

          return redirect('dashboard')
        return render(request, 'blog/addpost.html', {'form':form})
      else:
        form = PostForm()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
      messages.warning(request, f"Dear {user} you don't have permissions to add new the blogs")
      return HttpResponseRedirect('/dashboard/')
  else:
    return redirect('login')
  
 

# Update/Edit Post
def update_post(request, id):
  if request.user.is_authenticated:
    user  = request.user
    grps  = user.groups.all()
    if grps[0].name == 'Admin':

      if request.method == 'POST':
        pi = Post.objects.get(pk=id)
        form = PostForm(request.POST, instance=pi)
        if form.is_valid():
          form.save()
          messages.success(request, f"Congrats {user} blogs successfully updated")
          return redirect('dashboard')

      else:
        pi = Post.objects.get(pk=id)
        form = PostForm(instance=pi)
      return render(request, 'blog/updatepost.html', {'form':form})
    else:
      messages.warning(request, f"Dear {user} you don't have permissions to update the blogs")
      return redirect('dashboard')
  else:
    return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pi = Post.objects.get(pk=id)
      pi.delete()
      return HttpResponseRedirect('/dashboard/')
  else:
    return HttpResponseRedirect('/login/')