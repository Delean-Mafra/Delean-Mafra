#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Editor de Save RenPy - RenPy Save Editor
Created by: Delean Mafra
Simple Flask server for Editor de Save RenPy local development
"""

from flask import Flask, request, jsonify, render_template_string, send_from_directory
from werkzeug.utils import secure_filename

import os
import json
import pickle
import uuid
import tempfile
import zipfile
import io
import sys
import base64
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB max file size

# Directory to store uploaded files temporarily
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def safe_join(base, *paths):
    """
    Safer join using os.path.normpath and abspath, ensures no path traversal.
    Raises ValueError if the path would escape the base directory.
    """
    final_path = os.path.abspath(os.path.normpath(os.path.join(base, *paths)))
    if not final_path.startswith(os.path.abspath(base) + os.sep):
        raise ValueError("Attempted Path Traversal")
    return final_path

@app.route('/')
def index():
    """Serve the main index.html page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/UploadSave', methods=['POST'])
def upload_save():
    """Handle save file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo fornecido'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Generate unique ID for this upload
        file_id = str(uuid.uuid4())
        
        # Save file temporarily
        safe_name = secure_filename(file.filename)
        filename = f"{file_id}_{safe_name}"
        filepath = safe_join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze the file
        file_info = analyze_save_file(filepath)
        
        # Store file info for later retrieval
        info_path = safe_join(app.config['UPLOAD_FOLDER'], f"{file_id}_info.json")
        with open(info_path, 'w') as f:
            json.dump({
                'id': file_id,
                'original_name': file.filename,
                'filepath': filepath,
                'file_info': file_info,
                'upload_time': datetime.now().isoformat()
            }, f)
        
        return jsonify({'id': file_id, 'status': 'success'})
        
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/SaveEdit2/<file_id>')
def save_edit(file_id):
    """Generate editor interface for uploaded save file"""
    try:
        # Load file info
        info_path = safe_join(app.config['UPLOAD_FOLDER'], f"{file_id}_info.json")
        if not os.path.exists(info_path):
            return "Arquivo não encontrado ou expirado", 404
        
        with open(info_path, 'r') as f:
            file_data = json.load(f)
        
        file_info = file_data['file_info']
        original_name = file_data['original_name']
        
        # Generate editor HTML
        editor_html = generate_editor_html(file_id, original_name, file_info)
        return editor_html
        
    except Exception as e:
        app.logger.error(f"Editor error: {str(e)}")
        return f"Erro carregando editor: {str(e)}", 500

@app.route('/download/<file_id>')
def download_file(file_id):
    """Download the modified save file"""
    try:
        # Load file info
        info_path = safe_join(app.config['UPLOAD_FOLDER'], f"{file_id}_info.json")
        if not os.path.exists(info_path):
            return "Arquivo não encontrado ou expirado", 404
        
        with open(info_path, 'r') as f:
            file_data = json.load(f)
        
        original_name = file_data['original_name']
        filepath = file_data['filepath']
        
        # Ensure the filepath is within the allowed directory
        abs_filepath = safe_join(app.config['UPLOAD_FOLDER'], os.path.basename(filepath))
        
        if not os.path.exists(abs_filepath):
            return "Arquivo original não encontrado", 404
        
        return send_from_directory(
            os.path.dirname(abs_filepath), 
            os.path.basename(abs_filepath),
            as_attachment=True,
            download_name=f"modified_{original_name}"
        )
        
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return f"Erro baixando arquivo: {str(e)}", 500

@app.route('/api/file-info/<file_id>')
def get_file_info(file_id):
    """Get detailed file information as JSON"""
    try:
        info_path = safe_join(app.config['UPLOAD_FOLDER'], f"{file_id}_info.json")
        if not os.path.exists(info_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        with open(info_path, 'r') as f:
            file_data = json.load(f)
        
        return jsonify(file_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extract-files/<file_id>')
def extract_files(file_id):
    """Extract individual files from ZIP save"""
    try:
        # Load file info
        info_path = safe_join(app.config['UPLOAD_FOLDER'], f"{file_id}_info.json")
        if not os.path.exists(info_path):
            return jsonify({'error': 'File not found'}), 404
        
        with open(info_path, 'r') as f:
            file_data = json.load(f)
        
        filepath = file_data['filepath']
        # Ensure the filepath is within the allowed directory
        abs_filepath = safe_join(app.config['UPLOAD_FOLDER'], os.path.basename(filepath))
        
        # Extract files from ZIP
        with open(abs_filepath, 'rb') as f:
            file_content = f.read()
        
        extracted_files = {}
        with zipfile.ZipFile(io.BytesIO(file_content), 'r') as zip_file:
            for filename in zip_file.namelist():
                try:
                    file_data_content = zip_file.read(filename)
                    
                    # Try to decode as text if possible
                    try:
                        if filename.lower().endswith(('.json', '.txt', '.log')):
                            content = file_data_content.decode('utf-8')
                            extracted_files[filename] = {'type': 'text', 'content': content}
                        else:
                            # Store as base64 for binary files
                            content = base64.b64encode(file_data_content).decode('ascii')
                            extracted_files[filename] = {'type': 'binary', 'content': content, 'size': len(file_data_content)}
                    except:
                        # Fallback to hex for problematic files
                        content = file_data_content[:1000].hex()
                        extracted_files[filename] = {'type': 'hex', 'content': content, 'size': len(file_data_content)}
                        
                except Exception as e:
                    extracted_files[filename] = {'type': 'error', 'error': str(e)}
        
        return jsonify({'files': extracted_files})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/screenshot/<file_id>')
def get_screenshot(file_id):
    """Get screenshot from RenPy save"""
    try:
        # Load file info
        info_path = safe_join(app.config['UPLOAD_FOLDER'], f"{file_id}_info.json")
        if not os.path.exists(info_path):
            return jsonify({'error': 'File not found'}), 404
        
        with open(info_path, 'r') as f:
            file_data = json.load(f)
        
        filepath = file_data['filepath']
        # Ensure the filepath is within the allowed directory
        abs_filepath = safe_join(app.config['UPLOAD_FOLDER'], os.path.basename(filepath))
        
        # Extract screenshot from ZIP
        with open(abs_filepath, 'rb') as f:
            file_content = f.read()
        
        with zipfile.ZipFile(io.BytesIO(file_content), 'r') as zip_file:
            for filename in zip_file.namelist():
                if 'screenshot' in filename.lower() and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    screenshot_data = zip_file.read(filename)
                    screenshot_b64 = base64.b64encode(screenshot_data).decode('ascii')
                    
                    # Determine MIME type
                    if filename.lower().endswith('.png'):
                        mime_type = 'image/png'
                    elif filename.lower().endswith(('.jpg', '.jpeg')):
                        mime_type = 'image/jpeg'
                    else:
                        mime_type = 'image/png'
                    
                    return jsonify({
                        'filename': filename,
                        'data': screenshot_b64,
                        'mime_type': mime_type,
                        'size': len(screenshot_data)
                    })
        
        return jsonify({'error': 'Screenshot não encontrada'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save-data/<file_id>')
def get_save_data(file_id):
    """Get detailed save data from RenPy save"""
    try:
        # Load file info
        info_path = safe_join(app.config['UPLOAD_FOLDER'], f"{file_id}_info.json")
        if not os.path.exists(info_path):
            return jsonify({'error': 'File not found'}), 404
        
        with open(info_path, 'r') as f:
            file_data = json.load(f)
        
        # Return the save data that was already analyzed
        save_data = file_data.get('file_info', {}).get('data', {})
        
        return jsonify({
            'save_data': save_data,
            'analysis': {
                'file_count': save_data.get('file_count', 0),
                'has_screenshot': 'screenshot' in save_data,
                'has_save_data': 'save_data' in save_data,
                'files': save_data.get('files', [])
            }
        })
        
    except Exception as e:
        logging.exception("Exception in get_save_data:")
        return jsonify({'error': 'An internal error has occurred.'}), 500

@app.route('/api/decode-renpy-file/<file_id>/<path:filename>')
def decode_renpy_file(file_id, filename):
    """Decode a specific RenPy file from the save archive"""
    try:
        # Load file info
        info_path = safe_join(app.config['UPLOAD_FOLDER'], f"{file_id}_info.json")
        if not os.path.exists(info_path):
            return jsonify({'error': 'File not found'}), 404
        
        with open(info_path, 'r') as f:
            file_data = json.load(f)
        
        filepath = file_data['filepath']
        # Ensure the filepath is within the allowed directory
        abs_filepath = safe_join(app.config['UPLOAD_FOLDER'], os.path.basename(filepath))
        
        # Extract the specific file from ZIP
        with open(abs_filepath, 'rb') as f:
            file_content = f.read()
        
        with zipfile.ZipFile(io.BytesIO(file_content), 'r') as zip_file:
            if filename not in zip_file.namelist():
                return jsonify({'error': f'Arquivo {filename} não encontrado no arquivo'}), 404
            
            file_data_content = zip_file.read(filename)
            
            # Try to decode as RenPy pickle
            decoded_data = extract_renpy_variables(file_data_content)
            
            return jsonify(decoded_data)
        
    except Exception as e:
        logging.exception("Exception in decode_renpy_file:")

        return jsonify({'error': 'An internal error has occurred.'}), 500


@app.route('/api/save-renpy-changes/<file_id>/<path:filename>', methods=['POST'])
def save_renpy_changes(file_id, filename):
    """Save changes back to RenPy file (Note: This is complex and may not work for all saves)"""
    try:
        changes = request.json
        
        # For now, we'll just return the changes as confirmation
        # Actually modifying RenPy saves is very complex and risky
        return jsonify({
            'success': True, 
            'message': 'Alterações recebidas com sucesso',
            'note': 'Modificação real do save não implementada ainda por razões de segurança',
            'changes_count': len(changes)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'Arquivo muito grande. Tamanho máximo é 25MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint não encontrado.'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Erro interno do servidor.'}), 500

def analyze_save_file(filepath):
    """Analyze save file to determine format and extract data"""
    try:
        # Try to determine file type
        filename = os.path.basename(filepath)
        file_ext = os.path.splitext(filename)[1].lower()
        
        with open(filepath, 'rb') as f:
            file_content = f.read()
        
        file_info = {
            'filename': filename,
            'size': len(file_content),
            'type': 'unknown',
            'data': None,
            'error': None
        }
        
        # Check file header to detect different formats
        header = file_content[:10]
        
        # Check for ZIP format (RenPy saves are often ZIP files)
        if header.startswith(b'PK'):
            return analyze_zip_save(filepath, file_content, file_info)
        
        # Try direct pickle loading (original RenPy format)
        try:
            data = load_renpy_pickle(filepath)
            if data:
                file_info['type'] = 'renpy_save'
                file_info['data'] = serialize_pickle_data(data)
                return file_info
        except Exception as e:
            print(f"Direct pickle load failed: {e}")
        
        # Try JSON
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            file_info['type'] = 'json'
            file_info['data'] = data
            return file_info
        except:
            pass
        
        # Try as text with different encodings
        text_data = try_as_text(filepath)
        if text_data:
            file_info['type'] = 'text'
            file_info['data'] = text_data
            return file_info
        
        # Enhanced binary analysis for RenPy saves
        if is_likely_renpy_save(file_content, filename):
            file_info['type'] = 'renpy_binary'
            file_info['data'] = analyze_renpy_binary(file_content)
        else:
            # Generic binary file
            file_info['type'] = 'binary'
            file_info['data'] = {'size': len(file_content), 'preview': file_content[:200].hex()}
        
        return file_info
        
    except Exception as e:
        return {'error': str(e), 'type': 'error'}

def analyze_zip_save(filepath, file_content, file_info):
    """Analyze ZIP-based RenPy save files"""
    import zipfile
    import io
    
    try:
        # Try to open as ZIP
        with zipfile.ZipFile(io.BytesIO(file_content), 'r') as zip_file:
            file_list = zip_file.namelist()
            
            file_info['type'] = 'renpy_zip_save'
            zip_data = {
                'files': file_list,
                'file_count': len(file_list),
                'is_renpy': any('screenshot' in f.lower() or 'save' in f.lower() for f in file_list)
            }
            
            # Try to extract and analyze main save data
            for filename in file_list:
                if filename.lower() in ['save', 'data', 'game_data'] or filename.endswith('.save'):
                    try:
                        save_data = zip_file.read(filename)
                        # Try to unpickle the save data
                        try:
                            import pickle
                            data = pickle.loads(save_data)
                            zip_data['save_data'] = serialize_pickle_data(data)
                            zip_data['save_file'] = filename
                            break
                        except:
                            # Save as raw binary if can't unpickle
                            zip_data['save_data_raw'] = save_data[:500].hex()
                            zip_data['save_file'] = filename
                    except:
                        continue
            
            # Extract screenshot info if available
            for filename in file_list:
                if 'screenshot' in filename.lower() and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        screenshot_data = zip_file.read(filename)
                        zip_data['screenshot'] = {
                            'filename': filename,
                            'size': len(screenshot_data),
                            'format': filename.split('.')[-1].upper()
                        }
                        break
                    except:
                        continue
            
            file_info['data'] = zip_data
            return file_info
            
    except zipfile.BadZipFile:
        # Not a valid ZIP file, treat as binary
        file_info['type'] = 'binary'
        file_info['data'] = {'size': len(file_content), 'preview': file_content[:200].hex()}
        return file_info
    except Exception as e:
        file_info['error'] = f"ZIP analysis failed: {str(e)}"
        file_info['type'] = 'binary'
        file_info['data'] = {'size': len(file_content), 'preview': file_content[:200].hex()}
        return file_info

def load_renpy_pickle(filepath):
    """Load RenPy pickle with enhanced error handling"""
    import sys
    
    # Create comprehensive fake modules for RenPy
    fake_modules = {}
    original_modules = {}
    
    class FakeRenPyClass:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
        
        def __getattr__(self, name):
            return FakeRenPyClass()
        
        def __call__(self, *args, **kwargs):
            return FakeRenPyClass()
        
        def __getstate__(self):
            return {'fake': True}
        
        def __setstate__(self, state):
            pass
    
    class FakeModule:
        def __getattr__(self, name):
            return FakeRenPyClass()
    
    try:
        # Install fake modules
        renpy_modules = ['renpy', 'store', 'game', '_renpy', 'renpy.display', 'renpy.character']
        for module_name in renpy_modules:
            if module_name in sys.modules:
                original_modules[module_name] = sys.modules[module_name]
            sys.modules[module_name] = FakeModule()
            fake_modules[module_name] = FakeModule()
        
        # Try to load the pickle file
        with open(filepath, 'rb') as f:
            return pickle.load(f)
            
    except Exception as e:
        print(f"Enhanced pickle load failed: {e}")
        return None
    finally:
        # Restore original modules
        for module_name in renpy_modules:
            if module_name in original_modules:
                sys.modules[module_name] = original_modules[module_name]
            elif module_name in sys.modules:
                del sys.modules[module_name]

def try_as_text(filepath):
    """Try to read file as text with multiple encodings"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii', 'utf-16', 'utf-32']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            # Check if content looks like text (has reasonable ratio of printable chars)
            printable_ratio = sum(1 for c in content[:1000] if c.isprintable() or c.isspace()) / min(1000, len(content))
            if printable_ratio > 0.8:  # 80% printable characters
                return {'content': content[:2000] + '...' if len(content) > 2000 else content, 'encoding': encoding}
        except:
            continue
    
    return None

