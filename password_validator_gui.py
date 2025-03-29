print("Copyright © Delean Mafra, todos os direitos reservados | All rights reserved.")

import enum
import re
import string
import hashlib
import base64
import os
import functools
import gzip
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Optional, Set, Tuple, Any, Union, Callable
from dataclasses import dataclass, field
from pathlib import Path
from difflib import SequenceMatcher
from datetime import datetime


class PasswordStrength(enum.Enum):
    """Níveis de força da senha."""
    MUITO_FRACA = 0
    FRACA = 1
    VERY_WEAK = 0
    WEAK = 1
    MODERATE = 2
    STRONG = 3
    VERY_STRONG = 4
    FORTE = 3
    MUITO_FORTE = 4


@dataclass
class ValidationResult:
    """Classe para armazenar o resultado da validação da senha."""
    is_valid: bool = False
    strength: PasswordStrength = PasswordStrength.MUITO_FRACA
    failures: List[str] = field(default_factory=list)
    score: int = 0
    suggestions: List[str] = field(default_factory=list)
    entropy: float = 0.0
    time_to_crack: str = "desconhecido"


class PasswordHasher:
    """
    Classe para lidar com hashing e criptografia de senhas de forma segura.
    Implementa funções de hash modernas com salt e pepper.
    """
    
    def __init__(self, pepper: str = None, iterations: int = 100000):
        """
        Inicializa o hasher de senhas.
        
        Args:
            pepper: Uma string secreta adicional para aumentar a segurança
            iterations: Número de iterações para o algoritmo PBKDF2
        """
        # Se não for fornecido um pepper, use um padrão (em produção, isso deve ser uma configuração de ambiente)
        self._pepper = pepper or "S3cur1tyP3pp3rF0rH4sh1ng"
        self._iterations = iterations
    
    def hash_password(self, password: str) -> Dict[str, str]:
        """
        Cria um hash seguro da senha usando PBKDF2 com salt.
        
        Args:
            password: A senha a ser hasheada.
            
        Returns:
            Dicionário contendo o hash, salt, algoritmo e metadados.
        """
        # Gerar um salt único para esta senha
        salt = os.urandom(32)
        
        # Combinar a senha com o pepper antes de hashear
        peppered_password = password + self._pepper
        
        # Usar PBKDF2 com SHA-256 para gerar o hash
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            peppered_password.encode('utf-8'),
            salt,
            self._iterations,
            dklen=64
        )
        
        # Retornar as informações necessárias para verificação futura
        # (tudo em base64 para armazenamento seguro em texto)
        return {
            'algorithm': 'pbkdf2_sha256',
            'hash': base64.b64encode(pwd_hash).decode('utf-8'),
            'salt': base64.b64encode(salt).decode('utf-8'),
            'iterations': self._iterations,
            'created_at': datetime.now().isoformat()
        }
    
    def verify_password(self, password: str, stored_hash_data: Dict[str, Any]) -> bool:
        """
        Verifica se uma senha corresponde ao hash armazenado.
        
        Args:
            password: A senha fornecida para verificação.
            stored_hash_data: Os dados do hash previamente gerados.
            
        Returns:
            True se a senha corresponde ao hash, False caso contrário.
        """
        # Verificar se temos todos os dados necessários
        if not all(k in stored_hash_data for k in ('hash', 'salt', 'algorithm', 'iterations')):
            return False
        
        # Verificar se o algoritmo é suportado
        if stored_hash_data['algorithm'] != 'pbkdf2_sha256':
            return False
            
        # Recuperar o salt
        salt = base64.b64decode(stored_hash_data['salt'])
        
        # Combinar a senha com o pepper
        peppered_password = password + self._pepper
        
        # Calcular o hash com os mesmos parâmetros
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            peppered_password.encode('utf-8'),
            salt,
            stored_hash_data['iterations'],
            dklen=64
        )
        
        # Converter o hash calculado para base64 para comparação
        calculated_hash_b64 = base64.b64encode(pwd_hash).decode('utf-8')
        
        # Comparar os hashes (usando comparação de tempo constante para evitar timing attacks)
        return hashlib.compare_digest(calculated_hash_b64, stored_hash_data['hash'])
    
    @staticmethod
    def encrypt_data(data: Union[str, bytes], key: str) -> bytes:
        """
        Criptografa dados com AES usando uma chave derivada da senha.
        Simplificado para demonstração - em produção use bibliotecas como cryptography.
        
        Args:
            data: Dados a serem criptografados
            key: Chave para criptografia
            
        Returns:
            Dados criptografados
        """
        # Em produção, use bibliotecas dedicadas como 'cryptography'
        # Este é um exemplo simplificado para demonstração
        
        # Derivar uma chave a partir da senha
        derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            key.encode('utf-8'),
            b'static_salt_for_encryption',
            10000,
            dklen=32
        )
        
        # Converter dados para bytes se for string
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # XOR simples para demonstração - NÃO USE ISSO EM PRODUÇÃO
        # Em produção, use AES-GCM da biblioteca cryptography
        result = bytearray(len(data))
        for i, byte in enumerate(data):
            result[i] = byte ^ derived_key[i % len(derived_key)]
        
        # Comprimir o resultado para demonstrar o uso do gzip
        return gzip.compress(result)
    
    @staticmethod
    def decrypt_data(encrypted_data: bytes, key: str) -> bytes:
        """
        Descriptografa dados criptografados.
        Simplificado para demonstração - em produção use bibliotecas como cryptography.
        
        Args:
            encrypted_data: Dados criptografados
            key: Chave para descriptografia
            
        Returns:
            Dados descriptografados
        """
        # Descomprimir os dados
        try:
            decompressed = gzip.decompress(encrypted_data)
        except Exception:
            return b''
        
        # Derivar a mesma chave
        derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            key.encode('utf-8'),
            b'static_salt_for_encryption',
            10000,
            dklen=32
        )
        
        # Realizar o XOR inverso
        result = bytearray(len(decompressed))
        for i, byte in enumerate(decompressed):
            result[i] = byte ^ derived_key[i % len(derived_key)]
            
        return bytes(result)


