import csv, os
from django.conf import settings
from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import datetime
from .models import Post, Category, Tag, Comment, User
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, RegisterForm, LoginForm, CommentForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            messages.success(request, f'You are post created succesfully.')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
      return HttpResponse("You havn't access.")
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            messages.success(request, f'Your post updated succesfully.')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_wise_post(request, pk):
    category = Category.objects.get(pk=pk)
    post_list = Post.objects.filter(category=category)
    return render(request, 'blog/category_wise_post.html', {'post_list': post_list})

def tags(request):
    tags = Tag.objects.all().order_by('name')
    return render(request, 'blog/tags.html', {'tags':tags})

def tag_wise_post(request, pk):
    tags = Tag.objects.get(pk=pk)
    post_list = Post.objects.filter(tags=tags)
    return render(request, 'blog/category_wise_post.html', {'post_list': post_list})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                )
            if user is not None:
                login(request, user)
                messages.success(request, f' Your Account created and Now you are logged in succesfully.')
                return redirect('/')
        return render(request, 'blog/register.html', {'form':form})
    else:
        return render(request, 'blog/register.html', {'form':form})

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            try:
                try:
                    user = authenticate(
                        username=User.objects.get(username=name),
                        password=password,
                    )
                except:
                    user = authenticate(
                        username=User.objects.get(email__exact=name),
                        password=password,
                    )
            except Exception as e:
                return render(request, 'blog/login.html', {'form':form})
            if user is not None:
                login(request, user)
                messages.success(request, f' You are logged in succesfully.')
                return redirect('post_list')
            else:
                messages.info(request, f'account done not exit plz sign in')
            return render(request, 'blog/login.html', {'form':form})
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        return render(request, 'blog/login.html', {'form':form})

def user_logout(request):
    logout(request)
    messages.success(request, f'You are logged out succesfully.')
    return redirect('post_list')

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True, parent__isnull=True).order_by('-commented_date')
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            
            new_comment.post = post
            new_comment.save()
            return redirect(f'/post/{post.slug}')
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})

def user_profile(request):
    user = request.user
    return render(request, 'blog/user_profile.html', {'user':user})

def update_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()
            messages.success(request, f'User Details updated succesfully.')
            return redirect('user_profile')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'blog/update_profile.html', {'form':form})

def export(request):
    # Generate a unique filename (e.g., timestamp or random string)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f'user_{timestamp}.csv'

    # Define the file path where the CSV will be stored on the server
    file_path = os.path.join(settings.MEDIA_ROOT, unique_filename)

    # Create and write the CSV file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['first_name', 'last_name', 'email', 'gender', 'date_of_birth', 'phone_no', 'city', 'state', 'country'])
        for user in User.objects.all().values_list('first_name', 'last_name', 'email', 'gender', 'date_of_birth', 'phone_no', 'city', 'state', 'country'):
            writer.writerow(user)

    # Serve the file for download
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user.csv"'

    return response
