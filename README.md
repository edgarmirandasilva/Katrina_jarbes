# Katrina Agent 🤖

Um agente Python modular com arquitetura moderna que pode executar localmente, com suporte a múltiplas skills (plugins), memória de curto e longo prazo, reconhecimento de linguagem natural e execução de ações.

## 🌟 Características

- **Arquitetura Modular**: Componentes separados para raciocínio, memória e habilidades
- **Sistema de Skills (Plugins)**: Facilmente extensível com novas capacidades
- **Memória Dual**:
  - Memória de curto prazo: Histórico de conversação recente
  - Memória de longo prazo: Armazenamento persistente com busca
- **Processamento de Linguagem Natural**: Compreende comandos em linguagem natural
- **Técnicas Modernas de Agentes**:
  - Tool Calling (chamada de ferramentas)
  - Chain-of-Thought (raciocínio em cadeia)
  - Reflection (reflexão sobre ações)
  - Planning (planejamento de ações)
  - Action Loops (loops de ação iterativos)

## 📁 Estrutura do Projeto

```
Katrina_jarbes/
├── src/
│   ├── agent/
│   │   ├── agent_core.py          # Orquestrador principal do agente
│   │   ├── reasoning_engine.py    # Motor de raciocínio (CoT, reflexão, planejamento)
│   │   └── nlp_processor.py       # Processador de linguagem natural
│   ├── memory/
│   │   ├── short_term_memory.py   # Memória de curto prazo
│   │   ├── long_term_memory.py    # Memória de longo prazo persistente
│   │   └── memory_manager.py      # Coordenador de memória
│   └── skills/
│       ├── base_skill.py          # Interface base para skills
│       ├── calculator_skill.py    # Skill de calculadora
│       ├── file_operations_skill.py # Skill de operações com ficheiros
│       ├── knowledge_search_skill.py # Skill de busca em memória
│       └── skill_manager.py       # Gestor de skills
├── examples/
│   ├── basic_example.py           # Exemplo básico de uso
│   ├── interactive_example.py     # Modo interativo
│   └── custom_skill_example.py    # Criar skills personalizadas
├── requirements.txt               # Dependências
└── README.md                      # Este ficheiro

```

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/edgarmirandasilva/Katrina_jarbes.git
cd Katrina_jarbes
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. (Opcional) Configure variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env se necessário
```

### Execução

#### Exemplo Básico
```bash
python examples/basic_example.py
```

#### Modo Interativo
```bash
python examples/interactive_example.py
```

#### Skills Personalizadas
```bash
python examples/custom_skill_example.py
```

## 💡 Uso

### Exemplo Simples

```python
from src.agent import Agent

# Inicializar o agente
agent = Agent(name="Katrina", memory_dir="./memory_store")

# Processar comandos em linguagem natural
response = agent.process("calculate 15 + 27")
print(response)  # "The result of 15 + 27 is 42"

response = agent.process("write hello world to message.txt")
print(response)  # "Successfully wrote to message.txt"

response = agent.process("list files")
print(response)  # "Files in workspace: message.txt"
```

### Comandos Disponíveis

**Calculadora:**
- "calculate 5 + 3"
- "what is 10 * 20"
- "compute 100 / 4"

**Operações com Ficheiros:**
- "list files" - Lista ficheiros no workspace
- "read file notes.txt" - Lê conteúdo de um ficheiro
- "write hello to file.txt" - Escreve conteúdo num ficheiro

**Busca de Memória:**
- "search for Python"
- "find information about AI"
- "remember calculator"

**Ajuda:**
- "help" - Mostra comandos disponíveis

## 🔧 Criar Skills Personalizadas

Você pode criar suas próprias skills estendendo a classe base `Skill`:

```python
from src.skills import Skill
from typing import Dict, Any

class MyCustomSkill(Skill):
    def __init__(self):
        super().__init__()
        self.description = "Descrição da sua skill"
        self.parameters = {
            'type': 'object',
            'properties': {
                'param1': {
                    'type': 'string',
                    'description': 'Descrição do parâmetro'
                }
            },
            'required': ['param1']
        }
    
    def execute(self, param1: str, **kwargs) -> Dict[str, Any]:
        # Implementar a lógica da skill
        return {
            'success': True,
            'result': f"Processed: {param1}"
        }
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': 'my_custom_skill',
            'description': self.description,
            'parameters': self.parameters
        }

# Registrar a skill
agent = Agent()
agent.skill_manager.register_skill(MyCustomSkill())
```

## 🏗️ Arquitetura

### Componentes Principais

1. **Agent Core** (`agent_core.py`):
   - Orquestrador principal
   - Implementa o loop de ação
   - Coordena todos os componentes

2. **Reasoning Engine** (`reasoning_engine.py`):
   - Chain-of-Thought: Raciocínio explícito
   - Reflection: Reflexão sobre resultados
   - Planning: Criação de planos de ação

3. **NLP Processor** (`nlp_processor.py`):
   - Parse de linguagem natural
   - Extração de intenções e entidades
   - Mapeamento para ferramentas

4. **Memory Manager** (`memory_manager.py`):
   - Gestão de memória de curto prazo (conversações)
   - Gestão de memória de longo prazo (persistente)
   - Busca em memórias armazenadas

5. **Skill Manager** (`skill_manager.py`):
   - Carregamento dinâmico de skills
   - Registro de novas skills
   - Execução de skills com parâmetros

### Fluxo de Execução

```
Input do Usuário
    ↓
NLP Processor (parse de linguagem natural)
    ↓
Reasoning Engine (planejamento e raciocínio)
    ↓
Action Loop (execução iterativa)
    ↓
Skill Execution (tool calling)
    ↓
Reflection (análise de resultados)
    ↓
Memory Storage (armazenamento)
    ↓
Response ao Usuário
```

## 🧪 Técnicas de Agentes Implementadas

### 1. Tool Calling
O agente pode chamar ferramentas (skills) de forma dinâmica baseado na entrada do usuário.

### 2. Chain-of-Thought (CoT)
O agente explica seu raciocínio antes de executar ações:
```
Observation: Need to calculate 5 + 3
Context: Previous calculations...
Analysis: Will use calculator skill...
```

### 3. Reflection
Após cada ação, o agente reflete sobre o resultado:
```
Action succeeded. Result: 8
```
ou
```
Action failed. Error: ... Need to try a different approach.
```

### 4. Planning
O agente cria planos estruturados para atingir objetivos:
1. Analisar objetivo
2. Selecionar ferramenta apropriada
3. Executar com parâmetros corretos
4. Verificar resultado

### 5. Action Loops
O agente pode iterar múltiplas vezes até atingir o objetivo ou atingir o limite de iterações.

## 📝 Dependências

- Python 3.8+
- Bibliotecas básicas (incluídas no requirements.txt)

Sem dependência obrigatória de APIs externas - o agente funciona completamente offline!

## 🤝 Contribuir

Contribuições são bem-vindas! Para adicionar novas skills ou melhorar funcionalidades:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-skill`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova skill'`)
4. Push para a branch (`git push origin feature/nova-skill`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👥 Autor

Edgar Miranda Silva

## 🔮 Roadmap

- [ ] Integração com LLMs externos (OpenAI, Anthropic)
- [ ] Suporte a embeddings com ChromaDB
- [ ] Skills adicionais (web scraping, APIs, etc.)
- [ ] Interface web com Streamlit/Gradio
- [ ] Sistema de logging avançado
- [ ] Testes unitários completos
- [ ] Documentação API completa

## 📞 Suporte

Para questões ou suporte, abra uma issue no GitHub.