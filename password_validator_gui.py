import enum as TipoEnumeracao
import re as ProcessadorExpressoesRegulares
import string as ConstantesConjuntoCaracteres
import hashlib as BibliotecaAlgoritmoHashSeguro
import base64 as BibliotecaCodificacaoBase64
import os as InterfaceSistemaOperacional
import functools as AuxiliarFerramentasFuncionais
import gzip as InterfaceCompressaoGzip
import tkinter as KitFerramentasInterfaceGraficaUsuario
from tkinter import ttk as WidgetsThemedTkinter
from tkinter import scrolledtext as WidgetTextoRolavel
from typing import Dict as TipoDicionario
from typing import List as TipoLista
from typing import Optional as TipoOpcional
from typing import Set as TipoConjunto
from typing import Tuple as TipoTupla
from typing import Any as TipoQualquer
from typing import Union as TipoUniao
from dataclasses import dataclass as DecoradorDataClass
from dataclasses import field as AuxiliarCampoDataClass
from pathlib import Path as ObjetoCaminhoSistemaArquivos
from difflib import SequenceMatcher as UtilitarioComparacaoSequencia
from datetime import datetime as ProvedorObjetoDataHora
import math as OperacoesMatematicas

class IndicadorNivelSeguranca(TipoEnumeracao.Enum):
    EXTREMAMENTE_BAIXO = 0
    BAIXO = 1
    MEDIO = 2
    ALTO = 3
    MUITO_ALTO = 4
    MUITO_FRACA = 0
    FRACA = 1
    MODERADA = 2
    FORTE = 3
    MUITO_FORTE = 4

@DecoradorDataClass
class ContainerResultadoAvaliacao:
    flag_atende_criterios: bool = False
    categoria_avaliada: IndicadorNivelSeguranca = IndicadorNivelSeguranca.EXTREMAMENTE_BAIXO
    lista_razoes_falha: TipoLista[str] = AuxiliarCampoDataClass(default_factory=list)
    metrica_quantitativa: int = 0
    lista_dicas_aprimoramento: TipoLista[str] = AuxiliarCampoDataClass(default_factory=list)
    valor_entropia_informacao: float = 0.0
    rotulo_duracao_quebra_estimada: str = "indeterminado"

