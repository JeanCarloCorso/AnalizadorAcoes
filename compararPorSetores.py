import fundamentus
from bcb import sgs
from datetime import datetime
from prettytable import PrettyTable
import pandas as pd
import os

class Indicadores:
    def __init__(self, ativo, setor, cotacao, pl, pvp, lpa, vpa, pebit, div_yield, evebit, cres5a, marg_ebit, marg_liquida, roic, roe, lic_corr, div_bruta_pelo_patr, pontuacao):
        self.ativo = ativo
        self.setor = setor
        self.cotacao = cotacao
        self.pl = pl
        self.pvp = pvp
        self.lpa = lpa
        self.vpa = vpa
        self.preco_justo = 22.5 * lpa * vpa
        self.pebit = pebit
        self.div_yield = div_yield
        self.evebit = evebit
        self.cres5a = cres5a
        self.marg_ebit = marg_ebit
        self.marg_liquida = marg_liquida
        self.roic = roic
        self.roe = roe
        self.lic_corr = lic_corr
        self.div_bruta_pelo_patr = div_bruta_pelo_patr
        self.pontuacao = pontuacao

setores = [
   [ 'agro'            , 'Agropecuária'                       , 42 ] ,
   [ 'saneamento'      , 'Água e Saneamento'                  , 33 ] ,
   [ 'alimentos'       , 'Alimentos'                          , 15 ] ,
   [ 'bebidas'         , 'Bebidas'                            , 16 ] ,
   [ 'com1'            , 'Comércio'                           , 27 ] ,
   [ 'com2'            , 'Comércio'                           , 12 ] ,
   [ 'com3'            , 'Comércio e Distribuição'            , 20 ] ,
   [ 'computadores'    , 'Computadores e Equipamentos'        , 28 ] ,
   [ 'construcao'      , 'Construção e Engenharia'            , 13 ] ,
   [ 'engenharia'      , 'Construção e Engenharia'            , 13 ] ,
   [ 'diversos'        , 'Diversos'                           , 26 ] ,
   [ 'embalagens'      , 'Embalagens'                         , 6  ] ,
   [ 'energia'         , 'Energia Elétrica'                   , 32 ] ,
   [ 'equipamentos'    , 'Equipamentos Elétricos'             , 9  ] ,
   [ 'imoveis'         , 'Exploração de Imóveis'              , 39 ] ,
   [ 'financeiro'      , 'Financeiros'                        , 35 ] ,
   [ 'fumo'            , 'Fumo'                               , 17 ] ,
   [ 'gas'             , 'Gás'                                , 34 ] ,
   [ 'holdings'        , 'Holdings Diversificadas'            , 40 ] ,
   [ 'hoteis'          , 'Hoteis e Restaurantes'              , 24 ] ,
   [ 'restaurantes'    , 'Hoteis e Restaurantes'              , 24 ] ,
   [ 'papel'           , 'Madeira e Papel'                    , 5  ] ,
   [ 'maquinas'        , 'Máquinas e Equipamentos'            , 10 ] ,
   [ 'materiais'       , 'Materiais Diversos'                 , 7  ] ,
   [ 'transporte'      , 'Material de Transporte'             , 8  ] ,
   [ 'midia'           , 'Mídia'                              , 23 ] ,
   [ 'mineracao'       , 'Mineração'                          , 2  ] ,
   [ 'outros'          , 'Outros'                             , 41 ] ,
   [ 'petroleo'        , 'Petróleo, Gás e Biocombustíveis'    , 1  ] ,
   [ 'previdencia'     , 'Previdência e Seguros'              , 38 ] ,
   [ 'seguros'         , 'Previdência e Seguros'              , 38 ] ,
   [ 'usopessoal'      , 'Prods. de Uso Pessoal e de Limpeza' , 18 ] ,
   [ 'limpeza'         , 'Prods. de Uso Pessoal e de Limpeza' , 18 ] ,
   [ 'programas'       , 'Programas e Serviços'               , 29 ] ,
   [ 'quimicos'        , 'Químicos'                           , 4  ] ,
   [ 'saude'           , 'Saúde'                              , 19 ] ,
   [ 'securitizadoras' , 'Securitizadoras de Recebíveis'      , 36 ] ,
   [ 'servicos'        , 'Serviços'                           , 11 ] ,
   [ 'finandiversos'   , 'Serviços Financeiros Diversos'      , 37 ] ,
   [ 'siderurgia'      , 'Siderurgia e Metalurgia'            , 3  ] ,
   [ 'tecidos'         , 'Tecidos, Vestuário e Calçados'      , 21 ] ,
   [ 'vestuario'       , 'Tecidos, Vestuário e Calçados'      , 21 ] ,
   [ 'telecom'         , 'Telecomunicações'                   , 43 ] ,
   [ 'telefoniafixa'   , 'Telefonia Fixa'                     , 30 ] ,
   [ 'telefoniamovel'  , 'Telefonia Móvel'                    , 31 ] ,
   [ 'transporte'      , 'Transporte'                         , 14 ] ,
   [ 'utilidades'      , 'Utilidades Domésticas'              , 22 ] ,
   [ 'viagens'         , 'Viagens e Lazer'                    , 25 ] ,
]

