from .models import Patient, Scan
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



        
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        
class ScanSerializer(serializers.ModelSerializer):
    input_image = serializers.ImageField()
    # output_image = serializers.ImageField()
    class Meta:
        model = Scan
        fields = '__all__'

        
  