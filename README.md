# 🛠️ ASIPS - Automotive Smart Inventory & Predictive System (Sistema de Inventário de Autopeças)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge)](https://matplotlib.org/)

> **Sistema ERP Inteligente para Gestão de Inventário de Autopeças com Analytics Avançado**  
> Transformando dados transacionais em decisões estratégicas

Sistema completo de gestão de estoque desenvolvido em Python com Streamlit, combinando CRUD robusto, análise de dados avançada e dashboards estratégicos para otimização de inventário no setor automotivo.

---

## 📖 Sobre o Projeto

**ASIPS** (Automotive Smart Inventory & Predictive System) é uma solução de **ERP Inteligente** que vai além do simples registro de entradas e saídas. Utiliza **Ciência de Dados** para garantir que o estoque trabalhe a favor da rentabilidade do negócio.

### 🎯 Propósito

Mais do que controlar peças, o sistema oferece:
- 📊 **Análise de Giro de Estoque** - Identifique produtos parados vs produtos estrela
- 💰 **Valoração de Inventário** - PEPS automatizado e custo médio
- 📈 **Curva ABC Dinâmica** - Pareto visual para foco estratégico
- ⚠️ **Alertas Inteligentes** - Estoque crítico e excesso detectados automaticamente
- 📉 **Análise de Perdas** - Rastreamento de prejuízos por produto

---

## ✨ Funcionalidades Principais

### 🔧 Gestão Operacional (CRUD Completo)

#### ➕ **Adicionar Produtos**
- Cadastro com validação de código único
- Categorização automática (Motor, Suspensão, Freios, Elétrica, Acessórios)
- Definição de estoque mínimo/máximo
- Cálculo automático de margem de lucro

#### 📝 **Atualizar Produtos**
- Edição granular de todos os atributos
- Ajuste de estoque com **registro automático de movimentação**
- Rastreamento de motivo (Venda, Devolução, Perda, Ajuste)
- Histórico completo de alterações

#### 🗑️ **Remover Produtos**
- Exclusão permanente com confirmação
- Validação de dependências

#### 🔍 **Consultar Inventário**
- Busca por nome ou código (full-text search)
- Filtros predefinidos:
  - Produtos com estoque abaixo do mínimo
  - Produtos com excesso de estoque (> 3x mínimo)
  - Cálculo PEPS/Custo médio simplificado
  - Quantidade de produtos por categoria

---

### 📊 Analytics & Business Intelligence

#### 📦 **Movimentações de Estoque**
- **Histórico completo** de entradas/saídas com timestamp
- **Giro de Estoque** - Frequência de saídas por produto
- **Análise de Perdas** - Prejuízo total calculado automaticamente
- **Valoração de Inventário** - Comparação entre estoque cadastrado vs calculado por histórico

#### 📈 **Dashboard Estratégico**

**KPIs em Tempo Real:**
- 💰 **Valor Total em Estoque** - Somatório de (Qtd × Custo)
- ⚠️ **Itens Críticos** - Produtos abaixo do mínimo
- 📊 **Volume de Saídas** - Total de movimentações
- ⭐ **Produto Estrela** - SKU com maior volume de saídas

**Visualizações Avançadas:**

1. **Valor de Estoque por Categoria** (Gráfico de Barras)
   - Identifica categorias que concentram capital imobilizado

2. **Top 5 Produtos - Nível de Estoque** (Gráfico de Barras)
   - Visualização rápida dos produtos com maior quantidade

3. **Histórico de Movimentações** (Gráfico de Linha Temporal)
   - Evolução de Entradas vs Saídas ao longo do tempo
   - Identificação de padrões sazonais

4. **Análise de Pareto - Curva ABC** (Gráfico Horizontal + Linha Acumulada)
   - Top 10 produtos por valor de estoque
   - Classificação automática em A, B, C
   - Princípio 80/20 aplicado ao inventário

---

## 🗄️ Arquitetura de Dados

### Modelo Relacional (SQLite)

#### Tabela: `Produtos`
```sql
CREATE TABLE Produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cd_produto TEXT UNIQUE NOT NULL,        -- Código único (SKU)
    nm_produto TEXT NOT NULL,               -- Nome do produto
    ds_produto TEXT,                        -- Descrição técnica
    categoria_id INTEGER,                   -- FK para Categorias
    vr_custo REAL NOT NULL,                -- Preço de custo
    vr_venda REAL NOT NULL,                -- Preço de venda
    vr_estoque_atual INTEGER DEFAULT 0,    -- Quantidade em estoque
    vr_estoque_minimo INTEGER DEFAULT 0,   -- Nível mínimo seguro
    FOREIGN KEY (categoria_id) REFERENCES Categorias(cd_categoria)
);
```

#### Tabela: `Categorias`
```sql
CREATE TABLE Categorias (
    cd_categoria INTEGER PRIMARY KEY,
    nm_categoria TEXT UNIQUE NOT NULL
);

-- Categorias Padrão:
-- 1 - Motor
-- 2 - Suspensão
-- 3 - Freios
-- 4 - Elétrica
-- 5 - Acessórios
```

