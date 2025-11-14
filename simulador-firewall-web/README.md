# 🧱 Simulador de Filtro de Pacotes (Firewall)

Simulador profissional que reproduz o funcionamento básico de um firewall de filtragem de pacotes, analisando IPs e portas para permitir ou bloquear conexões com interface colorida (terminal) e **nova interface web moderna com Flask**.

## 🎯 Descrição

O sistema simula um firewall completo capaz de:
- ✅ Ler regras de permissão e bloqueio de um arquivo JSON
- 🔍 Testar conexões usando sockets para verificar conectividade
- 🛡️ Aplicar regras de filtragem para IPs e portas
- 📊 Exibir estatísticas dos testes realizados
- 🎮 Modo interativo para testar pacotes personalizados
- 🎨 Interface colorida e profissional no terminal
- 🌐 **NOVO: Interface web moderna com Flask e HTML/CSS/JavaScript**
- ⏰ Registro de data/hora das execuções

## 🆕 O QUE FOI ADICIONADO (Interface Web)

### Interface Web com Flask
Uma interface web completa foi adicionada ao projeto, permitindo:

1. **Teste de Pacotes via Web**
   - Formulário simples para testar IP + Porta
   - Teste de conectividade em tempo real
   - Resultado visual (PERMITIDO/BLOQUEADO)
   - Histórico de testes com timestamp

2. **Gerenciamento de Regras via Web**
   - Visualizar todas as regras em tabela
   - Adicionar novas regras com modal
   - Editar regras existentes
   - Deletar regras com confirmação
   - Persistência em arquivo JSON

3. **Estatísticas em Tempo Real**
   - Cards visuais mostrando contagem
   - Permitidos, Bloqueados, Total
   - Atualização automática

4. **API RESTful**
   - 7 endpoints funcionais
   - Validação de entrada
   - Tratamento de erros

## 🛠️ Tecnologias

### Backend (Terminal Original)
**Linguagem:** Python 3

**Bibliotecas:**
- `socket` - Para teste de conexões de rede
- `json` - Para leitura das regras de firewall
- `datetime` - Para registro de horário das execuções

### Frontend Web (NOVO)
**Backend Web:** Flask 3.0.0 (Python)
- Processamento de requisições
- API RESTful
- Gerenciamento de regras

**Frontend Web:** HTML5 + CSS3 + JavaScript Vanilla
- Interface responsiva
- Comunicação com API via Fetch
- Animações e transições

**Ferramentas:** GitHub, VS Code, Flask

## 📁 Estrutura do Projeto

```
simulador-firewall-web/
├── firewall.py                 # Script original (terminal)
├── firewall_web.py             # Backend Flask (interface web)
├── test_firewall.py            # 27 testes unitários
├── regras.json                 # Arquivo de configuração das regras
├── requirements.txt            # Dependências Python (Flask)
├── README.md                   # Este arquivo
│
├── templates/
│   └── index.html              # Interface web (HTML5)
│
├── static/
│   ├── css/
│   │   └── style.css           # Estilos da interface (CSS3)
│   └── js/
│       └── app.js              # Lógica da interface (JavaScript)
│
└── venv/                       # Ambiente virtual Python
```

## 👥 Equipe de Desenvolvimento e Divisão de Tarefas

### Projeto Original (Terminal)

| Integrante | Responsabilidades |
|------------|-------------------|
| **Gabriel Souza** | • Desenvolvimento do módulo de leitura de regras JSON<br>• Implementação da função `carregar_regras()`<br>• Tratamento de exceções e validação de dados<br>• Configuração do repositório GitHub |
| **Kayky Dias** | • Implementação da lógica de filtragem de pacotes<br>• Desenvolvimento da função `filtrar_pacote()`<br>• Criação do sistema de regras (PERMITIDO/BLOQUEADO)<br>• Implementação da política de segurança padrão |
| **Leandro de Morais** | • Teste de conexões com socket<br>• Implementação da função `verificar_porta()`<br>• Validação de conectividade de rede<br>• Testes de integração do sistema |
| **Levi Moraes** | • Documentação completa do projeto (README)<br>• Criação da interface visual com cores<br>• Desenvolvimento do modo interativo<br>• Testes finais e validação do sistema |
| **Enzo Antuna** | • Desenvolvimento da estrutura de dados do projeto<br>• Implementação da função principal `main()`<br>• Criação do sistema de estatísticas<br>• Identificação automática de serviços por porta |

### Refinamento e Interface Web (NOVO)

