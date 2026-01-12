
from google import genai  #  pip install google-genai

from google.genai.errors import ClientError

import secret_config

############################################

API_KEY = secret_config.API_KEY

if not API_KEY or not API_KEY.strip():
    raise ValueError("API_KEY is empty or not set")

try:
    
    client = genai.Client(api_key=API_KEY)

except Exception as e:
    print("Failed to initialize Gemini client:", e)
    raise SystemExit()
    
    
google_model='gemini-2.0-flash-lite'

template = "Translate the phrase '{text}' into {language}. Output only the translated phrase."

prompt = template.format(
    text="Я иду гулять",
    language="English"
)

RESPONSE = ''

if(1):
    
    try:
        res = client.models.generate_content(
            model=google_model,
            contents=prompt
        )
    
        # --- 2. Проверка что ответ вообще есть ---
        if res is None:
            raise RuntimeError("No response object returned by API")
    
        # --- 3. Проверка что есть текст ---
        if not hasattr(res, "text") or not res.text:
            raise RuntimeError("API returned no text (model refused or empty output)")
    
        RESPONSE = res.text
    
    # --- 4. Ошибки API (квоты, биллинг, неверная модель, доступ) ---
    except ClientError as e:
        status = e.status_code
    
        if status == 401:
            print("Invalid or missing API key")
        elif status == 403:
            print("Access denied or billing not enabled")
        elif status == 404:
            print("Model not found:", MODEL)
        elif status == 429:
            print("Quota exceeded or rate limit hit")
        else:
            print("Gemini API error:", e)
    
    # --- 5. Сетевые ошибки, таймауты, JSON и т.п. ---
    except Exception as e:
        print("Unexpected error:", type(e).__name__, str(e))    
    
     
print(RESPONSE)


