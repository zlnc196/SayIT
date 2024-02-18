from django.shortcuts import render, redirect
import smtplib
from .models import Users, Posts
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Now, Extract
from django.utils import timezone




# Create your views here.


loginValid = False

def handleLikes(request):
    currentUser = request.user.username
    #try:
    likeProcess = request.POST["likeProcess"]  #access the array turned int a string from the js file
    unlikeProcess = request.POST["unlikeProcess"] 
    print(likeProcess)          # Just for testing
    print(unlikeProcess)
    likeArray = []
    unlikeArray = []
    word=""
    for char in likeProcess:                               #Quick algorithm to convert it back into a list
        
        if char == "-":
            likeArray.append(word)
            word=""
        else:
            word=word+char
    likeArray.append(word)
    likeArray = list(dict.fromkeys(likeArray))
    print(likeArray)
    
    unword=""
    for char in unlikeProcess:                               #Quick algorithm to convert it back into a list
        
        if char == "-":
            unlikeArray.append(unword)
            unword=""
        else:
            unword=unword+char
    unlikeArray.append(unword)
    unlikeArray = list(dict.fromkeys(unlikeArray))
    print(unlikeArray)
    
    
    for elem in likeArray:
        idholder = request.user
        
        print("here we go-adding")
        try:
            testHolder = int(elem)
            canAdd = True
        except:
            canAdd = False
        
        if canAdd == True:
            if elem in idholder.liked_posts:
                print("already post already liked")
            else:
                idholder.liked_posts.append(elem)
                lidholder = Posts.objects.get(id = int(elem))
                lidholder.likes = lidholder.likes+1
                print(elem, "has been added")
                idholder.save()
                lidholder.save()
    
    
    for elem in unlikeArray:
        idholder = request.user
        print("here we go-deleting")
        try:
            testHolder = int(elem)
            canRemove = True
        except:
            canRemove = False
            
        if canRemove == True:
            if elem in idholder.liked_posts:
                idholder.liked_posts.remove(elem)
                lidholder = Posts.objects.get(id = int(elem))
                lidholder.likes = lidholder.likes-1
                print(elem, "has been Removed")
                idholder.save()
                lidholder.save()
            else:
                print("Not even liked, cant be removed")
            
    for elem in idholder.liked_posts:
        print(elem)
        
    #except:
        #print("nuttin to worry about")

def intro(request):
    print(request.user.username)
    logout(request)
    return render(request, 'intro.html')

def register(request):
    return render(request, 'register.html')

@csrf_protect
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

            
    if valid == True:
        user = get_user_model().objects.create_user(username=username, email=email, password=password, is_superuser=False, profilePicture='media\pfp.png',last_login = '2022-01-19 14:30:45.123456-05:00', is_active = True, date_joined = timezone.now() ,first_name = 'Dont', last_name = 'Worry', liked_posts=[], followedUsers = [], blockList=[]) #blockList=[], userReportedList=[] )
        user.save()
        return redirect("login")
    

        
    
    
    
    
    
    
    
    return render(request, 'register.html', {'Valid': valid})

@csrf_protect
def homepage(request):
    UserData = get_user_model().objects.all()
    idholder = 0
    loginValid=False
    
    print(request.user.username)
    if not request.user.is_authenticated:
        try:
            username = request.POST['lusername']
            password = request.POST['lpassword']
        

            user = authenticate(request, username=username, password=password)
            if user is not None:
                loginValid = True
                currentUser = username
                auth_login(request, user)  # Log in the user
                route = 'homepage.html'
                print("yeah")
            else:
                loginValid = False
                route = 'login.html'
                currentUser = None
                print("nah")
        except KeyError:
            route = 'login.html'
        
    else:
        route='homepage.html'
        currentUser = request.user.username
        try:
            likeProcess = request.POST["likeProcess"]  #access the array turned int a string from the js file
            unlikeProcess = request.POST["unlikeProcess"] 
            print(likeProcess)          # Just for testing
            print(unlikeProcess)
            likeArray = []
            unlikeArray = []
            word=""
            for char in likeProcess:                               #Quick algorithm to convert it back into a list
                
                if char == "-":
                    likeArray.append(word)
                    word=""
                else:
                    word=word+char
            likeArray.append(word)
            likeArray = list(dict.fromkeys(likeArray))
            print(likeArray)
            
            unword=""
            for char in unlikeProcess:                               #Quick algorithm to convert it back into a list
                
                if char == "-":
                    unlikeArray.append(unword)
                    unword=""
                else:
                    unword=unword+char
            unlikeArray.append(unword)
            unlikeArray = list(dict.fromkeys(unlikeArray))
            print(unlikeArray)
            
            
            for elem in likeArray:
                idholder = request.user
                
                print("here we go-adding")
                try:
                    testHolder = int(elem)
                    canAdd = True
                except:
                    canAdd = False
                
                if canAdd == True:
                    if elem in idholder.liked_posts:
                        print("already post already liked")
                    else:
                        idholder.liked_posts.append(elem)
                        lidholder = Posts.objects.get(id = int(elem))
                        lidholder.likes = lidholder.likes+1
                        print(elem, "has been added")
                        idholder.save()
                        lidholder.save()
            
            
            for elem in unlikeArray:
                idholder = request.user
                print("here we go-deleting")
                try:
                    testHolder = int(elem)
                    canRemove = True
                except:
                    canRemove = False
                    
                if canRemove == True:
                    if elem in idholder.liked_posts:
                        idholder.liked_posts.remove(elem)
                        lidholder = Posts.objects.get(id = int(elem))
                        lidholder.likes = lidholder.likes-1
                        print(elem, "has been Removed")
                        idholder.save()
                        lidholder.save()
                    else:
                        print("Not even liked, cant be removed")
                    
            for elem in idholder.liked_posts:
                print(elem)
            
        except:
            print("nuttin to worry about")
        route = 'homepage.html' 
        
            
        
            
            
    return render(request, route, {'cuser':currentUser, 'lValid': loginValid, 'cid': idholder})

            
        
    

 
