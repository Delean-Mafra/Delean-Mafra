// RenPy Save Editor Tools - JavaScript Functions
// Enhanced RenPy save file analysis and editing tools
// Created by: Delean Mafra

// Prevent multiple executions
var isModalOpen = false;
var currentFileId = null; // Store current file ID globally

// Global functions for RenPy ZIP tools
window.extractFiles = function() {
    if (isModalOpen) return; // Prevent multiple calls
    
    var fileId = getFileIdFromUrl();
    if (!fileId) {
        alert('Erro: Não foi possível determinar o ID do arquivo');
        return;
    }
    
    // Store file ID globally for use in other functions
    currentFileId = fileId;
    
    isModalOpen = true;
    
    // Destroy any existing modal completely
    $('#filesModal').modal('hide').remove();
    $('.modal-backdrop').remove();
    $('body').removeClass('modal-open');
    
    fetch('/api/extract-files/' + fileId)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Erro extraindo arquivos: ' + data.error);
                isModalOpen = false;
                return;
            }
            
            // Create modal HTML dynamically to avoid conflicts
            var modalHtml = `
                <div class="modal fade" id="filesModal" tabindex="-1" role="dialog" aria-labelledby="filesModalLabel" aria-hidden="true" style="z-index: 9999;">
                    <div class="modal-dialog modal-lg" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                                <h4 class="modal-title" id="filesModalLabel">📁 Arquivos Extraídos</h4>
                            </div>
                            <div class="modal-body" id="filesModalBody" style="max-height: 60vh; overflow-y: auto;">
                                <!-- Content will be loaded here -->
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Add modal to body
            $('body').append(modalHtml);
            
            // Build content
            var modalBody = document.getElementById('filesModalBody');
            var html = '';
            
            for (var filename in data.files) {
                var file = data.files[filename];
                html += '<div class="panel panel-default" style="margin-bottom: 10px;">';
                html += '<div class="panel-heading"><strong>' + escapeHtml(filename) + '</strong> (' + file.type + ')</div>';
                html += '<div class="panel-body">';
                
                if (file.type === 'text') {
                    html += '<pre style="max-height: 200px; overflow-y: auto; white-space: pre-wrap;">' + escapeHtml(file.content) + '</pre>';
                } else if (file.type === 'binary') {
                    html += '<p>Arquivo binário, tamanho: ' + file.size + ' bytes</p>';
                    html += '<button class="btn btn-sm btn-primary" onclick="downloadFile(\'' + escapeHtml(filename) + '\', \'' + file.content + '\')">Baixar</button>';
                    
                    // Special handling for RenPy save files (log file)
                    if (filename.toLowerCase() === 'log' || filename.toLowerCase().includes('save')) {
                        html += ' <button class="btn btn-sm btn-success" onclick="editRenPyFile(\'' + escapeHtml(filename) + '\', currentFileId)">🎮 Editar Dados do Save</button>';
                    }
                } else if (file.type === 'hex') {
                    html += '<p>Visualização binária (primeiros 1000 bytes como hex):</p>';
                    html += '<code style="word-break: break-all; font-family: monospace;">' + file.content + '</code>';
                } else {
                    html += '<p class="text-danger">Erro: ' + escapeHtml(file.error) + '</p>';
                }
                
                html += '</div></div>';
            }
            
            modalBody.innerHTML = html;
            
            // Show modal with events
            $('#filesModal').on('hidden.bs.modal', function () {
                $(this).remove();
                $('.modal-backdrop').remove();
                $('body').removeClass('modal-open');
                isModalOpen = false;
            });
            
            $('#filesModal').modal({
                backdrop: 'static',
                keyboard: true,
                show: true
            });
        })
        .catch(error => {
            alert('Erro extraindo arquivos: ' + error);
            isModalOpen = false;
        });
};

window.viewScreenshot = function() {
    if (isModalOpen) return; // Prevent multiple calls
    
    var fileId = getFileIdFromUrl();
    if (!fileId) {
        alert('Erro: Não foi possível determinar o ID do arquivo');
        return;
    }
    
    isModalOpen = true;
    
    // Destroy any existing modal completely
    $('#screenshotModal').modal('hide').remove();
    $('.modal-backdrop').remove();
    $('body').removeClass('modal-open');
    
    fetch('/api/screenshot/' + fileId)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Erro carregando screenshot: ' + data.error);
                isModalOpen = false;
                return;
            }
            
            // Create modal HTML dynamically
            var modalHtml = `
                <div class="modal fade" id="screenshotModal" tabindex="-1" role="dialog" aria-labelledby="screenshotModalLabel" aria-hidden="true" style="z-index: 9999;">
                    <div class="modal-dialog modal-lg" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                                <h4 class="modal-title" id="screenshotModalLabel">🖼️ Screenshot do Save</h4>
                            </div>
                            <div class="modal-body text-center" id="screenshotModalBody">
                                <!-- Screenshot will be loaded here -->
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Add modal to body
            $('body').append(modalHtml);
            
            // Add screenshot
            var modalBody = document.getElementById('screenshotModalBody');
            modalBody.innerHTML = '<img src="data:' + data.mime_type + ';base64,' + data.data + '" class="img-responsive" style="max-width: 100%; height: auto; border-radius: 5px;">';
            
            // Show modal with events
            $('#screenshotModal').on('hidden.bs.modal', function () {
                $(this).remove();
                $('.modal-backdrop').remove();
                $('body').removeClass('modal-open');
                isModalOpen = false;
            });
            
            $('#screenshotModal').modal({
                backdrop: 'static',
                keyboard: true,
                show: true
            });
        })
        .catch(error => {
            alert('Erro carregando screenshot: ' + error);
            isModalOpen = false;
        });
};

