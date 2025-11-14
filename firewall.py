import json
import socket
from datetime import datetime

# Cores para terminal (funciona no Linux/Mac, Windows 10+)
class Cores:
    HEADER = '\033[95m'
    AZUL = '\033[94m'
    CIANO = '\033[96m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Exibe o cabeçalho do programa"""
    print(f"\n{Cores.CIANO}{'='*70}{Cores.RESET}")
    print(f"{Cores.BOLD}{Cores.AZUL}🧱 SIMULADOR DE FIREWALL - FILTRO DE PACOTES{Cores.RESET}")
    print(f"{Cores.CIANO}{'='*70}{Cores.RESET}")
    print(f"{Cores.AMARELO}⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{Cores.RESET}\n")

def carregar_regras(arquivo):
    """Carrega regras de filtragem do arquivo JSON"""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            regras = json.load(f)
            print(f"{Cores.VERDE}✅ {len(regras)} regra(s) carregada(s) com sucesso!{Cores.RESET}\n")
            
            # Exibe as regras carregadas
            print(f"{Cores.BOLD}📋 Regras Configuradas:{Cores.RESET}")
            print(f"{Cores.CIANO}{'─'*70}{Cores.RESET}")
            for i, regra in enumerate(regras, 1):
                cor_acao = Cores.VERDE if regra['acao'] == 'PERMITIDO' else Cores.VERMELHO
                print(f"  {i}. IP: {regra['ip']:<15} | Porta: {regra['porta']:<6} | Ação: {cor_acao}{regra['acao']}{Cores.RESET}")
            print(f"{Cores.CIANO}{'─'*70}{Cores.RESET}\n")
            
            return regras
    except FileNotFoundError:
        print(f"{Cores.VERMELHO}❌ ERRO: Arquivo '{arquivo}' não encontrado!{Cores.RESET}")
        return []
    except json.JSONDecodeError:
        print(f"{Cores.VERMELHO}❌ ERRO: Formato JSON inválido no arquivo '{arquivo}'!{Cores.RESET}")
        return []

