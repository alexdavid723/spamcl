import pandas as pd
import re
import unicodedata

# === Cargar CSV exportado ===
# Usa raw string o / para evitar errores con la ruta
df = pd.read_csv(r"D:\calsificadorspam\sms_dataset.csv")

def clean_text(text):
    if pd.isna(text):
        return ""
    
    # pasar a minúsculas
    text = text.lower()
    
    # normalizar acentos (á->a, ñ->n)
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    
    # reemplazar URLs, emails, teléfonos, números
    text = re.sub(r"http\S+|www\.\S+", "<URL>", text)
    text = re.sub(r"\S+@\S+", "<EMAIL>", text)
    text = re.sub(r"\+?\d{6,}", "<PHONE>", text)
    text = re.sub(r"\b\d+\b", "<NUMBER>", text)
    
    # eliminar caracteres no alfabéticos excepto <> para tokens y ! ?
    text = re.sub(r"[^a-zA-Z<>!? ]+", " ", text)
    
    # eliminar espacios extra
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

# === Aplicar limpieza ===
df["clean_body"] = df["body"].apply(clean_text)

# Eliminar mensajes que quedaron vacíos
df = df[df["clean_body"].str.strip() != ""]

# === Guardar dataset limpio ===
df.to_csv(r"D:\calsificadorspam\sms_dataset_clean.csv", index=False, encoding="utf-8")

print("✅ Dataset limpio guardado en D:\\calsificadorspam\\sms_dataset_clean.csv")
