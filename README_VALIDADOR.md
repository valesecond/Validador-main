# Validador de Valores Monetários

Programa em Python que valida valores monetários baseado na especificação de expressão regular fornecida.

## Especificação da Gramática

```
LETRA ← [A-Za-z]
DIGITO ← [0-9]
SINAL ← -
SIMBOLO ← $
CODIGO ← LETRA+
PREFIXO_MOEDA ← CODIGO SIMBOLO
GRUPO_MILHAR ← .DIGITO{3}
INTEIRO ← DIGITO+(GRUPO_MILHAR)*
DECIMAL ← ,DIGITO{2}
VALOR_NORMAL ← SINAL? INTEIRO DECIMAL
VALOR_NEGATIVO ← (SINAL? INTEIRO DECIMAL)
VALOR_NUMERICO ← VALOR_NORMAL | VALOR_NEGATIVO
VALOR_MONETARIO ← PREFIXO_MOEDA VALOR_NUMERICO
```

---

## Como Executar o Programa

### Pré-requisitos

1. **Python instalado**: Certifique-se de ter Python 3.6 ou superior instalado no seu computador
2. **Arquivos necessários**: 
   - `validador_monetario.py` (programa principal)
   - `exemplos_valores.txt` (arquivo de exemplos - opcional)

### Verificar instalação do Python

Abra o terminal (PowerShell, CMD ou Terminal) e digite:

```bash
python --version
```

Se aparecer a versão do Python (ex: `Python 3.11.0`), está tudo pronto!

---

## Modos de Execução

O programa possui **2 modos de operação**:

### 1. MODO INTERATIVO (Padrão - Recomendado)

Este é o modo mais fácil e intuitivo para testar valores individualmente.

#### Passo a Passo:

**1. Navegue até a pasta do código:**
```bash
cd "c:\Users\braz_\OneDrive\Área de Trabalho\automato\codigo"
```

**2. Execute o programa sem argumentos:**
```bash
python validador_monetario.py
```

**3. O programa exibirá a tela inicial:**
```
================================================================================
VALIDADOR DE VALORES MONETÁRIOS - MODO INTERATIVO
================================================================================

Digite valores monetários para validação.
Digite 'sair' ou 'exit' para encerrar.
Digite 'exemplos' para ver exemplos de valores válidos.

Digite um valor monetário:
```

**4. Interaja com o programa:**

- **Digite um valor monetário** e pressione ENTER para validar
- **Digite `exemplos`** para ver uma lista de valores válidos
- **Digite `sair`** ou `exit` para encerrar o programa

#### Exemplo de Interação:

```
Digite um valor monetário: $100,00

✓ VÁLIDO - O valor está correto!

Digite um valor monetário: $100

✗ INVÁLIDO
Motivo: Erro: Falta a vírgula para separar os centavos

Digite um valor monetário: exemplos

================================================================================
EXEMPLOS DE VALORES VÁLIDOS
================================================================================
$0,00              - Valor zero
$5,50              - Valor simples
$100,00            - Três dígitos
$1.000,00          - Com separador de milhar
$10.000,50         - Múltiplos milhares
USD$1.234.567,89   - Com código de moeda
$-500,00           - Valor negativo com sinal
$(750,00)          - Valor negativo com parênteses
================================================================================

Digite um valor monetário: USD$1.234,56

✓ VÁLIDO - O valor está correto!

Digite um valor monetário: sair

Encerrando o validador. Até logo!
```

#### Comandos Especiais no Modo Interativo:

| Comando | Função |
|---------|--------|
| `exemplos` | Mostra exemplos de valores válidos |
| `sair`, `exit`, `quit`, `q` | Encerra o programa |
| `Ctrl+C` | Interrompe o programa (atalho de teclado) |

---

### 2. MODO ARQUIVO

Valida múltiplos valores de uma só vez, lendo de um arquivo de texto.

#### Passo a Passo:

**1. Navegue até a pasta do código:**
```bash
cd "c:\Users\braz_\OneDrive\Área de Trabalho\automato\codigo"
```

**2. Execute o programa passando o arquivo como argumento:**
```bash
python validador_monetario.py exemplos_valores.txt
```

