import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def ativar_empresas_sieg():
    # Conecta ao Chrome que já está aberto no modo de depuração
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    print("Conectando ao navegador...")
    driver = webdriver.Chrome(options=chrome_options)
    
    # Você tem 3700 empresas. Se estiver exibindo 200 por página, 19 ou 20 ciclos resolvem.
    # Se estiver exibindo 50 por página (como na imagem), você pode precisar aumentar esse range (ex: range(1, 75))
    for ciclo in range(1, 200):
        print(f"\n--- Iniciando ciclo {ciclo} ---")
        
        # Aguarda 1 segundos para garantir que a tabela da nova página carregou
        time.sleep(1) 
        
        try:
            # Busca todas as linhas da tabela
            linhas = driver.find_elements(By.XPATH, "//tbody/tr")
            print(f"Encontradas {len(linhas)} linhas na página atual.")
            
            empresas_ativadas = 0
            
            for linha in linhas:
                texto_linha = linha.text
                
                # Se o certificado FOR o especificado, vamos ativar
                if "EXEMPLO CONTABILIDADE LTDA" in texto_linha:
                    try:
                        # Encontra o botão de toggle na linha atual
                        toggle = linha.find_element(By.CSS_SELECTOR, "input.su-toggle")
                        
                        # Verifica se já está ativado. Se não estiver, clica.
                        if not toggle.is_selected():
                            driver.execute_script("arguments[0].click();", toggle)
                            empresas_ativadas += 1
                            time.sleep(0.5) # Pausa para o servidor registrar
                            
                    except Exception as e:
                        pass # Ignora erro de linha sem botão e continua
            
            print(f"{empresas_ativadas} novas empresas foram ativadas nesta página.")
            time.sleep(2) # Pausa antes de mudar de página
            
        except Exception as e:
            print(f"Erro ao ler as linhas da tabela: {e}")
        
        # Lógica para clicar na "Próxima Página"
        print("Indo para a próxima página...")
        try:
            # Busca botões de paginação pela classe que você mandou no print
            botoes_paginacao = driver.find_elements(By.CSS_SELECTOR, "button.d-btn.d-btn-md")
            
            if botoes_paginacao:
                # O botão de 'próxima' geralmente é o último ou penúltimo da lista de botões.
                # Se houver um botão de pular para o "último", você precisará ajustar o índice.
                # Aqui, usamos [-1] para pegar o último botão da lista de botões encontrados.
                botao_proxima = botoes_paginacao[-1]
                
                # Desce a tela até o botão (útil se o site não clicar em coisas invisíveis)
                driver.execute_script("arguments[0].scrollIntoView(true);", botao_proxima)
                time.sleep(1)
                
                # Clica na próxima
                driver.execute_script("arguments[0].click();", botao_proxima)
            else:
                print("Botão de próxima página não encontrado. Fim da lista?")
                break # Encerra o loop se não achar mais o botão
                
        except Exception as e:
            print(f"Não foi possível clicar na próxima página: {e}")
            break # Encerra o loop se der erro fatal na paginação

    print("\nProcesso finalizado com sucesso!")

if __name__ == "__main__":
    ativar_empresas_sieg()