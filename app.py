import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


# Configurando a página do streamlit
st.set_page_config(page_title="Gestão de Inventário Autopeças", layout="wide")


# Criando uma função para conexão do banco de dados do SQLite
def conectar_db():
    return sqlite3.connect('SQLite\inventario.db')


# Populando a tabela categorias quando não houver dados
def popular_categorias():
    dados = [
        (1, 'Motor'),
        (2, 'Suspensão'),
        (3, 'Freios'),
        (4, 'Elétrica'),
        (5, 'Acessórios')]
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO Categorias (cd_categoria, nm_categoria) VALUES (?, ?)", dados)
    conn.commit()
    conn.close()
popular_categorias()

# Função para registrar movimentações de estoque
def registrar_movimentacao(produto_id, tp_movimento, qt_movimento, nm_motivo):
    conn = conectar_db()
    cursor = conn.cursor()
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute('''INSERT INTO Movimentacoes (produto_id, tp_movimento, qt_movimento, dt_movimento, nm_motivo)
                          VALUES (?, ?, ?, ?, ?)''', (produto_id, tp_movimento, qt_movimento, data_hora, nm_motivo))
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao registrar movimentação: {e}")
    finally:
        conn.close()


# Cabeçalho com as opções do CRUD
st.title("🛠️ Sistema de Inventário de Autopeças")
st.markdown("<hr>", unsafe_allow_html=True)
menu = ["Sobre", "Adicionar Produto", "Atualizar/Remover", "Consultar", "Movimentações", "Dashboard"]
escolha = st.sidebar.radio("Menu de Navegação", menu)

# Sobre
if escolha == "Sobre":
    st.subheader("👋 Bem-vindo ao ASIPS")
    st.caption("Automotive Smart Inventory & Predictive System")
    
    st.markdown("""
    Este sistema é uma solução de **ERP Inteligente** projetada para transformar a gestão de inventário no setor de autopeças. 
    Mais do que um simples registro de entradas e saídas, o sistema utiliza **Ciência de Dados** para garantir que o estoque 
    trabalhe a favor da rentabilidade do negócio.
    """)


    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🏛️ Integridade")
        st.write("Gestão transacional via SQLite, garantindo que cada parafuso seja contabilizado sem redundâncias.")
    with col_b:
        st.markdown("### 📊 Analytics")
        st.write("Dashboards dinâmicos que traduzem números em insights visuais sobre o giro de estoque.")

    st.markdown("---")

    st.subheader("🛠️ Arquitetura Técnica")
    
    tab1, tab2, tab3 = st.tabs(["Linguagem & Interface", "Dados & Gráficos", "DevOps & Ferramentas"])
    
    with tab1:
        st.markdown("""
        * **Python 3.x**: Core do sistema.
        * **Streamlit**: Interface web reativa e moderna.
        * **Pandas*: Processamento de dados de alta performance.
        """)
    
    with tab2:
        st.markdown("""
        * **SQLite**: Banco de dados relacional robusto e local.
        * **SQL**: Queries complexas para cálculos de PEPS e Giro de Estoque.
        * **Matplotlib**: Visualizações customizadas para análises estratégicas.
        """)
        
    with tab3:
        st.markdown("""
        * **Poetry**: Gestão rigorosa de dependências e ambientes virtuais.
        * **VS Code**: Ambiente de desenvolvimento principal.
        * **Git**: Controle de versão e histórico do projeto.
        """)

    st.markdown("---")

    col_foto, col_info = st.columns([1, 3])
    with col_info:
        st.subheader("👤 Sobre o Desenvolvedor")
        st.markdown(f"""
        **Aram Bohmann Leite Da Luz** *Técnico em Ciência de Dados (CEDUP Timbó)*
        
        Especialista em transformar dados brutos em decisões estratégicas. Minha abordagem une o rigor técnico da análise 
        com a clareza do **storytelling**, permitindo que insights complexos sejam compreendidos por qualquer stakeholder.
        """)

        st.markdown("""
        [LinkedIn](https://www.linkedin.com/in/aram-luz-1b0ab1321/) | 
        [GitHub](https://www.github.com/Aram-Bohmann) | 
        [Portfólio](https://aram-bohmann.github.io/Site-Portfolio/) | 
        [Email](mailto:arambohmannleitedaluz@gmail.com)
        """)

