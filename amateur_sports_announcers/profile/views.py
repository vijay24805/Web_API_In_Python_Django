"""
class for creating, editing and viewing profiles
"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from profile.models import ProfileForm, UserProfile


def createprofile(request):
    """
    creating user profile i.e his favorite channels, announcers etc..
    """
    logged_in = True
    if request.method == "POST":
        form = ProfileForm(request.POST , \
         instance = UserProfile(mainUser = request.user))
        print("entered in Views for profile")
        if not form.is_valid():
            return render(request, "profile/createProfile.html", \
                 {"form" : form})
        #saving in DB
        form.save()
        return redirect("/accounts/viewProfile/")
    else:
        context = {'logged_in': logged_in , 'form' : ProfileForm()}
        return render(request, "profile/createProfile.html" , context)

def viewprofile(request):
    """
    user can view his favorite channels, games etc
    """
    logged_in = True
    if UserProfile.objects.filter(mainUser_id = request.user.id).count() > 0:
        profileexists = True
        profile  =  UserProfile.objects.filter(mainUser_id = \
         request.user.id).order_by('-id')[0]
        form = ProfileForm(instance = profile)
        return render(request, "profile/viewProfile.html", \
            {"form":form, "profileExists": profileexists})
    else:
        profileexists = False
        context = {'logged_in': logged_in , 'profileExists': profileexists}
        return render(request , "profile/viewProfile.html" , context)

#edit user profile
def editprofile(request):
    """
    edit profile
    """
    logged_in = True
    from django.forms.models import modelformset_factory
    profileformset = modelformset_factory(UserProfile, exclude=('mainUser',), \
      max_num = 1, can_delete= True)
    if request.method == "POST":
        formset = profileformset(request.POST, request.FILES)

        if not formset.is_valid():
            print(formset.errors())
        else:
            formset.save()
        context = {'logged_in': logged_in }
        return redirect("/accounts/viewProfile", context)
    else:
        if UserProfile.objects.all().filter(mainUser_id= request.user.id) \
                 .count() > 0:
            profileexists = True
            formset = profileformset(queryset= UserProfile.objects.all(). \
             filter(mainUser_id= request.user.id).order_by('-id')[: 1])
            context = {'logged_in': logged_in , "form": ProfileForm(), \
              "formset": formset,"profileExists": profileexists}
            return render(request, "profile/editProfile.html", context)

        else:
            profileexists = False
            context = {'logged_in': logged_in , 'profileExists': profileexists}
            return render(request, "profile/editProfile.html", context)

# user can edit his password,first name, last name and email id here
def manageaccount(request):
    """
    user can edit his password,first name, last name and email id here
    """
    logged_in = True
    from django.forms.models import modelformset_factory
    userformset = modelformset_factory(User , max_num = 1 , \
         fields = ("password", "first_name" , "last_name" , "email" , ))

    if request.method == "POST":
        formset = userformset(request.POST , request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect("/#/")
        else:
            print (formset.errors())

    else:
        if User.objects.all().filter(id = request.user.id).count() > 0:
            profileexists = True
            formset = userformset(queryset = User.objects.all(). \
                filter(id = request.user.id).order_by('-id')[: 1])
            context = {'logged_in': logged_in , "formset" : formset, \
                "profilEexists" : profileexists }
            return render(request , "profile/manageAccount.html" , context)
        else:
            context = {'logged_in': logged_in , 'profileExists': profileexists}
            return render(request, "profile/manageAccount.html" , context)