def verificar_porta(ip, porta, timeout=1):
    """Testa se uma porta está respondendo"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        resultado = s.connect_ex((ip, porta))
        s.close()
        return resultado == 0
    except socket.gaierror:
        return None  # Host não encontrado
    except:
        return False

def filtrar_pacote(pacote, regras):
    """Aplica regras de filtragem no pacote"""
    for regra in regras:
        if pacote['ip'] == regra['ip'] and pacote['porta'] == regra['porta']:
            return regra['acao']
    return "BLOQUEADO"  # Política padrão: negar tudo que não tem regra

def testar_pacote(pacote, regras, numero):
    """Testa um pacote específico"""
    print(f"{Cores.BOLD}{Cores.AZUL}🔍 Teste #{numero}: {pacote['ip']}:{pacote['porta']}{Cores.RESET}")
    print(f"{Cores.CIANO}{'─'*70}{Cores.RESET}")
    
    # 1. Teste de conectividade
    print(f"  📡 Testando conectividade...", end=" ")
    porta_status = verificar_porta(pacote['ip'], pacote['porta'])
    
    if porta_status is None:
        print(f"{Cores.AMARELO}⚠️  Host não encontrado (DNS falhou){Cores.RESET}")
    elif porta_status:
        print(f"{Cores.VERDE}✓ Porta ABERTA (serviço respondendo){Cores.RESET}")
    else:
        print(f"{Cores.VERMELHO}✗ Porta FECHADA (sem resposta){Cores.RESET}")
    
    # 2. Aplicação das regras
    resultado = filtrar_pacote(pacote, regras)
    print(f"  🛡️  Decisão do Firewall...", end=" ")
    
    if resultado == "PERMITIDO":
        print(f"{Cores.VERDE}{Cores.BOLD}✅ PERMITIDO{Cores.RESET}")
        print(f"      → Tráfego autorizado pelas regras")
    else:
        print(f"{Cores.VERMELHO}{Cores.BOLD}❌ BLOQUEADO{Cores.RESET}")
        print(f"      → Tráfego negado (regra de bloqueio ou sem regra)")
    
    print(f"{Cores.CIANO}{'─'*70}{Cores.RESET}\n")
    
    return resultado

def obter_descricao_servico(porta):
    """Retorna descrição comum do serviço"""
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

def modo_interativo(regras):
    """Modo interativo para testar pacotes personalizados"""
    print(f"\n{Cores.BOLD}{Cores.VERDE}🎮 MODO INTERATIVO{Cores.RESET}")
    print(f"{Cores.AMARELO}Digite os dados do pacote para testar (ou 'sair' para encerrar){Cores.RESET}\n")
    
    contador = 1
    while True:
        try:
            ip = input(f"{Cores.CIANO}IP de destino (ou 'sair'): {Cores.RESET}").strip()
            if ip.lower() == 'sair' or ip == '':
                print(f"{Cores.AMARELO}👋 Saindo do modo interativo...{Cores.RESET}")
                break
            
            porta = input(f"{Cores.CIANO}Porta (ou 'sair'): {Cores.RESET}").strip()
            if porta.lower() == 'sair' or porta == '':
                print(f"{Cores.AMARELO}👋 Saindo do modo interativo...{Cores.RESET}")
                break
            
            try:
                porta = int(porta)
            except ValueError:
                print(f"{Cores.VERMELHO}❌ Porta inválida! Digite um número.{Cores.RESET}\n")
                continue
            
            servico = obter_descricao_servico(porta)
            print(f"{Cores.AMARELO}ℹ️  Serviço comum: {servico}{Cores.RESET}\n")
            
            pacote = {"ip": ip, "porta": porta}
            testar_pacote(pacote, regras, contador)
            contador += 1
            
            # Pergunta se quer continuar
            continuar = input(f"{Cores.VERDE}Testar outro pacote? (s/n ou Enter para sair): {Cores.RESET}").strip().lower()
            if continuar == 'n' or continuar == 'sair' or continuar == '':
                print(f"{Cores.AMARELO}👋 Saindo do modo interativo...{Cores.RESET}")
                break
            print()  # Linha em branco para organizar
            
        except KeyboardInterrupt:
            print(f"\n{Cores.AMARELO}⚠️  Interrompido pelo usuário{Cores.RESET}")
            break

def main():
    """Função principal"""
    print_header()
    
    # Carrega regras
    regras = carregar_regras("regras.json")
    
    if not regras:
        print(f"{Cores.VERMELHO}⚠️  Nenhuma regra carregada. Encerrando...{Cores.RESET}")
        return
    
    # Testes automáticos
    print(f"{Cores.BOLD}{Cores.VERDE}🚀 EXECUTANDO TESTES AUTOMÁTICOS{Cores.RESET}\n")
    
    pacotes_teste = [
        {"ip": "8.8.8.8", "porta": 53},          # DNS Google
        {"ip": "192.168.0.10", "porta": 80},     # HTTP Local
        {"ip": "10.0.0.5", "porta": 22},         # SSH
        {"ip": "1.1.1.1", "porta": 443},         # HTTPS Cloudflare
    ]
    
    resultados = {"PERMITIDO": 0, "BLOQUEADO": 0}
    
    for i, pacote in enumerate(pacotes_teste, 1):
        resultado = testar_pacote(pacote, regras, i)
        resultados[resultado] += 1
    
    # Estatísticas
    print(f"{Cores.BOLD}{Cores.AZUL}📊 ESTATÍSTICAS DOS TESTES{Cores.RESET}")
    print(f"{Cores.CIANO}{'─'*70}{Cores.RESET}")
    print(f"  {Cores.VERDE}✅ Permitidos: {resultados['PERMITIDO']}{Cores.RESET}")
    print(f"  {Cores.VERMELHO}❌ Bloqueados: {resultados['BLOQUEADO']}{Cores.RESET}")
    print(f"  📦 Total de testes: {len(pacotes_teste)}")
    print(f"{Cores.CIANO}{'─'*70}{Cores.RESET}\n")
    
    # Pergunta se quer modo interativo
    resposta = input(f"{Cores.AMARELO}Deseja testar pacotes personalizados? (s/n): {Cores.RESET}").strip().lower()
    if resposta == 's':
        modo_interativo(regras)
    
    # Finalização
    print(f"\n{Cores.CIANO}{'='*70}{Cores.RESET}")
    print(f"{Cores.VERDE}{Cores.BOLD}✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!{Cores.RESET}")
    print(f"{Cores.CIANO}{'='*70}{Cores.RESET}\n")

if __name__ == "__main__":
    main()
