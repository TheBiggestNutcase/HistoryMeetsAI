import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import AdamW
import torch.nn.functional as F
from tqdm import tqdm

# Load and prepare data
def load_data(file_path):
    df = pd.read_json(file_path)
    return df

# Function to prepare data with proper tokenization
def prepare_data(df, tokenizer, max_len):
    X = df['date'].tolist()  # Dates as input strings
    y = df['significance_factor'].tolist()  # Significance as labels

    # Tokenize input text (dates) using BERT tokenizer
    encodings = tokenizer(X, truncation=True, padding=True, max_length=max_len, return_tensors="pt")

    # Convert significance labels to tensor
    labels = torch.tensor(y, dtype=torch.float32)  # Ensure labels are float for regression

    return encodings, labels

# Prepare DataLoader
def create_dataloader(input_ids, attention_mask, labels, batch_size):
    dataset = TensorDataset(input_ids, attention_mask, labels)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return dataloader

# Training Function
def train(model, dataloader, optimizer, device):
    model.train()
    for batch in tqdm(dataloader):
        input_ids, attention_mask, labels = [b.to(device) for b in batch]

        # Clear previous gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(input_ids, attention_mask=attention_mask)
        loss = F.mse_loss(outputs.logits.squeeze(), labels)  # Use MSE loss for regression

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

# Evaluation Function
def evaluate(model, dataloader, device):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in dataloader:
            input_ids, attention_mask, labels = [b.to(device) for b in batch]

            outputs = model(input_ids, attention_mask=attention_mask)
            loss = F.mse_loss(outputs.logits.squeeze(), labels)
            total_loss += loss.item()
    return total_loss / len(dataloader)

# Save model function
def save_model(model, file_path):
    torch.save(model.state_dict(), file_path)
    print(f"Model saved to {file_path}")

# Main Function
def main():
    # Load BERT tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Load data and prepare it
    file_path = 'PageViews/pageviews.json'  # Path to the cleaned data JSON file
    df = load_data(file_path)

    max_len = 16  # Adjust based on your data
    encodings, labels = prepare_data(df, tokenizer, max_len)

    # Convert PyTorch tensors to NumPy arrays
    input_ids_np = encodings['input_ids'].numpy()
    attention_mask_np = encodings['attention_mask'].numpy()
    labels_np = labels.numpy()

    # Split data into training and testing sets
    train_input_ids, test_input_ids, train_attention_mask, test_attention_mask, train_labels, test_labels = train_test_split(
        input_ids_np, attention_mask_np, labels_np, test_size=0.2
    )

    # Convert NumPy arrays back to PyTorch tensors
    train_input_ids = torch.tensor(train_input_ids)
    test_input_ids = torch.tensor(test_input_ids)
    train_attention_mask = torch.tensor(train_attention_mask)
    test_attention_mask = torch.tensor(test_attention_mask)
    train_labels = torch.tensor(train_labels, dtype=torch.float32)
    test_labels = torch.tensor(test_labels, dtype=torch.float32)

    # Create DataLoaders for training and testing
    train_dataloader = create_dataloader(train_input_ids, train_attention_mask, train_labels, batch_size=32)
    test_dataloader = create_dataloader(test_input_ids, test_attention_mask, test_labels, batch_size=32)

    # Initialize BERT model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=1)
    model.to(device)

    # Prepare optimizer
    optimizer = AdamW(model.parameters(), lr=1e-6)

    # Training Loop
    num_epochs = 3
    for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")
        train(model, train_dataloader, optimizer, device)
        eval_loss = evaluate(model, test_dataloader, device)
        print(f"Validation Loss: {eval_loss:.4f}")

    # Save the model after training
    save_model(model, "bert_significance_model.pth")

if __name__ == "__main__":
    main()