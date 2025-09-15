import streamlit as st
import torch
import torch.nn as nn
import joblib
import re

# -------------------
# Función de limpieza
# -------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -------------------
# Modelo PyTorch
# -------------------
class SpamClassifierNN(nn.Module):
    def __init__(self, input_dim):
        super(SpamClassifierNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 2)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x

# -------------------
# Cargar modelo y vectorizador
# -------------------
vectorizer = joblib.load('tfidf_vectorizer.pkl')
input_dim = len(vectorizer.get_feature_names_out())
model = SpamClassifierNN(input_dim)
model.load_state_dict(torch.load('spam_classifier_pytorch.pt'))
model.eval()

# -------------------
# Interfaz Streamlit
# -------------------
st.title("Clasificador de Mensajes SPAM/HAM")
st.write("Escribe un mensaje y el modelo te dirá si es SPAM o HAM.")

mensaje = st.text_area("Mensaje:", "")

if st.button("Clasificar"):
    if mensaje.strip() == "":
        st.warning("Por favor, escribe un mensaje.")
    else:
        # Preprocesar y vectorizar
        mensaje_vec = vectorizer.transform([clean_text(mensaje)])
        mensaje_tensor = torch.tensor(mensaje_vec.toarray(), dtype=torch.float32)

        # Predecir
        with torch.no_grad():
            output = model(mensaje_tensor)
            pred = torch.argmax(output, dim=1).item()

        resultado = "SPAM" if pred == 1 else "HAM"
        st.success(f"Predicción: {resultado}")
