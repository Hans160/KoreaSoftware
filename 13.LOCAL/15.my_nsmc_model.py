# 나만의 데이터로 모델 추가 학습하기 (fine-tuning)
# pip install transformers torch datasets
import numpy as np
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments
)

from datasets import Dataset

train_data = {
    "text": ["I love this!", "This is terrible!", "I am happy", "I am sad", "This product is amazing", "Worst experience ever.",
             "Absolutely fantastic", "I hate it."],
    "label": [1, 0, 1, 0, 1, 0, 1, 0]
}
eval_data = {
    "text": ["I feel greate today!", "The service was awful", "I'm super excited about this!", "Not what I expected"],
    "label": [1, 0, 1, 0]
}

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True)

train_ds = Dataset.from_dict(train_data).map(tokenize, batched=True)
eval_ds = Dataset.from_dict(eval_data).map(tokenize, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=2,
    id2label={0: "negative", 1: "positive"},
    label2id={"negative": 0, "positive": 1}
    )

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {"accuracy": float((preds == labels).mean())}

args = TrainingArguments(
    output_dir="./results_nsmc_kr",
    eval_strategy="epoch",  # 최신 라이브러리 가이드 적용
    save_strategy="epoch",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    num_train_epochs=1,
    logging_steps=25
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    compute_metrics=compute_metrics
)

trainer.train()
print("평가 결과:", trainer.evaluate())

save_path="./my_local_model"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
print("내 모델 저장 완료: ", save_path)