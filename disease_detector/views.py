from django.shortcuts import render
from django.http import JsonResponse
import json
from .crop_analyser import fun_call  # Import the function
from .image_classifier_code import predict_disease
from django.views.decorators.csrf import csrf_exempt
import os


def home(request):
    return render(request, 'index.html')

def home1(request):
    return render(request, 'index2.html')



@csrf_exempt  # Disable CSRF for testing (Not recommended for production)
def predict_crop_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extract input values
            N = float(data["N"])
            P = float(data["P"])
            K = float(data["K"])
            temperature = float(data["temperature"])
            humidity = float(data["humidity"])
            ph = float(data["ph"])
            rainfall = float(data["rainfall"])

            # Call the crop prediction function
            predicted_crop = fun_call(N, P, K, temperature, humidity, ph, rainfall)

            print("Predicted Crop:", predicted_crop) 
            return JsonResponse({"result": predicted_crop})  # Ensure output is sent correctly

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)





@csrf_exempt
def image_predict_crop_view(request):
    if request.method == "POST" and request.FILES.get("image"):
        try:
            image = request.FILES["image"]  

            # Save the uploaded image temporarily
            image_path = f"temp_images/{image.name}"
            os.makedirs("temp_images", exist_ok=True)  

            with open(image_path, "wb") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            # Predict the disease
            crop_name, predicted_disease = predict_disease(image_path)

            # Delete the image after prediction
            os.remove(image_path)

            return JsonResponse({"crop": crop_name, "disease": predicted_disease})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method or missing image"}, status=405)
