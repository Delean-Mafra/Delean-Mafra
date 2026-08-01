#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Editor de Save RenPy - RenPy Save Editor
Created by: Delean Mafra
Simple Flask server for Editor de Save RenPy local development
"""

from flask import Flask, request, jsonify, render_template_string, send_from_directory
import html
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

class RestrictedUnpickler(pickle.Unpickler):
    """
    Deserializador seguro que previne RCE (Remote Code Execution).
    Classes não reconhecidas são substituídas por um mock inofensivo.
    """
    def find_class(self, module, name):
        class FakeRenPyClass:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
            
            def __getattr__(self, attr):
                return FakeRenPyClass()
            
            def __call__(self, *args, **kwargs):
                return FakeRenPyClass()
            
            def __repr__(self):
                return f"<FakeClass {module}.{name}>"
            
            def __getstate__(self):
                return {'fake': True}
            
            def __setstate__(self, state):
                pass

        return FakeRenPyClass

def safe_pickle_load(file_obj):
    """Carrega dados usando o deserializador restrito."""
    return RestrictedUnpickler(file_obj).load()

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
        return jsonify({'error': 'Erro interno do servidor'}), 500

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
        return "Erro interno do servidor", 500

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
        return "Erro interno do servidor", 500

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
        app.logger.error(f"File info error: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

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
        app.logger.error(f"Extract files error: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

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
        app.logger.error(f"Screenshot error: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

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

def extract_renpy_variables(file_data_content):
    """Descompacta variáveis RenPy de bytes brutos de forma segura."""
    try:
        f = io.BytesIO(file_data_content)
        data = safe_pickle_load(f)
        return serialize_pickle_data(data)
    except Exception as e:
        return {"error": str(e)}

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
            
        # Decodifica o save do RenPy de forma segura
        decoded_data = extract_renpy_variables(file_data_content)
        
        # Valida se os dados retornados contêm algum indício de erro antes de enviar
        if isinstance(decoded_data, dict) and "error" in decoded_data:
            logging.error("Erro interno capturado na decodificação.")
            return jsonify({"success": False, "message": "Erro ao processar o arquivo de save."}), 400

        return jsonify(decoded_data)

    except Exception as e:
        logging.exception("Exception in decode_renpy_file:")
        return jsonify({"success": False, "message": "Erro interno no servidor."}), 500


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
        app.logger.error(f"Save changes error: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

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
        
        # Try direct pickle loading safely (original RenPy format)
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
                        # Try to unpickle the save data safely
                        try:
                            f_save = io.BytesIO(save_data)
                            data = safe_pickle_load(f_save)
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
    """Load RenPy pickle with secure custom Unpickler"""
    try:
        with open(filepath, 'rb') as f:
            return safe_pickle_load(f)
    except Exception as e:
        print(f"Secure pickle load failed: {e}")
        return None

def try_as_text(filepath):
    """Try to read file as text with multiple encodings"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii', 'utf-16', 'utf-32']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            # Check if content looks like text (has reasonable ratio of printable chars)
            printable_ratio = sum(1 for c in content[:1000] if c.isprintable() or c.isspace()) / min(1000, max(1, len(content)))
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
    """Attempt to load RenPy save safely"""
    try:
        with open(filepath, 'rb') as f:
            return safe_pickle_load(f)
    except Exception as e:
        print(f"Secure RenPy load failed: {e}")
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
        # For complex objects, return string representation
        return str(data)[:100]  # Limit length

