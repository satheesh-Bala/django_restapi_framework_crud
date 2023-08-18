from rest_framework import serializers
from .models import Person,Colors
from django.contrib.auth.models import User


#custom serializers
class LoginSerializers(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.IntegerField()

#default model serializer
class ColorsSerial(serializers.ModelSerializer):
    class Meta:
        model = Colors
        #fields = '__all__'
        fields = ['color_name']

class PersonsSerial(serializers.ModelSerializer):
    #color_id=ColorsSerial()# it will give you the color_name using color id in Person model
    #color_info=serializers.SerializerMethodField()# using predefined get prfix method we can create customs method
    class Meta:
        model=Person
        #fields=['name','age']  -> it only serialize the given two fields in model
        fields='__all__'
        #depth=1
        #exclude=['name']     -> this exclude the name field only

   # def get_color_info(self,obj):
        #color_obj=Colors.objects.get(color_name=obj.color_id)
        #print(obj.color_id.id) it gives the color id value
        #print(obj.color_id) it gives the color_name of the forign key 
        #return color_obj.color_name
        #return {"color_name":str(obj.color_id),"color_Hex":"#000"}

    # this method is called when the seializer object is created
    def validate(self,data):
        print('Hellow this is serializer checking')
        if all(65<=ord(i)<=90 or 97<=ord(i)<=122  for i in data["name"]):
            pass
        else:
            raise serializers.ValidationError("Name Should only contains characters")
    
        if data['age']>=18:
            pass
        else:
            raise serializers.ValidationError("Age Should greater Than 18")
        print(data)
        return (data)

# serializeng and validating and also creating the user
class RegisterSerial(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('User name is Taken')
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('email is already registered')
        
        return data
    
    def create(self, validated_data):
        user=User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    

class LoginUserSerial(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()