window.editRenPyFile = function(filename, fileId) {
    console.log('🎮 Edit Save Data button clicked! Filename:', filename, 'FileId:', fileId);
    
    // Reset modal state to ensure we can proceed
    isModalOpen = false;
    
    // Force cleanup any existing modals
    $('#editModal').remove();
    $('.modal-backdrop').remove();
    $('body').removeClass('modal-open');
    
    if (isModalOpen) {
        console.log('Modal is already open, returning');
        return;
    }
    
    // Use provided fileId or try to get from URL
    if (!fileId) {
        fileId = getFileIdFromUrl();
        console.log('Got file ID from URL:', fileId);
    }
    
    if (!fileId) {
        alert('Erro: Não foi possível determinar o ID do arquivo');
        return;
    }
    
    isModalOpen = true;
    
    // Destroy any existing modal completely
    $('#editModal').modal('hide').remove();
    $('.modal-backdrop').remove();
    $('body').removeClass('modal-open');
    
    console.log('Creating loading modal...');
    
    // Create loading modal first
    var loadingModalHtml = `
        <div class="modal fade" id="editModal" tabindex="-1" role="dialog" style="z-index: 9999;">
            <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        <h4 class="modal-title">🎮 Editing RenPy Save: ${filename}</h4>
                    </div>
                    <div class="modal-body text-center">
                        <div class="alert alert-info">
                            <i class="glyphicon glyphicon-refresh glyphicon-spin"></i>
                            Decoding RenPy save file... Please wait.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    $('body').append(loadingModalHtml);
    $('#editModal').modal('show');
    
    console.log('Making API request to:', '/api/decode-renpy-file/' + fileId + '/' + encodeURIComponent(filename));
    
    // Fetch and decode the specific file
    fetch('/api/decode-renpy-file/' + fileId + '/' + encodeURIComponent(filename))
        .then(response => {
            console.log('API Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('API Response data:', data);
            if (data.error) {
                alert('Error decoding file: ' + data.error);
                $('#editModal').modal('hide');
                isModalOpen = false;
                return;
            }
            
            // Update modal with editor
            var editorHtml = `
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title">🎮 RenPy Save Editor: ${filename}</h4>
                </div>
                <div class="modal-body">
                    <div class="alert alert-warning">
                        <strong>⚠️ Warning:</strong> This is advanced editing. Make sure you understand what you're changing!
                    </div>
                    
                    <div class="panel-group" id="saveDataEditor">
                        ${generateSaveDataEditor(data)}
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" onclick="saveRenPyChanges('${filename}')">
                        💾 Save Changes
                    </button>
                    <button type="button" class="btn btn-info" onclick="exportRenPyData('${filename}')">
                        📤 Export as JSON
                    </button>
                    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                </div>
            `;
            
            document.getElementById('editModal').querySelector('.modal-content').innerHTML = editorHtml;
        })
        .catch(error => {
            console.error('Error in editRenPyFile:', error);
            alert('Error loading file: ' + error.message);
            $('#editModal').modal('hide');
            isModalOpen = false;
        });
    
    // Modal cleanup
    $('#editModal').on('hidden.bs.modal', function () {
        $(this).remove();
        $('.modal-backdrop').remove();
        $('body').removeClass('modal-open');
        isModalOpen = false;
    });
};

function generateSaveDataEditor(data) {
    var html = '';
    
    if (data.variables && Object.keys(data.variables).length > 0) {
        html += `
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" href="#variablesPanel">
                            🎲 Game Variables (${Object.keys(data.variables).length} items)
                        </a>
                    </h4>
                </div>
                <div id="variablesPanel" class="panel-collapse collapse in">
                    <div class="panel-body">
                        <div class="form-group">
                            <label>Search Variables:</label>
                            <input type="text" class="form-control" id="variableSearch" placeholder="Type to search..." onkeyup="filterVariables()">
                        </div>
                        <div id="variablesContainer" style="max-height: 400px; overflow-y: auto;">
        `;
        
        for (var key in data.variables) {
            var value = data.variables[key];
            var valueStr = typeof value === 'string' ? value : JSON.stringify(value);
            
            html += `
                <div class="variable-item form-group">
                    <label class="variable-name">${escapeHtml(key)}:</label>
                    <div class="input-group">
                        <input type="text" class="form-control variable-value" 
                               data-key="${escapeHtml(key)}" 
                               value="${escapeHtml(valueStr)}"
                               placeholder="Variable value">
                        <span class="input-group-addon">
                            <small class="text-muted">${typeof value}</small>
                        </span>
                    </div>
                </div>
            `;
        }
        
        html += `
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    if (data.metadata) {
        html += `
            <div class="panel panel-info">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" href="#metadataPanel">
                            📝 Save Metadata
                        </a>
                    </h4>
                </div>
                <div id="metadataPanel" class="panel-collapse collapse">
                    <div class="panel-body">
                        <pre>${escapeHtml(JSON.stringify(data.metadata, null, 2))}</pre>
                    </div>
                </div>
            </div>
        `;
    }
    
    if (data.raw_preview) {
        html += `
            <div class="panel panel-warning">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" href="#rawPanel">
                            🔧 Raw Data Preview
                        </a>
                    </h4>
                </div>
                <div id="rawPanel" class="panel-collapse collapse">
                    <div class="panel-body">
                        <small class="text-muted">First 2000 characters of raw data:</small>
                        <pre style="font-size: 11px;">${escapeHtml(data.raw_preview)}</pre>
                    </div>
                </div>
            </div>
        `;
    }
    
    return html;
}

