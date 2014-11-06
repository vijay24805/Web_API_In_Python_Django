from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import Http404
from forms import ManageAccount
import urllib2
from django.http import HttpResponseRedirect
import json as simplejson


def index(request):
    logged_in = True if request.user.is_authenticated() else False
    context = { 'logged_in': logged_in }
    return render(request, 'homepage/index.html', context)
    # title is no longer necessary as we have default in base

	
	
