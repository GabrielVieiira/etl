# Status do Projeto: Sistema de Engenharia de Dados ETL

> **Guia da Verdade**: Este documento registra as decisões técnicas, regras de implementação e o progresso atual do projeto.

## 1. Decisões Arquiteturais & Regras de Ouro
- **Orquestração**: Prefect (Versão 2.x ou 3.x).
- **Estrutura de Código**:
  - Decoradores: Obrigatório uso de `@flow` e `@task`.
  - Atomicidade: Tarefas devem fazer apenas UMA coisa.
  - Resiliência: Uso de `retries` e `retry_delay_seconds` em chamadas externas.
  - Observabilidade: **PROIBIDO** usar `print()`. Usar `get_run_logger()` do Prefect.
  - **Idioma**: Todo o código (variáveis, funções, classes, comentários) deve estar estritamente em **PT-BR** (Português Brasileiro). Ex: `obter_clientes` ✅, `get_customers` ❌.
- **Gerenciamento de Dependências**: Poetry.
- **Estrutura de Diretórios**:
  - `etl/fluxos`: Orquestradores principais.
  - `etl/fontes_dados`: Conectores (extratores).
  - `etl/transformacoes`: Lógica de negócios e limpeza (Pandas).
  - `etl/loaders`: Carga de dados (Load).
  - `etl/schemas`: Definições de tipos e validação (Pydantic).

## 2. Progresso Atual
- [x] Inicialização do Repositório.
- [x] Estrutura de Diretórios Criada.
- [x] Criação da Documentação Inicial.
- [x] Refatoração do `main.py` para CLI (Typer) 🚀.
- [x] Validação de Execução (Fluxo Regionais) ✅.
- [ ] Implementação de novos fluxos.

## 3. Próximos Passos
1. Validar conexão com APIs ou arquivos locais.
2. Criar fluxo de exemplo "Hello World" ou caso de uso real.
