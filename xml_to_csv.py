import xml.etree.ElementTree as ET
import csv
from datetime import datetime

# Carga el XML (usa raw string o slashes normales)
tree = ET.parse(r"D:\calsificadorspam\2.xml")
# también puedes poner: tree = ET.parse("D:/calsificadorspam/asdasda12.xml")
root = tree.getroot()

# Prepara CSV
with open("sms_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["address", "date", "type", "body"])  # cabecera

    for sms in root.findall("sms"):
        address = sms.get("address", "")
        date_ms = sms.get("date", "")
        sms_type = sms.get("type", "")
        body = sms.get("body", "")

        # Convertir fecha de milisegundos a formato legible
        try:
            date = datetime.fromtimestamp(int(date_ms) / 1000).strftime("%Y-%m-%d %H:%M:%S")
        except:
            date = ""

        writer.writerow([address, date, sms_type, body])

print("✅ Exportado a sms_dataset.csv")
