import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def desativar_empresas_sieg():
    # Conecta ao Chrome que já está aberto no modo de depuração
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    print("Conectando ao navegador...")
    driver = webdriver.Chrome(options=chrome_options)
    
    # Ajuste o limite do range caso tenha mais ou menos páginas
    # Ex: range(1, 80) cobriria cerca de 3950 empresas de 200 em 200
    for ciclo in range(1, 200):
        print(f"\n--- Iniciando ciclo da Página {ciclo} ---")
        
        # Aguarda 1 segundos para garantir que a tabela carregou completamente
        time.sleep(1) 
        
        try:
            # Busca todas as linhas da tabela
            linhas = driver.find_elements(By.XPATH, "//tbody/tr")
            print(f"Encontradas {len(linhas)} linhas na página atual.")
            
            empresas_desativadas = 0
            
            for linha in linhas:
                texto_linha = linha.text
                
                # Nova Condição 1: O certificado é DIFERENTE de EXEMPLO?
                if "EXEMPLO CONTABILIDADE LTDA" not in texto_linha:
                    try:
                        # Encontra o botão de toggle (Ativo na Sieg)
                        toggle = linha.find_element(By.CSS_SELECTOR, "input.su-toggle")
                        
                        # Nova Condição 2: O botão JÁ ESTÁ selecionado (Ativo)?
                        # Se sim, clica para desativar.
                        if toggle.is_selected():
                            driver.execute_script("arguments[0].click();", toggle)
                            empresas_desativadas += 1
                            time.sleep(0.5) # Breve pausa para o sistema registrar o clique
                            
                    except Exception as e:
                        pass # Ignora erros pontuais (ex: linha sem botão)
            
            print(f"{empresas_desativadas} empresas foram desativadas nesta página.")
            time.sleep(2) # Pausa antes de ir para a próxima página
            
        except Exception as e:
            print(f"Erro ao ler as linhas da tabela: {e}")
        
        # Lógica de avançar para a próxima página
        print("Indo para a próxima página...")
        try:
            # Pega todos os botões que têm a classe da paginação
            botoes_paginacao = driver.find_elements(By.CSS_SELECTOR, "button.d-btn.d-btn-md")
            
            if botoes_paginacao:
                # O botão de "Próxima" geralmente é o último da sequência
                botao_proxima = botoes_paginacao[-1]
                
                # Rola a tela até o botão para evitar erros de elemento fora da visão
                driver.execute_script("arguments[0].scrollIntoView(true);", botao_proxima)
                time.sleep(1)
                
                # Executa o clique
                driver.execute_script("arguments[0].click();", botao_proxima)
            else:
                print("Botões de paginação não encontrados. Chegamos ao fim?")
                break # Sai do loop se não achar mais a paginação
                
        except Exception as e:
            print(f"Não foi possível clicar na próxima página: {e}")
            break # Sai do loop se houver um erro na hora de mudar de página

    print("\nProcesso de desativação finalizado!")

if __name__ == "__main__":
    desativar_empresas_sieg()