window.filterVariables = function() {
    var searchTerm = document.getElementById('variableSearch').value.toLowerCase();
    var items = document.querySelectorAll('.variable-item');
    
    items.forEach(function(item) {
        var varName = item.querySelector('.variable-name').textContent.toLowerCase();
        var varValue = item.querySelector('.variable-value').value.toLowerCase();
        
        if (varName.includes(searchTerm) || varValue.includes(searchTerm)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
};

window.saveRenPyChanges = function(filename) {
    // Collect all changed variables
    var changes = {};
    var inputs = document.querySelectorAll('.variable-value');
    
    inputs.forEach(function(input) {
        var key = input.getAttribute('data-key');
        var value = input.value;
        
        // Try to parse as JSON, fallback to string
        try {
            changes[key] = JSON.parse(value);
        } catch (e) {
            changes[key] = value;
        }
    });
    
    var fileId = getFileIdFromUrl();
    
    fetch('/api/save-renpy-changes/' + fileId + '/' + encodeURIComponent(filename), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(changes)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Changes saved successfully!');
            $('#editModal').modal('hide');
        } else {
            alert('❌ Error saving changes: ' + data.error);
        }
    })
    .catch(error => {
        alert('❌ Error saving changes: ' + error);
    });
};

window.exportRenPyData = function(filename) {
    var fileId = getFileIdFromUrl();
    
    fetch('/api/decode-renpy-file/' + fileId + '/' + encodeURIComponent(filename))
        .then(response => response.json())
        .then(data => {
            var blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = filename + '_decoded.json';
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        })
        .catch(error => {
            alert('Error exporting data: ' + error);
        });
};

window.exportSaveData = function() {
    var saveData = document.querySelector('pre');
    if (saveData) {
        var dataContent = saveData.textContent;
        var blob = new Blob([dataContent], {type: 'application/json'});
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'renpy_save_data.json';
        a.click();
        URL.revokeObjectURL(url);
    } else {
        // If no pre element, get data via API
        var fileId = getFileIdFromUrl();
        if (fileId) {
            fetch('/api/save-data/' + fileId)
                .then(response => response.json())
                .then(data => {
                    var blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
                    var url = URL.createObjectURL(blob);
                    var a = document.createElement('a');
                    a.href = url;
                    a.download = 'renpy_save_data.json';
                    a.click();
                    URL.revokeObjectURL(url);
                })
                .catch(error => {
                    alert('Error exporting save data: ' + error);
                });
        }
    }
};

window.saveInfo = function() {
    var fileId = getFileIdFromUrl();
    if (!fileId) {
        alert('Error: Could not determine file ID');
        return;
    }
    
    fetch('/api/save-data/' + fileId)
        .then(response => response.json())
        .then(data => {
            var info = 'RenPy Save Information:\n\n';
            info += 'Files in archive: ' + data.analysis.file_count + '\n';
            info += 'Has screenshot: ' + (data.analysis.has_screenshot ? 'Yes' : 'No') + '\n';
            info += 'Has save data: ' + (data.analysis.has_save_data ? 'Yes' : 'No') + '\n';
            info += '\nFiles in archive:\n';
            data.analysis.files.forEach(function(file) {
                info += '• ' + file + '\n';
            });
            alert(info);
        })
        .catch(error => {
            alert('Error getting save info: ' + error);
        });
};

function getFileIdFromUrl() {
    // Extract file ID from current URL or from button attributes
    var buttons = document.querySelectorAll('button[onclick*="downloadOriginalFile"]');
    if (buttons.length > 0) {
        var onclick = buttons[0].getAttribute('onclick');
        var match = onclick.match(/downloadOriginalFile\('([^']+)'\)/);
        return match ? match[1] : null;
    }
    return null;
}

window.downloadFile = function(filename, base64Content) {
    try {
        var blob = new Blob([atob(base64Content)], {type: 'application/octet-stream'});
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        alert('Error downloading file: ' + error.message);
    }
};

// Utility function to escape HTML to prevent XSS
function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') {
        return unsafe;
    }
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Additional utility functions
window.validateJSON = function() {
    try {
        JSON.parse(document.getElementById('jsonData').value);
        alert('JSON is valid!');
    } catch (e) {
        alert('JSON is invalid: ' + e.message);
    }
};

