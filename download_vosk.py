"""
Vosk - загрузчик модели для оффлайн распознавания.
Используется только когда нет интернета (основной STT - Google).

Модели по размеру/точности:
  small  ~45MB  - быстро, но плохо слышит
  medium ~500MB - хороший баланс (рекомендуется)
  large  ~1.8GB - максимальная точность, медленнее
"""
import urllib.request, zipfile, os, sys

# Какую модель скачать — medium намного точнее small
# Меняй здесь: "small" / "medium" / "large"
MODEL_SIZE = "small"

MODELS = {
    "small": {
        "name":   "vosk-model-small-ru-0.22",
        "dir":    "vosk-model-small-ru",
        "size":   "~45MB",
        "urls": [
            "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip",
            "https://github.com/alphacep/vosk-api/releases/download/v0.3.45/vosk-model-small-ru-0.22.zip",
        ],
    },
    "medium": {
        "name":   "vosk-model-ru-0.42",
        "dir":    "vosk-model-small-ru",   # сохраняем в ту же папку — Скарлетт найдёт
        "size":   "~500MB",
        "urls": [
            "https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip",
        ],
    },
    "large": {
        "name":   "vosk-model-ru-0.42",
        "dir":    "vosk-model-small-ru",
        "size":   "~1.8GB",
        "urls": [
            "https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip",
        ],
    },
}

def try_download(url: str, dest: str) -> bool:
    print(f"  URL: {url[:70]}...")
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-Agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)

        def progress(count, block, total):
            if total > 0:
                pct = min(100, count * block * 100 // total)
                mb  = count * block / 1024 / 1024
                bar = "#" * (pct // 5) + "-" * (20 - pct // 5)
                print(f"\r  [{bar}] {pct}%  {mb:.1f} MB", end="", flush=True)

        urllib.request.urlretrieve(url, dest, reporthook=progress)
        print()
        return True
    except Exception as e:
        print(f"\n  Ошибка: {e}")
        if os.path.exists(dest):
            os.remove(dest)
        return False

def main():
    cfg     = MODELS[MODEL_SIZE]
    dir_out = cfg["dir"]
    zip_tmp = "vosk-model.zip"

    if os.path.isdir(dir_out):
        print(f"[Vosk] Модель уже есть: {dir_out}")
        sys.exit(0)

    print(f"[Vosk] Скачиваем модель {MODEL_SIZE} ({cfg['size']})...")
    print(f"[Vosk] Это займёт некоторое время, не закрывай окно.")

    ok = False
    for url in cfg["urls"]:
        if try_download(url, zip_tmp):
            ok = True
            break

    if not ok:
        print("\n[Vosk] Все источники недоступны.")
        print("  → Скарлетт будет использовать Google STT (нужен интернет).")
        print("  → Для ручной установки: скачай модель с alphacephei.com/vosk/models")
        print(f"    и распакуй в C:\\Scarlett\\{dir_out}")
        sys.exit(1)

    print("  Распаковка...")
    try:
        with zipfile.ZipFile(zip_tmp, "r") as z:
            z.extractall(".")
        os.remove(zip_tmp)
        # Переименовываем если нужно
        extracted = cfg["name"]
        if os.path.isdir(extracted) and not os.path.isdir(dir_out):
            os.rename(extracted, dir_out)
        print(f"  Готово → {dir_out}")
        print("[Vosk] Оффлайн распознавание включено!")
    except Exception as e:
        print(f"  Ошибка распаковки: {e}")
        if os.path.exists(zip_tmp):
            os.remove(zip_tmp)
        sys.exit(1)

if __name__ == "__main__":
    main()
