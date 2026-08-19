from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super().form_valid(form)

    class Meta:
        model = Post
        fields = ["title", "content", "status", "published_date"]
