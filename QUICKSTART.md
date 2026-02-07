# Quick Start Guide

## Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/edgarmirandasilva/Katrina_jarbes.git
cd Katrina_jarbes

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o exemplo básico
python examples/basic_example.py
```

## Primeiro Uso

### Exemplo 1: Calculadora

```python
from src.agent import Agent

agent = Agent()
response = agent.process("calculate 42 * 2")
print(response)  # "The result of 42 * 2 is 84"
```

### Exemplo 2: Operações com Ficheiros

```python
from src.agent import Agent

agent = Agent()

# Escrever ficheiro
agent.process("write Python is awesome to notes.txt")

# Listar ficheiros
agent.process("list files")

# Ler ficheiro
agent.process("read notes.txt")
```

### Exemplo 3: Modo Interativo

```bash
python examples/interactive_example.py
```

Depois digite comandos como:
- `help` - Ver comandos disponíveis
- `calculate 100 / 4` - Fazer cálculos
- `list files` - Ver ficheiros
- `search for Python` - Buscar memórias
- `exit` - Sair

## Comandos Disponíveis

### Calculadora
- `calculate 5 + 3`
- `what is 10 * 20`
- `compute 100 / 4`
- `solve 2 ** 8`

### Ficheiros
- `list files` - Listar ficheiros
- `read file.txt` - Ler ficheiro
- `write content to file.txt` - Criar/escrever ficheiro

### Busca
- `search for keyword` - Buscar nas memórias
- `find information about topic` - Encontrar informação

### Ajuda
- `help` - Mostrar ajuda

## Criar Skill Personalizada

```python
from src.skills import Skill
from typing import Dict, Any

class MinhaSkill(Skill):
    def __init__(self):
        super().__init__()
        self.description = "Minha skill personalizada"
        self.parameters = {
            'type': 'object',
            'properties': {
                'param': {'type': 'string', 'description': 'Parâmetro'}
            },
            'required': ['param']
        }
    
    def execute(self, param: str, **kwargs) -> Dict[str, Any]:
        return {'success': True, 'result': f'Processado: {param}'}
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': 'minha_skill',
            'description': self.description,
            'parameters': self.parameters
        }

# Usar a skill
from src.agent import Agent

agent = Agent()
agent.skill_manager.register_skill(MinhaSkill())
result = agent.skill_manager.execute_skill('minha_skill', param='teste')
```

## Arquitetura

```
┌─────────────────────────────────────────────┐
│           Agent Core                        │
│  (Orquestração e Action Loop)               │
└─────────────────────────────────────────────┘
         │                   │
         ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│  Reasoning       │  │  NLP Processor   │
│  - CoT           │  │  - Intent Parse  │
│  - Reflection    │  │  - Entity Extract│
│  - Planning      │  │                  │
└──────────────────┘  └──────────────────┘
         │                   │
         ▼                   ▼
┌──────────────────────────────────────────┐
│          Skill Manager                   │
│  - Tool Calling                          │
│  - Dynamic Loading                       │
└──────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│          Skills (Plugins)                │
│  - Calculator                            │
│  - File Operations                       │
│  - Knowledge Search                      │
│  - [Custom Skills...]                    │
└──────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│          Memory Manager                  │
│  - Short-term (Recent Chat)              │
│  - Long-term (Persistent Storage)        │
└──────────────────────────────────────────┘
```

## Técnicas de Agentes

### 1. Tool Calling
```python
# O agente identifica a ferramenta necessária
# e chama automaticamente com os parâmetros corretos
agent.process("calculate 5 + 3")  # -> chama calculator skill
```

### 2. Chain-of-Thought
```
User input -> Parse -> Think -> Act -> Reflect -> Respond
                       ↑               │
                       └───────────────┘
                        (Reasoning loop)
```

### 3. Reflection
```python
# Após cada ação, o agente reflete:
# "Action succeeded. Result: X"
# ou
# "Action failed. Error: Y. Need different approach."
```

### 4. Planning
```python
# O agente cria planos estruturados:
# Step 1: Analyze goal
# Step 2: Select tool
# Step 3: Execute
# Step 4: Verify result
```

### 5. Action Loop
```python
# Iteração até atingir objetivo ou limite:
iteration = 0
while not goal_achieved and iteration < max_iterations:
    think() -> plan() -> act() -> reflect()
    iteration += 1
```

## Troubleshooting

### Erro de Import
Se encontrar erros de import, certifique-se de executar os scripts do diretório raiz do projeto.

### Memória não Persiste
A memória é salva em `./memory_store/`. Certifique-se de que o diretório tem permissões de escrita.

### Skills não Carregam
Verifique se todas as dependências do `requirements.txt` foram instaladas.

## Próximos Passos

1. Execute o exemplo básico
2. Experimente o modo interativo
3. Crie sua primeira skill personalizada
4. Explore o código fonte em `src/`
5. Leia o README completo para mais detalhes

## Recursos

- [README Completo](README.md)
- [Exemplos](examples/)
- [Documentação de Skills](src/skills/)
- [Documentação de Memória](src/memory/)
