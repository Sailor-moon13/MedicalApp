from sklearn.preprocessing import LabelEncoder
from PIL import Image
import torch
import torchvision
from torchvision.transforms import transforms
from torch.utils.data import Dataset
from torch.utils.data import DataLoader


def encode_labels(dataframe):

    label_encoder = LabelEncoder()
    
    label_encoder.fit(dataframe["label"])
    dataframe["label"] = label_encoder.transform(dataframe["label"])
    return dataframe


def split_data(dataframe, train_frac, includeTest):
    train_data = dataframe.sample(frac= train_frac)
    val_data = dataframe.drop(train_data.index)
    if includeTest == True:
        test_data = val_data.sample(frac= 0.5)
        val_data = val_data.drop(test_data.index)

    print(f"original dataframe shape: {dataframe.shape}")
    print(f"training dataframe shape: {train_data.shape}")
    print(f"validation dataframe shape: {val_data.shape}")
    if includeTest == True: print(f"test_df shape: {test_data.shape}")

    if includeTest == True: return train_data, val_data, test_data
    else: return train_data, val_data

    
def get_transforms():
    train_transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.RandomResizedCrop(128, scale=(0.8, 1.0)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5]),
        transforms.ConvertImageDtype(torch.float)
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((128,128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5]),
        transforms.ConvertImageDtype(torch.float)
    ])

    return train_transform, val_transform

    
class CustomDataset(Dataset):
    
    def __init__(self, dataframe, transform= None):
        self.dataframe = dataframe
        self.transform = transform
        self.labels = torch.tensor(dataframe["label"].values, dtype=torch.long)

    def __len__(self):
        return self.dataframe.shape[0]

    def __getitem__(self, idx):

        img_path = self.dataframe.iloc[idx, 0]
        image = Image.open(img_path).convert("RGB")
        if self.transform: 
            image = self.transform(image)
        label = self.labels[idx]
        return image, label


def create_dataloader(dataframe, includeTest, batchsize= 64):
    
    dataframe = encode_labels(dataframe)

    train_transform, val_transform = get_transforms()
    
    if includeTest == True: 
        
        train_data, val_data, test_data = split_data(dataframe, train_frac= 0.8, includeTest= True)
        
        train_dataset = CustomDataset(train_data, train_transform)
        val_dataset = CustomDataset(val_data, val_transform)
        test_dataset = CustomDataset(test_data, val_transform)

        train_loader = DataLoader(train_dataset, batch_size= batchsize, shuffle= True)
        val_loader = DataLoader(val_dataset, batch_size= batchsize, shuffle= False)
        test_loader = DataLoader(test_dataset, batch_size= batchsize, shuffle= False)

        return train_loader, val_loader, test_loader

    else: 
        
        train_data, val_data = split_data(dataframe, train_frac= 0.8, includeTest= False)
        
        train_dataset = CustomDataset(train_data, train_transform)
        val_dataset = CustomDataset(val_data, val_transform)
    
        train_loader = DataLoader(train_dataset, batch_size= batchsize, shuffle= True)
        val_loader = DataLoader(val_dataset, batch_size= batchsize, shuffle= False)

        return train_loader, val_loader