class LeakChecker:
    """
    Classe para verificar se uma senha foi comprometida em vazamentos conhecidos.
    Usa um sistema local simplificado, mas poderia integrar com APIs como "Have I Been Pwned".
    """
    
    def __init__(self, leaked_passwords_file: Optional[Path] = None):
        """
        Inicializa o verificador de vazamentos.
        
        Args:
            leaked_passwords_file: Caminho opcional para um arquivo contendo senhas vazadas
        """
        self._leaked_hashes = set()
        self._load_leaked_passwords(leaked_passwords_file)
    
    def _load_leaked_passwords(self, file_path: Optional[Path]) -> None:
        """Carrega senhas vazadas do arquivo especificado ou usa um conjunto padrão."""
        # Lista pequena de senhas comprometidas comuns para demonstração
        default_passwords = {
            "123456", "password", "123456789", "12345678", "12345", "qwerty",
            "1234567", "111111", "1234567890", "123123", "admin", "letmein",
            "welcome", "monkey", "1234", "sunshine", "master", "hottie",
            "football", "baseball", "access", "superman", "iloveyou", "trustno1"
        }
        
        # Inicializar com as senhas padrão
        for pwd in default_passwords:
            # Armazenar apenas os hashes para economizar espaço e aumentar privacidade
            self._leaked_hashes.add(self._hash_for_comparison(pwd))
        
        # Se um arquivo for fornecido, carregue senhas adicionais
        if file_path and file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        pwd = line.strip()
                        if pwd:
                            self._leaked_hashes.add(self._hash_for_comparison(pwd))
            except Exception:
                # Em caso de erro, continue com o que temos
                pass
    
    @staticmethod
    @functools.lru_cache(maxsize=1024)  # Cache para melhorar desempenho
    def _hash_for_comparison(password: str) -> str:
        """Gera um hash SHA-1 da senha para comparação com vazamentos."""
        # Usamos SHA-1 aqui porque é o formato comum usado por serviços como HIBP
        return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    def is_password_leaked(self, password: str) -> bool:
        """
        Verifica se a senha foi comprometida em vazamentos conhecidos.
        
        Args:
            password: A senha a ser verificada
            
        Returns:
            True se a senha foi encontrada em vazamentos, False caso contrário
        """
        # Hash a senha e verifique no conjunto local
        pwd_hash = self._hash_for_comparison(password)
        return pwd_hash in self._leaked_hashes
    
    def k_anonymity_check(self, password: str) -> bool:
        """
        Implementa uma versão simplificada da API k-anonymity do "Have I Been Pwned".
        Em produção, isso faria uma chamada à API real do HIBP.
        
        Args:
            password: A senha a ser verificada
            
        Returns:
            True se a senha foi comprometida, False se não foi encontrada
        """
        # Em produção, isso consultaria a API do HIBP usando apenas os primeiros
        # 5 caracteres do hash SHA-1 (k-anonymity)
        return self.is_password_leaked(password)


