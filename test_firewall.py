"""
Testes Unitários para o Simulador de Firewall
Testa todas as funções principais do sistema de filtragem de pacotes.
"""

import unittest
import json
import os
from app import (
    carregar_regras,
    salvar_regras,
    verificar_porta,
    filtrar_pacote,
    obter_descricao_servico,
    calcular_estatisticas
)


class TestCarregarRegras(unittest.TestCase):
    """
    Testes para a função de carregamento de regras.
    """
    
    def test_carregar_regras_arquivo_existe(self):
        """
        Testa se as regras são carregadas corretamente quando o arquivo existe.
        """
        regras = carregar_regras()
        
        # Verifica se retorna uma lista
        self.assertIsInstance(regras, list)
        
        # Verifica se tem pelo menos uma regra
        self.assertGreater(len(regras), 0)
    
    def test_regras_tem_campos_obrigatorios(self):
        """
        Testa se cada regra tem os campos obrigatórios: ip, porta, acao.
        """
        regras = carregar_regras()
        
        for regra in regras:
            self.assertIn('ip', regra)
            self.assertIn('porta', regra)
            self.assertIn('acao', regra)
    
    def test_acao_valida(self):
        """
        Testa se a ação de cada regra é PERMITIDO ou BLOQUEADO.
        """
        regras = carregar_regras()
        
        for regra in regras:
            self.assertIn(regra['acao'], ['PERMITIDO', 'BLOQUEADO'])
    
    def test_porta_eh_numero(self):
        """
        Testa se a porta é um número inteiro válido.
        """
        regras = carregar_regras()
        
        for regra in regras:
            self.assertIsInstance(regra['porta'], int)
            self.assertGreaterEqual(regra['porta'], 1)
            self.assertLessEqual(regra['porta'], 65535)


class TestSalvarRegras(unittest.TestCase):
    """
    Testes para a função de salvamento de regras.
    """
    
    def setUp(self):
        """
        Prepara o ambiente para cada teste.
        Carrega as regras originais para restaurar depois.
        """
        self.regras_originais = carregar_regras()
    
    def tearDown(self):
        """
        Limpa após cada teste.
        Restaura as regras originais.
        """
        salvar_regras(self.regras_originais)
    
    def test_salvar_regras_sucesso(self):
        """
        Testa se as regras são salvas com sucesso.
        """
        regras_teste = [
            {"ip": "192.168.1.1", "porta": 80, "acao": "PERMITIDO"}
        ]
        
        resultado = salvar_regras(regras_teste)
        self.assertTrue(resultado)
    
    def test_salvar_e_carregar_regras(self):
        """
        Testa se as regras salvas podem ser carregadas corretamente.
        """
        regras_teste = [
            {"ip": "10.0.0.1", "porta": 443, "acao": "BLOQUEADO"},
            {"ip": "172.16.0.1", "porta": 22, "acao": "PERMITIDO"}
        ]
        
        # Salva as regras de teste
        salvar_regras(regras_teste)
        
        # Carrega as regras
        regras_carregadas = carregar_regras()
        
        # Verifica se são iguais
        self.assertEqual(len(regras_carregadas), len(regras_teste))
        self.assertEqual(regras_carregadas[0]['ip'], "10.0.0.1")
        self.assertEqual(regras_carregadas[1]['porta'], 22)


class TestVerificarPorta(unittest.TestCase):
    """
    Testes para a função de verificação de conectividade de porta.
    """
    
    def test_verificar_porta_localhost_80(self):
        """
        Testa conexão com localhost na porta 80.
        Pode retornar False (porta fechada) ou None (erro DNS).
        """
        resultado = verificar_porta('127.0.0.1', 80, timeout=1)
        
        # Resultado deve ser bool ou None
        self.assertIn(type(resultado), [bool, type(None)])
    
    def test_verificar_porta_google_dns(self):
        """
        Testa conexão com Google DNS (8.8.8.8:53).
        Este é um servidor público e geralmente responde.
        """
        resultado = verificar_porta('8.8.8.8', 53, timeout=2)
        
        # Pode ser True (aberta), False (fechada) ou None (erro DNS)
        self.assertIn(type(resultado), [bool, type(None)])
    
    def test_verificar_porta_timeout(self):
        """
        Testa se a função respeita o timeout.
        Usa um IP que não responde (10.255.255.1).
        """
        resultado = verificar_porta('10.255.255.1', 80, timeout=1)
        
        # Deve retornar False (timeout) ou None
        self.assertIn(resultado, [False, None])


