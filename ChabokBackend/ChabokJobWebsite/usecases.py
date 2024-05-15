from .models import JobOffer, Resume, Application


def get_jobOffer_by_id(id):
    return JobOffer.find_by_id(id)

def create_job_offer(job_offer, user):
    jobOffer = JobOffer(author=user, **job_offer)
    jobOffer.save()
    return jobOffer

def find_jobOffers_by_user(user):
    return JobOffer.find_by_user(user)

def delete_job_offer(job_offer):
    job_offer.delete()
    
def update_job_offer(job_offer, jobOfferData):
    job_offer.title = jobOfferData['title']
    job_offer.company_name = jobOfferData['company_name']
    job_offer.location = jobOfferData['location']
    job_offer.type_collabration = jobOfferData['type_collabration']
    job_offer.job_description = jobOfferData['job_description']
    job_offer.reqired_skils = jobOfferData['reqired_skils']
    job_offer.company_description = jobOfferData['company_description']
    job_offer.save()
    return job_offer

def update_user_profile(user, user_profile):
    user.username = user_profile['username']
    user.first_name = user_profile['first_name']
    user.last_name = user_profile['last_name']
    user.email = user_profile['email']
    user.role = user_profile['role']
    user.gender = user_profile['gender']
    user.age = user_profile['age']
    user.city = user_profile['city']
    # resume = Resume(file_url=user_profile['resume'])
    # resume.save()
    # user.resume = resume
    user.save()
    return user


def create_application(user, job_offer):
    resume = user.get_resume()
    applciation = Application(user=user, resume=resume, job_offer=job_offer)
    applciation.save()
    return applciation
    