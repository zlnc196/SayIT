from django.shortcuts import render, redirect
from .models import Posts
import datetime
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Now, Extract
from django.utils import timezone
import os




# Create your views here.

#Things to render Now to use later



def CanBeInt(testing):
    try:
        holder = int(testing)
        return True
    except ValueError:
        return False
    
def convertToList(string, array):
    word=""
    for char in string:                               #Quick algorithm to convert it back into a list
            
        if char == "-":
            array.append(word)
            word=""
        else:
            word=word+char
    array.append(word)
    return list(dict.fromkeys(array))


#I made the decision to handle likes client side leading to a better user experience
# Therefore I need to handle the accumulation of all the likes does in a given page

def handleLikes(request):
    if "likeProcess" in request.POST and "unlikeProcess" in request.POST:
        
        likeProcess = request.POST["likeProcess"]  #access the array turned int a string from the js file
        unlikeProcess = request.POST["unlikeProcess"] 
        likeArray = []
        unlikeArray = []
       
        
        likeArray = convertToList(likeProcess, likeArray)
        
        unlikeArray = convertToList(unlikeProcess, unlikeArray)
        
        for elem in likeArray:
            idholder = request.user
            canAdd = CanBeInt(elem)
            
            if canAdd == True:
                if elem not in idholder.liked_posts:
                    idholder.liked_posts.append(elem)
                    lidholder = Posts.objects.get(id = int(elem))
                    lidholder.likes = lidholder.likes+1
                    idholder.save()
                    lidholder.save()
                
        for elem in unlikeArray:
            idholder = request.user
            canRemove = CanBeInt(elem)
                
            if canRemove == True:
                if elem in idholder.liked_posts:
                    idholder.liked_posts.remove(elem)
                    lidholder = Posts.objects.get(id = int(elem))
                    lidholder.likes = lidholder.likes-1
                    idholder.save()
                    lidholder.save()   
   
    
    
with open(r"C:\Users\User\SayIt social media\badwords.txt", "r") as file:  #Prevention of hate speech is very important and vert relevant
    badWords = file.read()
   
    
badWordList = badWords.split(",")


def intro(request): #Ensure security as Users cannot enter site logged in
    logout(request)
    return render(request, 'intro.html')

def register(request):
    return render(request, 'register.html')

@csrf_protect #Decorator to protect from CSRF attacks when logging in
def login(request):
    if request.user.is_authenticated:
        logout(request)
    
    return render(request, 'login.html')


def confirm(request):
    email = request.POST['Email']
    username = request.POST['username']
    password = request.POST['password']
    
    valid = False
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for char in password:
        if char in nums and len(password) >= 8:
            valid = True
            break
            
    allUsers = get_user_model().objects.all()
    errorMessage = "Number in password is required"
    if valid == True:
        for user in allUsers:
            if user.username == username:
                valid = False
                errorMessage = "Username taken"
                break
        
        for user in allUsers:
            if user.email == email:
                valid = False
                errorMessage = "email taken"
                break
            
        rulesCheck = "off"
        if "checkbox" in request.POST:
            rulesCheck = request.POST["checkbox"]
       
        if rulesCheck == "off":
            valid = False
            errorMessage = "Please confirm that you will adhere to the terms of service"
            
    
     
    if valid == True:
        user = get_user_model().objects.create_user(username=username, email=email, password=password, is_superuser=False, profilePicture='media\pfp.png',last_login = '2022-01-19 14:30:45.123456-05:00', is_active = True, date_joined = timezone.now() ,first_name = 'Dont', last_name = 'Worry', liked_posts=[], followedUsers = [], blockList=[], userReports=[]) #blockList=[], userReportedList=[] )
        user.save()
        return redirect("login")

    return render(request, 'register.html', {'Valid': valid, "errorMessage": errorMessage})

