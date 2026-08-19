import numpy as np
import pandas as pd
from PIL import Image
import torch
import torchvision

def train_model(model, train_loader, val_loader, criterion, optimizer, device, num_epochs):
    loss_acc_data = pd.DataFrame()

    for epoch in range(num_epochs):
        epoch_train_loss = 0.0
        epoch_validation_loss = 0.0
        correct = 0
        total = 0
        
        model.train()
        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            
            outputs = model(inputs)
        
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            epoch_train_loss += loss.item()

            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_accuracy = (correct / total)

        correct = 0
        total = 0
        model.eval()

        with torch.no_grad():
            for inputs, labels in val_loader:
                
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                
                outputs = model(inputs)
                loss = criterion(outputs, labels)
            
                epoch_validation_loss += loss.item()

                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_accuracy = (correct / total)
        epoch_train_loss /= len(train_loader)
        epoch_validation_loss /= len(val_loader)
    
        print(f"Epoch {epoch+1}, Train loss: {epoch_train_loss:.4f}, Validation loss: {epoch_validation_loss:.4f},  \
        Train accuracy: {train_accuracy:.4f}, Validation accuracy: {val_accuracy:.4f}")
       
    
        temp_loss_acc_data = pd.DataFrame({'Epoch': [epoch], 'Train Loss': [epoch_train_loss], 'Validation Loss': [epoch_validation_loss],\
                                           "Train accuracy": [train_accuracy], "Validation accuracy": [val_accuracy]})
        loss_acc_data = pd.concat([loss_acc_data, temp_loss_acc_data])
    return loss_acc_data


def evaluate_accuracy(model, dataloader, device):   
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            preds = torch.argmax(outputs, dim=1)

            all_preds.append(preds.cpu())
            all_labels.append(labels.cpu())

    all_preds = torch.cat(all_preds).numpy()
    all_labels = torch.cat(all_labels).numpy()
    print(f"accuracy_score: {accuracy_score(all_labels, all_preds)}")
    print(f"precision_score {precision_score(all_labels, all_preds, average= "macro")}")
    print(f"recall_score: {recall_score(all_labels, all_preds, average= "macro")}")


def get_prediction(model, img_path, transform, device): 
    img = Image.open("img_path").convert("RGB")
    image_tensor = transform(img)
    image_tensor = image_tensor.unsqueeze(0)
    image_tensor = image_tensor.to(device)
    
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted_class = torch.max(probabilities, 1)
    return confidence.item(), predicted_class.item()