# Adicionar Produto
elif escolha == "Adicionar Produto":
    st.subheader("Cadastro de Novo Produto")
    with st.form("form_adicionar"):
        col1, col2 = st.columns(2)
        cod = col1.text_input("Código Único do Produto")
        nome = col2.text_input("Nome do Produto")
        desc = st.text_area("Descrição Técnica")

        cat = col1.selectbox("Código da Categoria", ["1 - Motor", "2 - Suspensão", "3 - Freios", "4 - Elétrica", "5 - Acessórios"])
        custo = col1.number_input("Preço de Custo (R$)", min_value=0.0, format="%.2f")
        venda = col2.number_input("Preço de Venda (R$)", min_value=0.0, format="%.2f")
        estoque = col1.number_input("Estoque Atual", min_value=0)
        minimo = col2.number_input("Estoque Mínimo permitido", min_value=0)
        
        btn_cadastrar = st.form_submit_button("Salvar Produto")

    if btn_cadastrar:
        if cod and nome:
            try:
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Produtos (cd_produto, nm_produto, ds_produto, categoria_id, vr_custo, vr_venda, vr_estoque_atual, vr_estoque_minimo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (cod, nome, desc, cat, custo, venda, estoque, minimo))
                conn.commit()
                conn.close()
                st.success(f"Produto {nome} cadastrado com sucesso!")
            except sqlite3.IntegrityError:
                st.error("Erro: Este código já existe no sistema.")
        else:
            st.warning("Tente novamente, preenchendo todos os campos obrigatórios.")

# Atualizar/Remover Produto
elif escolha == "Atualizar/Remover":
    st.subheader("Produtos Existentes")
    if st.button("Atualizar Tabela", key="atualizar_produtos"):
        st.rerun()
    conn = conectar_db()
    query1 = "SELECT * FROM Produtos"
    df = pd.read_sql_query(query1, conn)
    conn.close()
    st.dataframe(df)

    
    st.subheader("Gerir Produtos Existentes")
    conn = conectar_db()
    df_prods = pd.read_sql_query("SELECT cd_produto, nm_produto, vr_venda, vr_estoque_atual FROM Produtos", conn)
    conn.close()

    cd_selecionado = st.selectbox("Selecione o produto pelo Código", df_prods['cd_produto'])

    col1, col2 = st.columns(2)
    with col1:
        novo_nome = st.text_input("Novo Nome do produto")
        if st.button("Atualizar Nome"):
            conn = conectar_db()
            conn.execute("UPDATE Produtos SET nm_produto = ? WHERE cd_produto = ?", (novo_nome, cd_selecionado))
            conn.commit()
            conn.close()
            st.success("Nome atualizado!")

        nova_descricao = st.text_input("Nova Descrição do produto")
        if st.button("Atualizar Descrição"):
            conn = conectar_db()
            conn.execute("UPDATE Produtos SET ds_produto = ? WHERE cd_produto = ?", (nova_descricao, cd_selecionado))
            conn.commit()
            conn.close()
            st.success("Descrição atualizada!")

        nova_categoria = st.number_input("Nova Categoria do produto", min_value=1, max_value=5)
        if st.button("Atualizar Categoria"):
            conn = conectar_db()
            conn.execute("UPDATE Produtos SET categoria_id = ? WHERE cd_produto = ?", (nova_categoria, cd_selecionado))
            conn.commit()
            conn.close()
            st.success("Categoria atualizada!")

        novo_preco_custo = st.number_input("Novo Custo de produção", min_value=0.0)
        if st.button("Atualizar Custo"):
            conn = conectar_db()
            conn.execute("UPDATE Produtos SET vr_custo = ? WHERE cd_produto = ?", (novo_preco_custo, cd_selecionado))
            conn.commit()
            conn.close()
            st.success("Preço atualizado!")

        novo_preco_vendas = st.number_input("Novo Preço de Venda", min_value=0.0)
        if st.button("Atualizar Preço"):
            conn = conectar_db()
            conn.execute("UPDATE Produtos SET vr_venda = ? WHERE cd_produto = ?", (novo_preco_vendas, cd_selecionado))
            conn.commit()
            conn.close()
            st.success("Preço atualizado!")

        novo_estoque_atual = st.number_input("Novo Estoque Atual", min_value=0)

        nm_motivo = st.text_input("Motivo da alteração (Venda, Devolução, Perda, Ajuste)", "Ajuste")

        if st.button("Atualizar Estoque"):
            conn = conectar_db()
            cursor = conn.cursor()
            
            cursor.execute("SELECT vr_estoque_atual FROM Produtos WHERE cd_produto = ?", (cd_selecionado,))
            estoque_antigo = cursor.fetchone()[0]
            
            diferenca = novo_estoque_atual - estoque_antigo
            
            if diferenca != 0:
                tp_movimento = "Entrada" if diferenca > 0 else "Saida"
                quantidade_mov = abs(diferenca)
                
                cursor.execute("UPDATE Produtos SET vr_estoque_atual = ? WHERE cd_produto = ?", (novo_estoque_atual, cd_selecionado))
                
                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute('''INSERT INTO Movimentacoes (produto_id, tp_movimento, qt_movimento, data_hora, nm_motivo) 
                                  VALUES (?, ?, ?, ?, ?)''', (cd_selecionado, tp_movimento, quantidade_mov, data_hora, nm_motivo))
                
                conn.commit()
                st.success(f"Estoque atualizado! Movimentação de {tp_movimento} registrada.")
            else:
                st.info("O novo valor é igual ao atual. Nenhuma movimentação registrada.")
            
            conn.close()

        novo_estoque_minimo = st.number_input("Novo Estoque Mínimo", min_value=0.0)
        if st.button("Atualizar Estoque Mínimo"):
            conn = conectar_db()
            conn.execute("UPDATE Produtos SET vr_estoque_minimo = ? WHERE cd_produto = ?", (novo_estoque_minimo, cd_selecionado))
            conn.commit()
            conn.close()
            st.success("Estoque atualizado!")

    with col2:
        st.write("Cuidado ao remover produtos!")
        if st.button("Remover Produto Permanentemente"):
            conn = conectar_db()
            conn.execute("DELETE FROM Produtos WHERE cd_produto = ?", (cd_selecionado,))
            conn.commit()
            conn.close()
            st.warning("Produto removido.")
            st.rerun()

