from django.db import models 
from django.utils import timezone 
from django.contrib.auth.models import User 
from django.urls import reverse
from tinymce import models as tinymce_model

class PublishedManager(models.Manager):  
    def get_queryset(self):  
        return super(PublishedManager,  
		     self).get_queryset().filter(status='published')

class Post(models.Model): 
    STATUS_CHOICES = (
        ('draft', 'Draft'), 
        ('published', 'Published'), 
    ) 
    title = models.CharField(max_length=250) #заголовок поста
    slug = models.SlugField(max_length=250, #URL
                            unique_for_date='publish') 
    author = models.ForeignKey(User, #автор поста
                               on_delete=models.CASCADE, #если удаляется пльзователь, то и его посты
                               related_name='blog_posts') 
    body = tinymce_model.HTMLField() #тело поста
    publish = models.DateTimeField(default=timezone.now) #дата публикации
    created = models.DateTimeField(auto_now_add=True) #дата создания
    updated = models.DateTimeField(auto_now=True) #дата обновления
    status = models.CharField(max_length=10, #статус поста
                              choices=STATUS_CHOICES, 
                              default='draft') 
    objects = models.Manager()  # Менеджер по умолчанию  
    published = PublishedManager()  # Собственный менеджер

    class Meta: 
        ordering = ('-publish',) #сортировка постов от новых к старым

    def __str__(self): 
        return self.title

    def get_absolute_url(self):  
        return reverse('blog:post_detail',  
		       args=[self.publish.year,  
		       self.publish.month,  
		       self.publish.day,  
		       self.slug])