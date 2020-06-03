from django.shortcuts import render, redirect
from .models import Post, Category
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm


# Create your views here.


# List로 보여줄 때는 django.views.generic의
# ListView를 상속하여 보여주면 간단하게 보여줄 수 있다.
class PostList(ListView):
    model = Post

    def get_queryset(self):
        # 역순으로 보여주기 위해 -로 붙인다.
        return Post.objects.order_by('-created')

    # templates로 추가적인 정보를 넘겨주고 싶을 경우
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # Post들 중에서 category가 None인 것의 갯수를 가져온다.
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # Post들 중에서 category가 None인 것의 갯수를 가져온다.
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm()

        return context

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category',
        # 'tags'
    ]

    def form_valid(self, form):
        # 작성자를 가지고 온다.
        current_user = self.request.user

        # 로그인을 한 상태인지 확인을 한다.
        if current_user.is_authenticated:
            # form의 author를 현재 작성중인 사람으로 채워 넣어
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else :
            return redirect('/blog/')


class PostUpdate(UpdateView):
    model = Post
    # post의 모든 field를 가져와라
    # fields = '__all__'
    fields = [
        'title', 'content', 'head_image', 'category',
        # 'tags'
    ]




class PostListByCategory(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']

        # slug가 none인경우
        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)

        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # Post들 중에서 category가 None인 것의 갯수를 가져온다.
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        slug = self.kwargs['slug']

        # slug가 none인경우
        if slug == '_none':
            context['category'] = '미분'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        # context['title'] = 'Blog - {}'.format(category.name)
        return context

def new_comment(request, pk):
    post = Post.objects.get(pk=pk)

    # POST 방식으로 들어왔는지 확인한다.
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect(comment.get_absolute_url())
    else:
        return redirect('/blog/')


# 상세 페이지를 보여주기 위한 함수를 추가한다.
# def post_detail(request, pk):
#     blog_post = Post.objects.get(pk=pk)

#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'blog_post': blog_post,
#         }
#     )

# def index(request):
#     # Post의 내용들을 전부 다 가져온다.
#     posts = Post.objects.all()

#     return render(
#         request,
#         # 템블릿이 되는 html 코드를 작성할 필요가 있다.
#         'blog/index.html',
#         # index.html에서 사용하도록 객체를 넘겨주고 있다.
#         # template에 전해주고 싶은 것들을 적어주면 된다.
#         {
#             'posts': posts,
#         }
#     )
