"""
this file takes care of sentiment analysis
sample tweets are taken as positive, negative and neutral, And performed
NaiveBayesALgorithm and classified it as positive or negative or neutral
after taking all user comments in chat app
"""
from django.shortcuts import render
from hot.models import Chat

def getlikelihoodtokens(tweetarraystring):
    """
    returns maximum likelihodd estimate tokens
    i.e. it removes unnecessary charachetrs, repetitions, and words start with
    @, www, http etc
    """
    tokenlist = []
    token = " "
    splitsubarray = []
    splitsubarray1  = []
    splitsubarray2 = []
    tempstr = ""

    for token in tweetarraystring.split(" "):
        temp = ""
        emptyloop = 0
        token = token.lower()
        if token != None and len(token) > 0:
            #we don't need urls or @nouns for calculating the probability, so
            #I'm ignoring them
            if token.startswith("@") or token.startswith("www") or \
                token.startswith("http"):
                continue
            #if the word starts with number, please ignore the word
            for i in range(0, 10):
                if token.startswith(str(i)):
                    continue

            for i in range(0 , len(token)):
                tokenchar = token[i]
                #print (token[i])
                # if tokens start with # ignore the character and proceed for
                #the rest of the string
                if token[0].startswith("#"):
                    continue

                #don't loop if you found similar characters
                if emptyloop > 0:
                    emptyloop -= 1
                    continue

                #if any character contains characters like "%","?","!" etc.
                #please ignore them
                if len(token) > 0 and (token[i] == '!' or \
                            token[i] == '\\' or  token[i] == '\'' or \
                            token[i] == '\"' or token[i] == ' ' or  \
                            token[i] == '.' or token[i] == ':' or \
                            token[i] == '-' or token[i] == ',' or \
                            token[i] == '&' or token[i] == '(' or \
                            token[i] == ')' or token[i] == '*' or \
                            token[i] == '[' or token[i] == ']'):
                    continue

                #if tokens start with ",",".","-" then
                if token[i] == "." or token[i] == "," or token[i] == "-":
                    splitsubarray  = token.split(".")
                    splitsubarray1  = token.split(",")
                    splitsubarray2  = token.split("-")

                    if len(splitsubarray) > 1 or len(splitsubarray1) > 1 or \
                                len(splitsubarray2) > 1:
                        for subtoken in splitsubarray:
                            for j in range(0, len(subtoken)):
                                if len(subtoken) > 0 and subtoken[j] != '!' or \
                                subtoken[j] != '\\' or  subtoken[j] != '\'' or \
                                subtoken[j] != '\"' or subtoken[j] != ' ' or  \
                                subtoken[j] != '.' or subtoken[j] != ':' or \
                                subtoken[j] != '-' or subtoken[j] != ',' or \
                                subtoken[j] != '&' or subtoken[j] != '(' or \
                                subtoken[j] != ')' or subtoken[j] != '*' or \
                                subtoken[j] != '[' or subtoken[j] != ']':
                                    tempstr +=  subtoken[j]

                            for i in range(0 , 10):
                                if tempstr.startswith(str(i)):
                                    continue
                            tokenlist.append(tempstr)
                        break
                #making it empty for the next iteration
                tempstr = ""
                #a)this condition is for if if the letter repeats more than
                #one time ignore remaining letters in the word
                # for example, hiiiii, you can write hii instead of hiiii..
                #b)Similarly if the two letter repeats more than one time
                #like CiCi, put only Ci.
                if i > 1 and ((i+1) < len(token)):
                    if token[i-2] == tokenchar and token[i-1] == tokenchar:
                        emptyloop = 1
                    if token[i:i+2] == token[i-2:i]:
                        emptyloop = 1
                        continue

                if i > 2 and ((i+2) < len(token)):
                    if token[i:i+3] == token[i-3:i]:
                        emptyloop = 2
                        continue

                if i > 3 and ((i+3) < len(token)):
                    if token[i:i+4] == token[i-4:i]:
                        emptyloop = 3
                        continue
                if i > 4 and ((i+4) < len(token)):
                    if token[i:i+5] == token[i-5:i]:
                        emptyloop = 4
                        continue

                temp += tokenchar

            #need to check if there are any unnecessary characters

            for j in range(0 , len(temp)):
                if len(temp) > 0 and temp[j] != '!' or \
                        temp[j] != '\\' or  temp[j] != '\'' or \
                        temp[j] != '\"' or temp[j] != ' ' or  \
                        temp[j] != '.' or temp[j] != ':' or \
                        temp[j] != '-' or temp[j] != ',' or \
                        temp[j] != '&' or temp[j] != '(' or \
                        temp[j] != ')' or temp[j] != '*' or \
                        temp[j] != '[' or temp[j] != ']':
                    tempstr +=  temp[j]
                else:
                    continue
            #checking if still some words start with numbers
                for k in range(0 , 10):
                    if temp[j] == str(k):
                        continue
            if not tempstr.startswith("@"):
                tokenlist.append(tempstr)
            else:
                continue
            #making it empty for the next iteration
            tempstr = ""

    return tokenlist

