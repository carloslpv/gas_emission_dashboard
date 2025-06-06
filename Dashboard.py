import streamlit as st
import pandas as pd
import plotly.express as px

#-- Page Config --#
st.set_page_config(layout= "wide")

#-- Funções --#
def formataNumero(valor):
    if valor >= 1_000_000_000:
        return f'{valor / 1_000_000_000:.1f} b'
    if valor >= 1_000_000_000:
        return f'{valor / 1_000_000_000:.1f} m'
    if valor >= 1000:
        return f'{valor / 1000:.1f} k'
    
    return str(valor)

#-- Dados --#
dados = pd.read_csv('emissoes.csv')

#-- Tabelas --#

##Estados
emissoesEstados = dados.groupby('Estado')[['Emissão']].sum().reset_index()
emissoesEstados = dados.drop_duplicates(subset='Estado')[['Estado', 'lat', 'long']].merge(emissoesEstados, on='Estado').reset_index()
emissoesEstados.drop('index', axis=1, inplace=True)

##Setores
emissoesSetores = dados.groupby('Setor de emissão')[['Emissão']].sum().reset_index()

## Anos
emissoesAnos = dados.groupby('Ano')[['Emissão']].sum().sort_values(by='Ano').reset_index()

##Gás
emissoesGas = dados.groupby('Gás')[['Emissão']].sum().reset_index()

#-- Gráficos --#

##Estados
figMapaEmissoes = px.scatter_geo(emissoesEstados,
                                 lat='lat',
                                 lon='long',
                                 scope='south america',
                                 size='Emissão',
                                 hover_name='Estado',
                                 hover_data= {'lat': False, 'long': False},
                                 color= 'Estado',
                                 text='Estado',
                                 title='Total de emissões por estado')

##Setores
figEmissoesSetores = px.bar(emissoesSetores,
                            x='Emissão',
                            y='Setor de emissão',
                            color= 'Setor de emissão',
                            text_auto=True,
                            title='Total de emissões por setores')
figEmissoesSetores.update_layout(yaxis_title='', showlegend= False)

##Anos
figEmissoesAnos = px.line(emissoesAnos,
                          x='Ano',
                          y='Emissão',
                          title='Total de emissões por ano')

#-- Dashboards --#

st.title('Emissões de gases de efeito estufa')

tabHome, tabGas = st.tabs(['Home', 'Gás'])

with tabHome:
    col1, col2  = st.columns(2)
    with col1:
        st.metric("Total de emissoes", formataNumero(dados['Emissão'].sum()) + " de toneladas")
        st.plotly_chart(figMapaEmissoes)

    with col2:
        idxMaiorEmissao = emissoesAnos.index[emissoesAnos['Emissão'] == emissoesAnos['Emissão'].max()]
        anoMaisPoluente =  emissoesAnos.iloc[idxMaiorEmissao[0]]['Ano']
        emissoesAnoMaisPoluente = emissoesAnos.iloc[idxMaiorEmissao[0]]['Emissão']
        st.metric(f'Ano mais poluente: {anoMaisPoluente}', formataNumero(emissoesAnoMaisPoluente) + ' de toneladas')
        st.plotly_chart(figEmissoesSetores)
    
    st.plotly_chart(figEmissoesAnos)

with tabGas:
    col1, col2  = st.columns(2, border=True)
    with col1:
        idxMaiorEmissao = emissoesGas.index[emissoesGas['Emissão'] == emissoesGas['Emissão'].max()]
        st.metric('Gás com mais emissões: ', emissoesGas.iloc[idxMaiorEmissao[0]]['Gás'])

    with col2:
        idMenorEmissao = emissoesGas.index[emissoesGas['Emissão'] == emissoesGas['Emissão'].min()]
        st.metric('Gás com menos emissões: ', emissoesGas.iloc[idMenorEmissao[0]]['Gás'])


#st.dataframe(emissoesEstados)