class TestFiltrarPacote(unittest.TestCase):
    """
    Testes para a função de filtragem de pacotes.
    """
    
    def setUp(self):
        """
        Prepara regras de teste para os testes.
        """
        self.regras_teste = [
            {"ip": "192.168.1.1", "porta": 80, "acao": "PERMITIDO"},
            {"ip": "192.168.1.2", "porta": 22, "acao": "BLOQUEADO"},
            {"ip": "10.0.0.1", "porta": 443, "acao": "PERMITIDO"}
        ]
    
    def test_filtrar_pacote_permitido(self):
        """
        Testa se um pacote com regra PERMITIDO é permitido.
        """
        resultado = filtrar_pacote('192.168.1.1', 80, self.regras_teste)
        self.assertEqual(resultado, 'PERMITIDO')
    
    def test_filtrar_pacote_bloqueado(self):
        """
        Testa se um pacote com regra BLOQUEADO é bloqueado.
        """
        resultado = filtrar_pacote('192.168.1.2', 22, self.regras_teste)
        self.assertEqual(resultado, 'BLOQUEADO')
    
    def test_filtrar_pacote_sem_regra(self):
        """
        Testa se um pacote sem regra é bloqueado (fail-safe).
        """
        resultado = filtrar_pacote('192.168.1.100', 3306, self.regras_teste)
        self.assertEqual(resultado, 'BLOQUEADO')
    
    def test_filtrar_pacote_ip_diferente(self):
        """
        Testa se um pacote com IP diferente é bloqueado.
        """
        resultado = filtrar_pacote('192.168.1.1', 22, self.regras_teste)
        self.assertEqual(resultado, 'BLOQUEADO')
    
    def test_filtrar_pacote_porta_diferente(self):
        """
        Testa se um pacote com porta diferente é bloqueado.
        """
        resultado = filtrar_pacote('192.168.1.1', 443, self.regras_teste)
        self.assertEqual(resultado, 'BLOQUEADO')


class TestObterDescricaoServico(unittest.TestCase):
    """
    Testes para a função de descrição de serviços.
    """
    
    def test_descricao_porta_22_ssh(self):
        """
        Testa se a porta 22 é identificada como SSH.
        """
        descricao = obter_descricao_servico(22)
        self.assertEqual(descricao, 'SSH')
    
    def test_descricao_porta_80_http(self):
        """
        Testa se a porta 80 é identificada como HTTP.
        """
        descricao = obter_descricao_servico(80)
        self.assertEqual(descricao, 'HTTP')
    
    def test_descricao_porta_443_https(self):
        """
        Testa se a porta 443 é identificada como HTTPS.
        """
        descricao = obter_descricao_servico(443)
        self.assertEqual(descricao, 'HTTPS')
    
    def test_descricao_porta_53_dns(self):
        """
        Testa se a porta 53 é identificada como DNS.
        """
        descricao = obter_descricao_servico(53)
        self.assertEqual(descricao, 'DNS')
    
    def test_descricao_porta_desconhecida(self):
        """
        Testa se uma porta desconhecida retorna "Desconhecido".
        """
        descricao = obter_descricao_servico(9999)
        self.assertEqual(descricao, 'Desconhecido')
    
    def test_descricao_porta_3306_mysql(self):
        """
        Testa se a porta 3306 é identificada como MySQL.
        """
        descricao = obter_descricao_servico(3306)
        self.assertEqual(descricao, 'MySQL')


