from PIL import Image

from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File
from ..predictor import predictors, predictors_classes


router = APIRouter()

@router.post("/predict/{model_name}")
async def predict(model_name: str, file: UploadFile = File(...)):

    if model_name not in predictors:
        raise HTTPException(status_code=404, detail="Model not found")

    image = Image.open(file.file)

    result = predictors[model_name].predict(image)

    return result
