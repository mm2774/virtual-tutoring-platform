from django import forms
from .models import Meeting, Course, Review
from django.forms.widgets import DateTimeInput
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta, timezone

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateMeetingForm(forms.ModelForm):
    _max_time_threshold = lambda: datetime.now(timezone.utc) + timedelta(days=10)
    _min_time_threshold = lambda: datetime.now(timezone.utc) + timedelta(days=1)
    meeting_datetime = forms.DateTimeField(label=(u'Date / Time'), input_formats=[
                                           '%d/%m/%Y %H:%M'], widget=DateTimeInput(attrs={'type': 'datetime-local'}), validators=[
                                               MaxValueValidator(limit_value=_max_time_threshold), MinValueValidator(limit_value=_min_time_threshold)])
    hours_available = forms.IntegerField(label=(u'Hours Available'),
        validators=[MaxValueValidator(24), MinValueValidator(1)])

    class Meta:
        model = Meeting
        fields = ['meeting_datetime']

class SearchMeetingForm(forms.ModelForm):
    _max_time_threshold = lambda: datetime.now(timezone.utc) + timedelta(days=10)
    _min_time_threshold = lambda: datetime.now(timezone.utc) + timedelta(days=1)
    meeting_datetime = forms.DateTimeField(label=(u'Date / Time'), input_formats=[
                                           '%d/%m/%Y %H:%M'], widget=DateTimeInput(attrs={'type': 'datetime-local'}), validators=[
                                               MaxValueValidator(limit_value=_max_time_threshold), MinValueValidator(limit_value=_min_time_threshold)])
    class Meta:
        model = Meeting
        fields = ['meeting_datetime']


class ScheduleMeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = []


CHOICES = [(1.0, 1.0),(2.0, 2.0), (3.0, 3.0), (4.0, 4.0), (5.0, 5.0)]


class CreateReviewForm(forms.ModelForm):
    review_value = forms.ChoiceField(label=(u'Review (out of 5.0)'), widget=forms.RadioSelect, choices=CHOICES)
    review_text = forms.CharField(label=(u'Review Text'), max_length=500)
    class Meta:
        model = Review
        fields = ['review_value', 'review_text']