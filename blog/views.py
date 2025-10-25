from django.shortcuts import render

# Create your views here.
from .models import Post, UserProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_posts = Post.objects.all().count()
    posts = Post.objects.all()


    # Number of visits to this view, as counted in the session variable.

    context = {
        'num_posts': num_posts,
        'posts': posts,
        
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic



class PostListView(generic.ListView):
    model = Post
    paginate_by = 5






def post_detail(request, pk):
    # Safely fetch the post by primary key (UUID) or return 404
    post = get_object_or_404(Post, pk=pk)
    recent_posts = Post.objects.exclude(pk=pk).order_by('-created_on')[:5]
    comments = post.comments.all().order_by('-created_on')  # Note: newest first with -created_on

    context = {
        'post': post,
        'author': post.author,
        'recent_posts': recent_posts,
            'comments': comments,
    }
    return render(request, 'post_detail.html', context)

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_on')
    bio = user.profile.bio if hasattr(user, 'profile') else '' 
    return render(request, 'user_detail.html', {'user': user, 'posts': posts})


from blog.forms import CommentForm
from django.shortcuts import redirect



def addComment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post-detail', pk=post.pk)


    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form, 'post': post})


class CommentListView(generic.ListView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['pk'])
    

from django.views.generic.edit import CreateView, UpdateView, DeleteView    
from django.urls import reverse_lazy

class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'tags']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)