def is_renpy_save_data(data):
    """Check if the unpickled data looks like a RenPy save"""
    if isinstance(data, dict):
        # Common RenPy save keys
        renpy_keys = ['version', 'save_name', 'extra_info', 'screenshot', 'store', 'log']
        return any(key in data for key in renpy_keys)
    return False

def is_likely_renpy_save(content, filename):
    """Check if file is likely a RenPy save based on content and filename"""
    # Check filename patterns
    if any(pattern in filename.lower() for pattern in ['-lt', 'save', '.sav']):
        return True
    
    # Check for pickle signatures in content
    pickle_signatures = [b'\x80\x03', b'\x80\x02', b'\x80\x01', b'\x80\x00', b'(']
    if any(sig in content[:20] for sig in pickle_signatures):
        return True
    
    return False

def load_renpy_save(filepath):
    """Attempt to load RenPy save with custom handling"""
    try:
        import sys
        
        # Create fake RenPy modules to handle missing imports
        class FakeRenPyModule:
            def __getattr__(self, name):
                return FakeRenPyObject()
        
        class FakeRenPyObject:
            def __init__(self, *args, **kwargs):
                pass
            def __getattr__(self, name):
                return FakeRenPyObject()
            def __call__(self, *args, **kwargs):
                return FakeRenPyObject()
        
        # Install fake modules
        fake_modules = ['renpy', 'store', 'game']
        original_modules = {}
        
        for module in fake_modules:
            if module in sys.modules:
                original_modules[module] = sys.modules[module]
            sys.modules[module] = FakeRenPyModule()
        
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            return data
        finally:
            # Restore original modules
            for module in fake_modules:
                if module in original_modules:
                    sys.modules[module] = original_modules[module]
                elif module in sys.modules:
                    del sys.modules[module]
                    
    except Exception as e:
        print(f"Custom RenPy load failed: {e}")
        return None

