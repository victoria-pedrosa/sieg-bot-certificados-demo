import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def executar_limpeza_sieg():
    # Conecta ao Chrome que você já deixou aberto
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    print("Conectando ao navegador...")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 1)
    
    # Repete o processo 20 vezes
    for ciclo in range(1, 200):
        print(f"\n--- Iniciando ciclo {ciclo} de 20 ---")
        
        # Dá um tempo para garantir que a tabela carregou completamente
        time.sleep(5) 
        
        try:
            # Busca todas as linhas da tabela (assumindo a tag <tr> padrão de tabelas)
            # Se a plataforma usar divs em vez de tr, este seletor precisará ser ajustado
            linhas = driver.find_elements(By.XPATH, "//tbody/tr")
            print(f"Encontradas {len(linhas)} linhas na página atual.")
            
            empresas_selecionadas = 0
            
            for linha in linhas:
                texto_linha = linha.text
                
                # Se o certificado NÃO for o especificado, seleciona a caixa
                if "EXEMPLO CONTABILIDADE LTDA" not in texto_linha:
                    try:
                        # Busca o checkbox oculto baseado na classe da sua imagem
                        checkbox = linha.find_element(By.CSS_SELECTOR, "input.p-checkbox-input")
                        
                        # Usamos JavaScript para clicar, pois checkboxes do PrimeVue/Angular 
                        # geralmente ficam ocultos sob uma div visual
                        driver.execute_script("arguments[0].click();", checkbox)
                        empresas_selecionadas += 1
                    except Exception as e:
                        print(f"Não foi possível clicar no checkbox de uma linha.")
            
            print(f"{empresas_selecionadas} empresas marcadas para exclusão.")
            
            if empresas_selecionadas > 0:
                # Clica no botão Excluir usando o texto do botão (visível na sua imagem)
                botao_excluir = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Excluir')]")))
                botao_excluir.click()
                print("Botão 'Excluir' clicado.")
                
                # ATENÇÃO: Se o sistema exibir um modal/popup perguntando "Tem certeza que deseja excluir?",
                # você precisará adicionar um clique para confirmar aqui. Exemplo:
                # btn_confirmar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sim')]")))
                # btn_confirmar.click()
                
                # Aguarda o sistema processar a exclusão antes de recarregar
                time.sleep(4) 
            
        except Exception as e:
            print(f"Ocorreu um erro neste ciclo: {e}")
        
        # Recarrega a página para o próximo lote de 200
        print("Recarregando a página para o próximo lote...")
        driver.refresh()

    print("\nProcesso finalizado!")

if __name__ == "__main__":
    executar_limpeza_sieg()