import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load the model function
def load_model(file_path):
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=1)
    model.load_state_dict(torch.load(file_path))
    model.eval()
    return model

# Function to preprocess user input and predict significance
def predict_significance(date_input, model, tokenizer, max_len, device):
    # Tokenize the input date
    encodings = tokenizer(date_input, truncation=True, padding=True, max_length=max_len, return_tensors="pt")

    # Move inputs to the device (GPU/CPU)
    input_ids = encodings['input_ids'].to(device)
    attention_mask = encodings['attention_mask'].to(device)

    # Set model to evaluation mode and make predictions
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    
    # Get the predicted significance score (regression output)
    predicted_significance = outputs.logits.squeeze().item()
    return predicted_significance

def main():
    # Load the pre-trained model
    model_file_path = "bert_significance_model.pth"  # Path to the saved model
    model = load_model(model_file_path)

    # Set the device (GPU/CPU)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # Load BERT tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # User input
    date_input = input("Enter a date (in format like '15 April' or 'dd mm'): ")

    # Tokenize and predict the significance of the event for this date
    max_len = 16  # Should be the same max_len used during training
    predicted_significance = predict_significance(date_input, model, tokenizer, max_len, device)

    # Output the result
    print(f"The predicted significance for {date_input} is: {predicted_significance:.4f}")

if __name__ == "__main__":
    main()