def analyze_renpy_binary(content):
    """Analyze binary RenPy save file"""
    try:
        # Look for common patterns
        analysis = {
            'size': len(content),
            'header': content[:20].hex(),
            'is_compressed': b'\x78\x9c' in content[:100],  # zlib signature
            'has_pickle': any(sig in content[:100] for sig in [b'\x80\x03', b'\x80\x02', b'\x80\x01']),
            'preview': content[:200].hex()
        }
        
        # Try to find readable strings
        try:
            strings = []
            current_string = b''
            for byte in content[:1000]:
                if 32 <= byte <= 126:  # Printable ASCII
                    current_string += bytes([byte])
                else:
                    if len(current_string) > 3:
                        strings.append(current_string.decode('ascii'))
                    current_string = b''
            
            if strings:
                analysis['readable_strings'] = strings[:10]  # First 10 strings
        except:
            pass
        
        return analysis
        
    except Exception as e:
        return {'error': str(e)}

def serialize_pickle_data(data, max_depth=3, current_depth=0):
    """Convert pickle data to JSON-serializable format"""
    if current_depth > max_depth:
        return f"<object too deep: {type(data).__name__}>"
    
    if isinstance(data, (str, int, float, bool)) or data is None:
        return data
    elif isinstance(data, dict):
        result = {}
        for k, v in list(data.items())[:50]:  # Limit to first 50 items
            try:
                key = str(k) if not isinstance(k, str) else k
                result[key] = serialize_pickle_data(v, max_depth, current_depth + 1)
            except:
                result[str(k)] = f"<error serializing: {type(v).__name__}>"
        if len(data) > 50:
            result['...'] = f"({len(data) - 50} more items)"
        return result
    elif isinstance(data, (list, tuple)):
        result = []
        for i, item in enumerate(data[:20]):  # Limit to first 20 items
            try:
                result.append(serialize_pickle_data(item, max_depth, current_depth + 1))
            except:
                result.append(f"<error serializing item {i}: {type(item).__name__}>")
        if len(data) > 20:
            result.append(f"... ({len(data) - 20} more items)")
        return result
    else:
        return f"<{type(data).__name__}: {str(data)[:100]}>"

