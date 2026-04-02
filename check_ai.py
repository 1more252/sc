"""
Scarlett AI — диагностика провайдеров
Запусти: python check_ai.py
"""
import urllib.request, json, sys, os

def test(name, url, headers, payload):
    try:
        req = urllib.request.Request(url,
            data=json.dumps(payload).encode(),
            headers={**headers, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        if "error" in data:
            return False, f"API error: {data['error']}"
        ans = data["choices"][0]["message"]["content"].strip()
        return True, ans[:60]
    except urllib.error.HTTPError as e:
        body = ""
        try: body = e.read().decode()[:100]
        except: pass
        return False, f"HTTP {e.code}: {body}"
    except Exception as e:
        return False, str(e)[:80]

print("=" * 55)
print("  SCARLETT AI — проверка провайдеров")
print("=" * 55)

# ── Читаем ключи из конфига ──────────────────────────
config_path = os.path.join(os.path.dirname(__file__), "scarlett_config.json")
keys = {}
if os.path.exists(config_path):
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)
    keys = {
        "openrouter": cfg.get("openrouter_key",""),
        "groq":       cfg.get("groq_key",""),
        "gemini":     cfg.get("gemini_key",""),
    }
else:
    print("[!] Конфиг не найден, введи ключи вручную")
    keys["openrouter"] = input("OpenRouter key (sk-or-...): ").strip()

# ── OpenRouter — перебираем все модели ───────────────
or_key = keys.get("openrouter","")
if or_key:
    print(f"\n[OpenRouter] ключ: {or_key[:20]}...")
    OR_MODELS = [
        "qwen/qwen2.5-72b-instruct:free",
        "qwen/qwen-2.5-72b-instruct:free",
        "deepseek/deepseek-chat:free",
        "deepseek/deepseek-r1:free",
        "mistralai/mistral-7b-instruct:free",
        "mistralai/mistral-nemo:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "meta-llama/llama-3.1-8b-instruct:free",
        "google/gemma-2-9b-it:free",
        "microsoft/phi-3-medium-128k-instruct:free",
        "openchat/openchat-7b:free",
    ]
    working = []
    for model in OR_MODELS:
        ok, msg = test(
            model,
            "https://openrouter.ai/api/v1/chat/completions",
            {"Authorization": f"Bearer {or_key}",
             "HTTP-Referer": "https://scarlett-ai.local",
             "X-Title": "Scarlett AI"},
            {"model": model,
             "messages": [{"role":"user","content":"Скажи: ок"}],
             "max_tokens": 10}
        )
        status = "✓" if ok else "✗"
        print(f"  {status} {model:<45} {msg[:40]}")
        if ok:
            working.append(model)

    if working:
        print(f"\n  ★ Лучшая рабочая модель: {working[0]}")
        # Записываем результат
        with open("working_model.txt","w") as f:
            f.write(working[0])
    else:
        print("\n  Ни одна модель не ответила — проверь ключ или интернет")
else:
    print("\n[OpenRouter] ключ не задан, пропускаю")

print("\n" + "=" * 55)
input("Нажми Enter для выхода...")