@csrf_protect
def homepage(request):
    idholder = 0
    loginValid=False
    
    if not request.user.is_authenticated:
        if "lusername" in request.POST and "lpassword" in request.POST:
            username = request.POST['lusername']
            password = request.POST['lpassword']
        

            user = authenticate(request, username=username, password=password)
            if user is not None:
                loginValid = True
                currentUsername = username
                auth_login(request, user)  # Log in the user
                route = 'homepage.html'
            else:
                loginValid = False
                route = 'login.html'
                currentUsername = None       
        else:
            route = 'login.html'
        
    else:
        route='homepage.html'
        currentUsername = request.user.username
        handleLikes(request)
        currentUsername = request.user.username
        idholder = request.user
        
            
        
            
            
    return render(request, route, {'currentUsername':currentUsername, 'lValid': loginValid, 'cid': idholder})

            
        
    

 
@login_required(login_url='login')
def profile(request):
    print("Now on profile")
    handleLikes(request)
    currentUser = request.user
    currentUsername = request.user.username
    etimeOfPost = datetime.datetime.now()
    timeOfPost = etimeOfPost.strftime('%c')
    if 'post' in request.POST:
        post = request.POST['post']
        postValid = True
    else:
        post=""
        postValid = False
        
    if 'image' in request.FILES:
        image = request.FILES['image']
        imageValid = True
    else:
        imageValid = False
        
    
    if post == "":
        postValid = False
        
    if 'replyCheck' in request.POST :
        replyCheck = request.POST["replyCheck"]    
    else:
        replyCheck = "False"
   
    for word in post.split():
        if word.lower() in badWordList:
            post = 'Invalid due to hate speech'
    if postValid == True or imageValid:   
        if imageValid:  
            if replyCheck == "True":
                repliedTo = request.POST["repliedTo"] 
                newPost = Posts.objects.create(post=post, user=currentUser, date = timeOfPost, likes = 0, img=image, replies=[], replyTo=repliedTo, postReports=[])
            else:
                newPost = Posts.objects.create(post=post, user=currentUser, date = timeOfPost, likes = 0, img=image, replies=[], replyTo="False", postReports=[])      
        else:
            if replyCheck == "True":
                repliedTo = request.POST["repliedTo"] 
                newPost = Posts.objects.create(post=post, user=currentUser, date = timeOfPost, likes = 0, replies=[], replyTo=repliedTo, postReports=[])
            else:    
                newPost = Posts.objects.create(post=post, user=currentUser, date = timeOfPost, likes = 0, replies=[], replyTo="False", postReports=[])
            
        newPost.save()
            
            
        
        if replyCheck == "True":
            repliedTo = request.POST["repliedTo"]
            postRepliedTo = Posts.objects.get(id=repliedTo)
            postRepliedTo.replies.append(newPost.id)
            postRepliedTo.save()
            
    if 'delpost' in request.POST:      
        delpost = request.POST["delpost"]
    else:
        delpost = "False"
    
    if delpost != "False":
        Posts.objects.get(id=delpost).delete()
        for users in get_user_model().objects.all():
            likeList = users.liked_posts 
            if str(delpost) in likeList: 
                likeList.remove(delpost)
        
        
    usersPosts = Posts.objects.filter(user=currentUser.id).order_by("-date_created")
    route = 'profile.html'
    
    currentUser = request.user
    
    likedList = currentUser.liked_posts
    likedList = "-".join(likedList)
    allUsers = get_user_model().objects.all()
    
    allPosts = Posts.objects.all()
    
    
    return render(request,route, {'currentUsername':currentUsername, 'uposts':usersPosts, "likedList": likedList, 'CurrentUser':currentUser, 'allUsers': allUsers, "allPosts":allPosts})




@login_required(login_url='login')
def AllPosts(request):
  
    currentUser = request.user
    allUsers = get_user_model().objects.all()
    likedList = currentUser.liked_posts
    likedList = "-".join(likedList)
   
    
    blocked = request.user.blockList
    allPosts = Posts.objects.exclude(user_id__in=blocked).annotate(
    days_since_created=ExpressionWrapper(
        Extract(Now() - F('date_created'), 'days'),
        output_field=fields.IntegerField()
    )
).annotate(
    likes_per_day=ExpressionWrapper(
        F('likes') / (F('days_since_created') + 1),  # Add 1 to avoid division by zero
        output_field=fields.FloatField()
    )
).order_by('-likes_per_day')
    
    return render(request,'AllPosts.html', {'allPosts':allPosts, 'currentUser': currentUser, "likedList": likedList, 'allUsers': allUsers })

