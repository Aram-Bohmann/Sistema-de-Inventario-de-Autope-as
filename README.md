🛠️ Sistema de Gestão de Inventário de Autopeças (ASIPS)
O Automotive Smart Inventory & Predictive System (ASIPS) é uma solução ERP (Enterprise Resource Planning) completa, desenvolvida para o setor de autopeças. O sistema une a robustez de um banco de dados relacional com o poder da Ciência de Dados para otimizar a cadeia de suprimentos e facilitar a tomada de decisão.

📋 Visão Geral
O projeto gerencia o fluxo de mercadorias, garante a integridade transacional via SQLite e utiliza bibliotecas de análise de dados para transformar registros brutos em insights estratégicos.

🚀 Funcionalidades Principais
1. Engenharia de Dados & CRUD
Gestão de Produtos: Cadastro completo com código, Nome, Descrição Técnica, Categoria, Preços (Custo/Venda) e níveis de estoque (Atual/Mínimo).

Integridade Transacional: Banco de dados SQLite com tabelas normalizadas e uso de chaves estrangeiras.

Controle de Movimentação: Registro automatizado de Entradas e Saídas com log de data, hora e motivo (Venda, Devolução, Perda, Ajuste).

2. Analytics & Consultas Estratégicas
O sistema executa queries complexas para fornecer relatórios de:

Giro de Estoque: Identificação da frequência de saída por código.

Ruptura de Estoque: Alertas para itens abaixo do estoque mínimo.

Valoração de Inventário: Cálculo de ativos baseado em custo real e histórico.

Histórico de Perdas: Monitoramento de prejuízos por motivo de perda.

3. Dashboard Interativo
Visualização de dados em tempo real utilizando Streamlit:

KPIs Financeiros: Valor total em estoque e volume de saídas.

Análise de Categorias: Distribuição de valor por tipo de peça (Motor, Suspensão, etc.).

Tendência Temporal: Gráfico de linhas comparando Entradas vs. Saídas ao longo do tempo.

Top 5 SKUs: Ranking de produtos com maior nível de estoque.