def generate_editor_html(file_id, filename, file_info):
    """Generate HTML editor interface"""
    return f"""
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">
                <i class="glyphicon glyphicon-edit"></i> Editando: {filename}
                <span class="badge pull-right">{file_info.get('type', 'desconhecido')}</span>
            </h3>
        </div>
        <div class="panel-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Tipo de Arquivo:</strong> <span class="label label-info">{file_info.get('type', 'desconhecido')}</span></p>
                </div>
                <div class="col-md-6">
                    <p><strong>Tamanho:</strong> {file_info.get('size', 0):,} bytes</p>
                </div>
            </div>
            
            {generate_data_editor(file_info.get('data', {}), file_info.get('type', 'desconhecido'))}
            
            <hr>
            <div class="text-center">
                <div class="btn-group" role="group">
                    <button class="btn btn-success" onclick="downloadOriginalFile('{file_id}')">
                        <i class="glyphicon glyphicon-download"></i> Baixar Original
                    </button>
                    <button class="btn btn-info" onclick="getFileInfo('{file_id}')">
                        <i class="glyphicon glyphicon-info-sign"></i> Info do Arquivo
                    </button>
                    <button class="btn btn-default" onclick="OnDownload()">
                        <i class="glyphicon glyphicon-arrow-left"></i> Voltar ao Upload
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function downloadOriginalFile(fileId) {{
        window.location.href = '/download/' + fileId;
    }}
    
    function getFileInfo(fileId) {{
        fetch('/api/file-info/' + fileId)
            .then(response => response.json())
            .then(data => {{
                var info = 'Informações do Arquivo:\\n\\n';
                info += 'Nome Original: ' + data.original_name + '\\n';
                info += 'Hora do Upload: ' + data.upload_time + '\\n';
                info += 'Tipo de Arquivo: ' + data.file_info.type + '\\n';
                info += 'Tamanho: ' + data.file_info.size.toLocaleString() + ' bytes\\n';
                if (data.file_info.error) {{
                    info += 'Erro: ' + data.file_info.error + '\\n';
                }}
                alert(info);
            }})
            .catch(error => {{
                alert('Erro obtendo informações do arquivo: ' + error);
            }});
    }}
    </script>
    """