class UnidadeProcessadoraStringSegura:
    def __init__(self, componente_secreto_auxiliar: TipoOpcional[str] = None, fator_custo_computacional: int = 100000):
        self._aditivo_secreto_interno = componente_secreto_auxiliar if componente_secreto_auxiliar is not None else "P1m3nt4S3cr3t4P4r4D3m0"
        self._parametro_iteracao_hash = max(10000, fator_custo_computacional)

    def gerar_representacao_segura(self, dados_string_entrada: str) -> TipoDicionario[str, TipoQualquer]:
        valor_sal_unico = InterfaceSistemaOperacional.urandom(32)
        string_com_pepper_intermediaria = dados_string_entrada + self._aditivo_secreto_interno
        string_com_pepper_codificada = string_com_pepper_intermediaria.encode('utf-8')
        chave_hash_derivada = BibliotecaAlgoritmoHashSeguro.pbkdf2_hmac(
            'sha256',
            string_com_pepper_codificada,
            valor_sal_unico,
            self._parametro_iteracao_hash,
            dklen=64
        )
        string_hash_codificada = BibliotecaCodificacaoBase64.b64encode(chave_hash_derivada).decode('utf-8')
        string_sal_codificada = BibliotecaCodificacaoBase64.b64encode(valor_sal_unico).decode('utf-8')
        estrutura_saida = {
            'id_algoritmo_hash': 'pbkdf2_sha256',
            'valor_hash_derivado': string_hash_codificada,
            'valor_sal_unico': string_sal_codificada,
            'contagem_iteracoes_usada': self._parametro_iteracao_hash,
            'timestamp_criacao': ProvedorObjetoDataHora.now().isoformat()
        }
        return estrutura_saida

    def validar_string_contra_representacao(self, string_texto_plano: str, dados_representacao_armazenados: TipoDicionario[str, TipoQualquer]) -> bool:
        chaves_necessarias = ('valor_hash_derivado', 'valor_sal_unico', 'id_algoritmo_hash', 'contagem_iteracoes_usada')
        todas_chaves_estao_presentes = all(nome_chave in dados_representacao_armazenados for nome_chave in chaves_necessarias)
        if not todas_chaves_estao_presentes:
            return False
        id_algoritmo_armazenado = dados_representacao_armazenados['id_algoritmo_hash']
        algoritmo_e_suportado = (id_algoritmo_armazenado == 'pbkdf2_sha256')
        if not algoritmo_e_suportado:
            return False
        try:
            bytes_sal_decodificados = BibliotecaCodificacaoBase64.b64decode(dados_representacao_armazenados['valor_sal_unico'])
        except Exception:
            return False
        string_com_pepper_para_verificar = string_texto_plano + self._aditivo_secreto_interno
        string_com_pepper_codificada_verificar = string_com_pepper_para_verificar.encode('utf-8')
        contagem_iteracao_armazenada = dados_representacao_armazenados['contagem_iteracoes_usada']
        chave_hash_recalculada = BibliotecaAlgoritmoHashSeguro.pbkdf2_hmac(
            'sha256',
            string_com_pepper_codificada_verificar,
            bytes_sal_decodificados,
            contagem_iteracao_armazenada,
            dklen=64
        )
        string_hash_recalculada_b64 = BibliotecaCodificacaoBase64.b64encode(chave_hash_recalculada).decode('utf-8')
        valor_hash_original_armazenado = dados_representacao_armazenados['valor_hash_derivado']
        hashes_sao_identicos = BibliotecaAlgoritmoHashSeguro.compare_digest(string_hash_recalculada_b64, valor_hash_original_armazenado)
        return hashes_sao_identicos

    @staticmethod
    def mascarar_carga_dados(carga_dados: TipoUniao[str, bytes], chave_mascaramento: str) -> bytes:
        sal_estatico_para_mascaramento = b'sal_estatico_inseguro_demo'
        bytes_mascaramento_derivados = BibliotecaAlgoritmoHashSeguro.pbkdf2_hmac(
            'sha256',
            chave_mascaramento.encode('utf-8'),
            sal_estatico_para_mascaramento,
            10000,
            dklen=32
        )
        if isinstance(carga_dados, str):
            bytes_carga = carga_dados.encode('utf-8')
        elif isinstance(carga_dados, bytes):
            bytes_carga = carga_dados
        else:
             raise TypeError("A carga de dados deve ser string ou bytes para mascaramento")
        bytearray_resultado_mascarado = bytearray(len(bytes_carga))
        comprimento_mascara = len(bytes_mascaramento_derivados)
        for posicao_indice, valor_byte_dados in enumerate(bytes_carga):
            byte_mascaramento = bytes_mascaramento_derivados[posicao_indice % comprimento_mascara]
            bytearray_resultado_mascarado[posicao_indice] = valor_byte_dados ^ byte_mascaramento
        try:
            dados_mascarados_comprimidos = InterfaceCompressaoGzip.compress(bytearray_resultado_mascarado)
            saida_final = dados_mascarados_comprimidos
        except Exception:
            saida_final = bytes(bytearray_resultado_mascarado)
        return saida_final

    @staticmethod
    def desmascarar_carga_dados(carga_mascarada: bytes, chave_mascaramento: str) -> bytes:
        try:
            carga_descomprimida = InterfaceCompressaoGzip.decompress(carga_mascarada)
        except Exception:
            carga_descomprimida = carga_mascarada
        sal_estatico_para_mascaramento = b'sal_estatico_inseguro_demo'
        bytes_mascaramento_derivados = BibliotecaAlgoritmoHashSeguro.pbkdf2_hmac(
            'sha256',
            chave_mascaramento.encode('utf-8'),
            sal_estatico_para_mascaramento,
            10000,
            dklen=32
        )
        bytearray_resultado_desmascarado = bytearray(len(carga_descomprimida))
        comprimento_mascara = len(bytes_mascaramento_derivados)
        try:
            for posicao_indice, valor_byte_mascarado in enumerate(carga_descomprimida):
                byte_mascaramento = bytes_mascaramento_derivados[posicao_indice % comprimento_mascara]
                bytearray_resultado_desmascarado[posicao_indice] = valor_byte_mascarado ^ byte_mascaramento
            bytes_dados_originais = bytes(bytearray_resultado_desmascarado)
        except Exception:
             bytes_dados_originais = b''
        return bytes_dados_originais

