import imaplib
import email
from email.header import decode_header

from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = "imap.naver.com"
SMTP_PORT = 993

NAVER_ID = os.getenv("NAVER_MAIL_ID")
NAVER_PASSWORD = os.getenv("NAVER_MAIL_APP_SECRET")
NAVER_EMAIL = f'{NAVER_ID}@naver.com'

mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
mail.login(NAVER_ID, NAVER_PASSWORD)

mail.select("INBOX")  # 나의 메일함 이름
status, messages = mail.search(None, "ALL")

mail_ids = messages[0].split()
latest_email_id = mail_ids[-1]

print("나의 메일들: ", mail_ids)
print("가장 최신 메일: ", latest_email_id)

status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
print(status)
print(msg_data)

#메일 데이터 본문 파싱
for response_part in msg_data:
    if isinstance(response_part, tuple):
        # 메일 데이터 디코딩
        msg = email.message_from_bytes(response_part[1])

        from_ = msg.get("From")
        print("메일 발신자: ", from_) 

        # 메일 제목 디코딩
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        print("메일 제목: ", subject)

        # 메일 본문 추출
        if msg.is_multipart():
            print("멀티파트는 지금은 생략")
        else:
            body = msg.get_payload(decode=True).decode("utf-8")
            print("메일 본문: ", body)

           
        
        
        