# Consultar Produto
elif escolha == "Consultar":

    st.subheader("Consulta de Inventário")
    busca = st.text_input("Procurar pelo nome ou código")

    if st.button("Atualizar Tabela", key="atualizar_produtos"):
        st.rerun()
    conn = conectar_db()
    query2 = "SELECT cd_produto AS 'Código', nm_produto AS 'Produto', ds_produto AS 'Descrição', categoria_id AS 'Categoria', vr_custo AS 'Custo', vr_venda AS 'Valor de Venda', vr_estoque_atual AS 'Estoque', vr_estoque_minimo AS 'Estoque Mínimo' FROM Produtos"
    if busca:
        query2 = f"SELECT cd_produto AS 'Código', nm_produto AS 'Produto', ds_produto AS 'Descrição', categoria_id AS 'Categoria', vr_custo AS 'Custo', vr_venda AS 'Valor de Venda', vr_estoque_atual AS 'Estoque', vr_estoque_minimo AS 'Estoque Mínimo' FROM Produtos WHERE nm_produto LIKE '%{busca}%' OR cd_produto LIKE '%{busca}%'"
    
    df = pd.read_sql_query(query2, conn)
    conn.close()
    
    st.dataframe(df, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("Consultas prédeterminadas")

    st.write("Produtos com estoque abaixo do mínimo:")
    conn = conectar_db()
    query3 = "SELECT cd_produto AS 'Código', nm_produto AS 'Produto', ds_produto AS 'Descrição', categoria_id AS 'Categoria', vr_custo AS 'Custo', vr_venda AS 'Valor de Venda', vr_estoque_atual AS 'Estoque', vr_estoque_minimo AS 'Estoque Mínimo' FROM Produtos WHERE vr_estoque_atual < vr_estoque_minimo"
    df = pd.read_sql_query(query3, conn)
    conn.close()
    st.dataframe(df, use_container_width=True)

    st.write("Produtos com muito estoque")
    conn = conectar_db()
    query4 = "SELECT cd_produto AS 'Código', nm_produto AS 'Produto', ds_produto AS 'Descrição', categoria_id AS 'Categoria', vr_custo AS 'Custo', vr_venda AS 'Valor de Venda', vr_estoque_atual AS 'Estoque', vr_estoque_minimo AS 'Estoque Mínimo' FROM Produtos WHERE vr_estoque_atual > (vr_estoque_minimo * 3)"
    df = pd.read_sql_query(query4, conn)
    conn.close()
    st.dataframe(df, use_container_width=True)

    st.write("Cálculo PEPS / Custo Médio Simplificado")
    conn = conectar_db()
    query5 = "SELECT cd_produto AS 'Código', nm_produto AS 'Produto', (vr_estoque_atual * vr_custo) as 'Custo total (R$)' FROM Produtos"
    df = pd.read_sql_query(query5, conn)
    conn.close()
    st.dataframe(df, use_container_width=True)

    st.write("Quantidade de Produtos por Categoria")
    conn = conectar_db()
    query6 = "SELECT c.nm_categoria AS 'Categoria', COUNT(p.cd_produto) AS 'Quantidade de Produtos' FROM Categorias c LEFT JOIN Produtos p ON c.cd_categoria = p.categoria_id GROUP BY c.nm_categoria"
    df = pd.read_sql_query(query6, conn)
    conn.close()
    st.dataframe(df, use_container_width=True)

# Movimentações
elif escolha == "Movimentações":
    st.subheader("Histórico de Movimentações")
    conn = conectar_db()
    df_mov = pd.read_sql_query("SELECT * FROM Movimentacoes ORDER BY data_hora DESC", conn)
    conn.close()
    st.dataframe(df_mov, use_container_width=True)

    st.write("Giro de Estoque (Frequência de Saídas)")
    conn = conectar_db()
    query7 = "SELECT p.nm_produto AS 'Produto',COUNT(m.id) AS 'Qtd Movimentos de Venda',SUM(m.qt_movimento) AS 'Total de Itens Saidos' FROM Produtos p JOIN Movimentacoes m ON p.cd_produto = m.produto_id WHERE m.tp_movimento = 'Saida' GROUP BY p.cd_produto ORDER BY 'Total de Itens Saidos' DESC"
    df = pd.read_sql_query(query7, conn)
    conn.close()
    st.dataframe(df, use_container_width=True)

    st.write("Histórico de Perdas")
    conn = conectar_db()
    query8 = "SELECT p.nm_produto AS 'Produto', SUM(m.qt_movimento) AS 'Qtd Perdida', p.vr_custo AS 'Custo Unitário', (SUM(m.qt_movimento) * p.vr_custo) AS 'Prejuizo Total' FROM Movimentacoes m JOIN Produtos p ON m.produto_id = p.cd_produto WHERE m.nm_motivo = 'Perda' GROUP BY p.cd_produto"
    df = pd.read_sql_query(query8, conn)
    conn.close()
    st.dataframe(df, use_container_width=True)

    st.write("Valoração de Inventário")
    conn = conectar_db()
    query9 = "SELECT p.nm_produto, p.vr_estoque_atual AS 'Estoque No Cadastro', SUM(CASE WHEN m.tp_movimento = 'Entrada' THEN m.qt_movimento ELSE 0 END) - SUM(CASE WHEN m.tp_movimento = 'Saida' THEN m.qt_movimento ELSE 0 END) AS 'Estoque Calculado Histórico' FROM Produtos p LEFT JOIN Movimentacoes m ON p.cd_produto = m.produto_id GROUP BY p.cd_produto"
    df = pd.read_sql_query(query9, conn)
    conn.close()
    st.dataframe(df, use_container_width=True)

# Dashboard
elif escolha == "Dashboard":
    st.subheader("Dashboard Estratégico")
    conn = conectar_db()

    col1, col2, col3, col4 = st.columns(4)
    valor_total = pd.read_sql_query("SELECT SUM(vr_estoque_atual * vr_custo) FROM Produtos", conn).iloc[0,0] or 0
    col1.metric("Valor em Estoque", f"R$ {valor_total:,.2f}")
    itens_criticos = pd.read_sql_query("SELECT COUNT(*) FROM Produtos WHERE vr_estoque_atual < vr_estoque_minimo", conn).iloc[0,0]
    col2.metric("Itens Críticos", itens_criticos, delta="Abaixo do Mínimo", delta_color="inverse")
    total_saidas = pd.read_sql_query("SELECT SUM(qt_movimento) FROM Movimentacoes WHERE tp_movimento = 'Saida'", conn).iloc[0,0] or 0
    col3.metric("Volume de Saídas", int(total_saidas))
    try:
        top_sku = pd.read_sql_query("SELECT p.nm_produto FROM Produtos p JOIN Movimentacoes m ON p.cd_produto = m.produto_id WHERE m.tp_movimento = 'Saida' GROUP BY p.cd_produto ORDER BY SUM(m.qt_movimento) DESC LIMIT 1", conn).iloc[0,0]
        col4.metric("Produto Estrela", top_sku)
    except:
        col4.metric("Produto Estrela", "N/A")

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 💰 Valor de Estoque por Categoria")
        query_cat = "SELECT c.nm_categoria, SUM(p.vr_estoque_atual * p.vr_custo) as valor FROM Produtos p JOIN Categorias c ON p.categoria_id = c.cd_categoria GROUP BY c.nm_categoria"
        df_cat = pd.read_sql_query(query_cat, conn)
        
        if not df_cat.empty:
            fig, ax = plt.subplots()
            ax.bar(df_cat['nm_categoria'], df_cat['valor'], color='#2E86C1')
            ax.set_ylabel("Valor (R$)")
            plt.xticks(rotation=0) 
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Sem dados de categorias.")

    with c2:
        st.markdown("### 📦 Top 5 Produtos - Nível de Estoque")
        df_estoque = pd.read_sql_query("SELECT nm_produto, vr_estoque_atual FROM Produtos ORDER BY vr_estoque_atual DESC LIMIT 5", conn)
        
        if not df_estoque.empty:
            fig, ax = plt.subplots()
            ax.bar(df_estoque['nm_produto'], df_estoque['vr_estoque_atual'], color='#28B463')
            ax.set_ylabel("Qtd em Estoque")
            plt.xticks(rotation=0)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Sem produtos cadastrados.")

    st.markdown("---")

    st.markdown("### 📉 Histórico de Movimentações (Entradas vs Saídas)")
    query_temporal = "SELECT SUBSTR(data_hora, 1, 10) as data, tp_movimento, SUM(qt_movimento) as total FROM Movimentacoes GROUP BY data, tp_movimento"
    df_temp = pd.read_sql_query(query_temporal, conn)

    if not df_temp.empty:
        df_pivot = df_temp.pivot(index='data', columns='tp_movimento', values='total').fillna(0)
        fig, ax = plt.subplots(figsize=(10, 4))
        df_pivot.plot(kind='line', marker='o', ax=ax)
        ax.set_title("Evolução Temporal")
        plt.xticks(rotation=0)
        plt.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
    else:
        st.info("Sem histórico temporal.")

    st.markdown("---")

    st.markdown("### 📊 Análise de Pareto (Curva ABC)")
    query_abc = "SELECT nm_produto, (vr_estoque_atual * vr_custo) as valor_total FROM Produtos"
    df_abc = pd.read_sql_query(query_abc, conn)

    if not df_abc.empty:

        df_abc = df_abc.sort_values(by='valor_total', ascending=False).head(10)

        total_valor_top10 = df_abc['valor_total'].sum()
        df_abc['percent_individual'] = (df_abc['valor_total'] / total_valor_top10 * 100)
        df_abc['percent_acumulado'] = df_abc['percent_individual'].cumsum()
        
        col_abc1, col_abc2 = st.columns([2, 1])
        
        with col_abc1:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            df_abc_plot = df_abc.iloc[::-1] 
            
            ax.barh(df_abc_plot['nm_produto'], df_abc_plot['percent_individual'], 
                    color='blue', alpha=0.3, label='Valor Individual (%)')
            
            ax.plot(df_abc_plot['percent_acumulado'], df_abc_plot['nm_produto'], 
                    color='red', marker='D', ms=5, label='Acumulado (%)')
            
            ax.set_xlim(0, 110)
            ax.set_xlabel("Percentual (%)")
            ax.set_title("Top 10 Produtos - Curva ABC (Vista Horizontal)")
            
            plt.legend(loc='lower right')
            plt.tight_layout()
            st.pyplot(fig)
            
        with col_abc2:
            def classificar_abc(perc):
                if perc <= 80: return 'A'
                elif perc <= 95: return 'B'
                else: return 'C'
                
            df_abc['Classe'] = df_abc['percent_acumulado'].apply(classificar_abc)
            st.write("**Top 10 - Classificação:**")
            st.dataframe(df_abc[['nm_produto', 'Classe']].sort_values(by='Classe'), use_container_width=True)

    conn.close()