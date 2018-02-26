from django.conf import settings
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.views.generic import RedirectView
from django.views.generic.edit import FormMixin

from .forms import PostForm, CommentForm, ContactForm, UserCreateForm
from .mixin import ContactFormMixin
from .models import Post,Comment,Category


class PostListView(ContactFormMixin, ListView):
    template_name = 'index.html'
    model = Post
    paginate_by = 8

    def get_queryset(self):
        qs = super(PostListView, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
            qs = Post.objects.filter(
                Q(title__icontains = query)
            )
        return qs.filter(published_date__lte=timezone.now()).order_by('-published_date')


def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'full_name'
            , '')
            contact_email = request.POST.get(
                'email'
            , '')
            form_content = request.POST.get('message', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = {
            'contact_name': contact_name,
            'contact_email': contact_email,
            'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['fcwilczynski@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('/')

    return render(request, 'index.html', {'form': form_class,})


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        self.object = self.get_object()
        context["contact"] = ContactForm
        context["latest_posts"] = Post.objects.all().order_by('-published_date')[:3]
        context["categories"] = Category.objects.all()
        context['form'] = self.get_form()
        context['comments'] = self.object.comments.all().order_by('-created_date')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            errors = form.errors.as_json()
            return HttpResponse(errors)

    def form_valid(self, form):
        post = get_object_or_404(Post,pk=self.object.pk)
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = post
        comment.save()
        return super(PostDetailView, self).form_valid(form)


class CreatePostView(LoginRequiredMixin, ContactFormMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, ContactFormMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, ContactFormMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ContactFormMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    template_name = 'post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class CategoryListView(ListView):
    model = Category
    template_name = "blog/category_list.html"


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        post_set = obj.category_list.all()
        context["posts"] = post_set
        context["latest_post"] = Post.objects.all().order_by("-title")
        context["contact"] = ContactForm
        context["latest_posts"] = Post.objects.all().order_by('-published_date')[:3]
        context["categories"] = Category.objects.all()
        return context


class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'


class LogoutView(RedirectView):
    url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request,*args, **kwargs)


@login_required
def post_publish(request,slug):
    # slug = self.kwargs['slug']
    post = get_object_or_404(Post,slug=slug)
    post.publish()
    return redirect('post_detail',slug=slug)

def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method =='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',slug=post.slug)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_list')


@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.delete()
    return redirect('post_list')