def RetornaNomeSetor(codSetor):
    for setor in setores:
        if setor[2] == codSetor:
            return setor[1]
    return "Setor não encontrado"

def RetornaCodSetor(nomeSetor):
    for setor in setores:
        if setor[1] == nomeSetor:
            return setor[2]
    return "Setor não encontrado"

def RetornaAcoesSetor(codSetor):
    return fundamentus.list_papel_setor(codSetor)

def RetornaTodasAcoes():
    df = fundamentus.get_resultado()

    return df.index.tolist()

def RetornaSelic():
    data_atual = datetime.now().strftime('%Y-%m-%d')
    selic_series = sgs.get({'selic': 432}, start=data_atual)

    return selic_series['selic'].iloc[-1]

def ValorStrToFloat(valor):
    if valor.iloc[0] != '-' and valor.iloc[0] != '':
        return float(valor.str.strip('%').iloc[0])
    else:
        return 0

def PreencheDados(listaAcoes):
    listaIndicadores = []

    for acao in listaAcoes:
        dados_da_acao = fundamentus.get_papel(acao)

        instancia_acao = Indicadores(
            str(dados_da_acao['Ativo'])[:5],
            dados_da_acao['Setor'].iloc[0],
            ValorStrToFloat(dados_da_acao['Cotacao']),
            ValorStrToFloat(dados_da_acao['PL'])/100,
            ValorStrToFloat(dados_da_acao['PVP'])/100,
            ValorStrToFloat(dados_da_acao['LPA'])/100,
            ValorStrToFloat(dados_da_acao['VPA'])/100,
            ValorStrToFloat(dados_da_acao['PEBIT'])/100,
            ValorStrToFloat(dados_da_acao['Div_Yield']),
            ValorStrToFloat(dados_da_acao['EV_EBIT'])/100,
            ValorStrToFloat(dados_da_acao['Cres_Rec_5a']),
            ValorStrToFloat(dados_da_acao['Marg_EBIT']),
            ValorStrToFloat(dados_da_acao['Marg_Liquida']),
            ValorStrToFloat(dados_da_acao['ROIC']),
            ValorStrToFloat(dados_da_acao['ROE']),
            ValorStrToFloat(dados_da_acao['Liquidez_Corr'])/100,
            ValorStrToFloat(dados_da_acao['Div_Br_Patrim'])/100,
            0
        )

        listaIndicadores.append(instancia_acao)

    return listaIndicadores

def MostraListaAcoes(listaAcoes):
    tabela = PrettyTable(['Ativo', 'Setor', 'Cotação', 'Preço Justo', 'P/L', 'P/VP', 'LPA', 'VPA', 'P/EBIT', 'Div. Yield', 
                          'EV/EBIT', 'Cres. Rec (5a)'])

    for indicadores in listaAcoes:
        tabela.add_row([indicadores.ativo, indicadores.setor, indicadores.cotacao, f"{indicadores.preco_justo:.2f}", indicadores.pl, indicadores.pvp, indicadores.lpa, 
                        indicadores.vpa, indicadores.pebit, indicadores.div_yield, indicadores.evebit, indicadores.cres5a])

    print(tabela)

def SalvaAcoes(listaAcoesIndicadores):
    df = pd.DataFrame([vars(indicador) for indicador in listaAcoesIndicadores])
    caminho_excel = os.path.join(os.getcwd(), 'arquivo.xlsx')
    df.to_excel(caminho_excel, index=False)

def ClassificaAcoes(listaAcoesIndicadores, concideraSelic=False, concideraGraham=False, dividendos=False):
    #Elimina empresas que não dão lucro e excessivamente endividadas
    lista_filtrada = list(filter(lambda indic: indic.pl > 0 and indic.pvp > 0 and indic.lpa > 0 and 
                                 indic.vpa > 0 and indic.pebit > 0 and indic.marg_liquida > 10 and
                                 indic.lic_corr > 1 and indic.div_bruta_pelo_patr < 1, listaAcoesIndicadores))

    #Elimina empresas que não estão crescendo
    lista_filtrada = list(filter(lambda indic: indic.pl > 0, listaAcoesIndicadores))

    #Elimina empresas que não são eficientes
    lista_filtrada = list(filter(lambda indic: indic.roic > 2 and indic.roe >= 15, listaAcoesIndicadores))

    if(concideraSelic):
        selic = RetornaSelic()
        lista_filtrada = list(filter(lambda indic: indic.pl <= 100/selic, lista_filtrada))
    
    if(concideraGraham):
        lista_filtrada = list(filter(lambda indic: indic.preco_justo >= indic.cotacao, lista_filtrada))

    if(dividendos):
        lista_filtrada = list(filter(lambda indic: indic.div_yield >= 12, lista_filtrada))

    return lista_filtrada

acoes = RetornaTodasAcoes()
#acoes = RetornaAcoesSetor(22)
listaIndicadores = PreencheDados(acoes)
acoesFiltradas = ClassificaAcoes(listaIndicadores, True, True, True)
SalvaAcoes(acoesFiltradas)
MostraListaAcoes(acoesFiltradas)