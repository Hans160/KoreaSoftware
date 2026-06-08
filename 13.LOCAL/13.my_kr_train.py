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
    "text": ["이 제품 진짜 최고예요!", "정말 최악입니다 돈 아까워요.", 
        "오늘 기분이 너무 좋아요", "너무 슬프고 우울하네요.", 
        "배송도 빠르고 상품도 마음에 듭니다", "다시는 구매하고 싶지 않은 경험이네요.",
        "완전 만족스럽습니다 강력 추천해요", "진짜 너무 별로예요 사지 마세요."],
    "label": [1, 0, 1, 0, 1, 0, 1, 0]
}
eval_data = {
    "text": ["오늘 하루 최고로 행복하네요!", "서비스가 정말 엉망이네요", 
        "완전 기대 이상으로 좋습니다!", "제가 생각했던 거랑 너무 달라요"],
    "label": [1, 0, 1, 0]
}

model_name = "beomi/kcbert-base"
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
    output_dir="./results",
    eval_strategy="epoch",  # 최신 라이브러리 가이드 적용
    save_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=7,
    logging_steps=1
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    compute_metrics=compute_metrics
)

trainer.train()
print("한국어 평가 결과:", trainer.evaluate())

save_path="./my_local_model"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
print("내 모델 저장 완료: ", save_path)