def generate_data_editor(data, file_type):
    """Generate editor interface based on data type"""
    if file_type == 'json':
        return f"""
        <h4>Editor de Dados JSON</h4>
        <textarea class="form-control" rows="20" id="jsonData">{json.dumps(data, indent=2)}</textarea>
        <div class="mt-2">
            <button class="btn btn-success" onclick="validateJSON()">Validar JSON</button>
        </div>
        """
    elif file_type == 'renpy_zip_save':
        return f"""
        <h4>🎮 Arquivo de Save ZIP RenPy</h4>
        <div class="alert alert-success">
            <strong>✅ Save ZIP RenPy Detectado!</strong> Este é um arquivo de save RenPy moderno armazenado como arquivo ZIP.
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="panel panel-info">
                    <div class="panel-heading">📁 Conteúdo do Arquivo</div>
                    <div class="panel-body">
                        <strong>Arquivos no pacote:</strong> {data.get('file_count', 0)}<br>
                        <strong>É Save RenPy:</strong> {'✅ Sim' if data.get('is_renpy') else '❓ Desconhecido'}<br>
                        
                        <h6 class="mt-2">Arquivos:</h6>
                        <ul class="list-unstyled" style="max-height: 200px; overflow-y: auto;">
                            {"".join(f"<li><code>{f}</code></li>" for f in data.get('files', []))}
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                {f'''<div class="panel panel-success">
                    <div class="panel-heading">📸 Informações da Screenshot</div>
                    <div class="panel-body">
                        <strong>Arquivo:</strong> {data['screenshot']['filename']}<br>
                        <strong>Tamanho:</strong> {data['screenshot']['size']:,} bytes<br>
                        <strong>Formato:</strong> {data['screenshot']['format']}
                    </div>
                </div>''' if data.get('screenshot') else '<div class="alert alert-info">Nenhuma screenshot encontrada no arquivo de save.</div>'}
            </div>
        </div>
        
        {f'''<div class="panel panel-primary">
            <div class="panel-heading">💾 Dados do Save ({data.get('save_file', 'desconhecido')})</div>
            <div class="panel-body">
                <div class="panel-group" id="saveDataAccordion">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#saveDataAccordion" href="#saveDataContent">
                                    📋 Ver Estrutura dos Dados do Save (Clique para expandir)
                                </a>
                            </h4>
                        </div>
                        <div id="saveDataContent" class="panel-collapse collapse">
                            <div class="panel-body">
                                <pre style="max-height: 400px; overflow-y: auto; font-size: 11px;">{json.dumps(data.get('save_data', {}), indent=2)}</pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>''' if data.get('save_data') else ''}
        
        {f'''<div class="alert alert-warning">
            <h6>Dados Brutos do Save (Binário)</h6>
            <p>Os dados do save não puderam ser totalmente decodificados. Aqui estão os dados binários brutos:</p>
            <code style="word-break: break-all;">{data.get('save_data_raw', '')}</code>
        </div>''' if data.get('save_data_raw') and not data.get('save_data') else ''}
        
        {generate_renpy_zip_tools(data)}
        """
    elif file_type in ['pickle', 'renpy_save']:
        return f"""
        <h4>Visualizador de Arquivo de Save RenPy</h4>
        <div class="alert alert-info">
            <strong>Save RenPy Detectado!</strong> Este parece ser um arquivo de save RenPy. 
            Abaixo está uma visualização simplificada da estrutura de dados.
        </div>
        
        <div class="panel-group" id="accordion">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" data-parent="#accordion" href="#dataStructure">
                            📋 Estrutura de Dados (Clique para expandir)
                        </a>
                    </h4>
                </div>
                <div id="dataStructure" class="panel-collapse collapse">
                    <div class="panel-body">
                        <pre style="max-height: 400px; overflow-y: auto; font-size: 12px;">{json.dumps(data, indent=2)}</pre>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="alert alert-warning">
            <strong>Nota:</strong> Arquivos de save RenPy são formatos binários complexos. 
            Edição direta pode corromper o arquivo de save. Considere fazer um backup antes de qualquer modificação.
        </div>
        
        {generate_renpy_editor_tools(data)}
        """
    elif file_type == 'renpy_binary':
        return f"""
        <h4>Arquivo de Save Binário RenPy</h4>
        <div class="alert alert-info">
            <strong>Save Binário RenPy Detectado!</strong> Este arquivo contém dados binários que não puderam ser diretamente extraídos.
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <h5>Análise do Arquivo:</h5>
                <ul class="list-unstyled">
                    <li><strong>Tamanho:</strong> {data.get('size', 0):,} bytes</li>
                    <li><strong>Comprimido:</strong> {'Sim' if data.get('is_compressed') else 'Não'}</li>
                    <li><strong>Tem Dados Pickle:</strong> {'Sim' if data.get('has_pickle') else 'Não'}</li>
                </ul>
            </div>
            <div class="col-md-6">
                <h5>Cabeçalho (primeiros 20 bytes):</h5>
                <code>{data.get('header', 'N/A')}</code>
            </div>
        </div>
        
        {f'''<div class="mt-3">
            <h5>Strings Legíveis Encontradas:</h5>
            <ul>
                {"".join(f"<li><code>{string}</code></li>" for string in data.get('readable_strings', [])[:10])}
            </ul>
        </div>''' if data.get('readable_strings') else ''}
        
        <div class="alert alert-warning">
            <strong>Usuários Avançados:</strong> Este arquivo binário pode exigir ferramentas especializadas ou 
            edição manual hexadecimal. Considere usar um editor hexadecimal para análise detalhada.
        </div>
        """
    elif file_type == 'text':
        encoding = data.get('encoding', 'utf-8') if isinstance(data, dict) else 'utf-8'
        content = data.get('content', str(data)) if isinstance(data, dict) else str(data)
        
        return f"""
        <h4>Editor de Arquivo de Texto</h4>
        <div class="alert alert-info">
            <strong>Codificação:</strong> {encoding}
        </div>
        <textarea class="form-control" rows="20" id="textData">{content}</textarea>
        <div class="mt-2">
            <button class="btn btn-info" onclick="countLines()">Contar Linhas</button>
            <button class="btn btn-info" onclick="countWords()">Contar Palavras</button>
            <button class="btn btn-warning" onclick="searchText()">Buscar Texto</button>
        </div>
        """
    else:
        return f"""
        <div class="alert alert-warning">
            <h4>Tipo de Arquivo Não Suportado</h4>
            <p>Este tipo de arquivo ({file_type}) não é atualmente suportado para edição.</p>
            <p><strong>Formatos suportados:</strong></p>
            <ul>
                <li>✅ Arquivos JSON (.json)</li>
                <li>✅ Arquivos de texto (.txt)</li>
                <li>✅ Saves ZIP RenPy (.save, .sav) - Formato moderno</li>
                <li>✅ Saves pickle RenPy - Formato legado</li>
                <li>✅ Arquivos pickle genéricos (.pkl, .pickle)</li>
            </ul>
            
            <div class="mt-3">
                <h5>💡 Sugestões:</h5>
                <ul>
                    <li>Se este é um save RenPy, tente renomeá-lo com extensão .save</li>
                    <li>Verifique se o arquivo está corrompido ou comprimido</li>
                    <li>Use um editor hexadecimal para análise binária de baixo nível</li>
                    <li>Tente abrir com um editor de save RenPy diferente</li>
                </ul>
            </div>
        </div>
        """