def generate_editor_html(file_id, filename, file_info):
    """Generate HTML editor interface"""
    # Escape user-controlled values
    safe_file_id = html.escape(str(file_id))
    safe_filename = html.escape(str(filename))
    safe_type = html.escape(str(file_info.get('type', 'desconhecido')))
    safe_size = html.escape(f"{file_info.get('size', 0):,}")
    
    return f"""
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">
                <i class="glyphicon glyphicon-edit"></i> Editando: {safe_filename}
                <span class="badge pull-right">{safe_type}</span>
            </h3>
        </div>
        <div class="panel-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Tipo de Arquivo:</strong> <span class="label label-info">{safe_type}</span></p>
                </div>
                <div class="col-md-6">
                    <p><strong>Tamanho:</strong> {safe_size} bytes</p>
                </div>
            </div>
            
            {generate_data_editor(file_info.get('data', {}), file_info.get('type', 'desconhecido'))}
            
            <hr>
            <div class="text-center">
                <div class="btn-group" role="group">
                    <button class="btn btn-success" onclick="downloadOriginalFile('{safe_file_id}')">
                        <i class="glyphicon glyphicon-download"></i> Baixar Original
                    </button>
                    <button class="btn btn-info" onclick="getFileInfo('{safe_file_id}')">
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

    function OnDownload() {{
        window.history.back();
    }}
    </script>
    """

def generate_data_editor(data, file_type):
    """Generate editor interface based on data type"""
    if file_type == 'json':
        safe_json = html.escape(json.dumps(data, indent=2))
        return f"""
        <h4>Editor de Dados JSON</h4>
        <textarea class="form-control" rows="20" id="jsonData">{safe_json}</textarea>
        <div class="mt-2">
            <button class="btn btn-success" onclick="validateJSON()">Validar JSON</button>
        </div>
        <script>
        function validateJSON() {{
            try {{
                var val = document.getElementById('jsonData').value;
                JSON.parse(val);
                alert('JSON válido!');
            }} catch (e) {{
                alert('JSON Inválido: ' + e.message);
            }}
        }}
        </script>
        """
    elif file_type == 'renpy_zip_save':
        if data.get('screenshot'):
            screenshot_html = (
                f'<div class="panel panel-success">'
                f'  <div class="panel-heading">📸 Informações da Screenshot</div>'
                f'  <div class="panel-body">'
                f'    <strong>Arquivo:</strong> {html.escape(str(data["screenshot"]["filename"]))}<br>'
                f'    <strong>Tamanho:</strong> {data["screenshot"]["size"]:,} bytes<br>'
                f'    <strong>Formato:</strong> {html.escape(str(data["screenshot"]["format"]))}'
                f'  </div>'
                f'</div>'
            )
        else:
            screenshot_html = '<div class="alert alert-info">Nenhuma screenshot encontrada no arquivo de save.</div>'

        if data.get('save_data'):
            safe_save_file = html.escape(str(data.get("save_file", "desconhecido")))
            safe_save_data = html.escape(json.dumps(data.get("save_data", {}), indent=2))
            save_data_html = (
                f'<div class="panel panel-primary">'
                f'  <div class="panel-heading">💾 Dados do Save ({safe_save_file})</div>'
                f'  <div class="panel-body">'
                f'    <div class="panel-group" id="saveDataAccordion">'
                f'      <div class="panel panel-default">'
                f'        <div class="panel-heading">'
                f'          <h4 class="panel-title">'
                f'            <a data-toggle="collapse" data-parent="#saveDataAccordion" href="#saveDataContent">'
                f'              📋 Ver Estrutura dos Dados do Save (Clique para expandir)'
                f'            </a>'
                f'          </h4>'
                f'        </div>'
                f'        <div id="saveDataContent" class="panel-collapse collapse">'
                f'          <div class="panel-body">'
                f'            <pre style="max-height: 400px; overflow-y: auto; font-size: 11px;">{safe_save_data}</pre>'
                f'          </div>'
                f'        </div>'
                f'      </div>'
                f'    </div>'
                f'  </div>'
                f'</div>'
            )
        else:
            save_data_html = '<div class="alert alert-warning">Não foi possível decodificar os dados internos.</div>'

        return screenshot_html + save_data_html
    
    return '<div class="alert alert-warning">Formato de arquivo não suportado para edição visual ainda.</div>'