@login_required(login_url='login')
def profile(request):
    cusers = request.user
    currentUser = request.user.username
    etimeOfPost = datetime.datetime.now()
    timeOfPost = etimeOfPost.strftime('%c')
    try:
        post = request.POST['post']
        postValid = True
    except:
        post=""
        postValid = False
        
    try:
        image = request.FILES['image']
        
        imageValid = True
        print("image is valid")
    except:
        imageValid = False
        print("image isnt valid")
    
    if post == "":
        postValid = False
        
        
    bannedWords = ['nigger', 'faggot', 'hitler', 'nazi', 'nigga', 'beaner', 'coon', 'ching', 'chong', 'kike']
    for word in post.split():
        if word.lower() in bannedWords:
            post = 'Invalid due to hate speech'
    if postValid == True or imageValid:   
        if imageValid:  
            newPost = Posts.objects.create(post=post, user=cusers, date = timeOfPost, likes = 0, img=image, replies=[])
        else:
            newPost = Posts.objects.create(post=post, user=cusers, date = timeOfPost, likes = 0, replies=[])
            
        newPost.save()
            
            
        replyCheck = request.POST["replyCheck"]
        if replyCheck == "True":
            print("should work")
            repliedTo = request.POST["repliedTo"]
            print(repliedTo)
            postRepliedTo = Posts.objects.get(id=repliedTo)
            postRepliedTo.replies.append(newPost.id)
            postRepliedTo.save()
        
            
    usersPosts = Posts.objects.filter(user=cusers.id).order_by("-date_created")
    route = 'profile.html'
    
    cusers = request.user
    
    likedList = cusers.liked_posts
    likedList = "-".join(likedList)
    allUsers = get_user_model().objects.all()
    
  
    
    
    
    
    
    
    
    return render(request,route, {'cuser':currentUser, 'uposts':usersPosts, "likedList": likedList, 'CurrentUser':cusers, 'allUsers': allUsers  })


@login_required(login_url='login')
def dprofile(request):
    currentUser = request.user.username
    cusers = request.user
    
    delpost = request.POST['delpost']
    
    
    
    
    Posts.objects.get(id=delpost).delete()
        
    usersPosts = Posts.objects.filter(user=cusers.id)
    for users in get_user_model().objects.all():
        likeList = users.liked_posts 
        if str(delpost) in likeList: 
            likeList.remove(delpost)
            
    likedList = cusers.liked_posts
    likedList = "-".join(likedList)
    allUsers = get_user_model().objects.all()
  
    return render(request,'profile.html', {'cuser':currentUser, 'uposts':usersPosts, "likedList": likedList, 'allUsers': allUsers, 'CurrentUser':cusers })


def AllPosts(request):
    currentUser = request.user.username
    cusers = request.user
    allUsers = get_user_model().objects.all()

    likedList = cusers.liked_posts
    likedList = "-".join(likedList)
    print(likedList)
    
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
    
    
    

  
    return render(request,'AllPosts.html', {'allPosts':allPosts, 'cusers': cusers, "likedList": likedList, 'allUsers': allUsers })


def FollowedPosts(request):
    currentUsername = request.user.username
    currentUser = request.user
    allUsers = get_user_model().objects.all()

    likedList = currentUser.liked_posts
    likedList = "-".join(likedList)
    print(likedList)
    followedList = currentUser.followedUsers
    followedPosts = Posts.objects.filter(user__in=followedList).order_by('-date_created')
  
    return render(request,'followedPosts.html', {'followedPosts':followedPosts, 'currentUser': currentUser, "likedList": likedList, 'allUsers': allUsers })

def LikedPosts(request):
    currentUser = request.user.username
    usersPosts = Posts.objects.all()
    cuser = request.user
    likeList = cuser.liked_posts 
    likedPosts = Posts.objects.filter(id__in=likeList)
    allUsers = get_user_model().objects.all()

    
    
        
    
    
    return render(request, 'liked.html', {"likedPosts": likedPosts, "cuser": currentUser, 'allUsers': allUsers })

