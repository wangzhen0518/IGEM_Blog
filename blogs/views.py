from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import blogpost
from .forms import blogform


# Create your views here.
def index(request):
    return render(request, 'blogs/index.html')


def check_blog_owner(request, blog):
    if blog.owner != request.user:
        raise Http404


@login_required
def blogs(request):
    blogs = blogpost.objects.filter(owner=request.user).order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.html', context)


@login_required
def blog(request, blog_id):
    blog = blogpost.objects.get(id=blog_id)
    check_blog_owner(request, blog)
    context = {'blog': blog}
    return render(request, 'blogs/blog.html', context)


@login_required
def new_blog(request):
    if request.method != 'POST':
        form = blogform
        context = {'form': form}
        return render(request, 'blogs/new_blog.html', context)
    else:
        form = blogform(request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return HttpResponseRedirect(reverse('blogs:blogs'))


@login_required
def edit_blog(request, blog_id):
    blog = blogpost.objects.get(id=blog_id)
    check_blog_owner(request, blog)
    if request.method != 'POST':
        form = blogform(instance=blog)
        context = {'blog': blog, 'form': form}
        return render(request, 'blogs/edit_blog.html', context)
    else:
        form = blogform(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blogs:blogs'))


@login_required
def delete_blog(request, blog_id):
    blog = blogpost.objects.get(id=blog_id)
    check_blog_owner(request, blog)
    blog.delete()
    return HttpResponseRedirect(reverse('blogs:blogs'))
