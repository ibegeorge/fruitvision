## Image Storage Strategy

FruitVision will initially use local image storage.

Uploaded images will be stored inside an uploads directory.

The database will store only the image path rather than the binary image data.

This keeps database responsibilities separate from file storage responsibilities and allows future migration to cloud storage solutions such as AWS S3.

# Prediction System

## Overview

The FruitVision prediction system allows authenticated users to upload fruit images, receive classification results, and store prediction history.

---

## Architecture

The prediction workflow follows:

API Layer

↓

Prediction Service

↓

Storage Service + AI Inference

↓

Prediction Repository

↓

Database

---

## Implemented Components

### Database

Created predictions table:

- id
- user_id
- image_path
- predicted_class
- confidence
- created_at


### Storage

Implemented local image storage.

Images are stored inside:

uploads/

The database stores only the image path.

---

### AI Layer

Created inference abstraction:

app/ai/inference.py

Currently uses a placeholder prediction.

Future implementation will replace this with a PyTorch model.

---

### API Endpoints

## Create Prediction

POST /predictions

Purpose:

Upload an image and generate a prediction.


## Prediction History

GET /predictions

Purpose:

Retrieve predictions belonging to the authenticated user.


---

## Current Limitation

The AI model is currently mocked.

All predictions return placeholder values.

Future work:

- dataset preparation
- model training
- model evaluation
- PyTorch inference integration