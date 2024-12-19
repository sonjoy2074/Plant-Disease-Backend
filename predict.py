# from flask import Blueprint, request, jsonify, session
# import torch
# from PIL import Image
# import base64
# from io import BytesIO
# from config import Config
# from torchvision import transforms as T
# import timm
# import torch.nn as nn

# # Define class names
# classes = ['Bacterialblight', 'Blast', 'Brownspot', 'Tungro']

# # Load the model
# HUB_URL = "SharanSMenon/swin-transformer-hub:main"
# MODEL_NAME = "swin_tiny_patch4_window7_224"

# model = torch.hub.load(HUB_URL, MODEL_NAME, pretrained=False)
# n_inputs = model.head.in_features
# model.head = nn.Sequential(
#     nn.Linear(n_inputs, 512),
#     nn.ReLU(),
#     nn.Dropout(0.3),
#     nn.Linear(512, len(classes))
# )

# # Load model weights
# model.load_state_dict(torch.load('model/rice_swin_model.pth', map_location=torch.device('cpu')))
# model.eval()
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = model.to(device)

# # Define the prediction blueprint
# predict_bp = Blueprint('predict', __name__)

# # Preprocessing function
# def preprocess_image(image):
#     transform = T.Compose([
#         T.Resize(256),
#         T.CenterCrop(224),
#         T.ToTensor(),
#         T.Normalize(timm.data.IMAGENET_DEFAULT_MEAN, timm.data.IMAGENET_DEFAULT_STD),
#     ])
#     image = transform(image).unsqueeze(0)  # Add batch dimension
#     return image

# @predict_bp.route('/predict', methods=['POST'])
# def predict():
#     # Check for 'Authorization' header
#     auth_header = request.headers.get('Authorization')
    
#     if auth_header:
#         # Extract the token part (assume format: "Bearer <user_id>")
#         try:
#             token = auth_header.split(" ")[1]  # Split 'Bearer <token>'
#         except IndexError:
#             return jsonify({'error': 'Invalid Authorization header format'}), 401
#     else:
#         return jsonify({'error': 'Authorization header missing'}), 401

#     # If you want to verify the token or user_id from a database or another mechanism, do it here.
#     # For simplicity, let's assume token is valid for now.
#     # You can add validation logic here (optional).

#     # Check if the request contains base64 image data
#     data = request.json
#     if 'image' not in data:
#         return jsonify({'error': 'No image provided'}), 400

#     try:
#         # Decode the base64 image
#         image_data = base64.b64decode(data['image'])
#         image = Image.open(BytesIO(image_data)).convert('RGB')

#         # Preprocess and predict
#         input_image = preprocess_image(image).to(device)
#         with torch.no_grad():
#             output = model(input_image)
#             _, predicted_class = torch.max(output, 1)

#         predicted_label = classes[predicted_class.item()]
#         return jsonify({'prediction': predicted_label})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



from flask import Blueprint, request, jsonify, session
import torch
from PIL import Image
import base64
from io import BytesIO
from config import Config
from torchvision import transforms as T
import timm
import torch.nn as nn
from datetime import datetime
from flask_mysqldb import MySQL
# Define class names
classes = ['Bacterialblight', 'Blast', 'Brownspot', 'Tungro']
mysql = MySQL()
# Load the model
HUB_URL = "SharanSMenon/swin-transformer-hub:main"
MODEL_NAME = "swin_tiny_patch4_window7_224"

model = torch.hub.load(HUB_URL, MODEL_NAME, pretrained=False)
n_inputs = model.head.in_features
model.head = nn.Sequential(
    nn.Linear(n_inputs, 512),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(512, len(classes))
)

# Load model weights
model.load_state_dict(torch.load('model/rice_swin_model.pth', map_location=torch.device('cpu')))
model.eval()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Define the prediction blueprint
predict_bp = Blueprint('predict', __name__)

# Preprocessing function
def preprocess_image(image):
    transform = T.Compose([
        T.Resize(256),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(timm.data.IMAGENET_DEFAULT_MEAN, timm.data.IMAGENET_DEFAULT_STD),
    ])
    image = transform(image).unsqueeze(0)  # Add batch dimension
    return image

@predict_bp.route('/predict', methods=['POST'])
def predict():
    # Check for 'Authorization' header
    auth_header = request.headers.get('Authorization')
    
    if auth_header:
        # Extract the token part (assume format: "Bearer <user_id>")
        try:
            token = auth_header.split(" ")[1]  # Split 'Bearer <token>'
        except IndexError:
            return jsonify({'error': 'Invalid Authorization header format'}), 401
    else:
        return jsonify({'error': 'Authorization header missing'}), 401

    # If you want to verify the token or user_id from a database or another mechanism, do it here.
    # For simplicity, let's assume token is valid for now.
    user_id = token  # This assumes the token contains the user_id

    # Check if the request contains base64 image data
    data = request.json
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    try:
        # Decode the base64 image
        image_data = base64.b64decode(data['image'])
        image = Image.open(BytesIO(image_data)).convert('RGB')

        # Preprocess and predict
        input_image = preprocess_image(image).to(device)
        with torch.no_grad():
            output = model(input_image)
            _, predicted_class = torch.max(output, 1)

        predicted_label = classes[predicted_class.item()]

        # Insert into the history table after a successful prediction
        cursor = mysql.connection.cursor()
        timestamp = datetime.now()

        try:
            cursor.execute(
                "INSERT INTO history (user_id, prediction, image, timestamp) VALUES (%s, %s, %s, %s)", 
                (user_id, predicted_label, data['image'], timestamp)
            )
            mysql.connection.commit()
            cursor.close()

        except Exception as e:
            mysql.connection.rollback()
            cursor.close()
            return jsonify({'error': 'Error saving history: ' + str(e)}), 500

        return jsonify({'prediction': predicted_label}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
