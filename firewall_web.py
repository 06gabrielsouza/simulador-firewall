"""
Simulador de Firewall - Interface Web com Flask
Sistema de simulação de firewall com interface web para testar pacotes,
gerenciar regras de filtragem e visualizar estatísticas.
"""

from flask import Flask, render_template, request, jsonify
import json
import socket
from datetime import datetime
import os

# Inicializa a aplicação Flask
app = Flask(__name__)

# Caminho do arquivo de configuração de regras
REGRAS_FILE = "regras.json"

# Lista para armazenar histórico de testes realizados
testes_realizados = []


# ============================================================================
# FUNÇÕES DE CARREGAMENTO E SALVAMENTO DE DADOS
# ============================================================================

def carregar_regras():
    """
    Carrega as regras de firewall do arquivo JSON.
    
    Retorna:
        list: Lista de regras ou lista vazia se houver erro
    """
    try:
        with open(REGRAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {REGRAS_FILE} não encontrado")
        return []
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON de {REGRAS_FILE}")
        return []


def salvar_regras(regras):
    """
    Salva as regras de firewall no arquivo JSON.
    
    Args:
        regras (list): Lista de regras a serem salvas
        
    Retorna:
        bool: True se salvo com sucesso, False caso contrário
    """
    try:
        with open(REGRAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(regras, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar regras: {e}")
        return False


# ============================================================================
# FUNÇÕES DE TESTE DE CONECTIVIDADE
# ============================================================================

def verificar_porta(ip, porta, timeout=1):
    """
    Testa se uma porta está aberta/respondendo usando socket.
    
    Args:
        ip (str): Endereço IP a testar
        porta (int): Número da porta a testar
        timeout (int): Tempo máximo de espera em segundos
        
    Retorna:
        bool: True se porta está aberta, False se fechada
        None: Se host não foi encontrado (erro de DNS)
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        resultado = s.connect_ex((ip, porta))
        s.close()
        return resultado == 0  # 0 = sucesso na conexão
    except socket.gaierror:
        # Erro de DNS - host não encontrado
        return None
    except Exception:
        # Qualquer outro erro = porta fechada
        return False


# ============================================================================
# FUNÇÕES DE FILTRAGEM E REGRAS
# ============================================================================

def filtrar_pacote(ip, porta, regras):
    """
    Aplica as regras de firewall para decidir se um pacote é permitido ou bloqueado.
    
    Política de segurança:
    - Se há regra PERMITIDO para IP:porta -> PERMITIDO
    - Se há regra BLOQUEADO para IP:porta -> BLOQUEADO
    - Se não há regra -> BLOQUEADO (fail-safe)
    
    Args:
        ip (str): Endereço IP do pacote
        porta (int): Porta do pacote
        regras (list): Lista de regras de firewall
        
    Retorna:
        str: "PERMITIDO" ou "BLOQUEADO"
    """
    # Procura por uma regra que corresponda ao IP e porta
    for regra in regras:
        if regra['ip'] == ip and regra['porta'] == porta:
            return regra['acao']
    
    # Se não encontrou regra, nega por padrão (fail-safe)
    return "BLOQUEADO"


def obter_descricao_servico(porta):
    """
    Retorna a descrição comum de um serviço baseado na porta.
    
    Args:
        porta (int): Número da porta
        
    Retorna:
        str: Nome do serviço ou "Desconhecido"
    """
    servicos = {
        20: "FTP Data",
        21: "FTP Control",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        8080: "HTTP Proxy"
    }
    return servicos.get(porta, "Desconhecido")


# ============================================================================
# FUNÇÕES DE ESTATÍSTICAS
# ============================================================================

def calcular_estatisticas(regras):
    """
    Calcula estatísticas sobre as regras configuradas.
    
    Args:
        regras (list): Lista de regras
        
    Retorna:
        dict: Dicionário com contagem de permitidos, bloqueados e total
    """
    permitidos = sum(1 for r in regras if r['acao'] == 'PERMITIDO')
    bloqueados = sum(1 for r in regras if r['acao'] == 'BLOQUEADO')
    
    return {
        'permitidos': permitidos,
        'bloqueados': bloqueados,
        'total': len(regras)
    }


# ============================================================================
# ROTAS - PÁGINAS
# ============================================================================

@app.route('/')
def index():
    """
    Rota principal - exibe a página inicial com todas as informações.
    """
    regras = carregar_regras()
    stats = calcular_estatisticas(regras)
    data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    return render_template('index.html', 
                         regras=regras, 
                         stats=stats,
                         data_hora=data_hora,
                         testes=testes_realizados)


# ============================================================================
# API - TESTES DE PACOTES
# ============================================================================

@app.route('/api/testar-pacote', methods=['POST'])
def testar_pacote():
    """
    API para testar um pacote contra as regras de firewall.
    
    Recebe JSON com:
        - ip (str): Endereço IP
        - porta (int): Número da porta
        
    Retorna:
        JSON com resultado do teste ou erro
    """
    try:
        data = request.json
        ip = data.get('ip', '').strip()
        porta = data.get('porta', '')
        
        # Validação de entrada
        if not ip:
            return jsonify({'erro': 'IP é obrigatório'}), 400
        
        # Converte e valida a porta
        try:
            porta = int(porta)
            if porta < 1 or porta > 65535:
                return jsonify({'erro': 'Porta deve estar entre 1 e 65535'}), 400
        except ValueError:
            return jsonify({'erro': 'Porta deve ser um número'}), 400
        
        # Testa conectividade da porta
        conectividade = verificar_porta(ip, porta)
        
        # Carrega regras e aplica filtragem
        regras = carregar_regras()
        decisao = filtrar_pacote(ip, porta, regras)
        
        # Obtém descrição do serviço
        servico = obter_descricao_servico(porta)
        
        # Monta resultado do teste
        resultado = {
            'ip': ip,
            'porta': porta,
            'servico': servico,
            'conectividade': conectividade,
            'decisao': decisao,
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        # Adiciona ao histórico
        testes_realizados.append(resultado)
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ============================================================================
# API - GERENCIAMENTO DE REGRAS
# ============================================================================

@app.route('/api/regras', methods=['GET'])
def get_regras():
    """
    API para obter todas as regras configuradas.
    """
    regras = carregar_regras()
    return jsonify(regras), 200


@app.route('/api/regras', methods=['POST'])
def adicionar_regra():
    """
    API para adicionar uma nova regra de firewall.
    
    Recebe JSON com:
        - ip (str): Endereço IP
        - porta (int): Número da porta
        - acao (str): "PERMITIDO" ou "BLOQUEADO"
        - descricao (str, opcional): Descrição da regra
    """
    try:
        data = request.json
        ip = data.get('ip', '').strip()
        porta = data.get('porta', '')
        acao = data.get('acao', '').upper()
        descricao = data.get('descricao', '').strip()
        
        # Validações
        if not ip:
            return jsonify({'erro': 'IP é obrigatório'}), 400
        
        try:
            porta = int(porta)
            if porta < 1 or porta > 65535:
                return jsonify({'erro': 'Porta deve estar entre 1 e 65535'}), 400
        except ValueError:
            return jsonify({'erro': 'Porta deve ser um número'}), 400
        
        if acao not in ['PERMITIDO', 'BLOQUEADO']:
            return jsonify({'erro': 'Ação deve ser PERMITIDO ou BLOQUEADO'}), 400
        
        # Carrega regras existentes
        regras = carregar_regras()
        
        # Verifica se já existe uma regra para este IP:porta
        for regra in regras:
            if regra['ip'] == ip and regra['porta'] == porta:
                return jsonify({'erro': 'Regra já existe para este IP e porta'}), 400
        
        # Cria nova regra
        nova_regra = {
            'ip': ip,
            'porta': porta,
            'acao': acao
        }
        if descricao:
            nova_regra['descricao'] = descricao
        
        # Adiciona à lista e salva
        regras.append(nova_regra)
        
        if salvar_regras(regras):
            return jsonify(nova_regra), 201
        else:
            return jsonify({'erro': 'Erro ao salvar regra'}), 500
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/regras/<int:index>', methods=['PUT'])
def editar_regra(index):
    """
    API para editar uma regra existente.
    
    Pode editar:
        - acao: "PERMITIDO" ou "BLOQUEADO"
        - descricao: descrição da regra
    """
    try:
        regras = carregar_regras()
        
        # Valida índice
        if index < 0 or index >= len(regras):
            return jsonify({'erro': 'Regra não encontrada'}), 404
        
        data = request.json
        
        # Atualiza ação se fornecida
        if 'acao' in data:
            acao = data['acao'].upper()
            if acao not in ['PERMITIDO', 'BLOQUEADO']:
                return jsonify({'erro': 'Ação deve ser PERMITIDO ou BLOQUEADO'}), 400
            regras[index]['acao'] = acao
        
        # Atualiza descrição se fornecida
        if 'descricao' in data:
            if data['descricao'].strip():
                regras[index]['descricao'] = data['descricao'].strip()
            elif 'descricao' in regras[index]:
                del regras[index]['descricao']
        
        # Salva mudanças
        if salvar_regras(regras):
            return jsonify(regras[index]), 200
        else:
            return jsonify({'erro': 'Erro ao salvar regra'}), 500
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/regras/<int:index>', methods=['DELETE'])
def deletar_regra(index):
    """
    API para deletar uma regra existente.
    """
    try:
        regras = carregar_regras()
        
        # Valida índice
        if index < 0 or index >= len(regras):
            return jsonify({'erro': 'Regra não encontrada'}), 404
        
        # Remove regra
        regra_deletada = regras.pop(index)
        
        # Salva mudanças
        if salvar_regras(regras):
            return jsonify({
                'mensagem': 'Regra deletada com sucesso',
                'regra': regra_deletada
            }), 200
        else:
            return jsonify({'erro': 'Erro ao salvar regras'}), 500
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ============================================================================
# API - HISTÓRICO DE TESTES
# ============================================================================

@app.route('/api/testes', methods=['GET'])
def get_testes():
    """
    API para obter o histórico de testes realizados.
    """
    return jsonify(testes_realizados), 200


@app.route('/api/testes', methods=['DELETE'])
def limpar_testes():
    """
    API para limpar o histórico de testes.
    """
    global testes_realizados
    testes_realizados = []
    return jsonify({'mensagem': 'Histórico limpo'}), 200


# ============================================================================
# EXECUÇÃO DA APLICAÇÃO
# ============================================================================

if __name__ == '__main__':
    # Inicia servidor Flask em modo debug
    # Acesse em http://localhost:5000
    app.run(debug=True, host='0.0.0.0', port=5000)
