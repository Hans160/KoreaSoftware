from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from flask import send_from_directory
app = Flask(__name__)
llm = ChatOpenAI(model='gpt-4o-mini')


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/name', methods=['POST'])
def name():
    data = request.get_json()
    product = data.get('product')
    user_prompt =f"what's a good company name that makes {product}.Do not give any explanation. Just give me the names."
    print(user_prompt)

    prompt = [
        SystemMessage(content='You are a creative branding expert.'),
        HumanMessage(content=user_prompt)
    ]
    result = llm.invoke(prompt)
    names = [line.strip() for line in result.content.split('\n')]
    return jsonify({'result': 'success', 'chatbot': names})

@app.route('/api/dinner')
def dinner():
    prompt = [
    SystemMessage(content='당신은 경력 10년차 호텔 쉐프입니다.'),
    HumanMessage(content='오늘 저녁 메뉴를 추천해주세요'),
]
    
    result = llm.invoke(prompt)
    # print(result.content)

    return jsonify({'result': 'success', 'chatbot': result.content}) # jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)







