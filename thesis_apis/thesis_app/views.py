from unicodedata import name
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from .models import Patient, Scan
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django import forms
from rest_framework import generics
from .serializers import PatientSerializer, ScanSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from _auth.models import RadiologistProfile
from _auth.serializers import RadiologistProfileSerializer
import os
import shutil


# class ProfileList(generics.ListCreateAPIView):
#     queryset = Radiologist.objects.all()
#     serializer_class = RadiologistSerializer


class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = RadiologistProfile.objects.all()
    serializer_class = RadiologistProfileSerializer


class ProfilePatients(APIView):
    def get(self, request):
        radiologist = RadiologistProfile.objects.get(user=self.request.user)
        print("-----------", radiologist)

        patient_obj = Patient.objects.filter(radiologist=radiologist)
        if patient_obj:
            serializer = PatientSerializer(patient_obj, many=True)
            # if serializer.is_valid():
            #     serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response("error", status.HTTP_400_BAD_REQUEST)


class PatientScans(APIView):
    def get(self, request, pk):

        scan_obj = Scan.objects.filter(patient=pk)
        if scan_obj:
            return Response(ScanSerializer(scan_obj, many=True).data, status.HTTP_200_OK)
        return Response(ScanSerializer(scan_obj).errors, status.HTTP_400_BAD_REQUEST)


class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class ScanList(generics.ListCreateAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer


class ScanDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer


def process(image):

    # image_id = str(image).split('/')[-1].split('.')[0]
    # print(image)
    # print(f"/home/g03-s-2022/Finaaaaaallllll/Thesis_Final/Thesis_Final/mediafiles/input/{image}")


    cmd = f"python /home/g03-s-2022/HAM/newScan.py -i /home/g03-s-2022/Finaaaaaallllll/Thesis_Final/Thesis_Final/mediafiles/images/input/{image} -w /home/g03-s-2022/HAM/checkpoints/resnet50/resnet50_best_auc.pth -cfg /home/g03-s-2022/HAM/configs/config.yaml"
    os.system(cmd)

    with open("/home/g03-s-2022/Finaaaaaallllll/Thesis_Final/Thesis_Final/mediafiles/result.txt", "r") as f:
        result = json.load(f)

    # out = "/home/g03-s-2022/HAM/" + result["Output"]

    # /home/g03-s-2022/Thesis_Backend/thesis_api/outputs/visual/test-yaml

    # shutil.copy(out, "/home/g03-s-2022/Finaaaaaallllll/Thesis_Final/Thesis_Final/mediafiles/images/output/")

    return result["Output"], str(result["Pathology"])


class ScanViewSet(APIView):
    def get(self, request):
        scans = Scan.objects.all()
        serializer = ScanSerializer(scans, many=True)
        return Response(serializer.data)

    # def post(self, request):

    #     data = request.data

    #     serializer = ScanSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         data["output_image"],  data["labels"] = process(data["input_image"])
    #         serializer.save()
    #         serializer.data["input_image"]
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        
        patient = Patient.objects.get(id=request.data["patient"])
        scan = Scan.objects.create(input_image = request.data["input_image"],patient=patient)

        print("-------------------------------------------------------------------")
        print(request.data)
        print("-------------------------------------------------------------------")
        
        input_image = scan.input_image
        input_image = str(input_image).split('/')[-1]
        scan.output_image,  scan.labels = process(input_image)
        print("Scan output before save: ", scan.output_image)
        scan.save()
        save_path = 'http://127.0.0.1:8000/media/images/output/'+scan.output_image.split('/')[-1]
        return JsonResponse({
            "id": scan.id,
            "input_image": str(scan.input_image),
            "output_image": save_path,
            "labels": scan.labels,
            "patient": scan.patient.id

        }, safe=False, status=status.HTTP_201_CREATED)

        # serializer1 = ScanSerializer(data=scan)
        #if scan.is_valid():
        #    scan.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(json.dumps(scan), status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     data = request.data
    #     data1 = data
    #     serializer = ScanSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()

    #     result, pathology = process(serializer.data["input_image"])
    #     data1["output_image"] = result
    #     data1["labels"] = pathology
    #     serializer = ScanSerializer(data=data1)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     data = request.data
    #     # data["output_image"], data["labels"] = process(data["input_image"])
    #     data["output_image"] = '/home/g03-s-2022/Finaaaaaallllll/Thesis_Final/Thesis_Final/mediafiles/images/output/'+str(data["input_image"])[:-4]+'_anomaly_img.png'
    #     serializer = ScanSerializer(data = data)
    #     if serializer.is_valid():
    #         serializer.save()

    #         print(process(str(data["input_image"])))

    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     data = request.data
    #     # data["output_image"], data["labels"] = process(data["input_image"])
    #     data["output_image"] = '/home/g03-s-2022/Finaaaaaallllll/Thesis_Final/Thesis_Final/mediafiles/images/output/'+str(data["input_image"])[:-4]+'_anomaly_img.png'
    #     serializer = ScanSerializer(data = data)
    #     if serializer.is_valid():
    #         serializer.save()

    #         print(process(str(data["input_image"])))

    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
