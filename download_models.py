from pathlib import Path

from huggingface_hub import hf_hub_download


REPO_ID = "EraldoCoil/medical-ai-models"

MODEL_DIR = Path("models")

MODELS = [
    "Bone_Fracture.pt",
    "Brain_Tumor.pt",
    "Pneumonia.pt",
    "Alzheimer.pt",
]


def download_models():
    MODEL_DIR.mkdir(exist_ok=True)

    for model_name in MODELS:

        model_path = MODEL_DIR / model_name

        if model_path.exists():
            print(f"{model_name} already exists. Skipping.")
            continue

        print(f"Downloading {model_name}...")

        hf_hub_download(
            repo_id=REPO_ID,
            filename=model_name,
            local_dir=MODEL_DIR,
        )

        print(f"{model_name} downloaded.")


if __name__ == "__main__":
    download_models()