@login_required(login_url='login')
def editProfile(request):
    cusers = request.user
    
    return render(request, 'editProfile.html', {"CurrentUser":cusers})


@login_required(login_url='login')
def changedProfile(request):
    newBio = request.POST['newBio']
    try:
        newPfp = request.FILES['newPfp']
    except KeyError:
        newPfp = request.user.profilePicture
    cusers = request.user
    cusers.bio = newBio
    cusers.profilePicture = newPfp
    cusers.save()
    currentUser = request.user.username
    usersPosts = Posts.objects.filter(user=cusers.id)
    return render(request, 'profile.html', {'cuser':currentUser, 'uposts':usersPosts, 'CurrentUser':cusers})


@login_required(login_url='login')
def search(request):
    UorP = request.POST['userOrPost']
    searchedFor = request.POST['searchedFor']
    returnDict = {}
    cusers = request.user
    print(UorP)
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
    print(f'other user id is {otherUserId}')
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
    print(f'other user id is {otherUserId}')
    otherUser = get_user_model().objects.get(id=otherUserId)
    otherUsersPosts = Posts.objects.filter(user=otherUser).order_by("-date_created")
    likedList = otherUser.liked_posts
    likedList = "-".join(likedList)
    currentUser = request.user
    followList = currentUser.followedUsers
    print(otherUser.id)
    print(followList)
    if otherUserId in followList:
        currentUser.followedUsers.remove(otherUserId)
        otherUser.followers -= 1
        print("Just unfollowed")
        followed = False
    elif otherUserId not in followList:
        currentUser.followedUsers.append(otherUserId)
        otherUser.followers += 1
        print("Just followed")
        followed = True
    else:
        print("Error")
        
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
    otherUserId = request.POST['otherUser2']
    print(f'other user id is {otherUserId}')
    otherUser = get_user_model().objects.get(id=otherUserId)
    likeList = otherUser.liked_posts 
    likedPosts = Posts.objects.filter(id__in=likeList)
    allUsers = get_user_model().objects.all()
    currentUser = request.user
    
    
    return render(request, 'otherLiked.html', {"likedPosts": likedPosts, "otherUser": otherUser, 'allUsers': allUsers, "currentUser": currentUser })    
    
@login_required(login_url='login')    
def replies(request):
    
    
    
    try:
        likeProcess = request.POST["likeProcess"]  #access the array turned int a string from the js file
        unlikeProcess = request.POST["unlikeProcess"] 
        print(likeProcess)          # Just for testing
        print(unlikeProcess)
        likeArray = []
        unlikeArray = []
        word=""
        for char in likeProcess:                               #Quick algorithm to convert it back into a list
            
            if char == "-":
                likeArray.append(word)
                word=""
            else:
                word=word+char
        likeArray.append(word)
        likeArray = list(dict.fromkeys(likeArray))
        print(likeArray)
        
        unword=""
        for char in unlikeProcess:                               #Quick algorithm to convert it back into a list
            
            if char == "-":
                unlikeArray.append(unword)
                unword=""
            else:
                unword=unword+char
        unlikeArray.append(unword)
        unlikeArray = list(dict.fromkeys(unlikeArray))
        print(unlikeArray)
        
        
        for elem in likeArray:
            idholder = request.user
            
            print("here we go-adding")
            try:
                testHolder = int(elem)
                canAdd = True
            except:
                canAdd = False
            
            if canAdd == True:
                if elem in idholder.liked_posts:
                    print("already post already liked")
                else:
                    idholder.liked_posts.append(elem)
                    lidholder = Posts.objects.get(id = int(elem))
                    lidholder.likes = lidholder.likes+1
                    print(elem, "has been added")
                    idholder.save()
                    lidholder.save()
        
        
        for elem in unlikeArray:
            idholder = request.user
            print("here we go-deleting")
            try:
                testHolder = int(elem)
                canRemove = True
            except:
                canRemove = False
                
            if canRemove == True:
                if elem in idholder.liked_posts:
                    idholder.liked_posts.remove(elem)
                    lidholder = Posts.objects.get(id = int(elem))
                    lidholder.likes = lidholder.likes-1
                    print(elem, "has been Removed")
                    idholder.save()
                    lidholder.save()
                else:
                    print("Not even liked, cant be removed")
                
        for elem in idholder.liked_posts:
            print(elem)
        
    except:
        print("nuttin to worry about")
        
        
    postId = request.POST["selectedPost"]
    
    selectedPost = Posts.objects.get(id=postId)
    currentUser = request.user
    
    repliedList = selectedPost.replies
    repliedPosts = Posts.objects.filter(id__in=repliedList)
    allUsers = get_user_model().objects.all()
    likedList = idholder.liked_posts
    likedList = "-".join(likedList)
    
    print(likedList)
    
    return render(request, "replies.html", {"post": selectedPost, "likedList":likedList, "repliedPosts": repliedPosts, 'allUsers': allUsers})


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
            print("Just unfollowed")
            followed = False
        
    currentUser.save()
    otherUser.save()
        
    otherUserId = request.POST['otherUser']
    print(f'other user id is {otherUserId}')
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
    





    
    


