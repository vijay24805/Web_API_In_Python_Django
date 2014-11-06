"""
this file takes care of chat app and top 10 channels
"""
from django.shortcuts import render
from hot.models import HotList
import urllib2
import json as simplejson
from hot.models import Chat, ChatForm
from django.forms.models import modelformset_factory


def chklogin(request):
    '''
    check if user is logged in, added by Joseph
    '''
    logged_in = False
    user = request.user
    if user.is_authenticated():
        logged_in = True
    return logged_in

def existingposts():
    """
    method to retrieve existing posts
    """
    form = modelformset_factory(Chat , exclude = ('user', 'id', \
    'userName', ) , extra = 0)
    formset = form(queryset = Chat.objects.all().order_by("added"))
    return formset

def chat(request):
    """
    chat method to show data in chat app
    """
    if request.method == "POST":
        #adding current time to retrieve posts based on time entered
        form = ChatForm(request.POST, instance = Chat(user_id = \
        request.user.id, userName=request.user))

        if form.is_valid():
            form.save()
        else:
            form.errors()
			
    	return render(request , "hot/chat.html", {"form" : ChatForm(), \
            "formset" : existingposts(), 'logged_in' : chklogin(request)})
    else:
	return render(request, "hot/chat.html", {"form" : ChatForm(), "formset" : existingposts() , "user" : request.user,\
            'logged_in': chklogin(request)})

def topchannels(request):
    """
    sending top10 channel data to template
    """
    hotlistset = modelformset_factory(HotList , max_num = 10, exclude = ('id',))
    hotlistobjset = hotlistset(queryset = HotList.objects.all().order_by('-viewers')[0 : 10])
    return render(request, "hot/topChannels.html", {"form1" : hotlistobjset,'logged_in' : chklogin(request)})


def hotchannel(request):
    """
    getting top 10 hot channels
    """
    savehotlist()
    print("entered in view profile")
    hotlistset = modelformset_factory(HotList, max_num = 10)
    hotlistobjset = hotlistset(queryset = HotList.objects.all().order_by('-viewers')[0:10])

    top10viewers = []
    dividend = 1

    if HotList.objects.all().order_by('-viewers').count() > 10:

        top10hotlist = HotList.objects.all().order_by('-viewers')[0 : 10]
        topviewers = HotList.objects.all().order_by('-viewers')[0]
        #some time one channel can get 1000000 viewers but anothe channel might
        #get 100 users, tried in D3.js for scale by specifiying domain and
        #range, but it was not working fine, so put some temporary fix, to
        #reduce the index, so to display graphs properly
        if topviewers.viewers > 1000 and topviewers.viewers < 10000:
            print ("s value less than 10000")
            dividend = 50
        elif topviewers.viewers > 10000 and topviewers.viewers < 100000:
            dividend = 500
            print ("s value less than 100000")
        elif topviewers.viewers > 100000 and topviewers.viewers < 1000000:
            dividend = 5000
            print ("s value less than 1000000")
        elif topviewers.viewers > 1000000 and topviewers.viewers < 10000000:
            dividend = 50000
            print ("s value less than 1000000")

        for views in top10hotlist:
            print("top channel" , views)
            top10viewers.append(views.viewers / dividend)

    return render(request, "hot/barchart.html", {"form1" : hotlistobjset, "top10" : simplejson.dumps(top10viewers),\
              'logged_in' :  chklogin(request)})

def savehotlist():
    """
    retrieved top channels from twitch api
    """
    url = 'https://api.twitch.tv/kraken/streams/featured?limit=25&offset=0&client_id=jqsd54ktgrxu0x05kh6w2lt4l3zkfck'
    jsoncontents = urllib2.urlopen(url)
    dictObj = simplejson.load(jsoncontents)
    returnli = []
    for streamnum in range(len(dictObj["featured"])):
        returnli.append( (streamnum, \
        dictObj["featured"][streamnum]["stream"]["channel"]["display_name"], \
        dictObj["featured"][streamnum]["stream"]["channel"]["status"], \
        dictObj["featured"][streamnum]["stream"]["viewers"], \
        dictObj["featured"][streamnum]["stream"]["channel"]["game"], \
        str(dictObj["featured"][streamnum]["stream"]["channel"]["url"]).\
        replace("http://www.twitch.tv/", "")) )
    channel = " "
    description = " "
    viewers = " "
    game = " "
    count = 0
    lastid = 0
    if HotList.objects.all().count() > 1:
        lastid = HotList.objects.latest('id').id
        print("last hot list id",lastid)
    else:
        lastid = 0

    #removing duplicate records
    for row in HotList.objects.all():
        if HotList.objects.filter(Channel=row.Channel).count() > 0:
            row.delete()

    for stream in returnli:
        i = 0
        for schannel in stream:
            i += 1
            if i == 2:
                if not schannel is None:
                    channel = schannel
                    print("channel is", channel)
            elif i == 3:
                if not schannel is None:
                    description = schannel
            elif i == 4:
    	       #check if channel is already existing, if yes check viewers
                #are greater than new record
                if not schannel is None:
                    print("viewers", schannel)
                    if HotList.objects.filter(Channel = channel).count() == 1:
                        hotlistinstance = HotList.objects.get(Channel = channel)
                        hotlistviewers = hotlistinstance.viewers
                        intviewers = int(hotlistviewers)
                        ints = int(schannel)
                        print("viewers count", hotlistinstance.viewers)
                        if intviewers < ints:
                            viewers = int(schannel)
                        else:
                            viewers = intviewers
                    else:
                        print("entering manually viewers ",schannel)
                        viewers = int(schannel)
                else:
                    break
            elif i == 5:
                if not schannel is None:
                    game = schannel
                    i = 0
            else:
                pass

        count += 1
        print(lastid+count, channel, description, game, viewers)
        instance = HotList(id = lastid + count, Channel = channel, Description = description, Game = game, viewers = viewers)
        instance.save()




