# Documentação da API

## Classes Principais

### Agent

Classe principal do agente que orquestra todos os componentes.

```python
from src.agent import Agent

agent = Agent(
    name="Katrina",           # Nome do agente (default: "Katrina")
    memory_dir="./memory",    # Diretório para memória persistente
    max_iterations=10         # Máximo de iterações no action loop
)
```

#### Métodos

##### process(user_input, verbose=True)
Processa input do usuário através do pipeline do agente.

**Parâmetros:**
- `user_input` (str): Input em linguagem natural
- `verbose` (bool): Imprimir detalhes do raciocínio (default: True)

**Retorna:**
- `str`: Resposta do agente

**Exemplo:**
```python
response = agent.process("calculate 5 + 3")
```

##### get_status()
Obtém informações de status do agente.

**Retorna:**
- `Dict[str, Any]`: Dicionário com status do agente

**Exemplo:**
```python
status = agent.get_status()
print(status['skills'])  # Lista de skills disponíveis
```

##### reset()
Limpa memória de curto prazo e histórico de raciocínio.

**Exemplo:**
```python
agent.reset()
```

---

### Skill (Base Class)

Classe base para criar skills personalizadas.

```python
from src.skills import Skill
from typing import Dict, Any

class MySkill(Skill):
    def __init__(self):
        super().__init__()
        self.description = "Descrição da skill"
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
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        # Implementar lógica aqui
        return {'success': True, 'result': 'resultado'}
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': 'my_skill',
            'description': self.description,
            'parameters': self.parameters
        }
```

#### Métodos a Implementar

##### execute(**kwargs)
Executa a skill com parâmetros fornecidos.

**Parâmetros:**
- `**kwargs`: Parâmetros definidos no schema

**Retorna:**
- `Dict[str, Any]`: Dicionário com 'success' (bool) e 'result' (any)

##### get_schema()
Retorna schema da skill para tool calling.

**Retorna:**
- `Dict[str, Any]`: Schema com name, description e parameters

---

### SkillManager

Gerencia todas as skills disponíveis.

```python
from src.skills import SkillManager

skill_manager = SkillManager(memory_manager=None)
```

#### Métodos

##### register_skill(skill)
Registra uma nova skill.

**Parâmetros:**
- `skill` (Skill): Instância da skill a registrar

**Exemplo:**
```python
skill_manager.register_skill(MyCustomSkill())
```

##### execute_skill(skill_name, **kwargs)
Executa uma skill pelo nome.

**Parâmetros:**
- `skill_name` (str): Nome da skill
- `**kwargs`: Parâmetros para a skill

**Retorna:**
- `Dict[str, Any]`: Resultado da execução

**Exemplo:**
```python
result = skill_manager.execute_skill('calculator', expression='5 + 3')
```

##### list_skills()
Lista todas as skills disponíveis.

**Retorna:**
- `List[str]`: Lista de nomes de skills

---

### MemoryManager

Gerencia memória de curto e longo prazo.

```python
from src.memory import MemoryManager

memory = MemoryManager(
    storage_dir="./memory_store",  # Diretório para memória persistente
    max_short_term=50              # Máximo de mensagens em curto prazo
)
```

#### Métodos

##### add_interaction(user_input, agent_response, metadata=None)
Adiciona interação a ambas as memórias.

**Parâmetros:**
- `user_input` (str): Input do usuário
- `agent_response` (str): Resposta do agente
- `metadata` (Dict, optional): Metadados adicionais

##### search_long_term_memory(query, max_results=5)
Busca em memória de longo prazo.

**Parâmetros:**
- `query` (str): Texto de busca
- `max_results` (int): Máximo de resultados (default: 5)

**Retorna:**
- `List[Dict[str, Any]]`: Lista de memórias relevantes

**Exemplo:**
```python
results = memory.search_long_term_memory("Python programming", max_results=3)
```

##### store_knowledge(content, metadata=None)
Armazena conhecimento em memória de longo prazo.

**Parâmetros:**
- `content` (str): Conteúdo a armazenar
- `metadata` (Dict, optional): Metadados

**Retorna:**
- `int`: ID da memória armazenada

---

### ReasoningEngine

Motor de raciocínio com CoT, reflexão e planejamento.

```python
from src.agent import ReasoningEngine

reasoning = ReasoningEngine()
```

#### Métodos

##### think(observation, context="")
Gera raciocínio chain-of-thought.

**Parâmetros:**
- `observation` (str): Observação atual
- `context` (str, optional): Contexto adicional

**Retorna:**
- `str`: Pensamento gerado

##### reflect(action_result)
Reflete sobre resultado de uma ação.

**Parâmetros:**
- `action_result` (Dict): Resultado da ação

**Retorna:**
- `str`: Reflexão sobre o resultado

##### plan(goal, available_tools)
Cria plano para atingir objetivo.

**Parâmetros:**
- `goal` (str): Objetivo a atingir
- `available_tools` (List[str]): Ferramentas disponíveis

**Retorna:**
- `List[Dict]`: Lista de passos planejados

---

### NaturalLanguageProcessor

Processa linguagem natural para extrair intenções.

```python
from src.agent import NaturalLanguageProcessor

nlp = NaturalLanguageProcessor()
```

#### Métodos

##### parse(user_input)
Analisa input para extrair intent e entidades.

**Parâmetros:**
- `user_input` (str): Input em linguagem natural

