import torch
from PIL import Image
from torchvision.transforms import transforms
from torchvision.models import resnet18
from pathlib import Path

class Predictor:

    def __init__(self, model_path, model_name):

        self.model_name = model_name

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = resnet18(weights= None)

        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 2)

        self.model.load_state_dict(torch.load(model_path, map_location= self.device))

        self.model.to(self.device)

        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((128,128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5])
        ])
    
    def predict(self, image: Image.Image): 
        
        image = image.convert("RGB")

        image_tensor = self.transform(image)

        image_tensor = image_tensor.unsqueeze(0)

        image_tensor = image_tensor.to(self.device)

        with torch.no_grad():

            outputs = self.model(image_tensor)

            probabilities = torch.softmax(outputs, dim=1)

            confidence, predicted_class = torch.max(probabilities, 1)
        
        return {
            "class": predictors_classes[self.model_name][predicted_class.item()],
            "confidence": confidence.item()
        }

MODEL_DIR = Path("models")

predictors = {
    "bone_fracture": Predictor(MODEL_DIR / "Bone_Fracture.pt", "bone_fracture"),
    "brain_tumor": Predictor(MODEL_DIR / "Brain_Tumor.pt", "brain_tumor"),
    "pneumonia": Predictor(MODEL_DIR / "Pneumonia.pt", "pneumonia"),
    "alzheimer": Predictor(MODEL_DIR / "Alzheimer.pt", "alzheimer")

}

predictors_classes = {
    "bone_fracture": ["fractured", "normal"],
    "brain_tumor": ["normal", "tumor"],
    "pneumonia": ["normal", "pneumonia"],
    "alzheimer": ["alzheimer", "normal"]
}