# Sistema de Engenharia de Dados ETL

Este repositório contém fluxos de ETL (Extract, Transform, Load) orquestrados pelo [Prefect](https://www.prefect.io/), utilizando Pandas para manipulação de dados e Requests para interações com APIs.

## estrutura do Projeto

O código fonte principal reside na pasta `etl/`:

- **`fluxos/`**: Definições dos Flows do Prefect.
- **`fontes_dados/`**: Scripts para extração de dados (APIs, Excel, Google Sheets).
- **`transformacoes/`**: Lógica de limpeza e transformação de dados com Pandas.
- **`loaders/`**: Scripts para carregar os dados processados no destino final.
- **`schemas/`**: Modelos Pydantic para validação de dados.
- **`utils/`**: Funções utilitárias e helpers.

## Configuração

Este projeto utiliza [Poetry](https://python-poetry.org/) para gerenciamento de dependências.

1. Instale as dependências:
   ```bash
   poetry install
   ```

2. Ative o ambiente virtual:
   ```bash
   poetry shell
   ```

3. Configure as variáveis de ambiente no arquivo `.env` (baseado em um `.env.example` se houver).

## Executando um Fluxo

Este projeto utiliza uma CLI construída com **Typer**. Não execute os scripts de fluxo diretamente. Use o `etl/main.py` como ponto de entrada.

### Listar Fluxos Disponíveis
```bash
poetry run python -m etl.main listar_fluxos
```

### Executar um Fluxo Específico
```bash
poetry run python -m etl.main executar_fluxo [NOME_DO_FLUXO]
# Exemplo:
poetry run python -m etl.main executar_fluxo regionais
```

### Executar Todos os Fluxos
```bash
poetry run python -m etl.main executar_tudo
```

### Ajuda
```bash
poetry run python -m etl.main --help
```

## Diretrizes de Desenvolvimento

Consulte o arquivo `status_do_projeto.md` para ver as "Regras de Ouro", decisões arquiteturais e o status atual do desenvolvimento.