class InterfaceRegistroDadosComprometidos:
    def __init__(self, fonte_dados_comprometidos_conhecidos: TipoOpcional[ObjetoCaminhoSistemaArquivos] = None):
        self._registro_interno_hash_comprometido: TipoConjunto[str] = set()
        self._preencher_registro_interno(fonte_dados_comprometidos_conhecidos)

    def _preencher_registro_interno(self, localizacao_arquivo_dados: TipoOpcional[ObjetoCaminhoSistemaArquivos]) -> None:
        entradas_comprometidas_padrao = {
            "123456", "password", "123456789", "12345678", "12345", "qwerty",
            "1234567", "111111", "1234567890", "123123", "admin", "letmein",
            "welcome", "monkey", "1234", "sunshine", "master", "hottie",
            "football", "baseball", "access", "superman", "iloveyou", "trustno1",
            "dragao", "sombra", "princesa", "segredo", "google"
        }
        iterador_entradas_padrao = iter(entradas_comprometidas_padrao)
        while True:
            try:
                entrada_atual = next(iterador_entradas_padrao)
                representacao_hash = self._gerar_hash_comparacao(entrada_atual)
                if representacao_hash:
                    self._registro_interno_hash_comprometido.add(representacao_hash)
            except StopIteration:
                break
        carregar_do_arquivo = localizacao_arquivo_dados is not None and localizacao_arquivo_dados.exists() and localizacao_arquivo_dados.is_file()
        if carregar_do_arquivo:
            try:
                with open(localizacao_arquivo_dados, 'r', encoding='utf-8', errors='ignore') as manipulador_arquivo:
                    leitor_linha = iter(manipulador_arquivo)
                    while True:
                        try:
                            conteudo_linha = next(leitor_linha)
                            linha_processada = conteudo_linha.strip()
                            if len(linha_processada) > 0:
                                hash_adicional = self._gerar_hash_comparacao(linha_processada)
                                if hash_adicional:
                                    self._registro_interno_hash_comprometido.add(hash_adicional)
                        except StopIteration:
                            break
            except IOError as erro_acesso_arquivo:
                pass
            except Exception as erro_geral:
                pass

    @staticmethod
    @AuxiliarFerramentasFuncionais.lru_cache(maxsize=2048)
    def _gerar_hash_comparacao(string_entrada: str) -> str:
        try:
            bytes_string_codificada = string_entrada.encode('utf-8')
            hasher_sha1 = BibliotecaAlgoritmoHashSeguro.sha1()
            hasher_sha1.update(bytes_string_codificada)
            resultado_digest_hex = hasher_sha1.hexdigest()
            digest_hex_maiusculo = resultado_digest_hex.upper()
            return digest_hex_maiusculo
        except Exception:
            return ""

    def verificar_status_comprometimento_string(self, string_entrada_para_verificar: str) -> bool:
        hash_alvo = self._gerar_hash_comparacao(string_entrada_para_verificar)
        esta_comprometido = bool(hash_alvo) and (hash_alvo in self._registro_interno_hash_comprometido)
        return esta_comprometido

    def executar_busca_k_anonimato_simulada(self, string_entrada_para_verificar: str) -> bool:
        resultado_verificacao_local = self.verificar_status_comprometimento_string(string_entrada_para_verificar)
        return resultado_verificacao_local

