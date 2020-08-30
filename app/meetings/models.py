from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Course(models.Model):
    subject = models.CharField(max_length=28)
    number = models.IntegerField()
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return "{} {}".format(str(self.subject), str(self.number))


class Meeting(models.Model):
    tutor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tutor")
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="student", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    meeting_datetime = models.DateTimeField()

    def __str__(self):
        return "{} {} by {} on {}".format(
            self.course.subject, self.course.number, self.tutor.first_name, self.meeting_datetime
        )


class Review(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_tutor")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_student")
    review_value = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    review_text = models.TextField(blank=True)

    def __str__(self):
        return "Review value: {}. Review: {}".format(self.review_value, self.review_text)

        