**3. O programa processará todas as linhas do arquivo e exibirá o resultado:**
```
================================================================================
VALIDAÇÃO DE VALORES MONETÁRIOS
================================================================================

Linha 5: $0,00
  Status: ✓ VÁLIDO

Linha 6: $5,50
  Status: ✓ VÁLIDO

Linha 7: $99,99
  Status: ✓ VÁLIDO

...

Linha 17: 100,00
  Status: ✗ INVÁLIDO
  Motivo: Erro: Falta o símbolo $ (cifrão)

================================================================================
RESUMO DA VALIDAÇÃO
================================================================================
Total de valores processados: 20
Valores válidos: 10
Valores inválidos: 10
Taxa de sucesso: 50.0%
================================================================================
```

#### Criar seu próprio arquivo de teste:

**1. Crie um arquivo de texto** (ex: `meus_valores.txt`)

**2. Adicione valores monetários, um por linha:**
```
# Meus testes
$100,00
$1.500,50
USD$999,99
$100
```

**3. Execute o validador:**
```bash
python validador_monetario.py meus_valores.txt
```

**Observações sobre o formato do arquivo:**
- Linhas vazias são ignoradas
- Linhas que começam com `#` são tratadas como comentários e ignoradas
- Cada valor deve estar em uma linha separada

---

## Regras de Validação

### Valores VÁLIDOS devem ter:

1. **Cifrão obrigatório** (`$`)
2. **Parte inteira** com um ou mais dígitos (`0-9`)
3. **Vírgula** separando inteiros e decimais (`,`)
4. **Parte decimal** com exatamente **2 dígitos** (centavos)
5. **Código de moeda opcional** antes do cifrão (ex: `BRL`, `USD`, `EUR`)
6. **Sinal de menos opcional** para valores negativos (`-`)
7. **Parênteses** para valores negativos são permitidos `()`
8. **Separador de milhar** (`.`) deve ter exatamente 3 dígitos após cada ponto

### Valores INVÁLIDOS:

- Sem cifrão: `100,00`
- Sem parte decimal: `$100`
- Decimal com 1 dígito: `$100,0`
- Decimal com 3 dígitos: `$100,000`
- Sem parte inteira: `$,00`
- Separador incorreto: `$1.00,00` (deve ser `$100,00` ou `$1.000,00`)
- Parênteses não balanceados: `$(100,00` 

### Exemplos Práticos:

| Valor | Status | Observação |
|-------|--------|------------|
| `$0,00` | ✅ VÁLIDO | Valor zero |
| `$5,50` | ✅ VÁLIDO | Valor simples |
| `$100,00` | ✅ VÁLIDO | Três dígitos |
| `$1.000,00` | ✅ VÁLIDO | Com separador de milhar |
| `$999.999,99` | ✅ VÁLIDO | Múltiplos separadores |
| `USD$1.234,56` | ✅ VÁLIDO | Com código de moeda |
| `$-500,00` | ✅ VÁLIDO | Negativo com sinal |
| `$(750,00)` | ✅ VÁLIDO | Negativo com parênteses |
| `100,00` | ❌ INVÁLIDO | Falta o cifrão |
| `$100` | ❌ INVÁLIDO | Falta a parte decimal |
| `$100,0` | ❌ INVÁLIDO | Decimal com 1 dígito |
| `R$$50,25` | ❌ INVÁLIDO | Cifrão duplicado |

---

## Solução de Problemas

### Erro: "python não é reconhecido como comando"

**Solução:** Python não está instalado ou não está no PATH do sistema.
- Baixe Python em: https://www.python.org/downloads/
- Durante a instalação, marque a opção "Add Python to PATH"

### Erro: "Arquivo não encontrado"

**Solução:** Certifique-se de estar na pasta correta:
```bash
cd "c:\Users\braz_\OneDrive\Área de Trabalho\automato\codigo"
```

### Programa não responde no modo interativo

**Solução:** Pressione `Ctrl+C` para interromper e execute novamente

---

## Implementação Técnica

O validador usa **expressões regulares (regex)** do Python para implementar a gramática especificada. A classe `ValidadorMonetario` compila a regex e oferece métodos para:
- Validação simples (retorna True/False)
- Validação com detalhes (retorna mensagens de erro específicas)
- Diagnóstico de erros comuns
