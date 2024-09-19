from django import forms


class SearchStoryForm(forms.Form):
    your_name = forms.CharField(label="Your Name", max_length=100)
    your_friend_name = forms.CharField(label="Your Friend Name", max_length=100)
    story_you_want = forms.CharField(label="What Story You want", max_length=100, widget=forms.Textarea)
    


