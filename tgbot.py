import os
import telebot
from openai import OpenAI

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY
)

histories = {}

MODELS = [
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "nvidia/nemotron-nano-9b-v2:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "google/gemma-3-27b-it:free",
    "google/gemma-3-12b-it:free",
    "google/gemma-3-4b-it:free",
    "google/gemma-3n-e4b-it:free",
    "google/gemma-3n-e2b-it:free",
    "liquid/lfm-2.5-1.2b-instruct:free",
    "liquid/lfm-2.5-1.2b-thinking:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "qwen/qwen3-coder:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "openai/gpt-oss-20b:free",
    "openai/gpt-oss-120b:free",
    "z-ai/glm-4.5-air:free",
    "inclusionai/ling-2.6-flash:free",
    "arcee-ai/trinity-large-preview:free",
    "minimax/minimax-m2.5:free",
]

def ask_ai(messages):
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except:
            continue
    return "Перегружен, попробуй через минуту."

def new_history():
    return [{"role": "user", "content": """Ты Максим — рыжий кот в пиджаке, умный ассистент. 
Правила:
1. Отвечаешь по делу и помогаешь с любыми вопросами
2. Иногда добавляешь кошачьи фразы типа "Мяу" или "как кот говорю"
3. Пишешь грамотно и понятно
4. Если вопрос сложный — отвечаешь подробно
5. Если вопрос глупый — отвечаешь с лёгкой иронией
6. Ты кот, но умный кот в пиджаке — не овощ"""}]

@bot.message_handler(commands=["start"])
def start(message):
    histories[message.chat.id] = new_history()
    bot.send_message(message.chat.id, "Мяу. Я Максим, рыжий кот в пиджаке. Чего надо? 🐱")

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, 
        "/start — начать заново\n"
        "/reset — очистить историю\n"
        "/help — эта справка"
    )

@bot.message_handler(commands=["reset"])
def reset(message):
    histories[message.chat.id] = new_history()
    bot.send_message(message.chat.id, "История очищена. Начинаем заново.")

@bot.message_handler(func=lambda m: True)
def handle(message):
    user_id = message.chat.id
    if user_id not in histories:
        histories[user_id] = new_history()
    
    histories[user_id].append({"role": "user", "content": message.text})
    answer = ask_ai(histories[user_id])
    histories[user_id].append({"role": "assistant", "content": answer})
    
    bot.send_message(user_id, answer)

print("Бот запущен!")
bot.polling()