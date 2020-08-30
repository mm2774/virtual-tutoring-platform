from datetime import date, datetime, timedelta, timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import F, Q, Avg
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from users.models import Profile

from .forms import CreateMeetingForm, SearchMeetingForm, ScheduleMeetingForm, CreateReviewForm
from .models import Course, Meeting, Review


def home(request):
    context = {}
    return render(request, 'templates/meetings/home.html', context)

def search(request):
    queryset_list = Course.objects.all()

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

    if len(queryset_list) > 12:
        queryset_list = queryset_list[0:12]

    context = {
        'courses': queryset_list,
        'values': request.GET
    }
    return render(request, 'templates/meetings/student/search.html', context)


class CourseMeetingListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'templates/meetings/student/course_meetings.html'
    context_object_name = 'tutors'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        today = date.today() # datetime 
        mindate = today + timedelta(days=2) 
        maxdate = today + timedelta(days=7)
        min_date = mindate.strftime("%Y-%m-%d") # string
        max_date = maxdate.strftime("%Y-%m-%d") 

        context = super().get_context_data(**kwargs)
        context['values'] = self.request.GET 
        context['course'] = Course.objects.get(pk=self.kwargs.get('course_id'))
        context['min_date'] = min_date
        context['max_date'] = max_date
        return context


    def get_queryset(self):
        user = self.request.user
        today = date.today() # datetime 
        mindate = today + timedelta(days=2) 
        maxdate = today + timedelta(days=7)
        min_date = mindate.strftime("%Y-%m-%d") # string
        max_date = maxdate.strftime("%Y-%m-%d") 
        
        selected = Course.objects.get(pk=self.kwargs.get('course_id'))
        courseQuery = Q(course=selected)
        minDateQuery = Q(meeting_datetime__gt=mindate)
        maxDateQuery = Q(meeting_datetime__lt=maxdate)
        # statusQuery = Q(status='INITIALIZED')
        meetingQuery = courseQuery & minDateQuery & maxDateQuery
        userQuery = Q(tutor=self.request.user)
        meetings_list = Meeting.objects.filter(meetingQuery).exclude(userQuery)
        
        if 'dates' in self.request.GET:
            meeting_date = self.request.GET['dates'] # string 
            
            if meeting_date:
                start_date = meeting_date + " 00:00:00"
                end_date = meeting_date + " 23:59:59"
                startdate = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
                enddate = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
                
                meetings_list = meetings_list.filter(meeting_datetime__gte=startdate).filter(meeting_datetime__lte=enddate)

            tutorslist = meetings_list.order_by().values('tutor').distinct()
            tidlist = []
            for t in tutorslist:
                tid = t['tutor']
                tidlist.append(tid)
            
            tutors_list = User.objects.filter(pk__in=tidlist)
            for t in tutors_list:
                t.meetings = meetings_list.filter(tutor=t.pk).order_by('meeting_datetime')
                t.profile = Profile.objects.get(user=t) 
                t.rating_value = str(Review.objects.filter(tutor=t.pk).aggregate(Avg('review_value'))['review_value__avg'])[:3]
                if t.rating_value == "Non":
                    t.rating_value = "0.0"
                t.rating_count = Review.objects.filter(tutor=t.pk).count()

            tutors_list_sorted = sorted(tutors_list, key=lambda t: float(t.rating_value), reverse=True)
            return tutors_list_sorted
        return []


@login_required
def search_tutor(request):
    queryset_list = Course.objects.all()

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

    if len(queryset_list) > 12:
        queryset_list = queryset_list[0:12]

    context = {
        'courses': queryset_list,
        'values': request.GET
    }
    return render(request, 'templates/meetings/tutor/search_tutor.html', context)


@login_required
def dashboard(request):

    #query meetings twice; once for user = student; once for user = tutor
    user = request.user

    tutor_meetings = Meeting.objects.filter(tutor = user.pk) #meetings where user is tutor
    student_meetings = Meeting.objects.filter(student = user.pk) #meetings where user is student

    #sort as queryset ; # print(type(ordered_t_meetings))
    tutor_meetings = tutor_meetings.order_by('meeting_datetime')
    student_meetings = student_meetings.order_by('meeting_datetime')

    #collect course ids from meetings
    for meeting in tutor_meetings:
        c_id = meeting.course.pk #id of course
        # print(c_id)  # print(type(c_id))
        course = Course.objects.get(pk = c_id) #get courses from id associated with meeting
        meeting.course_object = course #add this course to meeting for ez access in template

    for meeting in student_meetings:
        c_id2 = meeting.course.pk        
        course = Course.objects.get(pk = c_id2)
        meeting.course_object = course

        tutor_id = meeting.tutor.pk
        tutor_obj = User.objects.get(pk = tutor_id)
        meeting.tutor_object = tutor_obj
    
    #sends meeting objects, for both student/tutor versions, to dashboard.html.
    context = {
        'tutor_meetings': tutor_meetings,
        'student_meetings': student_meetings
    }
    return render(request, 'templates/meetings/dashboard.html', context)


@login_required
def schedule(request, course_id):
    selected = Course.objects.get(pk=course_id)
    user_course_queryset = Meeting.objects.filter(tutor=request.user)
    if request.method == 'POST':
        form = CreateMeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.course = selected
            meeting.tutor = request.user
            # meeting.save()
            valid = True 
            for _ in range(int(form.data['hours_available'])):
                ref = meeting.meeting_datetime
                if user_course_queryset.filter(meeting_datetime__date=ref.date(), meeting_datetime__hour=ref.hour).exists():
                    messages.warning(request, f'You already have a meeting scheduled at {ref.hour} to {(ref.hour+1) % 24} ')
                    valid = False
                else:
                    meeting.save()
                meeting.pk = None
                meeting.meeting_datetime += timedelta(hours=1)
            if valid:
                messages.success(request, f'Schedule Registered!')
                return redirect('search_tutor')
    else:
        form = CreateMeetingForm()
    return render(request, 'templates/meetings/tutor/schedule.html', {'course': selected, 'form': form})


@login_required
def schedule_meeting(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    if request.method == 'POST':
        form = ScheduleMeetingForm(request.POST)
        if form.is_valid():
            meeting.student = request.user
            meeting.save()
            messages.success(request, f'Schedule Registered!')
            return redirect('search')
    else:
        form = ScheduleMeetingForm()
    return render(request, 'templates/meetings/student/schedule_meeting.html')


@login_required
def delete_meeting(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, f'Successfully Removed!')
        return redirect('dashboard')
    return render(request, 'templates/meetings/delete_meeting.html', {'meeting': meeting, 'user':request.user})
        

@login_required
def review_meeting(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    can_review = _can_review(meeting)
    if request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.meeting = meeting
            review.tutor = meeting.tutor
            review.author = request.user  
            review.save() 
            messages.success(request, f'Review submitted!')
            return redirect('dashboard')
    else:
        form = CreateReviewForm()
    return render(request, 'templates/meetings/student/review_meeting.html', {'form': form, 'can_review': can_review })


def _can_review(meeting):
    # return bool depending on review availablity
    # if meeting.meeting_datetime + timedelta(hours=1) > datetime.now(timezone.utc):
    #     return False
    if Review.objects.filter(meeting=meeting).exists():
        return False
    return True