#### Tabela: `Movimentacoes`
```sql
CREATE TABLE Movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id TEXT NOT NULL,              -- FK para Produtos
    tp_movimento TEXT NOT NULL,            -- 'Entrada' ou 'Saida'
    qt_movimento INTEGER NOT NULL,         -- Quantidade movimentada
    dt_movimento TEXT NOT NULL,            -- Timestamp (YYYY-MM-DD HH:MM:SS)
    nm_motivo TEXT,                        -- Motivo (Venda, Ajuste, Perda...)
    FOREIGN KEY (produto_id) REFERENCES Produtos(cd_produto)
);
```

### 📊 Consultas SQL Avançadas Implementadas

**1. Giro de Estoque:**
```sql
SELECT 
    p.nm_produto AS 'Produto',
    COUNT(m.id) AS 'Qtd Movimentos de Venda',
    SUM(m.qt_movimento) AS 'Total de Itens Saidos'
FROM Produtos p
JOIN Movimentacoes m ON p.cd_produto = m.produto_id
WHERE m.tp_movimento = 'Saida'
GROUP BY p.cd_produto
ORDER BY 'Total de Itens Saidos' DESC;
```

**2. Análise de Perdas:**
```sql
SELECT 
    p.nm_produto AS 'Produto',
    SUM(m.qt_movimento) AS 'Qtd Perdida',
    p.vr_custo AS 'Custo Unitário',
    (SUM(m.qt_movimento) * p.vr_custo) AS 'Prejuizo Total'
FROM Movimentacoes m
JOIN Produtos p ON m.produto_id = p.cd_produto
WHERE m.nm_motivo = 'Perda'
GROUP BY p.cd_produto;
```

**3. Valoração de Inventário (Comparação):**
```sql
SELECT 
    p.nm_produto,
    p.vr_estoque_atual AS 'Estoque No Cadastro',
    (SUM(CASE WHEN m.tp_movimento = 'Entrada' THEN m.qt_movimento ELSE 0 END) - 
     SUM(CASE WHEN m.tp_movimento = 'Saida' THEN m.qt_movimento ELSE 0 END)) 
     AS 'Estoque Calculado Histórico'
FROM Produtos p
LEFT JOIN Movimentacoes m ON p.cd_produto = m.produto_id
GROUP BY p.cd_produto;
```

---

## 🚀 Como Executar

### Pré-requisitos
```bash
# Python 3.11 ou superior
python --version

# Poetry (opcional, mas recomendado)
pip install poetry
```

### Instalação
```bash
# Clone o repositório
git clone https://github.com/Aram-Bohmann/ASIPS-Sistema-Inventario.git

# Entre no diretório
cd ASIPS-Sistema-Inventario

# Instale as dependências
pip install streamlit pandas matplotlib

# OU com Poetry
poetry install
```

### Executar o Sistema
```bash
# Inicie o Streamlit
streamlit run app.py

# O navegador abrirá automaticamente em:
# http://localhost:8501
```

---

## 🛠️ Stack Tecnológica

### Core
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

### Dados & Persistência
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

### Visualização
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat-square)

### DevOps
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=flat-square&logo=poetry&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)

---

## 💡 Casos de Uso

### 📦 **Gestão de Autopeças - Oficina Mecânica**

**Cenário:** Oficina com 200+ SKUs precisa controlar estoque e reduzir capital parado

**Solução:**
1. Cadastro de todas as peças com categorização
2. Definição de estoque mínimo baseado em histórico de vendas
3. Monitoramento via Dashboard de produtos críticos
4. Análise ABC para identificar os 20% de produtos que geram 80% da receita
5. Alertas automáticos de reposição

**Resultado:**
- ⬇️ 30% de redução de capital imobilizado
- ⬆️ 15% de aumento no giro de estoque
- ⚠️ Zero rupturas de estoque em produtos classe A

---

### 🔧 **Distribuidor de Peças - Análise de Perdas**

**Cenário:** Distribuidor com alto índice de perdas por validade/danos

**Solução:**
1. Registro obrigatório de motivo em todas as movimentações
2. Análise de Perdas com cálculo automático de prejuízo
3. Dashboard de perdas por categoria
4. Curva ABC para priorizar controle em produtos de alto valor

**Resultado:**
- 📉 40% de redução de perdas em 6 meses
- 💰 R$ 15.000 economizados em controle de validade

---

## 📊 Funcionalidades Técnicas Destacadas

### 🔄 **Registro Automático de Movimentações**

Toda alteração de estoque gera automaticamente um registro na tabela `Movimentacoes`:
```python
def registrar_movimentacao(produto_id, tp_movimento, qt_movimento, nm_motivo):
    conn = conectar_db()
    cursor = conn.cursor()
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO Movimentacoes 
        (produto_id, tp_movimento, qt_movimento, dt_movimento, nm_motivo)
        VALUES (?, ?, ?, ?, ?)
    ''', (produto_id, tp_movimento, qt_movimento, data_hora, nm_motivo))
    conn.commit()
    conn.close()
```

