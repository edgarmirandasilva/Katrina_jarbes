"""
File Operations Skill - Read and write files
"""

import os
from typing import Dict, Any
from .base_skill import Skill


class FileOperationsSkill(Skill):
    """Perform file operations like read, write, list"""
    
    def __init__(self, allowed_dir: str = "./workspace"):
        super().__init__()
        self.description = "Read, write, or list files in the workspace"
        self.allowed_dir = os.path.abspath(allowed_dir)
        os.makedirs(self.allowed_dir, exist_ok=True)
        
        self.parameters = {
            'type': 'object',
            'properties': {
                'operation': {
                    'type': 'string',
                    'enum': ['read', 'write', 'list'],
                    'description': 'Operation to perform: read, write, or list'
                },
                'filename': {
                    'type': 'string',
                    'description': 'Name of the file (for read/write operations)'
                },
                'content': {
                    'type': 'string',
                    'description': 'Content to write (only for write operation)'
                }
            },
            'required': ['operation']
        }
    
    def execute(self, operation: str, filename: str = None, content: str = None, **kwargs) -> Dict[str, Any]:
        """Execute file operation"""
        try:
            if operation == 'list':
                return self._list_files()
            elif operation == 'read':
                if not filename:
                    return {'success': False, 'error': 'filename required for read'}
                return self._read_file(filename)
            elif operation == 'write':
                if not filename or content is None:
                    return {'success': False, 'error': 'filename and content required for write'}
                return self._write_file(filename, content)
            else:
                return {'success': False, 'error': f'Unknown operation: {operation}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the skill schema"""
        return {
            'name': 'file_operations',
            'description': self.description,
            'parameters': self.parameters
        }
    
    def _get_safe_path(self, filename: str) -> str:
        """Get safe file path within allowed directory"""
        path = os.path.abspath(os.path.join(self.allowed_dir, filename))
        if not path.startswith(self.allowed_dir):
            raise ValueError("Access denied: path outside workspace")
        return path
    
    def _list_files(self) -> Dict[str, Any]:
        """List files in workspace"""
        files = os.listdir(self.allowed_dir)
        return {
            'success': True,
            'files': files,
            'directory': self.allowed_dir
        }
    
    def _read_file(self, filename: str) -> Dict[str, Any]:
        """Read file content"""
        path = self._get_safe_path(filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {
            'success': True,
            'filename': filename,
            'content': content
        }
    
    def _write_file(self, filename: str, content: str) -> Dict[str, Any]:
        """Write content to file"""
        path = self._get_safe_path(filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {
            'success': True,
            'filename': filename,
            'message': f'File written successfully to {filename}'
        }
