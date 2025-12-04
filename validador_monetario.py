
import re
import sys


class ValidadorMonetario:
    def __init__(self):
        self.LETRA = r'[A-Za-z]'
        self.DIGITO = r'[0-9]'
        self.SINAL = r'-'
        self.SIMBOLO = r'\$'
        
        self.CODIGO = rf'{self.LETRA}+'
        self.PREFIXO_MOEDA = rf'(?:{self.CODIGO})?{self.SIMBOLO}'
        self.GRUPO_MILHAR = rf'\.{self.DIGITO}{{3}}'
        self.INTEIRO = rf'{self.DIGITO}+(?:{self.GRUPO_MILHAR})*'
        self.DECIMAL = rf',{self.DIGITO}{{2}}'
        
        self.VALOR_NORMAL = rf'{self.SINAL}?{self.INTEIRO}{self.DECIMAL}'
        self.VALOR_NEGATIVO = rf'\({self.SINAL}?{self.INTEIRO}{self.DECIMAL}\)'
        self.VALOR_NUMERICO = rf'(?:{self.VALOR_NORMAL}|{self.VALOR_NEGATIVO})'
        
        self.VALOR_MONETARIO = rf'^{self.PREFIXO_MOEDA}{self.VALOR_NUMERICO}$'
        
        self.pattern = re.compile(self.VALOR_MONETARIO)
    
    def validar(self, valor):
        if not valor or not isinstance(valor, str):
            return False
        
        valor = valor.strip()
        
        return bool(self.pattern.match(valor))
    
    def validar_com_detalhes(self, valor):
        valor_original = valor
        valor = valor.strip() if valor else ""
        
        resultado = {
            'valor': valor_original,
            'valido': False,
            'mensagem': ''
        }
        
        if not valor:
            resultado['mensagem'] = 'Valor vazio'
            return resultado
        
        if self.pattern.match(valor):
            resultado['valido'] = True
            resultado['mensagem'] = 'Valor válido'
        else:
            resultado['mensagem'] = self._diagnosticar_erro(valor)
        
        return resultado
    
    def _diagnosticar_erro(self, valor):
        if '$' not in valor:
            return 'Erro: Falta o símbolo $ (cifrão)'
        
        if ',' not in valor:
            return 'Erro: Falta a vírgula para separar os centavos'
        
        if valor.count('(') != valor.count(')'):
            return 'Erro: Parênteses não balanceados'
        
        if ',' in valor:
            partes = valor.split(',')
            if len(partes) == 2:
                parte_decimal = partes[1].rstrip(')')
                if not parte_decimal:
                    return 'Erro: Falta a parte decimal após a vírgula'
                if not parte_decimal.isdigit():
                    return 'Erro: Parte decimal contém caracteres inválidos'
        
        if '.' in valor:
            try:
                inicio = valor.index('$') + 1
                fim = valor.index(',')
                parte_inteira = valor[inicio:fim].replace('-', '').replace('(', '').strip()
                
                if '.' in parte_inteira:
                    blocos = parte_inteira.split('.')
                    for i, bloco in enumerate(blocos):
                        if i > 0 and len(bloco) != 3:
                            return f'Erro: Separador de milhar incorreto (bloco com {len(bloco)} dígitos ao invés de 3)'
            except:
                pass
        
        return 'Erro: Formato inválido'


def processar_arquivo(caminho_arquivo, validador):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        
        print("=" * 80)
        print("VALIDAÇÃO DE VALORES MONETÁRIOS")
        print("=" * 80)
        print()
        
        total = 0
        validos = 0
        invalidos = 0
        
        for i, linha in enumerate(linhas, 1):
            linha = linha.strip()
            
            if not linha or linha.startswith('#'):
                continue
            
            total += 1
            resultado = validador.validar_com_detalhes(linha)
            
            status = "✓ VÁLIDO" if resultado['valido'] else "✗ INVÁLIDO"
            print(f"Linha {i}: {linha}")
            print(f"  Status: {status}")
            
            if not resultado['valido']:
                print(f"  Motivo: {resultado['mensagem']}")
                invalidos += 1
            else:
                validos += 1
            
            print()
        
        print("=" * 80)
        print("RESUMO DA VALIDAÇÃO")
        print("=" * 80)
        print(f"Total de valores processados: {total}")
        print(f"Valores válidos: {validos}")
        print(f"Valores inválidos: {invalidos}")
        print(f"Taxa de sucesso: {(validos/total*100) if total > 0 else 0:.1f}%")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{caminho_arquivo}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"ERRO ao processar arquivo: {e}")
        sys.exit(1)


def modo_interativo(validador):
    print("=" * 80)
    print("VALIDADOR DE VALORES MONETÁRIOS - MODO INTERATIVO")
    print("=" * 80)
    print()
    print("Digite valores monetários para validação.")
    print("Digite 'sair' ou 'exit' para encerrar.")
    print("Digite 'exemplos' para ver exemplos de valores válidos.")
    print()
    
    while True:
        try:
            entrada = input("Digite um valor monetário: ").strip()
            
            if not entrada:
                continue
            
            if entrada.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\nEncerrando o validador. Até logo!")
                break
            
            if entrada.lower() == 'exemplos':
                print("\n" + "=" * 80)
                print("EXEMPLOS DE VALORES VÁLIDOS")
                print("=" * 80)
                print("$0,00              - Valor zero")
                print("$5,50              - Valor simples")
                print("$100,00            - Três dígitos")
                print("$1.000,00          - Com separador de milhar")
                print("$10.000,50         - Múltiplos milhares")
                print("USD$1.234.567,89   - Com código de moeda")
                print("$-500,00           - Valor negativo com sinal")
                print("$(750,00)          - Valor negativo com parênteses")
                print("=" * 80 + "\n")
                continue
            
            resultado = validador.validar_com_detalhes(entrada)
            
            print()
            if resultado['valido']:
                print("✓ VÁLIDO - O valor está correto!")
            else:
                print("✗ INVÁLIDO")
                print(f"Motivo: {resultado['mensagem']}")
            print()
            
        except KeyboardInterrupt:
            print("\n\nEncerrando o validador. Até logo!")
            break
        except EOFError:
            print("\n\nEncerrando o validador. Até logo!")
            break


def main():
    validador = ValidadorMonetario()
    
    if len(sys.argv) > 1:
        argumento = sys.argv[1]
        
        if argumento in ['-i', '--interativo', '--interactive']:
            modo_interativo(validador)
        else:
            processar_arquivo(argumento, validador)
    else:
        modo_interativo(validador)


if __name__ == "__main__":
    main()
