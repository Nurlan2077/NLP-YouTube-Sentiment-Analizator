from transformers import BertModel
import torch.nn as nn

from transformers import BertTokenizer
import torch


class BertClassifier(nn.Module):
    def __init__(self, dropout=0.5):
        super(BertClassifier, self).__init__()

        self.bert = BertModel.from_pretrained("DeepPavlov/rubert-base-cased")
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, 5)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):
        _, pooled_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)

        return final_layer


model = BertClassifier()
model.load_state_dict(torch.load("model_3_epochs", map_location=torch.device('cpu')))
model.eval()

tokenizer = BertTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")


def get_text_class(text):
    tokenized_text = tokenizer(text,
                               padding='max_length',
                               max_length=512,
                               truncation=True,
                               return_tensors="pt")
    mask = tokenized_text['attention_mask']
    input_id = tokenized_text['input_ids'].squeeze(1)

    output = model(input_id, mask)
    # print(output)
    return output.argmax(dim=1).item()