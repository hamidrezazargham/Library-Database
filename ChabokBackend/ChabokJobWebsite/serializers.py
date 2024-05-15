from rest_framework import serializers
from .models import Application, JobOffer, Role, Gender

    

class uploadResumeSerializer(serializers.Serializer):
    file_url = serializers.FileField(allow_empty_file=False, use_url=True)
    

class resumeSerializer(serializers.Serializer):
    file_url = serializers.SerializerMethodField("get_resume")
    
    def get_resume(self, obj):
        return obj.get_file()
    

class userInfoSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, allow_blank=False)
    first_name = serializers.CharField(max_length=128, allow_blank=False)
    last_name = serializers.CharField(max_length=128, allow_blank=False)
    email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    role = serializers.SerializerMethodField("get_role")
    gender = serializers.SerializerMethodField("get_gender")
    age = serializers.IntegerField()
    # image_url = serializers.ImageField(use_url=True)
    city = serializers.CharField(max_length=128, allow_blank=True, allow_null=True)
    description = serializers.CharField(max_length=512, allow_blank=True, allow_null=True)
    
    def get_role(self, obj):
        return obj.get_role()
    
    def get_gender(self, obj):
        return obj.get_gender()


class userProfileSerializer(serializers.Serializer):
    username = serializers.SerializerMethodField("get_username")
    email = serializers.SerializerMethodField("get_email")
    first_name = serializers.SerializerMethodField("get_first_name")
    last_name = serializers.SerializerMethodField("get_last_name")
    age = serializers.SerializerMethodField("get_age")
    gender = serializers.SerializerMethodField("get_gender")
    city = serializers.SerializerMethodField("get_city")
    description = serializers.SerializerMethodField("get_description")
    role = serializers.SerializerMethodField("get_role")
    resume = serializers.SerializerMethodField("get_resume")
    
    def get_username(self, obj):
        return obj.get_username()
    
    def get_email(self, obj):
        return obj.get_email()
    
    def get_first_name(self, obj):
        return obj.get_first_name()
    
    def get_last_name(self, obj):
        return obj.get_last_name()
    
    def get_age(self, obj):
        return obj.get_age()
    
    def get_gender(self, obj):
        return obj.get_gender()
    
    def get_city(self, obj):
        return obj.get_city()
    
    def get_description(self, obj):
        return obj.get_description()
    
    def get_role(self, obj):
        return obj.get_role_id()
    
    def get_resume(self, obj):
        resume = resumeSerializer(obj.get_resume())
        return resume.data
        
class editUserProfileSerializer(userInfoSerializer):
    role = serializers.IntegerField(
        max_value=1,
        min_value=0,
        default=Role.JOB_SEEKER
    )
    gender = serializers.IntegerField(
        max_value=1,
        min_value=0,
        default=None,
        allow_null=True,
    )
    # resume = serializers.FileField(allow_empty_file=False, use_url=True)


class jobOfferSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)
    company_name = serializers.CharField(max_length=128)
    location = serializers.CharField(max_length=128)
    type_collabration = serializers.CharField(max_length=128)
    job_description = serializers.CharField(max_length=512, allow_null=True, allow_blank=True)
    # reqired_skils = serializers.CharField(max_length=512, allow_null=True, allow_blank=True)
    # company_description = serializers.CharField(max_length=512, allow_null=True, allow_blank=True)
    salary = serializers.IntegerField(allow_null=True)
    id = serializers.SerializerMethodField("get_id")
    # author = serializers.SerializerMethodField("get_author")
    
    # def get_author(self, obj):
    #     author = userInfoSerializer(obj.get_author())
    #     return author.data
    
    def get_id(self, obj):
        return obj.id
    

class editJobOfferSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)
    company_name = serializers.CharField(max_length=128)
    location = serializers.CharField(max_length=128)
    type_collabration = serializers.CharField(max_length=128)
    job_description = serializers.CharField(max_length=512, allow_null=True, allow_blank=True)
    # reqired_skils = serializers.CharField(max_length=512, allow_null=True, allow_blank=True)
    # company_description = serializers.CharField(max_length=512, allow_null=True, allow_blank=True)
    salary = serializers.IntegerField(allow_null=True)


class applicationSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField("get_user")
    resume = serializers.SerializerMethodField("get_resume")
    status = serializers.SerializerMethodField("get_status")
    job_offer = serializers.SerializerMethodField("get_jobOffer")
    
    def get_user(self, obj):
        user = userInfoSerializer(obj.get_user())
        return user.data
    
    def get_resume(self, obj):
        resume = resumeSerializer(obj.get_resume())
        return resume.data
    
    def get_status(self, obj):
        return obj.get_status()
    
    def get_jobOffer(self, obj):
        job_offer = jobOfferSerializer(obj.get_job_offer())
        return job_offer.data
    
    
class jobSeekerHomePageSerializer(serializers.Serializer):
    # image_url = serializers.SerializerMethodField("get_image")
    applications = serializers.SerializerMethodField("get_applications")
    recomendations = serializers.SerializerMethodField("recommend")
    
    # def get_image(self, obj):
    #     return obj.get_image()
    
    def get_applications(self, obj):
        applications = applicationSerializer(Application.find_by_user(obj), many=True)
        return applications.data
    
    def recommend(self, obj):
        job_offers = jobOfferSerializer(JobOffer.recommend_by_user(obj), many=True)
        return job_offers.data
    

class employerHomePageSerializer(serializers.Serializer):
    # image_url = serializers.SerializerMethodField("get_image")
    job_offers = serializers.SerializerMethodField("get_jobOffers")
    
    # def get_image(self, obj):
    #     return obj.get_image()
    
    def get_jobOffers(self, obj):
        job_offers = jobOfferSerializer(JobOffer.find_by_user(obj), many=True)
        return job_offers.data
    

class viewJobApplicantsSerializer(serializers.Serializer):
    job_offer = serializers.SerializerMethodField("get_jobOffer")
    applications = serializers.Serializer("get_applications")
    
    def get_jobOffer(self, obj):
        job_offer = jobOfferSerializer(obj)
        return job_offer.data
    
    def get_applications(self, obj):
        applications = applicationSerializer(Application.find_by_job_offer(obj), many=True)
        return applications.data

