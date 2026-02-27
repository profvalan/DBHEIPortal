from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, HTML
from .models import NewsItem, NewsImage, SDGGoal


class NewsItemForm(forms.ModelForm):
    sdg_goals = forms.ModelMultipleChoiceField(
        queryset=SDGGoal.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='SDG Goals Mapping'
    )

    class Meta:
        model = NewsItem
        fields = ['title', 'summary', 'content', 'category', 'sdg_goals', 'featured_image', 'video_url']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 12, 'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/watch?v=...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title'),
            Row(
                Column('category', css_class='col-md-6'),
                Column('video_url', css_class='col-md-6'),
            ),
            Field('summary'),
            Field('content'),
            Field('featured_image'),
            HTML('<hr><h5 class="fw-semibold mb-3">SDG Goals Mapping</h5>'),
            Field('sdg_goals'),
        )


class NewsImageForm(forms.ModelForm):
    class Meta:
        model = NewsImage
        fields = ['image', 'caption']


class AdminReviewForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ['status', 'admin_notes']
        widgets = {
            'admin_notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            (NewsItem.STATUS_APPROVED, 'Approve & Publish'),
            (NewsItem.STATUS_REJECTED, 'Reject'),
            (NewsItem.STATUS_PENDING, 'Keep Pending'),
        ]
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('status'),
            Field('admin_notes'),
            Submit('submit', 'Save Decision', css_class='btn btn-primary mt-2'),
        )
