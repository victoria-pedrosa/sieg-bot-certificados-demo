# Demonstração — Gestão de certificados e procurações no SIEG

> Projeto de portfólio de **Victória Pedrosa**. **Demonstração** de gestão de certificados e procurações no SIEG — versão com dados fictícios (nomes, CNPJs, e-mails e IDs internos substituídos).

## Problema de negócio
Ativar e desativar certificados/procurações de milhares de empresas no SIEG era manual.

## Antes x depois
| | Antes | Depois |
|---|---|---|
| Como é feito | Clique a clique em ~3.700 empresas. | Robôs percorrem as páginas e ativam/desativam conforme o certificado. |

## Ganho
- Ajuste em massa em minutos.

## Tecnologias
Python, SQLite, Selenium

## Arquivos
- `ativarnosieg_bot_procuracao.py`
- `requirements.txt`
- `siebbot_desativar_certificadoproprio.py`
- `sieg_bot_certificados_EXCLUIR-POPRIO.py`

## Como rodar
1. `pip install -r requirements.txt`
2. Copie `.env.exemplo` para `.env` e preencha os caminhos.
3. Execute o script principal.

## Autora
Victória Pedrosa — Product Owner do Time de IA, automação de processos contábeis e fiscais.
