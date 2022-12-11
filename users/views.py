from .models import User
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login, logout
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serilalizers import UserSerializer, UserRegisterSerializer
from .forms import UserForm

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(["POST"])
def registerUser(request):
    data = request.POST
    
    try:
        dbuser = User.objects.get(Q(username=data["username"]) | Q(email=data["email"]))
        return Response("Username or Email already Exists !", status=400)
    except:
        if data["password"] == data["password2"]:
            user = UserRegisterSerializer(data=data)
            if user.is_valid():
                user.save()
                return Response("Registered !", status=status.HTTP_202_ACCEPTED)
            else:
                return Response("Data Is Not Valid !", status=400)
        else:
                return Response("Password Not Equal !", status=400)


@api_view(["POST"])
def loginUser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        dbuser = User.objects.get(username=username)
    except:
        return Response("User doesn't exist", status=status.HTTP_404_NOT_FOUND)
    
    if not dbuser.check_password(password):
        return Response("Password is not correct", status=status.HTTP_404_NOT_FOUND)
    
    login(request, dbuser)
        
    if dbuser is not None:
        tokens = get_tokens_for_user(dbuser)
        return Response(tokens, status=status.HTTP_202_ACCEPTED)
    else:
        return Response("User not Logged in", status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    form = UserForm(request.POST, request.FILES, instance=user)

    if form.is_valid():
        form.save()
        return Response("User Updated", status=status.HTTP_202_ACCEPTED)
    else:
        return Response("User Not Updated", status=404)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    currentUser = request.user
    user = User.objects.get(id=currentUser.id)
    try:
        user.delete()
        logout(request)
        return Response("User Deleted", status=status.HTTP_202_ACCEPTED)
    except:
        return Response("User Not Deleted", status=404)
    
    
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getUsers(request):
    dbusers = User.objects.all()
    users = UserSerializer(dbusers, many=True)
    return Response(users.data, status=200)