class PasswordValidator:
    """
    Classe para validação avançada de senhas com regras configuráveis,
    feedback detalhado para o usuário e verificação de vazamentos.
    """

    def __init__(self):
        # Configurações padrão
        self._min_length = 8
        self._max_length = 128
        self._require_uppercase = True
        self._require_lowercase = True
        self._require_digits = True
        self._require_special = True  # Agora requerido por padrão
        self._min_unique_chars = 5  # Aumentado para maior segurança
        self._check_leaks = True
        self._check_similarity = True
        self._common_passwords: Set[str] = {
            "password", "123456", "qwerty", "admin", "welcome",
            "letmein", "monkey", "abc123", "111111", "12345678"
        }
        self._blacklisted_words: Set[str] = set()
        
        # Carregar verificador de vazamentos
        self._leak_checker = LeakChecker()
        
        # Configurar regex para verificações avançadas
        # Expressão para detectar padrões de repetição como "aaa", "111"
        self._repetition_regex = re.compile(r'(.)\1{2,}')
        
        # Expressão para detectar sequências crescentes/decrescentes como "abc", "321"
        self._sequence_regex = re.compile(r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789|987|876|765|654|543|432|321|210)', re.IGNORECASE)
    
    # Métodos de configuração usando padrão builder (mantidos e atualizados)
    def set_min_length(self, length: int) -> 'PasswordValidator':
        """Define o tamanho mínimo da senha."""
        self._min_length = max(1, length)
        return self

    def set_max_length(self, length: int) -> 'PasswordValidator':
        """Define o tamanho máximo da senha."""
        self._max_length = max(self._min_length, length)
        return self

    def require_uppercase(self, required: bool = True) -> 'PasswordValidator':
        """Define se letras maiúsculas são obrigatórias."""
        self._require_uppercase = required
        return self

    def require_lowercase(self, required: bool = True) -> 'PasswordValidator':
        """Define se letras minúsculas são obrigatórias."""
        self._require_lowercase = required
        return self

    def require_digits(self, required: bool = True) -> 'PasswordValidator':
        """Define se dígitos são obrigatórios."""
        self._require_digits = required
        return self

    def require_special_chars(self, required: bool = True) -> 'PasswordValidator':
        """Define se caracteres especiais são obrigatórios."""
        self._require_special = required
        return self

    def set_min_unique_chars(self, count: int) -> 'PasswordValidator':
        """Define o número mínimo de caracteres únicos."""
        self._min_unique_chars = max(1, count)
        return self
    
    def enable_leak_checking(self, enabled: bool = True) -> 'PasswordValidator':
        """Habilita ou desabilita a verificação de vazamentos."""
        self._check_leaks = enabled
        return self
    
    def enable_similarity_checking(self, enabled: bool = True) -> 'PasswordValidator':
        """Habilita ou desabilita a verificação de similaridade com palavras conhecidas."""
        self._check_similarity = enabled
        return self

    def add_blacklisted_words(self, words: List[str]) -> 'PasswordValidator':
        """Adiciona palavras à lista negra."""
        self._blacklisted_words.update([w.lower() for w in words])
        return self

    def add_common_passwords(self, passwords: List[str]) -> 'PasswordValidator':
        """Adiciona senhas comuns à lista de senhas proibidas."""
        self._common_passwords.update([p.lower() for p in passwords])
        return self
    
    def _check_common_password(self, pwd: str) -> Tuple[bool, Optional[str]]:
        """Verifica se a senha é comum ou contém palavras da lista negra."""
        if pwd.lower() in self._common_passwords:
            return False, "A senha é muito comum e facilmente adivinhável"
        
        pwd_lower = pwd.lower()
        
        # Verificar palavras da lista negra
        for word in self._blacklisted_words:
            if word in pwd_lower and len(word) > 3:
                return False, f"A senha contém uma palavra proibida: '{word}'"
        
        # Verificar se a senha é similar a palavras comuns
        if self._check_similarity:
            for word in self._blacklisted_words.union(self._common_passwords):
                # Usar SequenceMatcher para encontrar similaridades
                similarity = SequenceMatcher(None, pwd_lower, word).ratio()
                if similarity > 0.8 and len(word) > 4:
                    return False, f"A senha é muito similar à palavra comum: '{word}'"
                
        return True, None
    
    def _check_sequential_characters(self, pwd: str) -> Tuple[bool, Optional[str]]:
        """Verifica se a senha contém sequências óbvias."""
        # Verificar sequências com regex
        if self._sequence_regex.search(pwd.lower()):
            match = self._sequence_regex.search(pwd.lower())
            return False, f"A senha contém uma sequência óbvia: '{match.group(0)}'"
        
        # Verificar repetições com regex
        if self._repetition_regex.search(pwd):
            match = self._repetition_regex.search(pwd)
            return False, f"A senha contém caracteres repetidos em sequência: '{match.group(0)}'"
            
        return True, None
    
    def _calculate_entropy(self, pwd: str, char_counts: Dict[str, int]) -> float:
        """
        Calcula a entropia estimada da senha em bits.
        Fórmula: Entropia = log2(pool_size^length) = length * log2(pool_size)
        """
        import math
        
        # Determinar o tamanho do pool de caracteres
        pool_size = 0
        if char_counts['uppercase'] > 0:
            pool_size += 26  # A-Z
        if char_counts['lowercase'] > 0:
            pool_size += 26  # a-z
        if char_counts['digit'] > 0:
            pool_size += 10  # 0-9
        if char_counts['special'] > 0:
            pool_size += 33  # Caracteres especiais comuns
        
        # Se não houver caracteres detectados (improvável), definir um valor mínimo
        if pool_size == 0:
            pool_size = 26
        
        # Calcular entropia
        entropy = len(pwd) * math.log2(pool_size)
        
        # Penalizar padrões comuns, cada padrão reduz a entropia
        if self._sequence_regex.search(pwd.lower()):
            entropy *= 0.8
            
        if self._repetition_regex.search(pwd):
            entropy *= 0.7
            
        # Penalizar senhas se contiverem palavras comuns
        pwd_lower = pwd.lower()
        for word in self._blacklisted_words.union(self._common_passwords):
            if word in pwd_lower and len(word) > 3:
                entropy *= 0.6
                break
                
        return entropy
    
    def _estimate_crack_time(self, entropy: float) -> str:
        """
        Estima o tempo necessário para quebrar uma senha com base em sua entropia.
        Assume 10 bilhões de tentativas por segundo (capacidade de ataque moderna).
        """
        # 10^10 tentativas por segundo
        attempts_per_second = 10_000_000_000
        
        # Calcular número de tentativas necessárias: 2^entropy
        attempts_needed = 2 ** entropy
        
        # Calcular segundos necessários
        seconds = attempts_needed / attempts_per_second
        
        # Converter para uma representação amigável
        if seconds < 60:
            return "menos de um minuto"
        elif seconds < 3600:
            return f"aproximadamente {int(seconds/60)} minutos"
        elif seconds < 86400:
            return f"aproximadamente {int(seconds/3600)} horas"
        elif seconds < 31536000:
            return f"aproximadamente {int(seconds/86400)} dias"
        elif seconds < 315360000:  # 10 anos
            return f"aproximadamente {int(seconds/31536000)} anos"
        elif seconds < 3153600000:  # 100 anos
            return f"dezenas de anos"
        elif seconds < 31536000000:  # 1000 anos
            return f"centenas de anos"
        else:
            return "milhares de anos ou mais"
    
    def validate(self, pwd: str) -> ValidationResult:
        """
        Valida a senha de acordo com as regras configuradas.
        Retorna um objeto ValidationResult com informações detalhadas.
        Executa todas as verificações em uma única passagem pela senha.
        """
        if pwd is None:
            return ValidationResult(is_valid=False, failures=["A senha não pode ser nula"])
            
        result = ValidationResult()
        char_counts = {
            'uppercase': 0,
            'lowercase': 0,
            'digit': 0,
            'special': 0
        }
        
        # Verificar tamanho
        if len(pwd) < self._min_length:
            result.failures.append(
                f"A senha deve ter pelo menos {self._min_length} caracteres"
            )
            
        if len(pwd) > self._max_length:
            result.failures.append(
                f"A senha não pode ter mais de {self._max_length} caracteres"
            )
        
        # Calcular caracteres únicos e tipos em uma única passagem
        unique_chars = set()
        for c in pwd:
            unique_chars.add(c)
            
            if c.isupper():
                char_counts['uppercase'] += 1
            elif c.islower():
                char_counts['lowercase'] += 1
            elif c.isdigit():
                char_counts['digit'] += 1
            elif c in string.punctuation:
                char_counts['special'] += 1
        
        # Verificar diversidade de caracteres
        if len(unique_chars) < self._min_unique_chars:
            result.failures.append(
                f"A senha deve conter pelo menos {self._min_unique_chars} caracteres únicos"
            )
        
        # Verificar presença dos tipos necessários
        if self._require_uppercase and char_counts['uppercase'] == 0:
            result.failures.append("A senha deve conter pelo menos uma letra maiúscula")
            
        if self._require_lowercase and char_counts['lowercase'] == 0:
            result.failures.append("A senha deve conter pelo menos uma letra minúscula")
            
        if self._require_digits and char_counts['digit'] == 0:
            result.failures.append("A senha deve conter pelo menos um dígito")
            
        if self._require_special and char_counts['special'] == 0:
            result.failures.append("A senha deve conter pelo menos um caractere especial")
        
        # Verificações adicionais
        common_check, common_msg = self._check_common_password(pwd)
        if not common_check:
            result.failures.append(common_msg)
            
        seq_check, seq_msg = self._check_sequential_characters(pwd)
        if not seq_check:
            result.failures.append(seq_msg)
        
        # Calcular entropia
        result.entropy = self._calculate_entropy(pwd, char_counts)
        
        # Estimar tempo para quebra
        result.time_to_crack = self._estimate_crack_time(result.entropy)
        
        # Calcular pontuação e força da senha
        score = self._calculate_score(pwd, char_counts)
        result.score = score
        result.strength = self._determine_strength(score)
        
        # Verificar validade com base nas falhas
        result.is_valid = len(result.failures) == 0
        
        # Adicionar sugestões se a senha falhou
        if not result.is_valid:
            result.suggestions = self._generate_suggestions(result.failures)
        
        return result
    
    def _calculate_score(self, pwd: str, char_counts: Dict[str, int]) -> int:
        """Calcula uma pontuação para a senha baseada em vários fatores."""
        score = 0
        
        # Pontos por comprimento
        score += min(20, len(pwd) * 2)
        
        # Pontos por tipos de caracteres
        for char_type, count in char_counts.items():
            if count > 0:
                score += 10  # Pontos por ter pelo menos um caractere de cada tipo
                score += min(10, count)  # Pontos extras por quantidade, até um limite
        
        # Pontos por diversidade
        unique_ratio = len(set(pwd)) / len(pwd)
        score += int(unique_ratio * 20)
        
        # Verificar padrões e penalizar
        # Sequências comuns
        common_sequences = ["123", "abc", "qwe", "asd", "zxc"]
        for seq in common_sequences:
            if seq.lower() in pwd.lower():
                score -= 10
        
        # Verificar repetições
        for i in range(len(pwd) - 2):
            if pwd[i] == pwd[i+1] == pwd[i+2]:
                score -= 10
                break
        
        # Garantir limites entre 0 e 100
        return max(0, min(100, score))
    
    def _determine_strength(self, score: int) -> PasswordStrength:
        """Determina a força da senha com base na pontuação."""
        if score < 20:
            return PasswordStrength.VERY_WEAK
        elif score < 40:
            return PasswordStrength.WEAK
        elif score < 60:
            return PasswordStrength.MODERATE
        elif score < 80:
            return PasswordStrength.STRONG
        else:
            return PasswordStrength.VERY_STRONG
    
    def _generate_suggestions(self, failures: List[str]) -> List[str]:
        """Gera sugestões com base nas falhas de validação."""
        suggestions = []
        
        if any("letra maiúscula" in failure for failure in failures):
            suggestions.append("Adicione pelo menos uma letra maiúscula (A-Z)")
            
        if any("letra minúscula" in failure for failure in failures):
            suggestions.append("Adicione pelo menos uma letra minúscula (a-z)")
            
        if any("dígito" in failure for failure in failures):
            suggestions.append("Adicione pelo menos um número (0-9)")
            
        if any("caractere especial" in failure for failure in failures):
            suggestions.append(f"Adicione pelo menos um caractere especial ({string.punctuation})")
            
        if any("caracteres únicos" in failure for failure in failures):
            suggestions.append("Use uma maior variedade de caracteres diferentes")
            
        if any("pelo menos" in failure and "caracteres" in failure for failure in failures):
            suggestions.append("Aumente o comprimento da sua senha")
            
        if any("comum" in failure for failure in failures):
            suggestions.append("Evite usar palavras comuns ou senhas conhecidas")
            
        if any("sequência" in failure for failure in failures):
            suggestions.append("Evite sequências óbvias como '123', 'abc' ou caracteres repetidos")
            
        return suggestions