def generate_renpy_zip_tools(data):
    """Generate specialized tools for RenPy ZIP save editing"""
    tools_html = """
    <div class="mt-3">
        <h5>🛠️ Ferramentas de Save ZIP RenPy</h5>
        <div class="btn-group" role="group">
            <button class="btn btn-info btn-sm" onclick="extractFiles()">
                📤 Extrair Arquivos
            </button>
            <button class="btn btn-warning btn-sm" onclick="viewScreenshot()">
                🖼️ Ver Screenshot
            </button>
            <button class="btn btn-primary btn-sm" onclick="exportSaveData()">
                💾 Exportar Dados do Save
            </button>
            <button class="btn btn-success btn-sm" onclick="saveInfo()">
                ℹ️ Informações do Save
            </button>
        </div>
    </div>
    """
    return tools_html

def generate_renpy_editor_tools(data):
    """Generate specialized tools for RenPy save editing"""
    tools_html = """
    <div class="mt-3">
        <h5>🛠️ Ferramentas de Save RenPy</h5>
        <div class="btn-group" role="group">
            <button class="btn btn-info btn-sm" onclick="searchInSave()">
                🔍 Buscar Dados
            </button>
            <button class="btn btn-warning btn-sm" onclick="showSaveInfo()">
                ℹ️ Info do Save
            </button>
            <button class="btn btn-primary btn-sm" onclick="exportAsJSON()">
                📤 Exportar como JSON
            </button>
        </div>
    </div>
    """
    return tools_html