class ModuloAvaliadorStringSeguranca:
    def __init__(self):
        self._config_limiar_comprimento_minimo: int = 8
        self._config_limiar_comprimento_maximo: int = 128
        self._config_flag_exigir_maiuscula: bool = True
        self._config_flag_exigir_minuscula: bool = True
        self._config_flag_exigir_digito: bool = True
        self._config_flag_exigir_especial: bool = True
        self._config_min_caracteres_unicos: int = 5
        self._config_ativar_verificacao_vazamento: bool = True
        self._config_ativar_verificacao_similaridade: bool = True
        self._registro_senhas_comuns: TipoConjunto[str] = {
            "password", "123456", "qwerty", "admin", "welcome", "senha", "senha123",
            "letmein", "monkey", "abc123", "111111", "12345678", "administrador"
        }
        self._lista_palavras_proibidas: TipoConjunto[str] = set()

        self._verificador_vazamento_instancia = InterfaceRegistroDadosComprometidos()

        self._regex_padrao_repeticao = ProcessadorExpressoesRegulares.compile(r'(.)\1{2,}')
        self._regex_padrao_sequencia = ProcessadorExpressoesRegulares.compile(
            r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789|987|876|765|654|543|432|321|210)',
            ProcessadorExpressoesRegulares.IGNORECASE
        )

    def configurar_limiar_comprimento_minimo(self, comprimento: int) -> 'ModuloAvaliadorStringSeguranca':
        self._config_limiar_comprimento_minimo = max(1, comprimento)
        return self

    def configurar_limiar_comprimento_maximo(self, comprimento: int) -> 'ModuloAvaliadorStringSeguranca':
        self._config_limiar_comprimento_maximo = max(self._config_limiar_comprimento_minimo, comprimento)
        return self

    def exigir_caracteres_maiusculos(self, exigido: bool = True) -> 'ModuloAvaliadorStringSeguranca':
        self._config_flag_exigir_maiuscula = exigido
        return self

    def exigir_caracteres_minusculos(self, exigido: bool = True) -> 'ModuloAvaliadorStringSeguranca':
        self._config_flag_exigir_minuscula = exigido
        return self

    def exigir_digitos_numericos(self, exigido: bool = True) -> 'ModuloAvaliadorStringSeguranca':
        self._config_flag_exigir_digito = exigido
        return self

    def exigir_caracteres_especiais(self, exigido: bool = True) -> 'ModuloAvaliadorStringSeguranca':
        self._config_flag_exigir_especial = exigido
        return self

    def definir_contagem_minima_unicos(self, contagem: int) -> 'ModuloAvaliadorStringSeguranca':
        self._config_min_caracteres_unicos = max(1, contagem)
        return self

    def habilitar_verificacao_contra_vazamentos(self, habilitado: bool = True) -> 'ModuloAvaliadorStringSeguranca':
        self._config_ativar_verificacao_vazamento = habilitado
        return self

    def habilitar_verificacao_similaridade_palavras(self, habilitado: bool = True) -> 'ModuloAvaliadorStringSeguranca':
        self._config_ativar_verificacao_similaridade = habilitado
        return self

    def adicionar_termos_a_lista_negra(self, palavras: TipoLista[str]) -> 'ModuloAvaliadorStringSeguranca':
        self._lista_palavras_proibidas.update([p.lower() for p in palavras if isinstance(p, str)])
        return self

    def adicionar_entradas_comuns_proibidas(self, senhas: TipoLista[str]) -> 'ModuloAvaliadorStringSeguranca':
        self._registro_senhas_comuns.update([s.lower() for s in senhas if isinstance(s, str)])
        return self

    def _validar_contra_termos_proibidos(self, string_avaliada: str) -> TipoTupla[bool, TipoOpcional[str]]:
        string_avaliada_minusc = string_avaliada.lower()
        if string_avaliada_minusc in self._registro_senhas_comuns:
            return False, "A senha é muito comum e facilmente adivinhável"
        iterador_palavras_proibidas = iter(self._lista_palavras_proibidas)
        while True:
            try:
                palavra_proibida = next(iterador_palavras_proibidas)
                if len(palavra_proibida) > 3 and palavra_proibida in string_avaliada_minusc:
                    return False, f"A senha contém uma palavra proibida: '{palavra_proibida}'"
            except StopIteration:
                break
        if self._config_ativar_verificacao_similaridade:
            conjunto_termos_referencia = self._lista_palavras_proibidas.union(self._registro_senhas_comuns)
            iterador_termos_referencia = iter(conjunto_termos_referencia)
            while True:
                try:
                    termo_referencia = next(iterador_termos_referencia)
                    if len(termo_referencia) > 4:
                        calculador_similaridade = UtilitarioComparacaoSequencia(None, string_avaliada_minusc, termo_referencia)
                        indice_similaridade = calculador_similaridade.ratio()
                        if indice_similaridade > 0.8:
                            return False, f"A senha é muito similar a um termo comum/proibido: '{termo_referencia}'"
                except StopIteration:
                    break
        return True, None

    def _verificar_padroes_sequenciais_repetitivos(self, string_avaliada: str) -> TipoTupla[bool, TipoOpcional[str]]:
        string_avaliada_minusc = string_avaliada.lower()
        match_sequencia = self._regex_padrao_sequencia.search(string_avaliada_minusc)
        if match_sequencia:
            return False, f"A senha contém uma sequência óbvia: '{match_sequencia.group(0)}'"
        match_repeticao = self._regex_padrao_repeticao.search(string_avaliada)
        if match_repeticao:
            return False, f"A senha contém caracteres repetidos em sequência: '{match_repeticao.group(0)}'"
        return True, None

    def _calcular_entropia_aproximada(self, string_avaliada: str, contagens_tipos_char: TipoDicionario[str, int]) -> float:
        tamanho_pool_caracteres = 0
        if contagens_tipos_char.get('maiuscula', 0) > 0:
            tamanho_pool_caracteres += 26
        if contagens_tipos_char.get('minuscula', 0) > 0:
            tamanho_pool_caracteres += 26
        if contagens_tipos_char.get('digito', 0) > 0:
            tamanho_pool_caracteres += 10
        if contagens_tipos_char.get('especial', 0) > 0:
            tamanho_pool_caracteres += len(ConstantesConjuntoCaracteres.punctuation)
        if len(string_avaliada) > 0 and tamanho_pool_caracteres < 2:
             tamanho_pool_caracteres = 10
        elif len(string_avaliada) == 0:
             return 0.0
        if tamanho_pool_caracteres > 1:
            entropia_base = len(string_avaliada) * OperacoesMatematicas.log2(tamanho_pool_caracteres)
        else:
            entropia_base = 0.0
        entropia_ajustada = entropia_base
        string_avaliada_minusc = string_avaliada.lower()
        if self._regex_padrao_sequencia.search(string_avaliada_minusc):
            entropia_ajustada *= 0.8
        if self._regex_padrao_repeticao.search(string_avaliada):
            entropia_ajustada *= 0.7
        conjunto_termos_penalidade = self._lista_palavras_proibidas.union(self._registro_senhas_comuns)
        iterador_termos_penalidade = iter(conjunto_termos_penalidade)
        penalidade_aplicada_palavra = False
        while not penalidade_aplicada_palavra:
            try:
                termo = next(iterador_termos_penalidade)
                if len(termo) > 3 and termo in string_avaliada_minusc:
                    entropia_ajustada *= 0.6
                    penalidade_aplicada_palavra = True
            except StopIteration:
                break
        entropia_final = max(0.0, entropia_ajustada)
        return entropia_final

    def _estimar_tempo_quebra_forca_bruta(self, valor_entropia: float) -> str:
        tentativas_por_segundo = 10_000_000_000_000
        try:
            numero_tentativas_necessarias = 2 ** valor_entropia
        except OverflowError:
            return "milênios ou mais (valor de entropia muito alto)"
        if tentativas_por_segundo <= 0:
            return "indeterminado (taxa de tentativa inválida)"
        segundos_necessarios = numero_tentativas_necessarias / tentativas_por_segundo
        if segundos_necessarios < 0.001:
            return "instantaneamente"
        elif segundos_necessarios < 60:
            return "menos de um minuto"
        elif segundos_necessarios < 3600:
            return f"aproximadamente {int(segundos_necessarios/60)} minutos"
        elif segundos_necessarios < 86400:
            return f"aproximadamente {int(segundos_necessarios/3600)} horas"
        elif segundos_necessarios < 2_592_000:
            return f"aproximadamente {int(segundos_necessarios/86400)} dias"
        elif segundos_necessarios < 31_536_000:
             return f"aproximadamente {int(segundos_necessarios/2_592_000)} meses"
        elif segundos_necessarios < 315_360_000:
            return f"aproximadamente {int(segundos_necessarios/31_536_000)} anos"
        elif segundos_necessarios < 3_153_600_000:
            return "décadas"
        elif segundos_necessarios < 31_536_000_000:
            return "séculos"
        else:
            return "milênios ou mais"

    def avaliar_string(self, string_para_avaliar: str) -> ContainerResultadoAvaliacao:
        if not isinstance(string_para_avaliar, str):
             resultado_imediato = ContainerResultadoAvaliacao()
             resultado_imediato.lista_razoes_falha.append("Entrada fornecida não é uma string válida.")
             return resultado_imediato
        if string_para_avaliar is None:
            resultado_imediato = ContainerResultadoAvaliacao()
            resultado_imediato.lista_razoes_falha.append("A senha não pode ser nula.")
            return resultado_imediato

        resultado_processamento = ContainerResultadoAvaliacao()
        comprimento_string = len(string_para_avaliar)
        contagem_por_tipo_char = {
            'maiuscula': 0, 'minuscula': 0, 'digito': 0, 'especial': 0, 'desconhecido': 0
        }
        conjunto_caracteres_unicos = set()
        indice_char = 0
        while indice_char < comprimento_string:
            caractere_atual = string_para_avaliar[indice_char]
            conjunto_caracteres_unicos.add(caractere_atual)
            if caractere_atual.isupper():
                contagem_por_tipo_char['maiuscula'] += 1
            elif caractere_atual.islower():
                contagem_por_tipo_char['minuscula'] += 1
            elif caractere_atual.isdigit():
                contagem_por_tipo_char['digito'] += 1
            elif caractere_atual in ConstantesConjuntoCaracteres.punctuation:
                contagem_por_tipo_char['especial'] += 1
            else:
                contagem_por_tipo_char['desconhecido'] += 1
            indice_char += 1

        if comprimento_string < self._config_limiar_comprimento_minimo:
            resultado_processamento.lista_razoes_falha.append(
                f"A senha deve ter pelo menos {self._config_limiar_comprimento_minimo} caracteres (possui {comprimento_string})"
            )
        if comprimento_string > self._config_limiar_comprimento_maximo:
            resultado_processamento.lista_razoes_falha.append(
                f"A senha não pode ter mais de {self._config_limiar_comprimento_maximo} caracteres (possui {comprimento_string})"
            )
        contagem_unicos = len(conjunto_caracteres_unicos)
        if contagem_unicos < self._config_min_caracteres_unicos:
             resultado_processamento.lista_razoes_falha.append(
                f"A senha deve conter pelo menos {self._config_min_caracteres_unicos} caracteres únicos (possui {contagem_unicos})"
            )
        if self._config_flag_exigir_maiuscula and contagem_por_tipo_char['maiuscula'] == 0:
            resultado_processamento.lista_razoes_falha.append("A senha deve conter pelo menos uma letra maiúscula (A-Z)")
        if self._config_flag_exigir_minuscula and contagem_por_tipo_char['minuscula'] == 0:
            resultado_processamento.lista_razoes_falha.append("A senha deve conter pelo menos uma letra minúscula (a-z)")
        if self._config_flag_exigir_digito and contagem_por_tipo_char['digito'] == 0:
            resultado_processamento.lista_razoes_falha.append("A senha deve conter pelo menos um dígito numérico (0-9)")
        if self._config_flag_exigir_especial and contagem_por_tipo_char['especial'] == 0:
            resultado_processamento.lista_razoes_falha.append(f"A senha deve conter pelo menos um caractere especial (ex: {ConstantesConjuntoCaracteres.punctuation})")

        check_comum_ok, msg_comum = self._validar_contra_termos_proibidos(string_para_avaliar)
        if not check_comum_ok:
            resultado_processamento.lista_razoes_falha.append(msg_comum)
        check_seq_ok, msg_seq = self._verificar_padroes_sequenciais_repetitivos(string_para_avaliar)
        if not check_seq_ok:
            resultado_processamento.lista_razoes_falha.append(msg_seq)

        if self._config_ativar_verificacao_vazamento:
             foi_comprometida = self._verificador_vazamento_instancia.executar_busca_k_anonimato_simulada(string_para_avaliar)
             if foi_comprometida:
                 resultado_processamento.lista_razoes_falha.append("Esta senha foi encontrada em vazamentos de dados conhecidos e não é segura.")

        resultado_processamento.valor_entropia_informacao = self._calcular_entropia_aproximada(string_para_avaliar, contagem_por_tipo_char)
        resultado_processamento.rotulo_duracao_quebra_estimada = self._estimar_tempo_quebra_forca_bruta(resultado_processamento.valor_entropia_informacao)

        pontuacao_calculada = self._computar_pontuacao_quantitativa(string_para_avaliar, contagem_por_tipo_char, resultado_processamento.lista_razoes_falha)
        resultado_processamento.metrica_quantitativa = pontuacao_calculada
        resultado_processamento.categoria_avaliada = self._inferir_categoria_seguranca(pontuacao_calculada)

        resultado_processamento.flag_atende_criterios = len(resultado_processamento.lista_razoes_falha) == 0

        if not resultado_processamento.flag_atende_criterios:
            resultado_processamento.lista_dicas_aprimoramento = self._elaborar_dicas_aprimoramento(resultado_processamento.lista_razoes_falha)
        elif resultado_processamento.categoria_avaliada in [IndicadorNivelSeguranca.EXTREMAMENTE_BAIXO, IndicadorNivelSeguranca.BAIXO, IndicadorNivelSeguranca.MEDIO]:
             resultado_processamento.lista_dicas_aprimoramento.append("Considere tornar a senha ainda mais longa e complexa para maior segurança.")

        return resultado_processamento

    def _computar_pontuacao_quantitativa(self, string_avaliada: str, contagens_tipos_char: TipoDicionario[str, int], lista_falhas_atuais: TipoLista[str]) -> int:
        pontuacao_base = 0
        comprimento = len(string_avaliada)
        pontuacao_base += min(40, comprimento * 4)
        tipos_presentes = 0
        if contagens_tipos_char.get('maiuscula', 0) > 0: tipos_presentes += 1
        if contagens_tipos_char.get('minuscula', 0) > 0: tipos_presentes += 1
        if contagens_tipos_char.get('digito', 0) > 0: tipos_presentes += 1
        if contagens_tipos_char.get('especial', 0) > 0: tipos_presentes += 1
        pontuacao_base += tipos_presentes * 10
        pontuacao_base += min(10, contagens_tipos_char.get('maiuscula', 0))
        pontuacao_base += min(10, contagens_tipos_char.get('minuscula', 0))
        pontuacao_base += min(10, contagens_tipos_char.get('digito', 0))
        pontuacao_base += min(10, contagens_tipos_char.get('especial', 0))
        if comprimento > 0:
            ratio_unicos = len(set(string_avaliada)) / comprimento
            pontuacao_base += int(ratio_unicos * 20)
        pontuacao_penalidade = 0
        pontuacao_penalidade += len(lista_falhas_atuais) * 15
        if any("pelo menos" in falha and "caracteres" in falha for falha in lista_falhas_atuais):
            pontuacao_penalidade += 10
        if any("comum" in falha or "proibida" in falha or "similar" in falha for falha in lista_falhas_atuais):
            pontuacao_penalidade += 15
        if any("sequência" in falha or "repetidos" in falha for falha in lista_falhas_atuais):
            pontuacao_penalidade += 10
        if any("vazamentos de dados" in falha for falha in lista_falhas_atuais):
             pontuacao_penalidade += 25
        pontuacao_final = pontuacao_base - pontuacao_penalidade
        pontuacao_final_limitada = max(0, min(100, pontuacao_final))
        return pontuacao_final_limitada

    def _inferir_categoria_seguranca(self, metrica_pontuacao: int) -> IndicadorNivelSeguranca:
        if metrica_pontuacao < 20:
            return IndicadorNivelSeguranca.MUITO_FRACA
        elif metrica_pontuacao < 40:
            return IndicadorNivelSeguranca.FRACA
        elif metrica_pontuacao < 60:
            return IndicadorNivelSeguranca.MODERADA
        elif metrica_pontuacao < 80:
            return IndicadorNivelSeguranca.FORTE
        else:
            return IndicadorNivelSeguranca.MUITO_FORTE

    def _elaborar_dicas_aprimoramento(self, lista_falhas: TipoLista[str]) -> TipoLista[str]:
        dicas_geradas = []
        mapa_falha_dica = {
            "letra maiúscula": "Adicione pelo menos uma letra maiúscula (A-Z)",
            "letra minúscula": "Adicione pelo menos uma letra minúscula (a-z)",
            "dígito numérico": "Adicione pelo menos um número (0-9)",
            "caractere especial": f"Adicione pelo menos um caractere especial ({ConstantesConjuntoCaracteres.punctuation})",
            "caracteres únicos": "Use uma maior variedade de caracteres diferentes",
            "pelo menos": "Aumente o comprimento da sua senha",
            "comum": "Evite usar palavras comuns ou senhas conhecidas",
            "proibida": "Evite usar palavras comuns ou termos proibidos",
            "similar": "Evite usar senhas muito parecidas com palavras comuns",
            "sequência": "Evite sequências óbvias como '123', 'abc' ou caracteres repetidos",
            "repetidos": "Evite sequências óbvias ou caracteres repetidos",
            "vazamentos de dados": "Escolha uma senha completamente diferente, pois esta já foi comprometida"
        }
        dicas_adicionadas = set()
        for falha_item in lista_falhas:
            falha_lower = falha_item.lower()
            for gatilho, dica_correspondente in mapa_falha_dica.items():
                 # Caso especial para comprimento "pelo menos X caracteres"
                if gatilho == "pelo menos" and "pelo menos" in falha_lower and "caracteres" in falha_lower:
                    if dica_correspondente not in dicas_adicionadas:
                        dicas_geradas.append(dica_correspondente)
                        dicas_adicionadas.add(dica_correspondente)
                    continue # Próxima falha
                # Outros gatilhos
                elif gatilho != "pelo menos" and gatilho in falha_lower:
                    if dica_correspondente not in dicas_adicionadas:
                        dicas_geradas.append(dica_correspondente)
                        dicas_adicionadas.add(dica_correspondente)
                    # Não precisa continuar procurando gatilhos para esta falha se um foi encontrado
                    # (a menos que uma falha possa acionar múltiplas dicas)
                    # break # Descomente se uma falha só deve gerar uma dica

        # Adiciona dica genérica se nenhuma específica foi adicionada mas houve falhas
        if not dicas_geradas and lista_falhas:
             dicas_geradas.append("Revise os critérios de senha e tente uma combinação mais complexa.")

        return dicas_geradas


