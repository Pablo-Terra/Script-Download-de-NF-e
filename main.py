import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import os

# Diretório base: mesma pasta onde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos dos arquivos
CSV_PATH = os.path.join(BASE_DIR, "ARUBA GRILL LTDA.csv")
DRIVER_PATH = os.path.join(BASE_DIR, "msedgedriver.exe")

# === 1. Ler as chaves do CSV ===
def carregar_chaves(csv_path):
    df = pd.read_csv(csv_path, sep=";")
    chaves = df["Chave de Acesso"].astype(str).str.strip().str.replace("'", "")
    return chaves.tolist()

# === 2. Abrir o navegador com Selenium (Edge) ===
def iniciar_navegador(driver_path):
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")

    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    return driver


# === 3. Buscar a nota no site da Receita ===
def consultar_nfe(driver, chave):
    url = "https://www.nfe.fazenda.gov.br/portal/consultaCompleta.aspx"
    driver.get(url)

    print(f"Aguardando para preencher chave: {chave}")
    time.sleep(5)  # Aguarda a página carregar

    try:
        input_chave = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtChaveAcessoCompleta")
        input_chave.clear()
        input_chave.send_keys(chave)
        print("✅ Chave preenchida. Complete o CAPTCHA manualmente se solicitado.")
    except Exception as e:
        print("❌ Erro ao localizar campo de chave:", e)

# === Execução principal ===
if __name__ == "__main__":
    chaves = carregar_chaves(CSV_PATH)
    print(f"🔑 {len(chaves)} chaves encontradas no arquivo.")

    driver = iniciar_navegador(DRIVER_PATH)

    # Testar com a primeira chave
    consultar_nfe(driver, chaves[0])

    input("⏳ Pressione Enter após resolver o CAPTCHA para continuar e encerrar...")
    driver.quit()