def validate_password(pwd: str, verbose: bool = False) -> bool:
    """
    Função simplificada para compatibilidade com o código anterior.
    Valida a senha usando as regras padrão e retorna True se for válida.
    
    Args:
        pwd: A senha a ser validada.
        verbose: Se True, imprime informações detalhadas sobre a validação.
        
    Returns:
        True se a senha for válida, False caso contrário.
    """
    validator = PasswordValidator()
    result = validator.validate(pwd)
    
    if verbose and not result.is_valid:
        print("Falhas de validação:")
        for failure in result.failures:
            print(f"- {failure}")
        
        if result.suggestions:
            print("\nSugestões:")
            for suggestion in result.suggestions:
                print(f"- {suggestion}")
        
        print(f"\nForça da senha: {result.strength.name}")
        print(f"Pontuação: {result.score}/100")
    
    return result.is_valid


def analyze_password(pwd: str) -> None:
    """
    Função para análise detalhada da senha, mostrando todas as informações
    sobre sua validação, força, problemas e sugestões.
    
    Args:
        pwd: A senha a ser analisada.
    """
    validator = PasswordValidator()
    result = validator.validate(pwd)
    
    print(f"\n{'=' * 50}")
    print(f"Análise de senha: {'APROVADA' if result.is_valid else 'REPROVADA'}")
    print(f"{'=' * 50}")
    
    print(f"Força: {result.strength.name}")
    print(f"Pontuação: {result.score}/100")
    
    if result.failures:
        print("\nProblemas encontrados:")
        for i, failure in enumerate(result.failures, 1):
            print(f"{i}. {failure}")
    
    if result.suggestions:
        print("\nSugestões para melhorar:")
        for i, suggestion in enumerate(result.suggestions, 1):
            print(f"{i}. {suggestion}")
    
    print(f"\n{'=' * 50}\n")


