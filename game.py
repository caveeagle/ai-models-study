
import time

from google import genai  #  pip install google-genai

from google.genai.errors import ClientError

import secret_config

####################################################################    
####################################################################    

API_KEY = secret_config.API_KEY
 
google_model = 'gemini-2.0-flash-lite' 

second_language = 'Russian' 

BASE_PHRASE = 'The old man, who claimed that time was a river that forgets its own source, insisted that every promise is a knot tied in water, and therefore the more carefully you try to keep it, the faster it slips away, which is why he said that honesty is not about telling the truth, but about choosing which illusion hurts the least.'

TURNS_NUMBER = 2
 
####################################################################    
####################################################################    

if not API_KEY or not API_KEY.strip():
    raise ValueError("API_KEY is empty or not set")

try:
    
    client = genai.Client(api_key=API_KEY)

except Exception as e:
    print("Failed to initialize Gemini client:", e)
    raise SystemExit()

####################################################################    
####################################################################    
    

def MakePrompt(client, prompt, google_model = 'gemini-2.0-flash-lite'):
    
    start = time.perf_counter()
    
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
        return ''
        
    # --- 5. Сетевые ошибки, таймауты, JSON и т.п. ---
    except Exception as e:
        print("Unexpected error:", type(e).__name__, str(e))
        return ''    
    
    end = time.perf_counter()
    elapsed_time = end - start
    
    if(0):
        print(f"{elapsed_time:.1f} sec")

    return RESPONSE 

####################################################################    
####################################################################    

template = "Translate the phrase '{text}' from {language_from} into {language_to}. Output only the translated phrase."

RESPONSE = BASE_PHRASE

for n in range(TURNS_NUMBER):
    
    print(f'Turn {n+1}')
    
    prompt = template.format(
        text=RESPONSE,
        language_from="English",
        language_to=second_language
    )
    
    RESPONSE = MakePrompt(client, prompt)
    
    time.sleep(0.5)
    
    prompt = template.format(
        text=RESPONSE,
        language_from=second_language,
        language_to="English"
    )

    RESPONSE = MakePrompt(client, prompt)
    
    time.sleep(0.5)

############################################
############################################

print('The base phrase:')
print(BASE_PHRASE)
print(f'\nAfter {TURNS_NUMBER} turns:')
print(RESPONSE)
print('\n\nJob finished.')