window.countLines = function() {
    var content = document.getElementById('textData').value;
    var lines = content.split('\n').length;
    alert('Total lines: ' + lines);
};

window.countWords = function() {
    var content = document.getElementById('textData').value;
    var words = content.trim().split(/\s+/).length;
    alert('Total words: ' + words);
};

window.searchText = function() {
    var searchTerm = prompt('Enter search term:');
    if (searchTerm) {
        var content = document.getElementById('textData').value;
        var matches = (content.match(new RegExp(searchTerm, 'gi')) || []).length;
        alert('Found ' + matches + ' occurrences of "' + searchTerm + '"');
    }
};

// RenPy Editor specific functions
window.searchInSave = function() {
    var searchTerm = prompt('Enter search term:');
    if (searchTerm) {
        var dataStr = document.querySelector('pre').textContent;
        var matches = (dataStr.match(new RegExp(searchTerm, 'gi')) || []).length;
        alert('Found ' + matches + ' occurrences of "' + searchTerm + '"');
    }
};

window.showSaveInfo = function() {
    // Extract basic info from the data
    alert('This feature would show save metadata like date, version, etc.');
};

window.exportAsJSON = function() {
    var dataContent = document.querySelector('pre').textContent;
    var blob = new Blob([dataContent], {type: 'application/json'});
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'save_data.json';
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};

console.log('RenPy Tools JavaScript loaded successfully');

// RenPy Save Editor Tools - Enhanced by Delean Mafra
// For advanced RenPy save file analysis and variable editing
