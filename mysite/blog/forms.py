from django import forms  
  
  
class EmailPostForm(forms.Form):  
    name = forms.CharField(label= 'Ваше имя',max_length=25)  
    email = forms.EmailField(label= 'Ваш email')  
    to = forms.EmailField(label= 'Кому')  
    comments = forms.CharField(label= 'Комментарий', required=False,  
			       widget=forms.Textarea)