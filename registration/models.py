from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from mail_templated import send_mail

# Create your models here.
GENDER = (('M', _('Male')), ('F', _('Female')))


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, email and password.
        """
        if not email:raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(email, username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """
    Extends the default User profiles of Django. The fields of this model can be obtained by the
    user.get_profile method and it's extended by the django-profile application.
    """
    user_id = models.AutoField(primary_key=True)
    user_first_name = models.CharField(_('First Name'), max_length=32, blank=True, null=True,
                                  validators=[RegexValidator(regex='^[A-Za-z]*$')])
    user_last_name = models.CharField(_('Last Name'), max_length=32, blank=True, null=True,
                                    validators=[RegexValidator(regex='^[A-Za-z0-9\ ]*$')])
    email = models.EmailField(_('Email'), db_index=True, unique=True)
    user_dob = models.DateField(_('Birth Date'), blank=True, null=True)
    user_gender = models.CharField(_('Gender'), max_length=1, choices=GENDER, blank=True, null=True)
    user_github = models.CharField(_('Github Profile'),max_length=100,blank=True )
    user_linkedin = models.CharField(_('Linkedin Profile'),max_length=100,blank=True )
    user_bio = models.CharField(_('Short Bio'), max_length=1000,blank=True )
    user_occupation = models.CharField(_('Occupation'), max_length=100,blank=True )
    user_nationality = models.CharField(_('Nationality'), max_length=100,blank=True )
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(_('username'), max_length=32, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def get_name(self):
        if self.user_first_name and self.user_last_name:
            return (self.user_first_name +' '+ self.user_last_name )
        else:
            return self.username

    def get_first_name(self):
        return (self.user_first_name)

    def get_short_name(self):
        return self.username

    def get_email(self):
        return self.email

    def get_full_name(self):
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_user_id(self):
        return self.user_id

    @property
    def is_staff(self):
        return self.is_admin

    def __unicode__(self):
        return self.username


DIFFICULTY = (('Easy', _('Easy')), ('Medium', _('Medium')), ('Advanced', _('Advanced')))
LANGUAGE = (('English', _('English')), ('Malayalam', _('Malayalam')), ('Hindi', _('Hindi')))
class Course(models.Model):
    """
    Course model
    """
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(_('Course Name'), max_length=100, blank=False, unique=True)
    course_bio = models.CharField(_('Course Description'), max_length=1000, blank=True, null=True)
    course_language = models.CharField(_('Course Language'), max_length=25, choices=LANGUAGE, blank=False, unique=False)
    course_difficulty = models.CharField(_('Course Difficulty'), max_length=20, choices=DIFFICULTY, blank=False, unique=False)
    course_fees = models.IntegerField(_('Course Fees'),
                                  validators=[MaxValueValidator(99999),MinValueValidator(0)],
                                  help_text=_('5 digits maximum'), blank=True, null=True)
    course_created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    course_user = models.ForeignKey(User, blank=False, null=False)

    def get_mentor(self):
        return self.course_user

    def get_course_name(self):
        return self.course_name

    def get_course_fees(self):
        return self.course_fees

    def get_enrolled_users(self):
        return CourseEnrollment.objects.filter(course=self.course_id, course_enrolled=True).count()

    def save(self):
        if self.approved:
            old_status = Course.objects.get(pk=self.course_id)
            if old_status.approved == False and self.approved == True:
                send_mail('emails/course_approved.html', {'user': self.course_user, 'course': self.course_name }, 'admin@thinkfoss.com', [self.course_user.email, 'admin@thinkfoss.com'])
        super(Course, self).save()

    def __unicode__(self):
        return self.course_name



class OrderManager(models.Manager):
    def start_checkout(self,order_id, amount,user):
        order_object = self.create(order_id=order_id,amount=amount,user=user)
        return order_object

class Order(models.Model):
    order_id = models.CharField(max_length=150, primary_key=True, blank=False, null=False )
    amount = models.FloatField( blank=False, null=False )
    user = models.ForeignKey(User, blank=False, null=False)
    bank_ref_no = models.CharField( max_length=20, blank=True, null=True)
    status_code = models.CharField( max_length=500, blank=True, null=True)
    failure_message = models.CharField( max_length=500, blank=True, null=True)
    status_message = models.CharField( max_length=170, blank=True, null=True)
    order_status = models.CharField( max_length=20, blank=True, null=True)
    tracking_id = models.CharField( max_length=20, blank=True, null=True)
    time_of_order = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    def get_owner(self):
        return self.user

class EnrollmentManager(models.Manager):
    def add_to_cart(self,course,user):
        cart_object = self.create(course=course, user=user )
        return cart_object


class CourseEnrollment(models.Model):
    checkout_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, blank=False, null=False)
    user = models.ForeignKey(User, blank=False, null=False)
    enrollment_time = models.DateTimeField(auto_now_add=True)
    course_enrolled = models.BooleanField(default=False)
    order = models.ForeignKey(Order, blank=True, null=True)

    def has_checked_out(self):
        return self.course_enrolled

    def owner_of_item(self):
        return self.user

    def get_course(self):
        return self.course

    def get_checkout_id(self):
        return self.checkout_id

    def __unicode__(self):
        return self.user.email + '-'+ self.course.course_name

    class Meta:
        unique_together = ("user", "course")

    objects = EnrollmentManager()


class CourseModules(models.Model):
    course = models.ForeignKey(Course, blank=False, null=False)
    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(_('Module Name'), max_length=100, blank=False, unique=True)
    module_description = models.CharField(_('Module Description'), max_length=1000, blank=True, null=True)
    module_duration = models.IntegerField(_('Duration of module'),
                                  validators=[MaxValueValidator(100),MinValueValidator(0)],
                                  help_text=_('3 digits maximum'), blank=True, null=True)

    def __unicode__(self):
        return self.course.course_name + '-' + self.module_name




class CourseProgressManager(models.Manager):
    def create_progress(self,checkout,module):
        created_progress_item = self.create(checkout=checkout, module=module,completed=False)
        return created_progress_item


class CourseProgress(models.Model):
    checkout = models.ForeignKey(CourseEnrollment, blank=False, null=False)
    module = models.ForeignKey(CourseModules, blank=False, null=False)
    completed = models.BooleanField(default=False)
    remarks = models.CharField(_('Remarks'), max_length=1000, blank=True, null=True)

    objects = CourseProgressManager()



PLATFORM = (('Web', _('Web')), ('Mobile', _('Mobile')), ('Web+Mobile', _('Web+Mobile')))

class Solution(models.Model):
    """
    Solution model
    """
    solution_id = models.AutoField(primary_key=True)
    solution_name = models.CharField(_('Solution Name'), max_length=100, blank=False, unique=True)
    solution_platform = models.CharField(_('Platform'), max_length=20, choices=PLATFORM, blank=True, null=True)
    solution_contact_email = models.CharField(_('Contact Email'), max_length=100, blank=False, unique=False)
    solution_contact_phone = models.IntegerField(_('Contact Number'),
                                  validators=[MaxValueValidator(99999999999),MinValueValidator(100000000)],
                                  help_text=_('10 digits maximum'), blank=True, null=True)
    solution_deadline = models.DateField(_('Deadline of Submission'), blank=True, null=True)
    solution_budget = models.IntegerField(_('Solution Budget'),
                                  validators=[MaxValueValidator(99999999),MinValueValidator(0)],
                                  help_text=_('8 digits maximum'), blank=True, null=True)
    solution_description = models.CharField(_('Description'), max_length=1000, blank=True, null=True)
    solution_created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.solution_name