def validar_senha_simplificado(pwd_input: str, modo_verboso: bool = False) -> bool:
    instancia_validador = ModuloAvaliadorStringSeguranca()
    dados_resultado = instancia_validador.avaliar_string(pwd_input)

    if modo_verboso and not dados_resultado.flag_atende_criterios:
        print("Falhas de validação detectadas:")
        indice_falha = 0
        total_falhas = len(dados_resultado.lista_razoes_falha)
        while indice_falha < total_falhas:
            falha_atual = dados_resultado.lista_razoes_falha[indice_falha]
            print(f"- {falha_atual}")
            indice_falha += 1

        if dados_resultado.lista_dicas_aprimoramento:
            print("\nSugestões para melhoria:")
            indice_dica = 0
            total_dicas = len(dados_resultado.lista_dicas_aprimoramento)
            while indice_dica < total_dicas:
                dica_atual = dados_resultado.lista_dicas_aprimoramento[indice_dica]
                print(f"- {dica_atual}")
                indice_dica += 1

        print(f"\nNível de Segurança: {dados_resultado.categoria_avaliada.name}")
        print(f"Pontuação Quantitativa: {dados_resultado.metrica_quantitativa}/100")

    return dados_resultado.flag_atende_criterios


def analisar_senha_detalhadamente(pwd_input: str) -> None:
    instancia_analisador = ModuloAvaliadorStringSeguranca()
    dados_analise = instancia_analisador.avaliar_string(pwd_input)

    delimitador_visual = '=' * 60
    status_aprovacao = 'APROVADA' if dados_analise.flag_atende_criterios else 'REPROVADA'

    print(f"\n{delimitador_visual}")
    print(f"Análise da Senha Fornecida: {status_aprovacao}")
    print(f"{delimitador_visual}")

    print(f"Nível de Segurança Avaliado: {dados_analise.categoria_avaliada.name}")
    print(f"Métrica Quantitativa (Pontuação): {dados_analise.metrica_quantitativa}/100")
    print(f"Entropia Estimada: {dados_analise.valor_entropia_informacao:.2f} bits")
    print(f"Tempo Estimado para Quebra (Força Bruta): {dados_analise.rotulo_duracao_quebra_estimada}")


    if dados_analise.lista_razoes_falha:
        print("\nProblemas Identificados:")
        numero_item_problema = 1
        for item_falha in dados_analise.lista_razoes_falha:
            print(f"{numero_item_problema}. {item_falha}")
            numero_item_problema += 1

    if dados_analise.lista_dicas_aprimoramento:
        print("\nSugestões para Aprimoramento:")
        numero_item_dica = 1
        for item_dica in dados_analise.lista_dicas_aprimoramento:
            print(f"{numero_item_dica}. {item_dica}")
            numero_item_dica += 1

    print(f"\n{delimitador_visual}\n")