| Componente | O que foi feito |
|-----------|-----------------|
| **Backend Flask** (`firewall_web.py`) | • Adaptação do código Python para API RESTful<br>• 7 endpoints funcionais<br>• Validação completa de entrada<br>• Tratamento robusto de erros<br>• 400+ linhas bem documentadas |
| **Frontend Web** (`index.html`) | • Interface web moderna e responsiva<br>• Formulários para teste e gerenciamento<br>• Tabelas dinâmicas com dados<br>• Modal para adicionar/editar regras<br>• 200+ linhas de HTML5 |
| **Estilos CSS** (`style.css`) | • Design moderno com gradientes<br>• Layout responsivo (mobile + desktop)<br>• Animações suaves<br>• Cards visuais para estatísticas<br>• 600+ linhas de CSS3 |
| **JavaScript** (`app.js`) | • Comunicação com API via Fetch<br>• Validação de entrada no cliente<br>• Gerenciamento de modal<br>• Feedback visual imediato<br>• 300+ linhas de JavaScript |
| **Testes Unitários** (`test_firewall.py`) | • 27 testes unitários completos<br>• Cobertura 100% das funções<br>• Testes de integração<br>• Validação de todas as funcionalidades |

### 🤝 Trabalho Colaborativo

- **Planejamento inicial**: Toda a equipe
- **Code review**: Revisões cruzadas entre os membros
- **Testes**: Validação conjunta de funcionalidades
- **Documentação**: Contribuições de todos os membros
- **Interface Web**: Refinamento e adição de funcionalidades

## ⚙️ Instalação e Execução

### Pré-requisitos
- Python 3.x instalado
- Terminal com suporte a cores ANSI (Windows 10+, Linux, macOS)

### Opção 1: Executar o Terminal Original

```bash
# Execute o programa original (terminal)
python firewall.py
```

### Opção 2: Executar a Interface Web (NOVO)

#### 1. Criar Ambiente Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 2. Instalar Dependências

```bash
pip install Flask
```

#### 3. Executar a Aplicação Web

```bash
python firewall_web.py
```

#### 4. Abrir no Navegador

```
http://localhost:5000
```

### Opção 3: Executar os Testes

```bash
# Com ambiente virtual ativado
python -m unittest test_firewall -v

# Resultado esperado: 27 testes OK
```

## 📝 Configuração das Regras

O arquivo `regras.json` deve conter as regras de filtragem no seguinte formato:

```json
[
  {"ip": "8.8.8.8", "porta": 53, "acao": "BLOQUEADO"},
  {"ip": "192.168.0.10", "porta": 80, "acao": "PERMITIDO"},
  {"ip": "10.0.0.5", "porta": 22, "acao": "BLOQUEADO"},
  {"ip": "1.1.1.1", "porta": 443, "acao": "PERMITIDO"}
]
```

**Campos:**
- `ip` - Endereço IP a ser filtrado
- `porta` - Número da porta (1-65535)
- `acao` - "PERMITIDO" ou "BLOQUEADO"
- `descricao` (opcional) - Descrição da regra

## 🔍 Funcionamento

### Terminal Original

O firewall executa automaticamente uma bateria de testes ao iniciar:

1. **Carrega as regras** do arquivo `regras.json`
2. **Exibe as regras** configuradas de forma organizada
3. **Testa cada pacote** verificando:
   - 📡 **Conectividade real** - Testa se a porta responde (ABERTA/FECHADA)
   - 🛡️ **Aplicação das regras** - Decide PERMITIR ou BLOQUEAR
4. **Exibe estatísticas** ao final (total permitido vs bloqueado)
5. **Modo Interativo** - Permite testar pacotes personalizados

### Interface Web (NOVO)

A interface web oferece:

1. **Teste de Pacotes**
   - Preencha IP e Porta
   - Clique "Enviar"
   - Veja resultado em tempo real

2. **Gerenciamento de Regras**
   - Visualize em tabela
   - Adicione com modal
   - Edite ou delete facilmente

3. **Estatísticas**
   - Cards visuais
   - Atualização automática
   - Histórico de testes

## 📊 Exemplo de Saída (Terminal)

```
======================================================================
🧱 SIMULADOR DE FIREWALL - FILTRO DE PACOTES
======================================================================
⏰ Data/Hora: 01/11/2025 14:30:45

✅ 4 regra(s) carregada(s) com sucesso!

📋 Regras Configuradas:
──────────────────────────────────────────────────────────────────────
  1. IP: 8.8.8.8          | Porta: 53     | Ação: BLOQUEADO
  2. IP: 192.168.0.10     | Porta: 80     | Ação: PERMITIDO
  3. IP: 10.0.0.5         | Porta: 22     | Ação: BLOQUEADO
  4. IP: 1.1.1.1          | Porta: 443    | Ação: PERMITIDO
──────────────────────────────────────────────────────────────────────

🚀 EXECUTANDO TESTES AUTOMÁTICOS

🔍 Teste #1: 8.8.8.8:53
──────────────────────────────────────────────────────────────────────
  📡 Testando conectividade... ✓ Porta ABERTA (serviço respondendo)
  🛡️  Decisão do Firewall... ❌ BLOQUEADO
      → Tráfego negado (regra de bloqueio ou sem regra)
──────────────────────────────────────────────────────────────────────

📊 ESTATÍSTICAS DOS TESTES
──────────────────────────────────────────────────────────────────────
  ✅ Permitidos: 2
  ❌ Bloqueados: 2
  📦 Total de testes: 4
──────────────────────────────────────────────────────────────────────
```

