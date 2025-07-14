#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RenPy Save Editor
Editor de arquivos .sav do RenPy similar ao grviewer.com

Autor: Assistant
Data: 2025
"""

import os
import pickle
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import traceback
import sys

class RenPySaveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("RenPy Save Editor - Arquivo 'log' direto")
        self.root.geometry("900x700")
        
        self.current_save_path = None
        self.save_data = None
        self.modified = False
        
        # Configurar módulos falsos do RenPy ANTES da UI
        self.setup_comprehensive_renpy_modules()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface gráfica"""
        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Abrir arquivo 'log'", command=self.open_save)
        file_menu.add_command(label="Salvar", command=self.save_current)
        file_menu.add_command(label="Salvar Como...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Info do arquivo
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Save", padding="5")
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.info_text = tk.Text(info_frame, height=4, state='disabled')
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba de Variáveis
        self.variables_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.variables_frame, text="Variáveis do Jogo")
        self.setup_variables_tab()
        
        # Aba de JSON Raw
        self.json_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.json_frame, text="JSON Raw")
        self.setup_json_tab()
        
        # Aba de Histórico
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="Histórico")
        self.setup_history_tab()
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Abrir Save", command=self.open_save).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Salvar Alterações", command=self.save_current).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Resetar", command=self.reset_changes).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto - Aguardando arquivo 'log'")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def setup_variables_tab(self):
        """Configura a aba de variáveis"""
        # Frame de busca
        search_frame = ttk.Frame(self.variables_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        search_entry.bind('<KeyRelease>', self.filter_variables)
        
        # Treeview para variáveis
        tree_frame = ttk.Frame(self.variables_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('Variable', 'Type', 'Value')
        self.var_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        self.var_tree.heading('Variable', text='Variável')
        self.var_tree.heading('Type', text='Tipo')
        self.var_tree.heading('Value', text='Valor')
        
        self.var_tree.column('Variable', width=200)
        self.var_tree.column('Type', width=100)
        self.var_tree.column('Value', width=300)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.var_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.var_tree.xview)
        self.var_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.var_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Bind double click para editar
        self.var_tree.bind('<Double-1>', self.edit_variable)
        
        # Frame de edição
        edit_frame = ttk.LabelFrame(self.variables_frame, text="Editar Variável", padding="5")
        edit_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(edit_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W)
        self.var_name_var = tk.StringVar()
        ttk.Entry(edit_frame, textvariable=self.var_name_var, state='readonly').grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        ttk.Label(edit_frame, text="Valor:").grid(row=1, column=0, sticky=tk.W)
        self.var_value_var = tk.StringVar()
        self.var_value_entry = ttk.Entry(edit_frame, textvariable=self.var_value_var)
        self.var_value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        ttk.Button(edit_frame, text="Aplicar", command=self.apply_variable_change).grid(row=1, column=2, padx=(5, 0))
        
        edit_frame.columnconfigure(1, weight=1)
    
    def setup_json_tab(self):
        """Configura a aba JSON raw"""
        self.json_text = scrolledtext.ScrolledText(self.json_frame, wrap=tk.WORD)
        self.json_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(self.json_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Aplicar JSON", command=self.apply_json_changes).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Formatar", command=self.format_json).pack(side=tk.LEFT, padx=(5, 0))
    
    def setup_history_tab(self):
        """Configura a aba de histórico"""
        self.history_text = scrolledtext.ScrolledText(self.history_frame, wrap=tk.WORD, state='disabled')
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def open_save(self):
        """Abre um arquivo 'log' do RenPy"""
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo 'log' (dados do save)",
            filetypes=[("Arquivo log", "log"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            try:
                self.load_save_file(file_path)
                self.status_var.set(f"Arquivo carregado: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{str(e)}")
                self.status_var.set("Erro ao carregar arquivo")
    
    def load_save_file(self, file_path):
        """Carrega um arquivo 'log' do RenPy diretamente"""
        with open(file_path, 'rb') as f:
            data = f.read()
        
        print(f"Arquivo carregado: {len(data)} bytes")
        print(f"Primeiros 100 bytes: {data[:100]}")
        
        # Tentar carregar com diferentes métodos
        load_methods = [
            # Método 1: pickle.loads direto
            ("Pickle direto", lambda d: pickle.loads(d)),
            # Método 2: pickle.loads com latin-1
            ("Pickle com latin-1", lambda d: pickle.loads(d, encoding='latin-1')),
            # Método 3: pickle.loads com bytes
            ("Pickle com bytes", lambda d: pickle.loads(d, encoding='bytes')),
            # Método 4: CustomUnpickler
            ("CustomUnpickler", lambda d: self.load_with_custom_unpickler(d)),
        ]
        
        last_error = None
        
        for method_name, method in load_methods:
            try:
                print(f"Tentando {method_name}...")
                self.save_data = method(data)
                print(f"✅ Sucesso com {method_name}")
                break
            except Exception as e:
                print(f"❌ {method_name} falhou: {str(e)[:150]}")
                last_error = e
                continue
        else:
            # Se todos os métodos falharam
            raise Exception(f"Não foi possível carregar o arquivo com nenhum método. Último erro: {str(last_error)}")
        
        self.current_save_path = file_path
        self.modified = False
        self.update_ui()
    
    def setup_comprehensive_renpy_modules(self):
        """Configura um sistema completo de módulos falsos do RenPy"""
        print("Configurando sistema completo de módulos RenPy...")
        
        # Classe universal para qualquer objeto do RenPy
        class UniversalRenPyClass:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs
                self._class_name = "UniversalRenPyClass"
                # Adicionar atributos esperados pelo RenPy
                self._uninitialized_submodules = set()
                self._modules = {}
                self._initialized = True
                # Atribuir todos os kwargs como atributos
                for k, v in kwargs.items():
                    setattr(self, k, v)
            
            def __setstate__(self, state):
                print(f"DEBUG: UniversalRenPyClass.__setstate__ chamado com state: {type(state)} - {state if not isinstance(state, (list, dict)) or len(str(state)) < 100 else str(state)[:100]+'...'}")
                if isinstance(state, dict):
                    for k, v in state.items():
                        setattr(self, k, v)
                elif isinstance(state, (list, tuple)):
                    # Algumas vezes o estado pode ser uma lista/tupla
                    if len(state) > 0:
                        if isinstance(state[0], dict):
                            for k, v in state[0].items():
                                setattr(self, k, v)
                        else:
                            self._state_list = state
                else:
                    # Para outros tipos, armazenar como estado bruto
                    self._state = state
                
                # Garantir que os atributos esperados sempre existam após __setstate__
                if not hasattr(self, '_uninitialized_submodules'):
                    self._uninitialized_submodules = set()
                if not hasattr(self, '_modules'):
                    self._modules = {}
                if not hasattr(self, '_initialized'):
                    self._initialized = True
            
            def __getstate__(self):
                return self.__dict__
            
            def __getattr__(self, name):
                print(f"DEBUG: UniversalRenPyClass.__getattr__ chamado para atributo: {name} (self: {type(self)})")
                # Retornar sempre uma instância da classe universal para qualquer atributo
                if name.startswith('_'):
                    # Para atributos especiais, retornar valores padrão
                    if name == '_uninitialized_submodules':
                        print(f"DEBUG: Retornando set() para _uninitialized_submodules")
                        return set()
                    elif name == '_modules':
                        return {}
                    elif name == '_initialized':
                        return True
                    elif name == '__dict__':
                        return self.__dict__ if hasattr(self, '__dict__') else {}
                    elif name == '__class__':
                        return UniversalRenPyClass
                    else:
                        return None
                return UniversalRenPyClass()
            
            def __repr__(self):
                return f"UniversalRenPyClass({self._class_name})"
        
        # Criar classes específicas baseadas na UniversalRenPyClass
        class Item(UniversalRenPyClass):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._class_name = "Item"
        
        class RevertableList(list):
            def __init__(self, *args, **kwargs):
                super().__init__(*args)
            
            def __setstate__(self, state):
                print(f"DEBUG: RevertableList.__setstate__ com state: {type(state)}")
                if isinstance(state, dict):
                    # Se o estado é um dicionário, pode conter 'data' ou elementos similares
                    if 'data' in state:
                        self.clear()
                        self.extend(state['data'])
                    # Aplicar outros atributos do estado
                    for k, v in state.items():
                        if k != 'data':
                            setattr(self, k, v)
                elif isinstance(state, (list, tuple)):
                    # Se o estado é uma lista, substituir o conteúdo
                    self.clear()
                    self.extend(state)
                else:
                    # Para outros tipos, tentar usar como lista
                    try:
                        self.clear()
                        if hasattr(state, '__iter__'):
                            self.extend(state)
                        else:
                            self.append(state)
                    except:
                        setattr(self, '_state', state)
        
        class RevertableDict(dict):
            def __init__(self, *args, **kwargs):
                super().__init__(*args)
            
            def __setstate__(self, state):
                print(f"DEBUG: RevertableDict.__setstate__ com state: {type(state)}")
                if isinstance(state, dict):
                    self.clear()
                    self.update(state)
                elif isinstance(state, (list, tuple)) and len(state) == 2:
                    # Algumas vezes o estado pode ser (keys, values) ou similar
                    try:
                        keys, values = state
                        self.clear()
                        for k, v in zip(keys, values):
                            self[k] = v
                    except:
                        setattr(self, '_state', state)
                else:
                    setattr(self, '_state', state)
        
        class RevertableSet(set):
            def __init__(self, *args, **kwargs):
                super().__init__(*args)
            
            def __setstate__(self, state):
                print(f"DEBUG: RevertableSet.__setstate__ com state: {type(state)}")
                if isinstance(state, dict):
                    # Se o estado é um dicionário, pode conter 'data' ou elementos similares
                    if 'data' in state:
                        self.clear()
                        try:
                            self.update(state['data'])
                        except TypeError as e:
                            # Se algum elemento não é hashable, converter para strings
                            print(f"DEBUG: Convertendo elementos não-hashable para strings: {e}")
                            hashable_data = []
                            for item in state['data']:
                                try:
                                    # Testar se é hashable
                                    hash(item)
                                    hashable_data.append(item)
                                except TypeError:
                                    # Se não é hashable, converter para string
                                    hashable_data.append(str(item))
                            self.update(hashable_data)
                    # Aplicar outros atributos do estado
                    for k, v in state.items():
                        if k != 'data':
                            setattr(self, k, v)
                elif isinstance(state, (list, tuple, set)):
                    # Se o estado é uma lista/tupla/set, substituir o conteúdo
                    self.clear()
                    try:
                        self.update(state)
                    except TypeError as e:
                        # Se algum elemento não é hashable, converter para strings
                        print(f"DEBUG: Convertendo elementos não-hashable para strings: {e}")
                        hashable_items = []
                        for item in state:
                            try:
                                # Testar se é hashable
                                hash(item)
                                hashable_items.append(item)
                            except TypeError:
                                # Se não é hashable, converter para string
                                hashable_items.append(str(item))
                        self.update(hashable_items)
                else:
                    # Para outros tipos, tentar usar como set
                    try:
                        self.clear()
                        if hasattr(state, '__iter__'):
                            try:
                                self.update(state)
                            except TypeError:
                                # Se não é hashable, adicionar como string
                                self.add(str(state))
                        else:
                            try:
                                self.add(state)
                            except TypeError:
                                # Se não é hashable, adicionar como string
                                self.add(str(state))
                    except:
                        setattr(self, '_state', state)
        
        class deleted:
            def __init__(self, *args, **kwargs):
                pass
            
            def __setstate__(self, state):
                print(f"DEBUG: deleted.__setstate__ com state: {type(state)}")
                # deleted objects podem ter qualquer tipo de estado
                setattr(self, '_state', state)
            
            def __repr__(self):
                return "deleted"
        
        # Módulo renpy.python
        class RenPyPython:
            pass
        
        # Atribuir as classes ao módulo python depois de definidas
        RenPyPython.RevertableList = RevertableList
        RenPyPython.RevertableDict = RevertableDict
        RenPyPython.RevertableSet = RevertableSet
        RenPyPython.deleted = deleted
        
        # Módulo store
        class Store:
            pass
        
        # Atribuir Item ao Store
        Store.Item = Item
        
        def store_getattr(self, name):
            return f"store_{name}"
        Store.__getattr__ = store_getattr
        
        # Módulo renpy.display com classes comuns
        class RenPyDisplay:
            # Adicionar classes comuns do renpy.display
            def __getattr__(self, name):
                # Retornar nossa classe universal para qualquer atributo do display
                return UniversalRenPyClass
        
        # Módulo renpy.styledata  
        class RenPyStyleData:
            def __getattr__(self, name):
                # Retornar nossa classe universal para qualquer atributo do styledata
                return UniversalRenPyClass
        
        # Módulo renpy principal
        class RenPy:
            python = RenPyPython()
            display = RenPyDisplay()
            styledata = RenPyStyleData()
        
        # Registrar todos os módulos
        sys.modules['renpy'] = RenPy()
        sys.modules['renpy.python'] = RenPyPython()
        sys.modules['renpy.display'] = RenPyDisplay()
        sys.modules['renpy.styledata'] = RenPyStyleData()
        sys.modules['store'] = Store()
        
        # Adicionar ao builtins para acesso direto
        import builtins
        builtins.RevertableList = RevertableList
        builtins.RevertableDict = RevertableDict
        builtins.RevertableSet = RevertableSet
        builtins.deleted = deleted
        builtins.Item = Item
        builtins.UniversalRenPyClass = UniversalRenPyClass
        
        # Configurar hook de importação personalizado para interceptar módulos do RenPy
        import importlib.util
        
        def create_renpy_module(name):
            """Cria um módulo RenPy genérico"""
            try:
                spec = importlib.util.spec_from_loader(name, loader=None)
                module = importlib.util.module_from_spec(spec)
                
                # Para módulos store, adicionar atributos especiais
                if name.startswith('store'):
                    module._uninitialized_submodules = set()
                    module._modules = {}
                    module._initialized = True
                
                # Adicionar classes básicas ao módulo
                module.UniversalRenPyClass = UniversalRenPyClass
                module.RevertableList = RevertableList
                module.RevertableDict = RevertableDict
                module.Item = Item
                module.deleted = deleted
                module.Deleted = deleted
                
                # Adicionar getattr personalizado que sempre retorna UniversalRenPyClass
                def module_getattr(attr_name):
                    print(f"DEBUG: Módulo {name} pedindo atributo: {attr_name}")
                    # Criar uma instância com os atributos necessários
                    instance = UniversalRenPyClass()
                    instance._uninitialized_submodules = set()
                    instance._modules = {}
                    instance._initialized = True
                    return instance
                
                module.__getattr__ = module_getattr
                
                print(f"✓ Módulo {name} criado com sucesso")
                return module
                
            except Exception as e:
                print(f"Erro ao criar módulo {name}: {e}")
                # Fallback - criar módulo simples
                import types
                module = types.ModuleType(name)
                module._uninitialized_submodules = set()
                module._modules = {}
                module._initialized = True
                module.__getattr__ = lambda attr: UniversalRenPyClass()
                return module
        
        # Instalar um meta path finder personalizado para interceptar importações do RenPy
        class RenPyModuleFinder:
            def find_spec(self, fullname, path, target=None):
                # Interceptar qualquer módulo que comece com 'renpy' ou 'store'
                if (fullname.startswith('renpy') or fullname.startswith('store')) and fullname not in sys.modules:
                    print(f"Interceptando importação de módulo: {fullname}")
                    try:
                        # Criar módulo genérico
                        module = create_renpy_module(fullname)
                        sys.modules[fullname] = module
                        
                        # Criar spec corretamente
                        spec = importlib.util.spec_from_loader(fullname, loader=None)
                        if spec:
                            spec.submodule_search_locations = []
                        return spec
                    except Exception as e:
                        print(f"Erro ao criar módulo {fullname}: {e}")
                        return None
                return None
            
            def find_module(self, fullname, path=None):
                # Para compatibilidade com versões mais antigas do Python
                return None
        
        # Instalar o finder no início da lista para ter prioridade
        if not any(isinstance(finder, RenPyModuleFinder) for finder in sys.meta_path):
            sys.meta_path.insert(0, RenPyModuleFinder())
        
        print("Sistema de módulos RenPy configurado com sucesso!")
    
    def analyze_pickle_structure(self, data):
        """Analisa a estrutura do pickle para entender melhor os problemas"""
        print("=== ANÁLISE DA ESTRUTURA PICKLE ===")
        
        # Primeiros 200 bytes para análise
        sample = data[:200]
        print(f"Primeiros 200 bytes: {sample}")
        
        # Procurar por opcodes específicos
        opcodes = {
            b'\x80': 'PROTO',
            b'\x81': 'NEWOBJ', 
            b'\x82': 'NEWOBJ_EX',
            b'}': 'EMPTY_DICT',
            b'q': 'BINPUT',
            b'X': 'BINUNICODE',
            b'K': 'BININT1',
            b'.': 'STOP'
        }
        
        for i, byte in enumerate(sample):
            byte_val = bytes([byte])
            if byte_val in opcodes:
                print(f"Posição {i}: {byte_val} ({opcodes[byte_val]}) - valor: {byte}")
                
        return True
    
    def fix_newobj_opcodes(self, data):
        """Substitui NEWOBJ opcodes por versões compatíveis"""
        try:
            print("Procurando e corrigendo NEWOBJ opcodes...")
            
            # Converter para bytearray para modificação
            data_array = bytearray(data)
            corrections = 0
            
            i = 0
            while i < len(data_array) - 1:
                # Procurar por NEWOBJ (0x81)
                if data_array[i] == 0x81:
                    print(f"NEWOBJ encontrado na posição {i}")
                    # Substituir por BUILD (0x62) que é mais compatível
                    data_array[i] = 0x62
                    corrections += 1
                    
                # Procurar por NEWOBJ_EX (0x82) 
                elif data_array[i] == 0x82:
                    print(f"NEWOBJ_EX encontrado na posição {i}")
                    # Substituir por BUILD 
                    data_array[i] = 0x62
                    corrections += 1
                    
                i += 1
                
            print(f"Correções NEWOBJ aplicadas: {corrections}")
            return bytes(data_array)
            
        except Exception as e:
            print(f"Erro ao corrigir NEWOBJ: {e}")
            return data
        
    def load_save_data_from_bytes(self, data):
        """Carrega dados de save a partir de bytes usando todos os métodos disponíveis"""
        print(f"Tamanho dos dados: {len(data)} bytes")
        print(f"Primeiros 100 bytes: {data[:100]}")
        
        # Configurar módulos falsos para o RenPy antes de tentar carregar
        self.setup_fake_renpy_modules()
        
        # Análise da estrutura do pickle
        self.analyze_pickle_structure(data)
        
        # Primeira tentativa: apenas correção de NEWOBJ opcodes (SEM reparo de caracteres)
        try:
            print("Tentando APENAS correção de NEWOBJ opcodes...")
            corrected_data = self.fix_newobj_opcodes(data)
            try:
                result = self.load_with_custom_unpickler(corrected_data)
                print("✅ Sucesso com correção de NEWOBJ opcodes APENAS")
                return result
            except Exception as e:
                print(f"❌ NEWOBJ correction falhou: {str(e)[:150]}")
                
                # Tentar também com pickle.loads padrão
                try:
                    result = pickle.loads(corrected_data)
                    print("✅ Sucesso com NEWOBJ + pickle.loads padrão")
                    return result
                except Exception as e2:
                    print(f"❌ NEWOBJ + pickle.loads falhou: {str(e2)[:150]}")
                    
        except Exception as e:
            print(f"❌ Erro na correção NEWOBJ: {str(e)[:150]}")
        
        # Segunda tentativa: conversão de protocolo
        try:
            print("Tentando conversão de protocolo...")
            converted_data = self.convert_pickle_protocol(data)
            if converted_data:
                result = pickle.loads(converted_data)
                print("✅ Sucesso com conversão de protocolo")
                return result
        except Exception as e:
            print(f"❌ Conversão de protocolo falhou: {str(e)[:150]}")
        
        # Terceira tentativa: CustomUnpickler direto
        try:
            print("Tentando CustomUnpickler direto...")
            result = self.load_with_custom_unpickler(data)
            print("✅ Sucesso com CustomUnpickler direto")
            return result
        except Exception as e:
            print(f"❌ CustomUnpickler direto falhou: {str(e)[:150]}")
            
        # Quarta tentativa: diferentes encodings
        encoding_methods = [
            ("Pickle loads padrão", lambda d: pickle.loads(d)),
            ("Pickle loads com latin-1", lambda d: pickle.loads(d, encoding='latin-1')),
            ("Pickle loads com bytes", lambda d: pickle.loads(d, encoding='bytes')),
        ]
        
        for method_name, method in encoding_methods:
            try:
                print(f"Tentando {method_name}...")
                result = method(data)
                print(f"✅ Sucesso com {method_name}")
                return result
            except Exception as e:
                print(f"❌ {method_name} falhou: {str(e)[:150]}")
                continue
        
        # Se nada funcionou, tentar reparo + métodos anteriores (como último recurso)
        print("Tentando reparar dados do pickle...")
        try:
            repaired_data = self.repair_pickle_data(data)
            
            # Tentar métodos com dados reparados (como último recurso)
            repair_methods = [
                ("CustomUnpickler direto com dados reparados", lambda d: self.load_with_custom_unpickler(d)),
                ("Pickle loads padrão com dados reparados", lambda d: pickle.loads(d)),
                ("Pickle loads com latin-1 com dados reparados", lambda d: pickle.loads(d, encoding='latin-1')),
                ("Pickle loads com bytes com dados reparados", lambda d: pickle.loads(d, encoding='bytes')),
            ]
            
            for method_name, method in repair_methods:
                try:
                    print(f"Tentando {method_name}...")
                    result = method(repaired_data)
                    print(f"✅ Sucesso com {method_name}")
                    return result
                except Exception as e:
                    print(f"❌ {method_name} falhou mesmo com reparo: {str(e)[:150]}")
                    continue
                    
        except Exception as e:
            print(f"❌ Erro no reparo: {str(e)[:150]}")
        
        # Métodos finais (compressão, etc.)
        final_methods = [
            ("Carregar com correção cirúrgica de persistent IDs", self.load_with_surgical_fixes),
            ("Carregar ignorando caracteres problemáticos", lambda d: pickle.loads(d, encoding='latin-1', errors='ignore')),
        ]
        
        for method_name, method in final_methods:
            try:
                print(f"Tentando {method_name}...")
                result = method(data)
                print(f"✅ Sucesso com {method_name}")
                return result
            except Exception as e:
                print(f"❌ {method_name} falhou: {str(e)[:150]}")
                continue
        
        # Se nada funcionou, tentar métodos finais
        final_methods = [
            ("Carregar ignorando caracteres problemáticos", lambda d: pickle.loads(d, encoding='latin-1', errors='ignore')),
        ]
        
        for method_name, method in final_methods:
            try:
                print(f"Tentando {method_name}...")
                result = method(data)
                print(f"✅ Sucesso com {method_name}")
                return result
            except Exception as e:
                print(f"❌ {method_name} falhou: {str(e)[:150]}")
                continue
        
        raise Exception("Não foi possível carregar os dados de save com nenhum método")
        
    def convert_pickle_protocol(self, data):
        """Tenta converter pickle protocolo 2 para protocolo 1 ou 0"""
        try:
            import io
            
            # Verificar se é protocolo 2
            if data[:2] != b'\x80\x02':
                return None
                
            print("Detectado protocolo 2, tentando conversão...")
            
            # Abordagem simples: tentar substituir o header
            # Protocolo 1: \x80\x01
            # Protocolo 0: sem header
            
            # Tentar protocolo 1
            protocol_1_data = b'\x80\x01' + data[2:]
            
            # Tentar carregar para validar
            try:
                test_result = pickle.loads(protocol_1_data)
                print("Conversão para protocolo 1 bem-sucedida")
                return protocol_1_data
            except:
                pass
            
            # Tentar protocolo 0 (sem header)
            protocol_0_data = data[2:]
            
            try:
                test_result = pickle.loads(protocol_0_data)
                print("Conversão para protocolo 0 bem-sucedida")
                return protocol_0_data
            except:
                pass
                
            # Se as conversões simples não funcionaram, tentar uma abordagem mais complexa
            # Converter NEWOBJ para INST
            converted_data = bytearray(data)
            
            # Substituir opcodes problemáticos
            replacements = {
                b'\x81': b'\x69',  # NEWOBJ -> INST
                # Adicionar mais substituições conforme necessário
            }
            
            for old, new in replacements.items():
                converted_data = converted_data.replace(old, new)
            
            return bytes(converted_data)
            
        except Exception as e:
            print(f"Erro na conversão de protocolo: {e}")
            return None
    
    def repair_pickle_data(self, data):
        """Tenta reparar dados de pickle problemáticos"""
        print("Iniciando reparo dos dados pickle...")
        
        # Converter para bytearray para permitir modificações
        data_array = bytearray(data)
        
        # Procurar apenas por strings problemáticas sem alterar a estrutura do pickle
        i = 0
        modifications = 0
        
        while i < len(data_array) - 30:
            # Procurar pelo padrão "store." seguido de caracteres
            if data_array[i:i+6] == b'store.':
                print(f"Encontrado 'store.' na posição {i}")
                
                # Analisar o contexto para ver se é realmente uma string de variável
                # Verificar se há marcador de string antes (típico do pickle)
                context_start = max(0, i - 10)
                context = data_array[context_start:i]
                
                # Se parece com uma string do pickle (tem tamanho antes)
                string_marker_found = False
                for marker in [b'X', b'U', b'S']:  # Marcadores comuns de string no pickle
                    if marker in context[-5:]:
                        string_marker_found = True
                        break
                
                if string_marker_found:
                    # Procurar o final da string (próximo marcador ou caractere especial)
                    j = i + 6
                    
                    while j < len(data_array) and j < i + 50:  # Limitar busca
                        current_char = data_array[j]
                        
                        # Parar em caracteres de controle típicos do pickle
                        if current_char in [0, 10, 13, 40, 41, 46, 113, 75, 88, 85, 83]:  # null, \n, \r, (, ), ., q, K, X, U, S
                            break
                        
                        # Se é um caractere não-ASCII, substituir apenas se for problemático
                        if current_char > 127:
                            # Verificar se é um caractere que realmente causa problema
                            if current_char in [136, 137, 150, 155, 181, 200, 203, 214, 228, 131, 132, 145, 146, 147, 148, 149, 151, 152, 153, 154, 156, 176, 183, 254, 255]:
                                print(f"Substituindo caractere problemático na posição {j}: {current_char} -> 95 ('_')")
                                data_array[j] = 95  # '_'
                                modifications += 1
                        
                        j += 1
            
            i += 1
        
        print(f"Reparo refinado concluído: {modifications} modificações feitas")
        return bytes(data_array)
    
    def load_with_custom_unpickler(self, data):
        """Carrega dados usando um unpickler customizado para lidar com IDs persistentes"""
        import io
        
        class CustomUnpickler(pickle.Unpickler):
            def persistent_load(self, pid):
                print(f"Carregando ID persistente: {pid} (tipo: {type(pid)})")
                
                # RenPy usa IDs persistentes no formato "store.variavel_name"
                if isinstance(pid, bytes):
                    try:
                        pid_str = pid.decode('ascii')
                        print(f"Decodificado como ASCII: {pid_str}")
                    except UnicodeDecodeError:
                        try:
                            pid_str = pid.decode('latin-1', errors='ignore')
                            print(f"Decodificado como Latin-1: {pid_str}")
                        except:
                            pid_str = str(pid)
                elif isinstance(pid, str):
                    try:
                        pid.encode('ascii')
                        pid_str = pid
                        print(f"String ASCII válida: {pid}")
                    except UnicodeEncodeError:
                        pid_str = pid.encode('ascii', errors='ignore').decode('ascii')
                        print(f"Convertido para ASCII: {pid_str}")
                else:
                    pid_str = str(pid)
                
                # Retornar um objeto ao invés de string simples
                from builtins import UniversalRenPyClass
                obj = UniversalRenPyClass()
                obj._persistent_id = pid_str
                obj._name = pid_str
                return obj
            
            def load_newobj(self):
                """Override para NEWOBJ que pode receber strings ao invés de classes"""
                try:
                    print(f"DEBUG: load_newobj chamado")
                    cls = self.pop()
                    print(f"DEBUG: Classe para NEWOBJ: {cls} (tipo: {type(cls)})")
                    
                    # Se recebemos uma string ao invés de uma classe, usar UniversalRenPyClass
                    if isinstance(cls, str):
                        print(f"DEBUG: Convertendo string '{cls}' para UniversalRenPyClass")
                        from builtins import UniversalRenPyClass
                        cls = UniversalRenPyClass
                    
                    # Chamada original
                    args = self.pop()
                    obj = cls.__new__(cls, *args)
                    self.append(obj)
                    
                except Exception as e:
                    print(f"DEBUG: Erro em load_newobj: {e}, criando objeto fallback")
                    from builtins import UniversalRenPyClass
                    obj = UniversalRenPyClass()
                    self.append(obj)
                """Override para capturar erros de __setstate__ e tornar mais tolerante"""
                try:
                    return super().load_build()
                except Exception as e:
                    if "state is not a dictionary" in str(e):
                        print(f"DEBUG: Interceptando erro 'state is not a dictionary', criando objeto tolerante")
                        # Pegar o objeto e o estado da pilha
                        state = self.pop()
                        obj = self.pop()
                        
                        # Tentar aplicar o estado de forma mais tolerante
                        try:
                            if hasattr(obj, '__setstate__'):
                                obj.__setstate__(state)
                            else:
                                # Se não tem __setstate__, tentar definir atributos diretamente
                                if isinstance(state, dict):
                                    for k, v in state.items():
                                        setattr(obj, k, v)
                                else:
                                    setattr(obj, '_state', state)
                        except Exception as inner_e:
                            print(f"DEBUG: Erro ao aplicar estado tolerante: {inner_e}, criando objeto wrapper")
                            from builtins import UniversalRenPyClass
                            wrapper = UniversalRenPyClass()
                            wrapper._original_object = obj
                            wrapper._original_state = state
                            obj = wrapper
                        
                        self.append(obj)
                        return
                    else:
                        raise
            
            def load_global(self):
                """Override para lidar com globais problemáticos"""
                try:
                    module = self.readline()[:-1].decode('ascii')
                    name = self.readline()[:-1].decode('ascii')
                    print(f"Tentando carregar global: {module}.{name}")
                    
                    # Se é um módulo do RenPy, usar nossos módulos falsos
                    if module.startswith('renpy'):
                        print(f"✓ Carregando classe RenPy: {module}.{name}")
                        # Sempre retornar UniversalRenPyClass para qualquer classe do renpy
                        from builtins import UniversalRenPyClass
                        self.append(UniversalRenPyClass)
                        return UniversalRenPyClass
                    
                    # Se é o módulo store (variáveis do jogo)
                    elif module == 'store':
                        print(f"✓ Carregando classe Store: {module}.{name}")
                        # Retornar Item se for Item, senão classe universal
                        if name == 'Item':
                            from builtins import Item
                            self.append(Item)
                            return Item
                        else:
                            from builtins import UniversalRenPyClass
                            self.append(UniversalRenPyClass)
                            return UniversalRenPyClass
                    
                    # Para outros módulos, tentar carregar normalmente
                    print(f"Tentando carregar módulo padrão: {module}.{name}")
                    __import__(module)
                    mod = sys.modules[module]
                    klass = getattr(mod, name)
                    self.append(klass)
                    return klass
                    
                except Exception as e:
                    print(f"Erro ao carregar global {module if 'module' in locals() else 'unknown'}.{name if 'name' in locals() else 'unknown'}, usando placeholder: {e}")
                    # Retorna nossa classe universal
                    from builtins import UniversalRenPyClass
                    self.append(UniversalRenPyClass)
                    return UniversalRenPyClass
        
        try:
            # Pré-criar módulos conhecidos para evitar problemas de importação
            known_modules = [
                'store', 'store._console', 'store._preferences', 'store._gamepad',
                'renpy', 'renpy.display', 'renpy.display.layout', 'renpy.styledata', 
                'renpy.styledata.styleclass', 'renpy.python', 'renpy.character'
            ]
            
            for module_name in known_modules:
                if module_name not in sys.modules:
                    print(f"Pré-criando módulo: {module_name}")
                    import types
                    from builtins import UniversalRenPyClass
                    
                    module = types.ModuleType(module_name)
                    if module_name.startswith('store'):
                        module._uninitialized_submodules = set()
                        module._modules = {}
                        module._initialized = True
                    
                    def module_getattr(attr_name):
                        return UniversalRenPyClass
                    module.__getattr__ = module_getattr
                    
                    sys.modules[module_name] = module
            
            buffer = io.BytesIO(data)
            unpickler = CustomUnpickler(buffer)
            result = unpickler.load()
            print(f"CustomUnpickler carregou com sucesso")
            return result
            
        except Exception as e:
            import traceback
            if "NEWOBJ class argument must be a type" in str(e):
                print(f"❌ CRITICAL ERROR: {e}")
                print("Tentando método alternativo - carregamento básico de variáveis...")
                try:
                    return self.load_basic_variables(data)
                except Exception as e2:
                    print(f"Método alternativo também falhou: {e2}")
                    return None
            else:
                print(f"CustomUnpickler falhou: {e}")
                print(f"Tipo do erro: {type(e)}")
                print(f"Traceback completo:")
                traceback.print_exc()
                raise
    
    def load_basic_variables(self, data):
        """Método alternativo para extrair variáveis básicas sem unpickling completo"""
        print("=== CARREGAMENTO BÁSICO DE VARIÁVEIS ===")
        
        # Procurar por padrões de strings que parecem variáveis do jogo
        text_data = str(data, errors='ignore')
        
        # Padrões comuns de variáveis do RenPy
        import re
        
        # Procurar variáveis store.*
        store_vars = re.findall(r'store\.([a-zA-Z_][a-zA-Z0-9_]*)', text_data)
        
        print(f"Encontradas {len(store_vars)} possíveis variáveis store:")
        for var in store_vars[:20]:  # Mostrar apenas as primeiras 20
            print(f"  - store.{var}")
        
        # Criar um dicionário básico com as variáveis encontradas
        basic_data = {}
        for var in store_vars:
            basic_data[f"store.{var}"] = f"<Variável do jogo: {var}>"
        
        # Adicionar algumas informações básicas
        basic_data['_info'] = "Carregamento básico - dados limitados"
        basic_data['_variables_found'] = len(store_vars)
        basic_data['_file_size'] = len(data)
        
        print(f"✓ Carregamento básico concluído com {len(basic_data)} entradas")
        return basic_data
    
    def update_ui(self):
        """Atualiza toda a interface com os dados do save"""
        if not self.save_data:
            return
        
        # Atualizar informações
        self.update_info()
        
        # Atualizar variáveis
        self.update_variables_tree()
        
        # Atualizar JSON
        self.update_json_view()
        
        # Atualizar histórico
        self.update_history_view()
    
    def update_info(self):
        """Atualiza as informações do save"""
        self.info_text.config(state='normal')
        self.info_text.delete(1.0, tk.END)
        
        info = []
        info.append(f"Arquivo: {os.path.basename(self.current_save_path) if self.current_save_path else 'N/A'}")
        
        # Verificar se os dados estão carregados
        if not self.save_data:
            info.append("Nenhum save carregado")
            self.info_text.insert(1.0, '\n'.join(info))
            self.info_text.config(state='disabled')
            return
        
        # Para carregamento básico, mostrar informações do método alternativo
        if isinstance(self.save_data, dict) and '_info' in self.save_data:
            info.append(f"Método: {self.save_data['_info']}")
            info.append(f"Variáveis encontradas: {self.save_data.get('_variables_found', 0)}")
            info.append(f"Tamanho do arquivo: {self.save_data.get('_file_size', 0)} bytes")
        else:
            # Para carregamento completo
            if 'version' in self.save_data:
                info.append(f"Versão RenPy: {self.save_data['version']}")
            
            if 'stores' in self.save_data and 'store' in self.save_data['stores']:
                var_count = len(self.save_data['stores']['store'])
                info.append(f"Variáveis: {var_count}")
                
                # Procurar por timestamp
                store_data = self.save_data['stores']['store']
                if '_save_name' in store_data:
                    save_name = store_data['_save_name']
                    info.append(f"Nome do Save: {save_name}")
            else:
                # Contar variáveis diretamente
                var_count = len([k for k in self.save_data.keys() if k.startswith('store.')])
                info.append(f"Variáveis store.*: {var_count}")
        
        self.info_text.insert(1.0, '\n'.join(info))
        self.info_text.config(state='disabled')
    
    def update_variables_tree(self):
        """Atualiza a árvore de variáveis"""
        # Limpar árvore
        for item in self.var_tree.get_children():
            self.var_tree.delete(item)
        
        # Verificar se os dados estão carregados
        if not self.save_data:
            return
        
        # Adaptar para diferentes formatos de dados
        variables = {}
        
        # Formato completo (com estrutura stores)
        if 'stores' in self.save_data and 'store' in self.save_data['stores']:
            variables = self.save_data['stores']['store']
        # Formato básico (carregamento alternativo)
        elif isinstance(self.save_data, dict):
            # Filtrar apenas variáveis store.*
            variables = {k: v for k, v in self.save_data.items() if k.startswith('store.')}
        
        if not variables:
            # Mostrar mensagem se não há variáveis
            self.var_tree.insert('', tk.END, values=("Nenhuma variável encontrada", "info", "Tente carregar um arquivo de save válido"))
            return
        
        # Criar lista de variáveis com nomes convertidos para ordenação
        var_list = []
        for name, value in variables.items():
            # Converter nome se for bytes
            display_name = name
            if isinstance(name, bytes):
                try:
                    display_name = name.decode('utf-8')
                except UnicodeDecodeError:
                    display_name = name.decode('latin-1', errors='ignore')
            
            var_list.append((display_name, name, value))
        
        # Ordenar por nome de exibição
        try:
            var_list.sort(key=lambda x: str(x[0]).lower())
        except Exception:
            # Se a ordenação falhar, usar sem ordenação
            pass
        
        for display_name, original_name, value in var_list:
            try:
                value_type = type(value).__name__
                
                # Converter valor para string de forma segura
                if isinstance(value, bytes):
                    try:
                        value_str = value.decode('utf-8')
                    except UnicodeDecodeError:
                        value_str = value.decode('latin-1', errors='ignore')
                else:
                    value_str = str(value)
                
                # Limitar o tamanho da string mostrada
                if len(value_str) > 100:
                    value_str = value_str[:97] + "..."
                
                self.var_tree.insert('', tk.END, values=(display_name, value_type, value_str))
            except Exception as e:
                # Se houver qualquer erro, ainda assim mostrar a variável
                self.var_tree.insert('', tk.END, values=(str(display_name), "unknown", "Error displaying value"))
    
    def filter_variables(self, event=None):
        """Filtra as variáveis baseado na busca"""
        # Verificar se os dados estão carregados
        if not self.save_data:
            return
            
        search_term = self.search_var.get().lower()
        
        # Limpar árvore
        for item in self.var_tree.get_children():
            self.var_tree.delete(item)
        
        # Adaptar para diferentes formatos de dados
        variables = {}
        
        # Formato completo (com estrutura stores)
        if 'stores' in self.save_data and 'store' in self.save_data['stores']:
            variables = self.save_data['stores']['store']
        # Formato básico (carregamento alternativo)
        elif isinstance(self.save_data, dict):
            # Filtrar apenas variáveis store.*
            variables = {k: v for k, v in self.save_data.items() if k.startswith('store.')}
        
        if not variables:
            return
        
        for name, value in sorted(variables.items()):
            # Converter nome se for bytes
            display_name = name
            if isinstance(name, bytes):
                try:
                    display_name = name.decode('utf-8')
                except UnicodeDecodeError:
                    display_name = name.decode('latin-1', errors='ignore')
            
            # Converter valor para string de forma segura
            if isinstance(value, bytes):
                try:
                    value_str = value.decode('utf-8')
                except UnicodeDecodeError:
                    value_str = value.decode('latin-1', errors='ignore')
            else:
                value_str = str(value)
            
            # Verificar se corresponde ao filtro
            try:
                name_lower = str(display_name).lower()
                value_lower = value_str.lower()
                
                if search_term in name_lower or search_term in value_lower:
                    value_type = type(value).__name__
                    
                    # Limitar o tamanho da string mostrada
                    if len(value_str) > 100:
                        value_str = value_str[:97] + "..."
                    
                    self.var_tree.insert('', tk.END, values=(display_name, value_type, value_str))
            except Exception as e:
                self.var_tree.insert('', tk.END, values=(str(display_name), type(value).__name__, str(value)[:100]))
    
    def edit_variable(self, event):
        """Edita uma variável selecionada"""
        selection = self.var_tree.selection()
        if not selection:
            return
        
        # Verificar se os dados estão carregados
        if not self.save_data:
            return
        
        item = self.var_tree.item(selection[0])
        var_name = item['values'][0]
        
        # Adaptar para diferentes formatos de dados
        var_value = None
        
        # Formato completo (com estrutura stores)
        if 'stores' in self.save_data and 'store' in self.save_data['stores']:
            var_value = self.save_data['stores']['store'].get(var_name)
        # Formato básico (carregamento alternativo)
        elif isinstance(self.save_data, dict):
            # Buscar diretamente no dicionário
            if var_name in self.save_data:
                var_value = self.save_data[var_name]
            else:
                # Buscar com prefixo store.
                store_name = f"store.{var_name}"
                if store_name in self.save_data:
                    var_value = self.save_data[store_name]
        
        if var_value is None:
            messagebox.showerror("Erro", f"Variável '{var_name}' não encontrada")
            return
        
        self.var_name_var.set(var_name)
        self.var_value_var.set(str(var_value))
        self.var_value_entry.focus()
    
    def apply_variable_change(self):
        """Aplica mudança em uma variável"""
        var_name = self.var_name_var.get()
        new_value_str = self.var_value_var.get()
        
        if not var_name or not self.save_data:
            return
        
        try:
            # Encontrar a variável e seu valor atual
            old_value = None
            store_key = None
            
            # Formato completo (com estrutura stores)
            if 'stores' in self.save_data and 'store' in self.save_data['stores']:
                if var_name in self.save_data['stores']['store']:
                    old_value = self.save_data['stores']['store'][var_name]
                    store_key = ('stores', var_name)
            # Formato básico (carregamento alternativo)
            elif isinstance(self.save_data, dict):
                # Buscar diretamente no dicionário
                if var_name in self.save_data:
                    old_value = self.save_data[var_name]
                    store_key = ('direct', var_name)
                else:
                    # Buscar com prefixo store.
                    store_name = f"store.{var_name}"
                    if store_name in self.save_data:
                        old_value = self.save_data[store_name]
                        store_key = ('store_prefix', store_name)
            
            if old_value is None or store_key is None:
                messagebox.showerror("Erro", f"Variável '{var_name}' não encontrada")
                return
            
            # Tentar converter para o tipo original
            old_type = type(old_value)
            
            if old_type == bool:
                new_value = new_value_str.lower() in ('true', '1', 'yes', 'sim')
            elif old_type == int:
                new_value = int(new_value_str)
            elif old_type == float:
                new_value = float(new_value_str)
            else:
                new_value = new_value_str
            
            # Aplicar a mudança baseado no formato
            if store_key[0] == 'stores':
                self.save_data['stores']['store'][store_key[1]] = new_value
            elif store_key[0] == 'direct':
                self.save_data[store_key[1]] = new_value
            elif store_key[0] == 'store_prefix':
                self.save_data[store_key[1]] = new_value
            
            self.modified = True
            self.update_variables_tree()
            self.update_json_view()
            self.status_var.set(f"Variável '{var_name}' modificada")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao converter valor:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado:\n{str(e)}")
    
    def update_json_view(self):
        """Atualiza a visualização JSON"""
        if not self.save_data:
            return
        
        # Criar uma versão simplificada para JSON (sem objetos não serializáveis)
        json_data = self.create_json_safe_data(self.save_data)
        
        self.json_text.delete(1.0, tk.END)
        json_str = json.dumps(json_data, indent=2, ensure_ascii=False, default=str)
        self.json_text.insert(1.0, json_str)
    
    def create_json_safe_data(self, data):
        """Cria uma versão JSON-safe dos dados"""
        if isinstance(data, dict):
            result = {}
            for k, v in data.items():
                # Converter chaves que não são strings
                if isinstance(k, bytes):
                    try:
                        k = k.decode('utf-8')
                    except UnicodeDecodeError:
                        k = k.decode('latin-1', errors='ignore')
                elif not isinstance(k, str):
                    k = str(k)
                
                result[k] = self.create_json_safe_data(v)
            return result
        elif isinstance(data, list):
            return [self.create_json_safe_data(item) for item in data]
        elif isinstance(data, (str, int, float, bool, type(None))):
            return data
        elif isinstance(data, bytes):
            try:
                return data.decode('utf-8')
            except UnicodeDecodeError:
                return data.decode('latin-1', errors='ignore')
        else:
            return str(data)
    
    def apply_json_changes(self):
        """Aplica mudanças do JSON raw"""
        try:
            json_str = self.json_text.get(1.0, tk.END)
            json_data = json.loads(json_str)
            
            # Adaptar para diferentes formatos de dados
            if 'stores' in json_data and 'store' in json_data['stores']:
                # Formato completo
                if 'stores' in self.save_data and 'store' in self.save_data['stores']:
                    self.save_data['stores']['store'] = json_data['stores']['store']
                else:
                    # Formato básico - atualizar variáveis store.*
                    for var_name, var_value in json_data['stores']['store'].items():
                        store_key = f"store.{var_name}"
                        if store_key in self.save_data:
                            self.save_data[store_key] = var_value
                        else:
                            self.save_data[var_name] = var_value
            elif isinstance(json_data, dict) and isinstance(self.save_data, dict):
                # Formato básico direto
                # Atualizar apenas chaves que existem e começam com store.
                for key, value in json_data.items():
                    if key.startswith('store.') and key in self.save_data:
                        self.save_data[key] = value
            
            self.modified = True
            self.update_variables_tree()
            self.status_var.set("JSON aplicado com sucesso")
                
        except json.JSONDecodeError as e:
            messagebox.showerror("Erro", f"JSON inválido:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar JSON:\n{str(e)}")
    
    def format_json(self):
        """Formata o JSON"""
        try:
            json_str = self.json_text.get(1.0, tk.END)
            json_data = json.loads(json_str)
            formatted = json.dumps(json_data, indent=2, ensure_ascii=False)
            
            self.json_text.delete(1.0, tk.END)
            self.json_text.insert(1.0, formatted)
            
        except json.JSONDecodeError as e:
            messagebox.showerror("Erro", f"JSON inválido:\n{str(e)}")
    
    def update_history_view(self):
        """Atualiza a visualização do histórico"""
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        
        if 'log' in self.save_data:
            log_entries = self.save_data['log']
            
            history_info = []
            history_info.append(f"Entradas no histórico: {len(log_entries)}")
            history_info.append("-" * 50)
            
            for i, entry in enumerate(log_entries[-20:]):  # Últimas 20 entradas
                if isinstance(entry, dict) and 'what' in entry:
                    what = entry.get('what', '')
                    who = entry.get('who', 'Narrador')
                    history_info.append(f"{i+1}. {who}: {what}")
                else:
                    history_info.append(f"{i+1}. {str(entry)}")
            
            self.history_text.insert(1.0, '\n'.join(history_info))
        else:
            self.history_text.insert(1.0, "Nenhum histórico encontrado")
        
        self.history_text.config(state='disabled')
    
    def save_current(self):
        """Salva o arquivo atual"""
        if not self.save_data or not self.current_save_path:
            messagebox.showwarning("Aviso", "Nenhum arquivo carregado")
            return
        
        try:
            self.save_to_file(self.current_save_path)
            self.modified = False
            self.status_var.set("Arquivo salvo com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{str(e)}")
    
    def save_as(self):
        """Salva como novo arquivo"""
        if not self.save_data:
            messagebox.showwarning("Aviso", "Nenhum arquivo carregado")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salvar arquivo como",
            defaultextension="",
            filetypes=[("Arquivo log", "log"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            try:
                self.save_to_file(file_path)
                self.current_save_path = file_path
                self.modified = False
                self.status_var.set(f"Arquivo salvo como: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar:\n{str(e)}")
    
    def save_to_file(self, file_path):
        """Salva os dados no arquivo"""
        # Serializar com pickle (formato original)
        pickled_data = pickle.dumps(self.save_data)
        
        # Salvar no arquivo
        with open(file_path, 'wb') as f:
            f.write(pickled_data)
    
    def reset_changes(self):
        """Reseta as mudanças"""
        if self.current_save_path and self.modified:
            if messagebox.askyesno("Confirmar", "Descartar todas as mudanças?"):
                self.load_save_file(self.current_save_path)
                self.status_var.set("Mudanças descartadas")

def main():
    """Função principal"""
    root = tk.Tk()
    app = RenPySaveEditor(root)
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()