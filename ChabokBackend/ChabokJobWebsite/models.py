from django.db import models
from django.contrib.auth.models import User as User_
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user.username/<filename>
    return 'profile/user_{0}/{1}'.format(instance.user.get().username, instance.user.get().username + "." + filename.split(".")[-1])
    
class Resume(models.Model):
    file_url = models.FileField(upload_to=user_directory_path, default=None, null=True)
    
    def get_file(self):
        if self.file_url is not None:
            return self.file_url.url
        return None
    
    @classmethod
    def find_by_id(cls, id):
        return cls.objects.get(id=id)
    
class Gender(models.IntegerChoices):
    MALE = 0, _('Male')
    FEMALE = 1, _('Female')
    NONE = -1, _('None')
    
class Role(models.IntegerChoices):
    EMPLOYER = 0, _('Employer')
    JOB_SEEKER = 1, _('Jobseeker')
    
class Status(models.IntegerChoices):
    REJECTED = -1, _('REJECTED')
    WAITING = 0, _('WAITING')
    ACCEPTED = 1, _('ACCEPTED')

class User(AbstractUser):
    role = models.IntegerField(
        choices=Role.choices,
        default=Role.JOB_SEEKER
    )
    gender = models.IntegerField(
        choices=Gender.choices,
        default=None,
        null=True,
        blank=True
    )
    age = models.IntegerField(default=21, null=True, blank=True)
    # image = models.ImageField(upload_to=user_directory_path, default=None, null=True)
    city = models.CharField(max_length=128, default='', null=True, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, related_name='user', default=None, null=True)
    description = models.CharField(max_length=512, default='', null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']
    
    def __str__(self):
        return self.username
    
    def get_username(self):
        return self.username
    
    def get_email(self):
        return self.email
    
    def get_role(self):
        return Role(int(self.role)).name
    
    def get_role_id(self):
        return self.role
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_gender(self):
        if self.gender != None:
            return Gender(int(self.gender)).name
        return self.gender
    
    def get_age(self):
        return self.age
    
    def get_image(self):
        if self.image.url is not None:
            return self.image.url
        return None
    
    def get_city(self):
        return self.city
    
    def get_resume(self):
        return self.resume
    
    def get_description(self):
        return self.description
        
    @classmethod
    def find_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def find_by_username(cls, username):
        return cls.objects.get(username=username)
    
class JobOffer(models.Model):
    title = models.CharField(max_length=256)
    company_name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    type_collabration = models.CharField(max_length=128)
    job_description = models.CharField(max_length=512, null=True, blank=True)
    # reqired_skils = models.CharField(max_length=512, null=True, blank=True)
    # company_description = models.CharField(max_length=512, null=True, blank=True)
    author = models.ForeignKey(User, related_name='job_offer', on_delete=models.SET_NULL, null=True)
    salary = models.IntegerField(null=True)
    
    def get_title(self): 
        return self.title
    
    def get_company_name(self):
        return self.company_name
    
    def get_location(self):
        return self.location
    
    def get_type_collabration(self):
        return self.type_collabration
    
    def get_job_description(self):
        return self.job_description
    
    def get_required_skills(self):
        return self.reqired_skils
    
    def get_company_description(self):
        return self.company_description
    
    def get_author(self):
        return self.author
    
    @classmethod
    def find_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def find_by_user(cls, user):
        return cls.objects.filter(author=user)
    
    @classmethod
    def get_all(cls):
        return [offer for offer in cls.objects.all()]
    
    @classmethod
    def recommend_by_user(cls, user):
        recommendations = []
        return recommendations
    
class Tag(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tags', default=None, null=True)
    job_offer = models.ForeignKey(JobOffer, on_delete=models.SET_NULL, related_name='tags', default=None, null=True)
    
    def get_name(self):
        return self.name
    
    def get_user_id(self):
        if self.user is not None:
            return self.user.id
        return None
    
    def get_job_offer_id(self):
        if self.job_offer is not None:
            return self.job_offer
        return None
    
    @classmethod
    def find_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def find_by_user_id(cls, id):
        return [tag.id for tag in cls.objects.filter(user__id=id)]
    
    @classmethod
    def find_by_job_offer_id(cls, id):
        return [tag.id for tag in cls.objects.filter(job_offer__id=id)]

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='applications', null=True)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, related_name='applications', null=True)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.WAITING
    )
    job_offer = models.ForeignKey(JobOffer, on_delete=models.SET_NULL, related_name='applications', null=True)
    
    def get_user(self):
        return self.user
    
    def get_resume(self):
        return self.resume
    
    def get_status(self):
        return Status(int(self.status)).name
    
    def get_job_offer(self):
        return self.job_offer
    
    @classmethod
    def find_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def find_by_user(cls, user):
        return [application.id for application in cls.objects.filter(user=user)]
    
    @classmethod
    def find_by_job_offer(cls, job_offer):
        return [application.id for application in cls.objects.filter(job_offer=job_offer)]
    
    