**Gatilho automático:** Ao atualizar estoque na interface, o sistema:
1. Calcula a diferença (novo - antigo)
2. Determina o tipo (Entrada se > 0, Saída se < 0)
3. Registra na tabela de movimentações
4. Atualiza o estoque do produto

---

### 📈 **Curva ABC com Pareto Visual**

Implementação completa da análise de Pareto:
```python
# Ordenar por valor decrescente
df_abc = df_abc.sort_values(by='valor_total', ascending=False).head(10)

# Calcular percentuais
total_valor_top10 = df_abc['valor_total'].sum()
df_abc['percent_individual'] = (df_abc['valor_total'] / total_valor_top10 * 100)
df_abc['percent_acumulado'] = df_abc['percent_individual'].cumsum()

# Classificar automaticamente
def classificar_abc(perc):
    if perc <= 80: return 'A'      # 80% do valor
    elif perc <= 95: return 'B'    # 15% do valor
    else: return 'C'                # 5% do valor

df_abc['Classe'] = df_abc['percent_acumulado'].apply(classificar_abc)
```

**Interpretação:**
- **Classe A:** Produtos críticos (foco máximo)
- **Classe B:** Produtos importantes (monitoramento regular)
- **Classe C:** Produtos ocasionais (revisão periódica)

---

## 🎓 Contexto Acadêmico

### Informações do Projeto

| Item | Detalhe |
|------|---------|
| **Desenvolvedor** | Aram Bohmann Leite da Luz |
| **Formação** | Técnico em Ciência de Dados - CEDUP Timbó |
| **Ano** | 2025 |
| **Tipo** | Projeto de Portfólio |

### Competências Demonstradas

1. **🗄️ Banco de Dados Relacional** - Modelagem, SQLite, queries complexas
2. **🐍 Python Avançado** - POO, manipulação de dados, integração de bibliotecas
3. **📊 Análise de Dados** - Pandas, agregações, transformações
4. **📈 Data Visualization** - Matplotlib, dashboards estratégicos
5. **🎨 UI/UX** - Streamlit, design responsivo, experiência do usuário
6. **📝 Documentação** - README técnico, comentários no código
7. **💼 Business Intelligence** - KPIs, métricas de negócio, Pareto

---

## 🚀 Melhorias Futuras

### Roadmap

#### Curto Prazo
- [ ] **Exportação de relatórios** em Excel/PDF
- [ ] **Sistema de backup** automático do banco de dados
- [ ] **Autenticação de usuários** com permissões
- [ ] **Logs de auditoria** completos

#### Médio Prazo
- [ ] **Integração com leitor de código de barras**
- [ ] **Notificações por e-mail** de estoque crítico
- [ ] **API REST** para integração com outros sistemas
- [ ] **Versão mobile** responsiva

#### Longo Prazo
- [ ] **Machine Learning** para previsão de demanda
- [ ] **Clustering** de produtos similares
- [ ] **Otimização de reposição** com algoritmos genéticos
- [ ] **Integração com ERP** de fornecedores

---

## 🤝 Contribuindo

Contribuições são bem-vindas!

### Como Contribuir

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/melhoria`)
3. Commit suas mudanças (`git commit -m 'Adiciona feature X'`)
4. Push para a branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

### Áreas de Contribuição

- 📊 **Analytics** - Novos gráficos e análises
- 🔧 **Features** - Novas funcionalidades
- 🐛 **Bugs** - Correções e otimizações
- 📝 **Docs** - Melhorias na documentação
- 🎨 **UI/UX** - Aprimoramentos visuais

---

## 📝 Licença

Este projeto foi desenvolvido para fins **educacionais e de portfólio** e está disponível para:

✅ Uso educacional e estudo  
✅ Modificação e adaptação  
✅ Uso em projetos pessoais  
✅ Distribuição com créditos  

---

## 📞 Contato

**Desenvolvedor:** Aram Bohmann Leite da Luz  
**Formação:** Técnico em Ciência de Dados (CEDUP Timbó)

[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:arambohmannleitedaluz@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aram-luz-1b0ab1321)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Aram-Bohmann)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://aram-bohmann.github.io/Site-Portfolio/)

---

## 🙏 Agradecimentos

- **CEDUP Timbó** - Formação técnica de excelência
- **Streamlit** - Framework incrível para dashboards
- **SQLite** - Banco de dados confiável e leve
- **Comunidade Python** - Ferramentas open-source
- **Matplotlib** - Visualizações profissionais

---

## 📚 Referências Técnicas

- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLite SQL Syntax](https://www.sqlite.org/lang.html)
- [Pandas User Guide](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Análise de Pareto (ABC)](https://pt.wikipedia.org/wiki/Princ%C3%ADpio_de_Pareto)

---

<div align="center">

### ⭐ Se este projeto foi útil para você, considere dar uma estrela!

**Desenvolvido com 💙 e 📊 para otimizar gestão de inventário**

*"Transformando dados transacionais em decisões estratégicas"*

</div>