def extract_renpy_variables(file_content):
    """Extract RenPy variables from save data - Implementation by Delean Mafra"""
    print(f"DEBUG: extract_renpy_variables called with {len(file_content)} bytes")
    
    result = {
        'variables': {},
        'metadata': {},
        'raw_preview': '',
        'decoded': False
    }
    
    try:
        # Extract readable strings from the binary data
        print("DEBUG: Starting string extraction")
        preview_text = ""
        current_string = b''
        readable_strings = []
        
        for byte in file_content:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += bytes([byte])
            else:
                if len(current_string) > 5:  # Only strings longer than 5 chars
                    string_val = current_string.decode('ascii')
                    readable_strings.append(string_val)
                    if len(preview_text) < 2000:
                        preview_text += string_val + ' '
                current_string = b''
        
        # Add final string if exists
        if len(current_string) > 5:
            string_val = current_string.decode('ascii')
            readable_strings.append(string_val)
        
        result['raw_preview'] = preview_text[:2000]
        print(f"DEBUG: Found {len(readable_strings)} readable strings")
        
        # Try to find store variables from readable strings
        store_vars = {}
        for string in readable_strings:
            if string.startswith('store.') and len(string) > 6:
                var_name = string.replace('store.', '')
                # Clean up variable name
                var_name = var_name.split()[0] if ' ' in var_name else var_name
                if var_name and var_name not in store_vars:
                    store_vars[var_name] = f"Variable found in save data"
        
        print(f"DEBUG: Found {len(store_vars)} store variables")
        
        result['variables'] = store_vars
        result['decoded'] = True if store_vars else False
        
        if store_vars:
            result['message'] = f"Encontradas {len(store_vars)} variáveis store nos dados do save"
            print(f"DEBUG: Successfully extracted variables: {list(store_vars.keys())[:10]}")
        else:
            result['error'] = "Nenhuma variável store encontrada nas strings legíveis"
            print("DEBUG: No store variables found")
            
    except Exception as e:
        print(f"DEBUG: Exception in extract_renpy_variables: {str(e)}")
        result['error'] = f"Falha ao extrair dados: {str(e)}"
    
    print(f"DEBUG: Returning result with decoded={result['decoded']}, variables count: {len(result['variables'])}")
    return result