@login_required(login_url='login')
def FollowedPosts(request):
    currentUsername = request.user.username
    currentUser = request.user
    allUsers = get_user_model().objects.all()

    likedList = currentUser.liked_posts
    likedList = "-".join(likedList)
    followedList = currentUser.followedUsers
    followedPosts = Posts.objects.filter(user__in=followedList).order_by('-date_created')
  
    return render(request,'followedPosts.html', {'followedPosts':followedPosts, 'currentUser': currentUser, "likedList": likedList, 'allUsers': allUsers })

@login_required(login_url='login')
def LikedPosts(request):
    handleLikes(request)
    currentUsername = request.user.username
    allPosts = Posts.objects.all()
    currentUser = request.user
    likedList = currentUser.liked_posts 
    likedPosts = Posts.objects.filter(id__in=likedList)
    likedList = "-".join(likedList)
    allUsers = get_user_model().objects.all()

    return render(request, 'liked.html', {"likedPosts": likedPosts, "currentUsername": currentUsername, 'allUsers': allUsers, "likedList":likedList, "allPosts":allPosts })

@login_required(login_url='login')
def editProfile(request):
    handleLikes(request)
    currentUser = request.user
    
    return render(request, 'editProfile.html', {"CurrentUser":currentUser})


@login_required(login_url='login')
def changedProfile(request):
    newBio = request.POST['newBio']
    if 'newPfp' in request.POST:
        newPfp = request.FILES['newPfp']
    else:
        newPfp = request.user.profilePicture
    currentUser = request.user
    currentUser.bio = newBio
    currentUser.profilePicture = newPfp
    currentUser.save()
    currentUsername = request.user.username
    usersPosts = Posts.objects.filter(user=currentUser.id)
    return render(request, 'profile.html', {'CurrentUser':currentUser, 'uposts':usersPosts, 'currentUsername':currentUsername})


@login_required(login_url='login')
def search(request):
    UorP = request.POST['userOrPost']
    searchedFor = request.POST['searchedFor']
    returnDict = {}
    cusers = request.user
    if UorP == 'post':
        selectedPosts = Posts.objects.filter(post__icontains = searchedFor)
        route = 'searchedPosts.html'
        returnDict['selectedPosts'] = selectedPosts
    else:
        selectedUsers = get_user_model().objects.filter(username__icontains = searchedFor)
        route = 'searchedUsers.html'
        returnDict['selectedUsers'] = selectedUsers
    likedList = cusers.liked_posts
    likedList = "-".join(likedList)
    returnDict['likedList'] = likedList
    
    return render(request, route, returnDict)


@login_required(login_url='login')
def otherProfile(request):
    otherUserId = request.POST['otherUser']
    otherUser = get_user_model().objects.get(id=otherUserId)
    otherUsersPosts = Posts.objects.filter(user=otherUser).order_by("-date_created")
    likedList = otherUser.liked_posts
    likedList = "-".join(likedList)
    allUsers = get_user_model().objects.all()
    currentUser = request.user
    otherUser = get_user_model().objects.get(id=otherUserId)
    blockList = currentUser.blockList
    followList = currentUser.followedUsers
    if otherUserId in followList:
        followed = True
    else:
        followed = False
        
    if otherUserId in blockList:
        blocked = True
    else:
        blocked = False
    
    return render(request, "otherProfile.html", {'otherUser': otherUser, 'otherUsersPosts':otherUsersPosts, 'likedList':likedList, "followed":followed, "blocked":blocked, "currentUser":currentUser, "allUsers":allUsers})
    

