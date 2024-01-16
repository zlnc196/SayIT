from django.shortcuts import render
import smtplib
from .models import Users, Posts
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
# Create your views here.

global currentUser
global loginValid
loginValid = False

def intro(request):
    return render(request, 'intro.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')


def confirm(request):
    email = request.POST['Email']
    username = request.POST['username']
    password = request.POST['password']
    Users.objects.create(email=email, username=username, password=password, liked_posts=[] )
    
    
    valid = False
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for char in password:
        if char in nums and len(password) >= 8:
            valid = True
            regDirection = 'login.html'
        else:
            regDirection = 'register.html'
        
    
    
    
    
    
    
    
    return render(request, regDirection, {'Valid': valid})


def homepage(request):
    global currentUser
    global loginValid
    UserData = Users.objects.all()
    idholder = 0
    print(loginValid)
    if loginValid != True:
        try:
            username = request.POST['lusername']
            password = request.POST['lpassword']
        except:
            route = 'login.html'
            username = '0'
            password = '0'

        for objs in UserData:
            if objs.username == username and objs.password == password:
                loginValid = True
                currentUser = objs.username
        if loginValid == False:
            route = 'login.html'
            currentUser = 0
        else:
            route = 'homepage.html'
            print(currentUser)
    else:
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
                idholder = Users.objects.filter(username=currentUser).first()
                
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
                idholder = Users.objects.filter(username=currentUser).first()    
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



def profile(request):
    print(currentUser)
    etimeOfPost = datetime.datetime.now()
    timeOfPost = etimeOfPost.strftime('%c')
    try:
        post = request.POST['post']
        postValid = True
    except:
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
    if postValid == True:   
        if imageValid:  
            Posts.objects.create(post=post, user=currentUser, date = timeOfPost, likes = 0, img=image)
        else:
            Posts.objects.create(post=post, user=currentUser, date = timeOfPost, likes = 0)
            
    usersPosts = Posts.objects.filter(user=currentUser).order_by("-date_created")
    route = 'profile.html'
    
    cusers = Users.objects.filter(username=currentUser).first()
    
    likedList = cusers.liked_posts
    likedList = "-".join(likedList)
  
    
    
    
    
    
    
    
    return render(request,route, {'cuser':currentUser, 'uposts':usersPosts, "likedList": likedList })



def dprofile(request):
    global currentUser
    
    delpost = request.POST['delpost']
    
    
    
    
    Posts.objects.filter(id=delpost).delete()
        
    usersPosts = Posts.objects.filter(user=currentUser)
    for users in Users.objects.all():
        likeList = users.liked_posts 
        if str(delpost) in likeList: 
            likeList.remove(delpost)
  
    return render(request,'profile.html', {'cuser':currentUser, 'uposts':usersPosts})


def AllPosts(request):
    global currentUser
    cusers = Users.objects.filter(username=currentUser).first()
    
    likedList = cusers.liked_posts
    likedList = "-".join(likedList)
    print(likedList)
    
    
    allPosts = Posts.objects.all().order_by('-date_created')
  
    return render(request,'AllPosts.html', {'allPosts':allPosts, 'cusers': cusers, "likedList": likedList })


def LikedPosts(request):
    global currentUser
    usersPosts = Posts.objects.all()
    user = Users.objects.filter(username = currentUser).first()
    likeList = user.liked_posts 
    likedPosts = Posts.objects.filter(id__in=likeList)
    
        
    
    
    return render(request, 'liked.html', {"likedPosts": likedPosts, "cuser": currentUser})
    
    


