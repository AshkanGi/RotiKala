from django import forms


class CommentCreatForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'peer w-full rounded-lg border-none bg-transparent px-4 py-3 placeholder-transparent focus:outline-none focus:ring-0', 'placeholder': 'عنوان دیدگاه'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'peer w-full rounded-lg border-none bg-transparent px-4 py-3 placeholder-transparent focus:outline-none focus:ring-0', 'placeholder': 'کامنت خود را اینجا بنویسید'}))