def decode_renpy_save_data(file_content):
    """Decode RenPy save data from binary content - Created by Delean Mafra"""
    print(f"DEBUG: decode_renpy_save_data called with {len(file_content)} bytes")
    
    result = {
        'variables': {},
        'metadata': {},
        'raw_preview': '',
        'decoded': False
    }
    
    # For now, let's skip the complex pickle decoding and focus on extracting readable data
    try:
        # Extract readable strings from the binary data
        preview_text = ""
        current_string = b''
        readable_strings = []
        
        for byte in file_content:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += bytes([byte])
            else:
                if len(current_string) > 5:  # Only strings longer than 5 chars
                    string_val = current_string.decode('ascii')
                    readable_strings.append(string_val)
                    if len(preview_text) < 2000:
                        preview_text += string_val + ' '
                current_string = b''
        
        result['raw_preview'] = preview_text[:2000]
        
        # Try to find store variables from readable strings
        store_vars = {}
        for string in readable_strings:
            if string.startswith('store.') and len(string) > 6:
                var_name = string.replace('store.', '')
                if var_name not in store_vars:
                    store_vars[var_name] = f"Found in save data: {string}"
        
        result['variables'] = store_vars
        result['decoded'] = True if store_vars else False
        
        if store_vars:
            result['message'] = f"Encontradas {len(store_vars)} variáveis store nos dados do save"
        else:
            result['error'] = "Nenhuma variável store encontrada nas strings legíveis"
            
    except Exception as e:
        result['error'] = f"Falha ao extrair dados: {str(e)}"
    
    print(f"DEBUG: Returning result with decoded={result['decoded']}, variables count: {len(result['variables'])}")
    return result

def serialize_for_edit(value):
    """Convert values to editable format"""
    try:
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        elif isinstance(value, (list, tuple)):
            if len(value) < 10:  # Only for small lists
                return [serialize_for_edit(item) for item in value]
            else:
                return f"<list with {len(value)} items>"
        elif isinstance(value, dict):
            if len(value) < 10:  # Only for small dicts
                return {str(k): serialize_for_edit(v) for k, v in value.items()}
            else:
                return f"<dict with {len(value)} items>"
        else:
            # For complex objects, return string representation
            return str(value)[:100]  # Limit length
    except:
        return "<unable to serialize>"

if __name__ == '__main__':
    print("Iniciando servidor local do Editor de Save RenPy...")
    print("Abra seu navegador em: http://localhost:5000")
    print("Pressione Ctrl+C para parar o servidor")
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