def criar_interface_grafica():
    instancia_validador_gui = ModuloAvaliadorStringSeguranca()

    def acao_botao_validar():
        senha_digitada = campo_entrada_senha.get()
        resultado_validacao_gui = instancia_validador_gui.avaliar_string(senha_digitada)

        texto_resultado_formatado = f"Resultado da Avaliação: {'APROVADA' if resultado_validacao_gui.flag_atende_criterios else 'REPROVADA'}\n"
        texto_resultado_formatado += f"Nível de Segurança: {resultado_validacao_gui.categoria_avaliada.name}\n"
        texto_resultado_formatado += f"Pontuação: {resultado_validacao_gui.metrica_quantitativa}/100\n"
        texto_resultado_formatado += f"Entropia (bits): {resultado_validacao_gui.valor_entropia_informacao:.2f}\n"
        texto_resultado_formatado += f"Tempo Estimado para Quebra: {resultado_validacao_gui.rotulo_duracao_quebra_estimada}\n"

        if resultado_validacao_gui.lista_razoes_falha:
            texto_resultado_formatado += "\nProblemas Encontrados:\n"
            num_problema = 1
            for falha_gui in resultado_validacao_gui.lista_razoes_falha:
                texto_resultado_formatado += f"{num_problema}. {falha_gui}\n"
                num_problema += 1

        if resultado_validacao_gui.lista_dicas_aprimoramento:
            texto_resultado_formatado += "\nSugestões para Melhorar:\n"
            num_dica = 1
            for dica_gui in resultado_validacao_gui.lista_dicas_aprimoramento:
                texto_resultado_formatado += f"{num_dica}. {dica_gui}\n"
                num_dica += 1

        caixa_texto_resultados.config(state=KitFerramentasInterfaceGraficaUsuario.NORMAL)
        caixa_texto_resultados.delete(1.0, KitFerramentasInterfaceGraficaUsuario.END)
        caixa_texto_resultados.insert(KitFerramentasInterfaceGraficaUsuario.END, texto_resultado_formatado)
        caixa_texto_resultados.config(state=KitFerramentasInterfaceGraficaUsuario.DISABLED)

    janela_principal = KitFerramentasInterfaceGraficaUsuario.Tk()
    janela_principal.title("Ferramenta de Avaliação de Segurança de Senhas")
    janela_principal.geometry("650x500") # Tamanho ajustado

    frame_principal = WidgetsThemedTkinter.Frame(janela_principal, padding="15 15 15 15")
    frame_principal.grid(row=0, column=0, sticky=(KitFerramentasInterfaceGraficaUsuario.W, KitFerramentasInterfaceGraficaUsuario.E, KitFerramentasInterfaceGraficaUsuario.N, KitFerramentasInterfaceGraficaUsuario.S))
    janela_principal.columnconfigure(0, weight=1)
    janela_principal.rowconfigure(0, weight=1)

    rotulo_instrucao_senha = WidgetsThemedTkinter.Label(frame_principal, text="Digite a Senha para Avaliação:")
    rotulo_instrucao_senha.grid(row=0, column=0, columnspan=2, sticky=KitFerramentasInterfaceGraficaUsuario.W, pady=(0, 5))

    campo_entrada_senha = WidgetsThemedTkinter.Entry(frame_principal, width=40, show="•") # Alterado show para ponto
    campo_entrada_senha.grid(row=1, column=0, sticky=(KitFerramentasInterfaceGraficaUsuario.W, KitFerramentasInterfaceGraficaUsuario.E), padx=(0, 10))

    botao_executar_validacao = WidgetsThemedTkinter.Button(frame_principal, text="Avaliar Agora", command=acao_botao_validar)
    botao_executar_validacao.grid(row=1, column=1, sticky=KitFerramentasInterfaceGraficaUsuario.E)

    rotulo_resultados = WidgetsThemedTkinter.Label(frame_principal, text="Detalhes da Avaliação:")
    rotulo_resultados.grid(row=2, column=0, columnspan=2, sticky=KitFerramentasInterfaceGraficaUsuario.W, pady=(10, 5))

    caixa_texto_resultados = WidgetTextoRolavel.ScrolledText(frame_principal, width=75, height=20, wrap=KitFerramentasInterfaceGraficaUsuario.WORD, state=KitFerramentasInterfaceGraficaUsuario.DISABLED)
    caixa_texto_resultados.grid(row=3, column=0, columnspan=2, sticky=(KitFerramentasInterfaceGraficaUsuario.W, KitFerramentasInterfaceGraficaUsuario.E, KitFerramentasInterfaceGraficaUsuario.N, KitFerramentasInterfaceGraficaUsuario.S))

    frame_principal.columnconfigure(0, weight=1)
    frame_principal.rowconfigure(3, weight=1)

    campo_entrada_senha.focus() # Foco inicial no campo de senha
    janela_principal.bind('<Return>', lambda evento: acao_botao_validar()) # Permite validar com Enter

    janela_principal.mainloop()

if __name__ == "__main__":
    print("Copyright © Delean Mafra, todos os direitos reservados | All rights reserved.")
    criar_interface_grafica()