def readandparse(request):
    """
    this method reads and parse the tweets which
    are segregated as positive or neutral or negative
    """
    tweetsfile = open("sentimentAnalysis/sampleTweets.txt", "r")
    stopwordfile = open("sentimentAnalysis/stopwords.txt", "r")
    #positivewordfile = open("positiveWords.txt", "r")
    #negativewordfile = open("negativeWords.txt", "r")
    #positive tweet count
    postweetcount = 0
    #Negative tweet count
    negtweetcount = 0
    #Neutral tweet count
    neutweetcount = 0
    #list which stores positive tokens
    csvpositive = []
    #list which stores negative tokens
    csvnegative = []
    #list which stores neutral tokens
    csvneutral = []
    #stores the positive word and its count
    posmap = {}
    #stores the negative word and its count
    negmap = {}
    #stores the neutral word and its count
    neumap = {}
    #stores maximum likelihood elements for positive words
    posmaplikelihood = {}
    #stores maximum likelihood elements for negative words
    negmaplikelihood = {}
    #stores maximum likelihood elements for neutral words
    neumaplikelihood = {}
    #storing after remove unnecessary characters in the tweet
    exampletweet = []
    #storing user comments from chat application in a list
    usercomments = []
    comment = ""
    #print ("tweets ",tweetsfile.readlines())
    #print ("stop words ", stopwordfile.readlines())
    #print ("positive words ", positivewordfile.readlines())
    #print ("negative words ", negativewordfile.readlines())
    usercomments = Chat.objects.all().values_list("opinion")

    #print("chat app comments", userComments)
    #iterating total tweets in chat app and making them into one big string
    for strcomment in usercomments:
        comment += " "
    for com in strcomment:
        comment += str(com) + ""
    #print("comment total", comment)
    exampletweet = getlikelihoodtokens(comment)
    #print("checking the user comments together",exampleTweet)

    #stopWords list initialization
    stopwords = []
    tweetarray = []

    for stopword in stopwordfile:
        stopwords.append(stopword)

    #for posword in positivewordfile:
     #   positiveWords.append(posword)

    #for negword in negativewordfile:
     #   negativeWords.append(negword)

    #print ("stop words are " , stopWords)
    #print ("positive words are " , positiveWords)
    #print ("negative words are " , negativeWords)

    #reading each and every tweet and storing in
    #tweetArray i.e.tuple
    for line in open('sentimentAnalysis/sampleTweets.txt'):
        lines = line.strip()
        tweetarray = lines.split(",")
        #print("sample tweets are ", tweetArray[0])
        #if len(tweetArray) > 0:
            #print("sample tweets are ", tweetArray[1])
        #checking if tweet as positive or negative or neutral
        if tweetarray[0] == "\"positive\"":
            postweetcount = postweetcount + 1
            tempcsv = getlikelihoodtokens(tweetarray[1])
            #print("positive tokens",tempCSV)
            for positivetoken in tempcsv:
                if positivetoken not in stopwords:
                    if not positivetoken.startswith("@"):
                        if positivetoken in posmap.keys():
                            posmap[positivetoken] = posmap[positivetoken] + 1
                        else:
                            posmap[positivetoken] = 1
                        csvpositive.append(positivetoken)
            #print("csvPositive words", csvPositive)

        if tweetarray[0] == "\"negative\"":
            negtweetcount = negtweetcount + 1
            tempcsv = getlikelihoodtokens(tweetarray[1])
            #print("negative tokens",tempcsv)
            for negativetoken in tempcsv:
                if negativetoken not in stopwords:
                    if not negativetoken.startswith("@"):
                        if negativetoken in negmap.keys():
                            negmap[negativetoken] = negmap[negativetoken] + 1
                        else:
                            negmap[negativetoken] = 1
                        csvnegative.append(negativetoken)
            #print("csvNegative words", csvNegative)

        if tweetarray[0] == "\"neutral\"":
            neutweetcount = neutweetcount + 1
            tempcsv = getlikelihoodtokens(tweetarray[1])
            #print("neutral tokens",tempCSV)
            for neutraltoken in tempcsv:
                if neutraltoken not in stopwords:
                    if not neutraltoken.startswith("@"):
                        if neutraltoken in neumap.keys():
                            neumap[neutraltoken] = neumap[neutraltoken] + 1
                        else:
                            neumap[neutraltoken] = 1
                        csvneutral.append(neutraltoken)
            #print("csvNeutral words", csvNeutral)

    #closing the file objects
    tweetsfile.close()
    stopwordfile.close()
    #positivewordfile.close()
    #negativewordfile.close()

    #initializing wordcounts for pos, neg, neutral
    positivewordcount = 0.0
    negativewordcount = 0.0
    neutralwordcount = 0.0

    #adding all the tweets for calculating prior probability
    totaltweetcount = 0
    #positive prior probaility
    pospriorprobability = 0.0
    #negative prior probaility
    negpriorprobability = 0.0
    #neutral prior probaility
    neupriorprobability = 0.0

    #print("positive map", posMap.items())

    for poskey, posval in posmap.items():
        #sometimes value may be 0, so better add 1
        posval += 1
        #calculate the length and add 6 items
        positivewordcount = len(csvpositive) + 6
        #print("posVal/positiveWordCount", positiveWordCount)
        positivewordcount = (posval + positivewordcount) / positivewordcount
        #print("after divison", positiveWordCount)
        #rint("example", 1/2000)
        #print("divison",positiveWordCount)
        #print("divison", posVal/positiveWordCount)
        posmaplikelihood[poskey] = positivewordcount
        #print(posKey, " repeated in positive list for" , \
                  #  posVal/positiveWordCount, " times ")

    for negkey, negval in negmap.items():
        negval += 1
        #calculate the length and add 6 items
        negativewordcount = len(csvnegative) + 6
        #print(negKey, " repeated in negative list for" , \
         #        negVal/negativeWordCount, " times ")
        negmaplikelihood[negkey] = (negval + negativewordcount) / \
        negativewordcount

    for neukey, neuval in neumap.items():
        neuval += 1
        #calculate the length and add 6 items
        neutralwordcount = len(csvneutral) + 6
        #print(neuKey, " repeated in neutral list for" , \
         #        neuVal/neutralWordCount, " times ")
        neumaplikelihood[neukey] = (neuval + neutralwordcount) / \
        neutralwordcount

    #currently I am not getting decimal values properly like in windows machi
    #ne ex:0.00006666, so adding total count to denominator to avoid 0.0
    #values as a workaround and it works fine in windows not in vim :(
    totaltweetcount = postweetcount + negtweetcount + neutweetcount
    #calculating positive prior probability
    pospriorprobability = (postweetcount + totaltweetcount) / totaltweetcount
    #calculating negative prior probability
    negpriorprobability = (negtweetcount + totaltweetcount) / totaltweetcount
    #calculating neutral prior probability
    neupriorprobability = (neutweetcount + totaltweetcount) / totaltweetcount

    #posNaiveBayesProbability initialization
    posnaivebayesprobability = 0.0
    #negNaiveBayesProbability initialization
    negnaivebayesprobability = 0.0
    #neuNaiveBayesProbability initialization
    neunaivebayesprobability = 0.0

    #calculating positive NaiveBayesProbability
    for word in exampletweet:
        if word in posmaplikelihood:
            posnaivebayesprobability += (posmaplikelihood[word] + 0.01) * \
                                         pospriorprobability
    #print("final posNaiveBayesProbability is ",posNaiveBayesProbability)

    #calculating negative NaiveBayesProbability
    for word in exampletweet:
        if word in negmaplikelihood:
            negnaivebayesprobability += (negmaplikelihood[word] + 0.01) * \
                                         negpriorprobability
    #print("final negNaiveBayesProbability is ",negNaiveBayesProbability)

    #calculating neutral NaiveBayesProbability
    for word in exampletweet:
        if word in neumaplikelihood:
            neunaivebayesprobability += (neumaplikelihood[word] + 0.01) * \
                                         neupriorprobability
    #print("final neuNaiveBayesProbability is ",neuNaiveBayesProbability)

    maxvalue = 0.0
    sentiment = ""

    maxvalue = max(posnaivebayesprobability, \
                negnaivebayesprobability, neunaivebayesprobability)

    print("final max value is", max(posnaivebayesprobability, \
            negnaivebayesprobability, neunaivebayesprobability))

    if  maxvalue == posnaivebayesprobability:
        sentiment = "POSITIVE"
        #print("the sentiment is positive")
    elif maxvalue == negnaivebayesprobability:
        sentiment = "NEGATIVE"
        #print("the sentiment is negative")
    else:
        sentiment = "NEUTRAL"
        #print("the sentiment is neutral")

    return render(request, "sentimentAnalysis/sentiment.html", \
    {"sentiment" : sentiment, 'logged_in' : chklogin(request)})


def chklogin(request):
    '''
    check if user is logged in, added by Joseph
    '''
    logged_in = False
    user = request.user
    if user.is_authenticated():
        logged_in = True
    return logged_in

