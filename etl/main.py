from etl.fluxos.funcionarios_fluxo import etl_funcionarios_flow
from etl.fluxos.cargos_fluxo import etl_cargos_flow
from etl.fluxos.departamentos_fluxo import etl_departamentos_flow
from etl.fluxos.empresas_fluxo import etl_empresas_flow
from etl.fluxos.justificativas_abono_fluxo import etl_justificativas_abono_flow
from etl.fluxos.regionais_fluxo import etl_regionais_flow
from etl.fluxos.pontos_fluxo import etl_pontos_flow
from etl.fluxos.ajustes_manuais_fluxo import etl_ajustes_manuais_flow
from etl.fluxos.controle_refeicao_fluxo import etl_controle_refeicoes_flow
from etl.fluxos.entregaveis_fluxo import etl_entregaveis_flow
from etl.fluxos.obs_refeicao_fluxo import etl_obs_refeicao_flow
from etl.fluxos.check_lists_fluxo import etl_check_lists_flow

etl_cargos_flow()
etl_departamentos_flow()
etl_empresas_flow()
etl_justificativas_abono_flow()
etl_regionais_flow()
etl_funcionarios_flow()
etl_pontos_flow()
etl_ajustes_manuais_flow()
etl_controle_refeicoes_flow()
etl_entregaveis_flow()
etl_obs_refeicao_flow()
etl_check_lists_flow()