## 🌐 Interface Web (NOVO)

A interface web oferece uma experiência moderna e intuitiva:

- **Formulário de Teste**: Teste pacotes com IP e Porta
- **Tabela de Regras**: Visualize todas as regras configuradas
- **Modal de Gerenciamento**: Adicione, edite ou delete regras
- **Estatísticas**: Cards mostrando contagem de regras
- **Histórico**: Veja todos os testes realizados
- **Responsivo**: Funciona em desktop e mobile

## 🎨 Recursos Visuais

### Terminal
- **Cores ANSI** para melhor visualização
- **Emojis** para identificação rápida
- **Separadores visuais** para organização
- **Destaques** em informações importantes
- **Identificação automática** de serviços conhecidos

### Web
- **Design moderno** com gradientes
- **Animações suaves** e transições
- **Layout responsivo** para todos os dispositivos
- **Cards visuais** para informações
- **Modal intuitivo** para gerenciamento

## 🔒 Política de Segurança

O simulador implementa uma **política de segurança padrão**:
- ✅ Pacotes **com regra PERMITIDO** → Autorizados
- ❌ Pacotes **com regra BLOQUEADO** → Negados
- ❌ Pacotes **sem regra definida** → Bloqueados por padrão (fail-safe)

## 📚 Serviços Identificados

O sistema reconhece automaticamente portas comuns:

| Porta | Serviço |
|-------|---------|
| 20/21 | FTP |
| 22    | SSH |
| 23    | Telnet |
| 25    | SMTP |
| 53    | DNS |
| 80    | HTTP |
| 110   | POP3 |
| 143   | IMAP |
| 443   | HTTPS |
| 3306  | MySQL |
| 3389  | RDP |
| 5432  | PostgreSQL |
| 8080  | HTTP Proxy |

## 🧪 Testes Unitários (27 Testes)

O projeto inclui 27 testes unitários que cobrem todas as funcionalidades:

```
✅ TestCarregarRegras (4 testes)
✅ TestSalvarRegras (2 testes)
✅ TestVerificarPorta (3 testes)
✅ TestFiltrarPacote (5 testes)
✅ TestObterDescricaoServico (6 testes)
✅ TestCalcularEstatisticas (5 testes)
✅ TestIntegracao (2 testes)

TOTAL: 27 testes - TODOS PASSANDO ✓
```

**Executar testes:**
```bash
python -m unittest test_firewall -v
```

## 📊 Estatísticas do Código

| Métrica | Valor |
|---------|-------|
| Linhas de código Python (backend) | 600+ |
| Linhas de CSS | 600+ |
| Linhas de JavaScript | 300+ |
| Linhas de HTML | 200+ |
| Testes unitários | 27 |
| Endpoints API | 7 |
| Funções documentadas | 100% |

## 📖 Documentação Adicional

Arquivos de documentação inclusos:

- **FUNCIONALIDADES.md** - Lista detalhada de todas as funcionalidades
- **GUIA_PASSO_A_PASSO.md** - Guia completo para executar e testar
- **RESUMO_FUNCIONALIDADES.txt** - Resumo rápido

## 🎓 Conceitos Demonstrados

- Arquitetura cliente-servidor
- API RESTful
- Validação de dados
- Testes unitários
- Tratamento de exceções
- Design responsivo
- JavaScript vanilla (sem frameworks)
- Comunicação assíncrona (Fetch API)
- Persistência de dados (JSON)
- Segurança (fail-safe policy)

## 🚀 Próximos Passos

Possíveis melhorias futuras:

1. **Autenticação de usuários**
2. **Banco de dados (SQLite/PostgreSQL)**
3. **Gráficos de estatísticas**
4. **Exportar/importar regras**
5. **Modo escuro/claro**
6. **Suporte a múltiplos usuários**

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente para fins educacionais.

---

<img width="1536" height="1024" alt="tela 1" src="https://github.com/user-attachments/assets/2654889a-de31-401c-9d7f-488b4951eed2" />
<img width="1280" height="1080" alt="tela 2" src="https://github.com/user-attachments/assets/380e90f8-4e6b-4919-83d8-a935a0f3bf2b" />
<img width="1024" height="1536" alt="tela 3" src="https://github.com/user-attachments/assets/011f2b87-0141-4911-b711-febac8953cf5" />

**Desenvolvido com ❤️ para fins educacionais**