class TestCalcularEstatisticas(unittest.TestCase):
    """
    Testes para a função de cálculo de estatísticas.
    """
    
    def setUp(self):
        """
        Prepara regras de teste para os testes.
        """
        self.regras_teste = [
            {"ip": "192.168.1.1", "porta": 80, "acao": "PERMITIDO"},
            {"ip": "192.168.1.2", "porta": 22, "acao": "BLOQUEADO"},
            {"ip": "10.0.0.1", "porta": 443, "acao": "PERMITIDO"},
            {"ip": "10.0.0.2", "porta": 25, "acao": "BLOQUEADO"}
        ]
    
    def test_calcular_estatisticas_total(self):
        """
        Testa se o total de regras é calculado corretamente.
        """
        stats = calcular_estatisticas(self.regras_teste)
        self.assertEqual(stats['total'], 4)
    
    def test_calcular_estatisticas_permitidos(self):
        """
        Testa se a contagem de PERMITIDOS é correta.
        """
        stats = calcular_estatisticas(self.regras_teste)
        self.assertEqual(stats['permitidos'], 2)
    
    def test_calcular_estatisticas_bloqueados(self):
        """
        Testa se a contagem de BLOQUEADOS é correta.
        """
        stats = calcular_estatisticas(self.regras_teste)
        self.assertEqual(stats['bloqueados'], 2)
    
    def test_calcular_estatisticas_lista_vazia(self):
        """
        Testa se as estatísticas funcionam com lista vazia.
        """
        stats = calcular_estatisticas([])
        self.assertEqual(stats['total'], 0)
        self.assertEqual(stats['permitidos'], 0)
        self.assertEqual(stats['bloqueados'], 0)
    
    def test_calcular_estatisticas_apenas_permitidos(self):
        """
        Testa estatísticas com apenas regras PERMITIDO.
        """
        regras = [
            {"ip": "192.168.1.1", "porta": 80, "acao": "PERMITIDO"},
            {"ip": "192.168.1.2", "porta": 443, "acao": "PERMITIDO"}
        ]
        stats = calcular_estatisticas(regras)
        self.assertEqual(stats['permitidos'], 2)
        self.assertEqual(stats['bloqueados'], 0)


class TestIntegracao(unittest.TestCase):
    """
    Testes de integração do sistema completo.
    """
    
    def setUp(self):
        """
        Prepara o ambiente para testes de integração.
        """
        self.regras_originais = carregar_regras()
    
    def tearDown(self):
        """
        Restaura o estado original após os testes.
        """
        salvar_regras(self.regras_originais)
    
    def test_fluxo_completo_adicionar_e_filtrar(self):
        """
        Testa o fluxo completo: adicionar regra, salvar, carregar e filtrar.
        """
        # Cria nova regra
        nova_regra = {"ip": "203.0.113.1", "porta": 8080, "acao": "PERMITIDO"}
        regras = carregar_regras()
        regras.append(nova_regra)
        
        # Salva
        self.assertTrue(salvar_regras(regras))
        
        # Carrega novamente
        regras_carregadas = carregar_regras()
        
        # Verifica se a regra foi adicionada
        encontrada = any(
            r['ip'] == "203.0.113.1" and r['porta'] == 8080
            for r in regras_carregadas
        )
        self.assertTrue(encontrada)
        
        # Testa filtragem
        resultado = filtrar_pacote("203.0.113.1", 8080, regras_carregadas)
        self.assertEqual(resultado, "PERMITIDO")
    
    def test_fluxo_completo_com_estatisticas(self):
        """
        Testa o fluxo completo incluindo cálculo de estatísticas.
        """
        regras = carregar_regras()
        
        # Calcula estatísticas
        stats = calcular_estatisticas(regras)
        
        # Verifica se os números fazem sentido
        self.assertEqual(
            stats['total'],
            stats['permitidos'] + stats['bloqueados']
        )
        self.assertGreaterEqual(stats['total'], 0)


if __name__ == '__main__':
    # Executa todos os testes com verbosidade
    unittest.main(verbosity=2)