@login_required(login_url='login')    
def followChange(request):
    otherUserId = request.POST['otherUser']
    otherUser = get_user_model().objects.get(id=otherUserId)
    otherUsersPosts = Posts.objects.filter(user=otherUser).order_by("-date_created")
    likedList = otherUser.liked_posts
    likedList = "-".join(likedList)
    currentUser = request.user
    followList = currentUser.followedUsers
    if otherUserId in followList:
        currentUser.followedUsers.remove(otherUserId)
        otherUser.followers -= 1
        followed = False
    elif otherUserId not in followList:
        currentUser.followedUsers.append(otherUserId)
        otherUser.followers += 1
        followed = True
    
        
    allUsers = get_user_model().objects.all()
        
    currentUser.save()
    otherUser.save()
        
    likedList = otherUser.liked_posts
    likedList = "-".join(likedList)
    currentUser = request.user
    otherUser = get_user_model().objects.get(id=otherUserId)
    blockList = currentUser.blockList
    followList = currentUser.followedUsers
    if otherUserId in followList:
        followed = True
    else:
        followed = False
        
    if otherUserId in blockList:
        blocked = True
    else:
        blocked = False
      
      
    currentUser.save()
    otherUser.save()
    

    
    return render(request, "otherProfile.html", {'otherUser': otherUser, 'otherUsersPosts':otherUsersPosts, 'likedList':likedList, "followed":followed, "blocked":blocked, "currentUser":currentUser, "allUsers":allUsers})
    
    
@login_required(login_url='login')   
def otherLikedPosts(request):
    handleLikes(request)
    otherUserId = request.POST['otherUser2']
    otherUser = get_user_model().objects.get(id=otherUserId)
    otherLikedList = otherUser.liked_posts
    likedPosts = Posts.objects.filter(id__in=otherLikedList)
    currentUser = request.user
    likedList = currentUser.liked_posts
    likedList = "-".join(likedList)
    allUsers = get_user_model().objects.all()
  
    
    return render(request, 'otherLiked.html', {"likedPosts": likedPosts, "otherUser": otherUser, 'allUsers': allUsers, "currentUser": currentUser, "likedList":likedList })    
    
@login_required(login_url='login')    
def replies(request):
    
    handleLikes(request)
    postId = request.POST["selectedPost"]
    selectedPost = Posts.objects.get(id=postId)
    currentUser = request.user
    repliedList = selectedPost.replies
    repliedPosts = Posts.objects.filter(id__in=repliedList)
    allUsers = get_user_model().objects.all()
    likedList = currentUser.liked_posts
    likedList = "-".join(likedList)
    allPosts = Posts.objects.all()
    
    return render(request, "replies.html", {"post": selectedPost, "likedList":likedList, "repliedPosts": repliedPosts, 'allUsers': allUsers, "allPosts":allPosts})

@login_required(login_url='login')  
def blockUser(request):
    blockedID = request.POST["otherUser"] 
    currentUser = request.user
    otherUser = get_user_model().objects.get(id=blockedID)
    followList = otherUser.followedUsers
    if blockedID in currentUser.blockList:
        currentUser.blockList.remove(blockedID)
    else:
        currentUser.blockList.append(blockedID)
        if blockedID in currentUser.followedUsers:
            currentUser.followedUsers.remove(blockedID)
            otherUser.followers -= 1
            followed = False
        
    currentUser.save()
    otherUser.save()
        
    otherUserId = request.POST['otherUser']
    otherUser = get_user_model().objects.get(id=otherUserId)
    otherUsersPosts = Posts.objects.filter(user=otherUser).order_by("-date_created")
    
    likedList = otherUser.liked_posts
    likedList = "-".join(likedList)
    currentUser = request.user
    otherUser = get_user_model().objects.get(id=otherUserId)
    blockList = currentUser.blockList
    followList = currentUser.followedUsers
    if otherUserId in followList:
        followed = True
    else:
        followed = False
        
    if otherUserId in blockList:
        blocked = True
    else:
        blocked = False
        
    allUsers = get_user_model().objects.all()
    
    return render(request, "otherProfile.html", {'otherUser': otherUser, 'otherUsersPosts':otherUsersPosts, 'likedList':likedList,"blocked":blocked, "followed":followed, "currentUser": currentUser, "allUsers": allUsers})
    

@login_required(login_url='login')
def afterReport(request):
    reason = request.POST["reportReason"]
    otherUserId = request.POST['otherUser']
    otherUser = get_user_model().objects.get(id=otherUserId)
    otherUser.userReports.append(reason)
    otherUser.save()
    
    return render(request, "afterReport.html")

@login_required(login_url='login')
def afterPostReport(request):
    reason = request.POST["reportReason"]
    reportedPostID = request.POST['reportedPost']
    reportedPost = Posts.objects.get(id=reportedPostID)
    reportedPost.postReports.append(reason)
    reportedPost.save()
    
    return render(request, "afterReport.html")


    
    