**Retorna:**
- `Dict[str, Any]`: Dicionário com 'intent', 'entities', 'confidence'

**Exemplo:**
```python
result = nlp.parse("calculate 5 + 3")
# {'intent': 'calculate', 'entities': {'expression': '5 + 3'}, ...}
```

---

## Skills Incorporadas

### CalculatorSkill

Realiza cálculos matemáticos seguros.

**Nome:** `calculator`

**Parâmetros:**
- `expression` (str): Expressão matemática

**Exemplo:**
```python
result = skill_manager.execute_skill('calculator', expression='10 * 5')
```

### FileOperationsSkill

Operações com ficheiros no workspace.

**Nome:** `file_operations`

**Parâmetros:**
- `operation` (str): 'read', 'write', ou 'list'
- `filename` (str, optional): Nome do ficheiro
- `content` (str, optional): Conteúdo (para write)

**Exemplos:**
```python
# Listar ficheiros
skill_manager.execute_skill('file_operations', operation='list')

# Ler ficheiro
skill_manager.execute_skill('file_operations', operation='read', filename='notes.txt')

# Escrever ficheiro
skill_manager.execute_skill('file_operations', operation='write', 
                          filename='notes.txt', content='Hello World')
```

### KnowledgeSearchSkill

Busca em memória de longo prazo.

**Nome:** `knowledge_search`

**Parâmetros:**
- `query` (str): Texto de busca
- `max_results` (int, optional): Máximo de resultados (default: 5)

**Exemplo:**
```python
result = skill_manager.execute_skill('knowledge_search', 
                                    query='Python', max_results=3)
```

---

## Exemplos Avançados

### Exemplo 1: Pipeline Completo

```python
from src.agent import Agent

# Inicializar agente
agent = Agent(name="MyAgent", memory_dir="./my_memory")

# Processar múltiplos comandos
commands = [
    "calculate 100 + 50",
    "write result is 150 to result.txt",
    "read result.txt",
    "search for calculate"
]

for cmd in commands:
    print(f"Command: {cmd}")
    response = agent.process(cmd, verbose=False)
    print(f"Response: {response}\n")
```

### Exemplo 2: Skill Personalizada Complexa

```python
from src.skills import Skill
from typing import Dict, Any
import requests

class APISkill(Skill):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.description = "Call external API"
        self.parameters = {
            'type': 'object',
            'properties': {
                'endpoint': {'type': 'string', 'description': 'API endpoint'},
                'method': {'type': 'string', 'enum': ['GET', 'POST']}
            },
            'required': ['endpoint', 'method']
        }
    
    def execute(self, endpoint: str, method: str, **kwargs) -> Dict[str, Any]:
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            if method == 'GET':
                response = requests.get(endpoint, headers=headers)
            else:
                response = requests.post(endpoint, headers=headers, json=kwargs)
            
            return {
                'success': True,
                'status_code': response.status_code,
                'data': response.json()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': 'api_call',
            'description': self.description,
            'parameters': self.parameters
        }

# Usar
agent = Agent()
agent.skill_manager.register_skill(APISkill('my_api_key'))
```

### Exemplo 3: Memória Avançada

```python
from src.memory import MemoryManager

memory = MemoryManager(storage_dir="./knowledge_base")

# Armazenar conhecimento estruturado
memory.store_knowledge(
    "Python é uma linguagem de programação de alto nível",
    metadata={'topic': 'programming', 'language': 'Python'}
)

memory.store_knowledge(
    "FastAPI é um framework web moderno para Python",
    metadata={'topic': 'web', 'framework': 'FastAPI'}
)

# Buscar conhecimento
results = memory.search_long_term_memory("Python web framework")
for result in results:
    print(f"Content: {result['content']}")
    print(f"Metadata: {result['metadata']}")
```

---

## Extensões e Customizações

### Adicionar Novos Padrões de Intent

```python
from src.agent import NaturalLanguageProcessor

nlp = NaturalLanguageProcessor()

# Adicionar novos padrões
nlp.intent_patterns['translate'] = [
    r'translate\s+(.+)\s+to\s+(\w+)',
    r'how\s+do\s+you\s+say\s+(.+)\s+in\s+(\w+)'
]

# Adicionar mapeamento de intent para tool
def custom_intent_to_tool(intent):
    if intent == 'translate':
        return 'translator'
    return nlp.intent_to_tool(intent)
```

### Modificar Behavior do Action Loop

```python
from src.agent import Agent

class CustomAgent(Agent):
    def _action_loop(self, parse_result, verbose):
        # Implementar lógica customizada
        # Pode adicionar validações, retry logic, etc.
        return super()._action_loop(parse_result, verbose)
```

---

## Debugging

### Modo Verbose

```python
# Ver todo o processo de raciocínio
agent.process("calculate 5 + 3", verbose=True)
```

### Inspecionar Estado do Agente

```python
status = agent.get_status()
print(f"Skills: {status['skills']}")
print(f"Memory: {status['memory_summary']}")
print(f"Thoughts: {status['thought_chain_length']}")
```

### Ver Cadeia de Pensamento

```python
thoughts = agent.reasoning.get_thought_chain()
for i, thought in enumerate(thoughts):
    print(f"Thought {i+1}: {thought}")
```

### Ver Reflexões

```python
reflections = agent.reasoning.get_reflections()
for reflection in reflections:
    print(f"Reflection: {reflection}")
```
