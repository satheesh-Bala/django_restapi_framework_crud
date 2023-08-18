from rest_framework.decorators import api_view,APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Person
from .serializers import PersonsSerial,LoginSerializers,RegisterSerial,LoginUserSerial
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


#using APIView decorators. it can be automtically call the functions based on the request
class PersonAPIview(APIView):
    #adding this two classes django automatically give the permission for only authenticated users
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get(self,request):
        print(request.user)
        personsData=Person.objects.filter(color_id__isnull=False)
        serialDataGet=PersonsSerial(personsData,many=True)
        return Response(serialDataGet.data)
    def post(self,request):
        return Response(request.method)
    def put(self,request):
        return Response(request.method)
    def patch(self,request):
        return Response(request.method)
    def delete(self,request):
        return Response(request.method)

# Function to get and post the person details in the data base using api
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def PersonManuplate(request):
    if request.method=='GET':
        personsData=Person.objects.filter(color_id__isnull=False)
        serialDataGet=PersonsSerial(personsData,many=True)
        return Response(serialDataGet.data)
    
    elif request.method=='POST':
        dataPost=request.data
        serialDataPost=PersonsSerial(data=dataPost)
        if serialDataPost.is_valid():
            serialDataPost.save()
            return Response(serialDataPost.data)
        else:
            return Response(serialDataPost.errors)

    elif request.method=='PUT':
        dataPost=request.data
        objs=Person.objects.get(id=(dataPost["id"]))
        serialData=PersonsSerial(objs,data=dataPost)
        if serialData.is_valid():
            serialData.save()
            return Response(serialData.data)
        else:
            return Response(serialData.errors)

    elif request.method=='PATCH':
        dataPost=request.data
        objs=Person.objects.get(id=(dataPost["id"]))
        serialData=PersonsSerial(objs,data=dataPost,partial=True)
        if serialData.is_valid():
            serialData.save()
            return Response(serialData.data)
        else:
            return Response(serialData.errors)
    
    elif request.method=='DELETE':
        data=request.data
        objs=Person.objects.get(id=(data['id']))
        #Person.delete(objs)
        objs.delete()
        return Response("Person Deleted")


# api_view used to rute the function by checking
@api_view(['GET','POST'])
def index(request):

    if request.method=='GET':
        print(request.GET.get('name'))
        cources={
            'cource':'python',
            'learns':['api','flask','fastapi'],
            'teacher':'Scalar'
        }
        return Response(cources)
    elif request.method=='POST':
        cources=request.data
        return Response(cources)



# using custom serializer to serialize data  
@api_view(['POST'])
def Login(request):
    if request.method=='POST':
        data=request.data
        dataSerial=LoginSerializers(data=data)
        if dataSerial.is_valid():
            return Response(dataSerial.data)
        else:
            return Response(dataSerial.errors)
        
# using ModelViewsets is easy to make curd operations for table or model
class personViewSets(viewsets.ModelViewSet):
    serializer_class=PersonsSerial
    queryset=Person.objects.all()
    #http_method_names=['get','post','patch','delete']

    #it is used to take the letter starting with query
    ''' def list(self,request):
        if request.GET.get('search'):
            data=request.GET.get('search')
            queryData=self.queryset.filter(name__startswith=data)
            if queryData:
                serialize=PersonsSerial(queryData,many=True)
                return Response(serialize.data)
            else:
                return Response(request.data)'''


#using inbulit authentication validating and creating the user
class RegisterUser(APIView):
    def post(self,request):
        data=request.data
        serializedData=RegisterSerial(data=data)
        if serializedData.is_valid():
            serializedData.save()
            return Response({"status":"saved","data":serializedData.data})
        else:
            return Response(serializedData.errors)


class LoginUser(APIView):

    def post(self,request):
        data=request.data
        serialize=LoginUserSerial(data=data)

        if serialize.is_valid():
            try:
                user=authenticate(username=serialize.data['username'],password=serialize.data['password'])
                if user:
                    token,_=Token.objects.get_or_create(user=user)
                    return Response({"status":"saved","data":serialize.data,"token":str(token)})
                else:
                    return Response({"error":"invalid credintials"})
            except Exception as error:
                return Response({"error":str(error)})
        else:
            return Response(serialize.errors)