def create_gui():
    """
    Cria a interface gráfica para validação de senhas.
    """
    def on_validate():
        password = password_entry.get()
        result = validator.validate(password)
        
        result_text = f"Validação: {'APROVADA' if result.is_valid else 'REPROVADA'}\n"
        result_text += f"Força: {result.strength.name}\n"
        result_text += f"Pontuação: {result.score}/100\n"
        result_text += f"Entropia: {result.entropy:.2f} bits\n"
        result_text += f"Tempo para quebra: {result.time_to_crack}\n"
        
        if result.failures:
            result_text += "\nProblemas encontrados:\n"
            for i, failure in enumerate(result.failures, 1):
                result_text += f"{i}. {failure}\n"
        
        if result.suggestions:
            result_text += "\nSugestões para melhorar:\n"
            for i, suggestion in enumerate(result.suggestions, 1):
                result_text += f"{i}. {suggestion}\n"
        
        result_textbox.config(state=tk.NORMAL)
        result_textbox.delete(1.0, tk.END)
        result_textbox.insert(tk.END, result_text)
        result_textbox.config(state=tk.DISABLED)
    
    validator = PasswordValidator()
    
    root = tk.Tk()
    root.title("Validador de Senhas")
    
    mainframe = ttk.Frame(root, padding="10")
    mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    password_label = ttk.Label(mainframe, text="Senha:")
    password_label.grid(row=0, column=0, sticky=tk.W)
    
    password_entry = ttk.Entry(mainframe, width=30, show="*")
    password_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
    
    validate_button = ttk.Button(mainframe, text="Validar", command=on_validate)
    validate_button.grid(row=0, column=2, sticky=tk.W)
    
    result_textbox = scrolledtext.ScrolledText(mainframe, width=80, height=20, wrap=tk.WORD, state=tk.DISABLED)
    result_textbox.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
    
    root.mainloop()


# Exemplo de uso:
if __name__ == "__main__":
    create_gui()
