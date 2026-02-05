import typer
import importlib
from rich.console import Console
from typing import Optional

# Configuração do Typer e Rich Console
app = typer.Typer(help="CLI para Orquestração Local do ETL Sigflor")
console = Console()

# Mapa de Fluxos disponíveis (Nome CLI -> "modulo:funcao")
# Usamos strings para evitar importação lenta no startup da CLI
FLUXOS_MAPA = {
    "funcionarios": "etl.fluxos.funcionarios_fluxo:etl_funcionarios_flow",
    "cargos": "etl.fluxos.cargos_fluxo:etl_cargos_flow",
    "departamentos": "etl.fluxos.departamentos_fluxo:etl_departamentos_flow",
    "empresas": "etl.fluxos.empresas_fluxo:etl_empresas_flow",
    "justificativas_abono": "etl.fluxos.justificativas_abono_fluxo:etl_justificativas_abono_flow",
    "regionais": "etl.fluxos.regionais_fluxo:etl_regionais_flow",
    "pontos": "etl.fluxos.pontos_fluxo:etl_pontos_flow",
    "ajustes_manuais": "etl.fluxos.ajustes_manuais_fluxo:etl_ajustes_manuais_flow",
    "controle_refeicoes": "etl.fluxos.controle_refeicao_fluxo:etl_controle_refeicoes_flow",
    "entregaveis": "etl.fluxos.entregaveis_fluxo:etl_entregaveis_flow",
    "obs_refeicao": "etl.fluxos.obs_refeicao_fluxo:etl_obs_refeicao_flow",
    "check_lists": "etl.fluxos.check_lists_fluxo:etl_check_lists_flow",
    "despesas_veiculos": "etl.fluxos.despesas_veiculos_fluxo:etl_despesa_veiculos_flow"
}

def _importar_e_executar(caminho: str):
    """
    Importa dinamicamente a função e a executa.
    Formato caminho: 'pacote.modulo:funcao'
    """
    modulo_path, func_name = caminho.split(":")
    try:
        mod = importlib.import_module(modulo_path)
        func = getattr(mod, func_name)
        func()
    except ImportError as e:
        console.print(f"[bold red]Erro de Importação:[/bold red] Não foi possível carregar {modulo_path}. Detalhe: {e}")
        raise
    except AttributeError as e:
        console.print(f"[bold red]Erro de Atributo:[/bold red] Função '{func_name}' não encontrada em {modulo_path}.")
        raise

@app.command("listar_fluxos")
def listar_fluxos():
    """
    Lista todos os fluxos ETL disponíveis para execução.
    """
    console.print("[bold green]Fluxos Disponíveis:[/bold green]")
    for nome in FLUXOS_MAPA:
        console.print(f"- [cyan]{nome}[/cyan]")

@app.command("executar_fluxo")
def executar_fluxo(
    nome: str = typer.Argument(..., help="Nome do fluxo para executar (use 'listar_fluxos' para ver opções).")
):
    """
    Executa um fluxo específico pelo NOME.
    Carrega o módulo apenas no momento da execução (Lazy Loading).
    """
    if nome not in FLUXOS_MAPA:
        console.print(f"[bold red]Erro:[/bold red] Fluxo '{nome}' não encontrado.")
        console.print("Use o comando [bold]listar_fluxos[/bold] para ver as opções válidas.")
        raise typer.Exit(code=1)
    
    console.print(f"[bold blue]Iniciando fluxo:[/bold blue] {nome}...")
    try:
        caminho = FLUXOS_MAPA[nome]
        _importar_e_executar(caminho)
        console.print(f"[bold green]Sucesso![/bold green] Fluxo '{nome}' finalizado.")
    except Exception as e:
        console.print(f"[bold red]Falha na execução:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command("executar_tudo")
def executar_tudo():
    """
    Executa TODOS os fluxos sequencialmente.
    Importa cada fluxo sob demanda.
    """
    console.print("[bold yellow]Iniciando execução completa de todos os fluxos...[/bold yellow]")
    
    erros = []
    for nome, caminho in FLUXOS_MAPA.items():
        console.print(f"\n[bold blue]>>> Executando:[/bold blue] {nome}")
        try:
            _importar_e_executar(caminho)
        except Exception as e:
            msg_erro = f"Falha em '{nome}': {str(e)}"
            console.print(f"[bold red]{msg_erro}[/bold red]")
            erros.append(msg_erro)
            
    if erros:
        console.print("\n[bold red]A execução completa terminou com erros:[/bold red]")
        for erro in erros:
            console.print(f"- {erro}")
        raise typer.Exit(code=1)
    else:
        console.print("\n[bold green]Todos os fluxos foram executados com sucesso![/bold green]")

if __name__ == "__main__":
    app()