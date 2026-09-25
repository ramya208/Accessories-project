# from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ProductSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# def home(request):
#     products = Product.objects.all()

#     return render(request, 'home.html', {
#         'products': products
#     })
# def product_list(request):

#       products = Product.objects.filter(
#         owner=request.user
#       )

#     return render(request, "products.html", {
#         "products": products
#     })
# def product_list(request):

#     products = Product.objects.filter(
#         owner=request.user
#     )

#     return render(request, "products.html", {
#         "products": products
#     })
# def product_list(request):

#     products = Product.objects.all()

#     return render(request, "products.html", {
#         "products": products
#     })
def product_list(request):

    if request.user.is_staff:
        # Admin → அவருடைய products மட்டும்
        products = Product.objects.filter(
            owner=request.user
        )
    else:
        # User → எல்லா admin products
        products = Product.objects.all()

    return render(
        request,
        "products.html",
        {
            "products": products
        }
    )
# def signup_view(request):

#     if request.method == "POST":

#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

#         return redirect("login")

#     return render(request, "signup.html")
# def signup_view(request):

#     if request.method == "POST":

#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # Username already exists
#         if User.objects.filter(username=username).exists():

#             return render(
#                 request,
#                 "signup.html",
#                 {
#                     "error": "This username is already registered!"
#                 }
#             )

#         # Email already exists
#         if User.objects.filter(email=email).exists():

#             return render(
#                 request,
#                 "signup.html",
#                 {
#                     "error": "This email is already registered!"
#                 }
#             )

#         # Create new user
#         User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

#         return redirect("login")

#     return render(request, "signup.html")
# def signup_view(request):

#     if request.method == "POST":

#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")

#         print("Password:", password)
#         print("Confirm Password:", confirm_password)

    
#         if password != confirm_password:

#             return render(
#                 request,
#                 "signup.html",
#                 {
#                     "error": "Password and Confirm Password do not match!"
#                 }
#             )

        
#         if User.objects.filter(username=username).exists():

#             return render(
#                 request,
#                 "signup.html",
#                 {
#                     "error": "This username is already registered!"
#                 }
#             )

#         if User.objects.filter(email=email).exists():

#             return render(
#                 request,
#                 "signup.html",
#                 {
#                     "error": "This email is already registered!"
#                 }
#             )

        
#         User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

#         return redirect("login")

#     return render(request, "signup.html")
def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm_password:
            return render(request, "signup.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {
                "error": "Email already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if role == "admin":
            user.is_staff = True
        else:
            user.is_staff = False

        user.save()

        return redirect("login")

    return render(request, "signup.html")
# def login_view(request):

#     if request.method == "POST":

#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user is not None:

#             login(request, user)

#             return redirect("products")

#         else:

#             return render(
#                 request,
#                 "login.html",
#                 {
#                     "error": "Invalid username or password"
#                 }
#             )

#     return render(request, "login.html")
# def login_view(request):
#     if request.method == "POST":

#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user is not None:
#             login(request, user)

#             return redirect("products")

#         else:
#             return render(
#                 request,
#                 "login.html",
#                 {
#                     "error": "Invalid username or password"
#                 }
#             )

#     return render(request, "login.html")
def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            refresh = RefreshToken.for_user(user)

            return render(
                request,
                "login.html",
                {
                    "success": True,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }
            )

        else:
            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username or password"
                }
            )

    return render(request, "login.html")
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user is not None:
#             login(request, user)

#             refresh = RefreshToken.for_user(user)

#             return render(request, "login.html", {
#                 "access_token": str(refresh.access_token),
#                 "refresh_token": str(refresh),
#                 "success": True,
#             })

#         return render(request, "login.html", {
#             "error": "Invalid username or password"
#         })

#         return render(request, "login.html")
class ProductAPI(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    parser_classes = [MultiPartParser, FormParser]


    # def get(self, request):

    #     # products = Product.objects.all()
    #     # products = Product.objects.filter(owner=request.user)
    #     products = Product.objects.all()

    #     serializer = ProductSerializer(
    #         products,
    #         many=True
    #     )

    #     return Response(serializer.data)
def get(self, request):

    if request.user.is_staff:
        # Admin → அவருடைய products மட்டும்
        products = Product.objects.filter(
            owner=request.user
        )
    else:
        # User → எல்லா products
        products = Product.objects.all()

    serializer = ProductSerializer(
        products,
        many=True
    )

    return Response(serializer.data)

    def post(self, request):

        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can add product"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():
            # serializer.save()
            serializer.save(owner=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class ProductDetailAPI(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    parser_classes = [MultiPartParser, FormParser]

   
    def put(self, request, id):

        try:

            # product = Product.objects.get(id=id)
            product = Product.objects.get(
    id=id,
    owner=request.user
)

        except Product.DoesNotExist:

            return Response(
                {
                    "error": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_staff:

            return Response(
                {
                    "error": "Only admin can edit product"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    def delete(self, request, id):

        try:
            # product = Product.objects.get(id=id)
            product = Product.objects.get(
    id=id,
    owner=request.user
)

        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can delete product"},
                status=status.HTTP_403_FORBIDDEN
            )

        product.delete()

        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_200_OK
        )
# def add_product(request):

#     return render(request, "add_product.html")    
def add_product(request):

    if not request.user.is_staff:
        return redirect("products")

    if request.method == "POST":

        name = request.POST.get("name")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        Product.objects.create(
            name=name,
            price=price,
            image=image,
            owner=request.user
        )

        return redirect("products")

    return render(
        request,
        "add_product.html"
    )
# def edit_product(request, id):

#     try:
#         product = Product.objects.get(id=id)

#     except Product.DoesNotExist:
#         return redirect("products")

#     if not request.user.is_staff:
#         return redirect("products")

#     return render(
#         request,
#         "edit_product.html",
#         {
#             "product": product
#         }
#     )
def edit_product(request, id):

    if not request.user.is_staff:
        return redirect("products")

    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return redirect("products")

    if request.method == "POST":

        product.name = request.POST.get("name")
        product.price = request.POST.get("price")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()

        return redirect("products")

    return render(
        request,
        "edit_product.html",
        {"product": product}
    )
@api_view(['POST'])
@permission_classes([AllowAny])
def token_login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is not None:

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response({
            "token": token.key,
            "username": user.username,
            "role": "admin" if user.is_staff else "user"
        })

    return Response(
        {"error": "Invalid username or password"},
        status=status.HTTP_401_UNAUTHORIZED
    )