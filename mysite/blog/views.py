from django.shortcuts import render, get_object_or_404 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post 
from .forms import EmailPostForm  
from django.core.mail import send_mail 


def post_list(request): 
    object_list = Post.published.all()  
    paginator = Paginator(object_list, 3)  # 3 поста на каждой странице  
    page = request.GET.get('page')  
    try:  
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        # Если страница не является целым числом, поставим первую страницу  
        posts = paginator.page(1)  
    except EmptyPage:  
        # Если страница больше максимальной, доставить последнюю страницу результатов  
        posts = paginator.page(paginator.num_pages)  
    return render(request,'blog/post/list.html', {'page': page,'posts': posts})

def post_detail(request, year, month, day, post):  
    post = get_object_or_404(Post, slug=post,  
			     status='published',  
			     publish__year=year,  
			     publish__month=month,  
			     publish__day=day) 
    return render(request,  
		  'blog/post/detail.html',  
		  {'post': post})

def post_share(request, post_id):   
    # Получить пост по id   
    post = get_object_or_404(Post, id=post_id, status='published')   
    sent = False   
    if request.method == 'POST':   
        # Форма была отправлена   
        form = EmailPostForm(request.POST)   
        if form.is_valid():   
            # Поля формы прошли проверку   
            cd = form.cleaned_data   
            post_url = request.build_absolute_uri(post.get_absolute_url())   
            subject = '{} ({}) recommends you reading " {}"'.format(cd['name'], cd['email'], post.title)   
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])   
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])   
            sent = True   
    else:   
        form = EmailPostForm()   
    return render(request, 'blog/post/share.html', {'post': post,   
                            'form': form,   
                            'sent': sent})