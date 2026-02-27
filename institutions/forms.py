from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, HTML
from .models import Institution, InstitutionStats


class InstitutionProfileForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = [
            'name', 'short_name', 'logo', 'website', 'place', 'province',
            'foundation_year', 'institution_category', 'institution_type',
            'address', 'contact_email', 'contact_phone', 'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-8'),
                Column('short_name', css_class='col-md-4'),
            ),
            Row(
                Column('province', css_class='col-md-4'),
                Column('place', css_class='col-md-4'),
                Column('foundation_year', css_class='col-md-4'),
            ),
            Row(
                Column('institution_category', css_class='col-md-6'),
                Column('institution_type', css_class='col-md-6'),
            ),
            Row(
                Column('website', css_class='col-md-6'),
                Column('contact_email', css_class='col-md-6'),
            ),
            Row(
                Column('contact_phone', css_class='col-md-6'),
                Column('logo', css_class='col-md-6'),
            ),
            Field('address'),
            Field('description'),
            Submit('submit', 'Save Profile', css_class='btn btn-primary mt-2'),
        )


class InstitutionStatsForm(forms.ModelForm):
    class Meta:
        model = InstitutionStats
        exclude = ['institution', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h6 class="fw-bold mb-3"><i class="bi bi-people me-2"></i>People</h6>'),
            Row(
                Column('total_students', css_class='col-md-4'),
                Column('total_faculty', css_class='col-md-4'),
                Column('phd_holders', css_class='col-md-4'),
            ),
            HTML('<hr><h6 class="fw-bold mb-3"><i class="bi bi-book me-2"></i>Academics</h6>'),
            Row(
                Column('total_programs', css_class='col-md-4'),
                Column('total_departments', css_class='col-md-4'),
                Column('research_papers', css_class='col-md-4'),
            ),
            Row(
                Column('naac_grade', css_class='col-md-4'),
                Column('placement_rate', css_class='col-md-4'),
            ),
            HTML('<hr><h6 class="fw-bold mb-3"><i class="bi bi-building me-2"></i>Infrastructure</h6>'),
            Row(
                Column('campus_area_acres', css_class='col-md-3'),
                Column('library_books', css_class='col-md-3'),
                Column('hostels', css_class='col-md-3'),
                Column('labs', css_class='col-md-3'),
            ),
            Submit('submit', 'Save Statistics', css_class='btn btn-primary mt-3'),
        )
