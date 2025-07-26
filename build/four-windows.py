# Four Programming Language Interpreter - Windows Complete Version
# A programming language made with love ❤️
# Optimized for Windows with enhanced features

import sys
import os
import re
import json
import tempfile
import subprocess
import shutil
import zipfile
import platform
import time
import hashlib
from pathlib import Path
from datetime import datetime

class FourError(Exception):
    """Four errors with love"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class WindowsConsole:
    """Windows-specific console utilities"""
    
    @staticmethod
    def enable_colors():
        """Enable ANSI colors on Windows"""
        if platform.system() == 'Windows':
            try:
                import colorama
                colorama.init()
            except ImportError:
                # Fallback: try to enable ANSI directly
                try:
                    import ctypes
                    kernel32 = ctypes.windll.kernel32
                    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                except:
                    pass
    
    @staticmethod
    def print_colored(text, color='white'):
        """Print colored text"""
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'reset': '\033[0m'
        }
        print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

class FourInterpreter:
    def __init__(self):
        self.project_name = None
        self.config = {
            'platform': None,
            'run': None,
            'readme': 'Welcome to my app made with Love! ❤️',
            'version': '1.0',
            'author': 'Unknown',
            'description': '',
            'icon': None,
            'dependencies': [],
            'build_time': None
        }
        self.exports = {}
        self.main_code = ""
        self.project_declared = False
        self.in_define = False
        self.folders = []
        self.files = []
        self.console = WindowsConsole()
        
        # Windows-specific paths
        self.windows_paths = {
            'temp': os.environ.get('TEMP', 'C:\\temp'),
            'appdata': os.environ.get('APPDATA', ''),
            'programfiles': os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
            'userprofile': os.environ.get('USERPROFILE', 'C:\\Users\\Default')
        }
        
        # Enable console colors
        self.console.enable_colors()

    def get_current_platform(self):
        """Get current platform with Windows-specific detection"""
        system = platform.system().lower()
        if system == 'windows':
            # Detect Windows version
            version = platform.version()
            release = platform.release()
            return f"windows-{release.lower()}"
        return 'linux' if system in ('linux', 'darwin') else 'windows'

    def validate_windows_compatibility(self, command):
        """Validate if command is Windows-compatible"""
        windows_commands = ['python', 'python3', 'node', 'java', 'dotnet', 'powershell', 'cmd']
        base_cmd = command.split()[0].lower()
        
        # Remove .exe extension if present
        if base_cmd.endswith('.exe'):
            base_cmd = base_cmd[:-4]
            
        return base_cmd in windows_commands or os.path.exists(base_cmd)

    def parse_line(self, line):
        """Parse individual line with Windows-specific enhancements"""
        if self.in_define:
            self.main_code += line + "\n"
            return

        line = line.strip()
        if not line or line.startswith('->'):
            return

        if line.startswith('PROJECT'):
            if self.project_declared:
                raise FourError("Error with love: PROJECT can only be declared once ❤️")
            match = re.match(r'PROJECT\s+"([^"]+)"', line)
            if match:
                self.project_name = match.group(1)
                # Sanitize project name for Windows
                self.project_name = re.sub(r'[<>:"/\\|?*]', '_', self.project_name)
                self.project_declared = True
            else:
                raise FourError("Error with love: Incorrect syntax in PROJECT ❤️")

        elif line.startswith('CONFIGURE'):
            match = re.match(r'CONFIGURE\["([^"]+)",\s*"([^"]+)"\]', line)
            if match:
                key, value = match.groups()
                if key == 'readme' and value in self.exports:
                    self.config[key] = self.exports[value]
                elif key == 'run':
                    # Validate Windows compatibility
                    if not self.validate_windows_compatibility(value):
                        self.console.print_colored(f"Warning: Command '{value}' might not be Windows-compatible", 'yellow')
                    self.config[key] = value
                else:
                    self.config[key] = value
            else:
                raise FourError("Error with love: Incorrect syntax in CONFIGURE ❤️")

        elif line.startswith('EXPORT'):
            self._parse_export(line)

        elif line.startswith('FOLDER'):
            match = re.match(r'FOLDER\s+"([^"]+)"', line)
            if match:
                folder_name = match.group(1)
                # Convert to Windows path format
                folder_name = folder_name.replace('/', '\\')
                self.folders.append(folder_name)
            else:
                raise FourError("Error with love: Incorrect syntax in FOLDER ❤️")

        elif line.startswith('FILE'):
            match = re.match(r'FILE\s+"([^"]+)"\s+"([^"]+)"', line)
            if match:
                src, dest = match.groups()
                # Convert to Windows path format
                src = src.replace('/', '\\')
                dest = dest.replace('/', '\\')
                self.files.append((src, dest))
            else:
                raise FourError("Error with love: Incorrect syntax in FILE ❤️")

        elif line.startswith('DEFINE'):
            match = re.match(r'DEFINE\s+(\w+)', line)
            if match:
                self.in_define = True
            else:
                raise FourError("Error with love: Incorrect syntax in DEFINE ❤️")

    def _parse_export(self, line):
        """Parse EXPORT statements with enhanced type support"""
        if 'string[' in line:
            match = re.match(r'EXPORT\s+(\w+)\["([^"]+)"\]', line)
            if match:
                var_name, value = match.groups()
                self.exports[var_name] = value
            else:
                raise FourError("Error with love: Incorrect syntax in EXPORT string ❤️")
        elif 'numero[' in line:
            match = re.match(r'EXPORT\s+(\w+)\[(\d+)\]', line)
            if match:
                var_name, value = match.groups()
                self.exports[var_name] = int(value)
            else:
                raise FourError("Error with love: Incorrect syntax in EXPORT numero ❤️")
        elif 'float[' in line:
            match = re.match(r'EXPORT\s+(\w+)\[(\d+\.?\d*)\]', line)
            if match:
                var_name, value = match.groups()
                self.exports[var_name] = float(value)
            else:
                raise FourError("Error with love: Incorrect syntax in EXPORT float ❤️")
        elif 'bool[' in line:
            match = re.match(r'EXPORT\s+(\w+)\[(true|false)\]', line)
            if match:
                var_name, value = match.groups()
                self.exports[var_name] = value.lower() == 'true'
            else:
                raise FourError("Error with love: Incorrect syntax in EXPORT bool ❤️")
        else:
            match = re.match(r'EXPORT\s+(\w+)\["', line)
            if match:
                var_name = match.group(1)
                self.exports[var_name] = ""

    def parse_multiline_export(self, lines, start_idx):
        """Parse multiline EXPORT with Windows line endings support"""
        line = lines[start_idx].strip()
        match = re.match(r'EXPORT\s+(\w+)\["', line)
        if not match:
            return start_idx

        var_name = match.group(1)
        content = ""
        i = start_idx
        first_line_content = line[line.find('["') + 2:]
        
        if first_line_content.endswith('"]'):
            content = first_line_content[:-2]
            self.exports[var_name] = content
            return i + 1
            
        content = first_line_content + "\n"
        i += 1
        
        while i < len(lines):
            current_line = lines[i].rstrip('\r\n')  # Handle Windows line endings
            if current_line.endswith('"]'):
                content += current_line[:-2]
                break
            else:
                content += current_line + "\n"
            i += 1
            
        self.exports[var_name] = content
        return i + 1

    def parse_file(self, filename):
        """Parse .four file with enhanced error handling"""
        try:
            # Try different encodings for Windows compatibility
            encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'iso-8859-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(filename, 'r', encoding=encoding) as f:
                        content = f.readlines()
                    break
                except UnicodeDecodeError:
                    continue
                    
            if content is None:
                raise FourError(f"Error with love: Could not decode file {filename} ❤️")
                
            lines = content
            i = 0
            
            while i < len(lines):
                original_line = lines[i].rstrip('\n\r')
                line = original_line.strip()
                
                if not self.in_define and (not line or line.startswith('->')):
                    i += 1
                    continue
                    
                if not self.in_define and line.startswith('EXPORT') and '["' in line and not (line.count('"') >= 2 and line.endswith('"]')):
                    i = self.parse_multiline_export(lines, i)
                    continue
                    
                if self.in_define:
                    self.parse_line(original_line)
                else:
                    self.parse_line(line)
                i += 1
                
        except FileNotFoundError:
            raise FourError(f"Error with love: File {filename} not found ❤️")
        except Exception as e:
            raise FourError(f"Error with love: {str(e)} ❤️")

    def validate(self):
        """Validate project configuration with Windows-specific checks"""
        if not self.project_name:
            raise FourError("Error with love: Missing PROJECT declaration ❤️")
        if not self.config['platform']:
            raise FourError("Error with love: Missing mandatory 'platform' configuration ❤️")
        if not self.config['run']:
            raise FourError("Error with love: Missing mandatory 'run' configuration ❤️")
        if not self.main_code.strip():
            raise FourError("Error with love: Missing mandatory DEFINE ❤️")
            
        valid_platforms = ['linux', 'windows', 'windows-10', 'windows-11', 'all']
        if self.config['platform'] not in valid_platforms:
            raise FourError(f"Error with love: Platform '{self.config['platform']}' is not valid. Use: {', '.join(valid_platforms)} ❤️")

    def create_windows_executable_wrapper(self, temp_dir):
        """Create a Windows batch file wrapper"""
        wrapper_content = f"""@echo off
cd /d "%~dp0"
{self.config['run']} code.four-code
pause
"""
        wrapper_path = os.path.join(temp_dir, 'run.bat')
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
        return 'run.bat'

    def build(self, output_file):
        """Build project with Windows-specific enhancements"""
        self.validate()
        
        self.console.print_colored("Building Binary with love.. ❤️", 'cyan')
        start_time = time.time()
        
        with tempfile.TemporaryDirectory(dir=self.windows_paths['temp']) as temp_dir:
            # Enhanced settings
            settings_data = {
                'project': self.project_name,
                'platform': self.config['platform'],
                'run': self.config['run'],
                'readme': self.config['readme'],
                'version': self.config['version'],
                'author': self.config.get('author', 'Unknown'),
                'description': self.config.get('description', ''),
                'build_time': datetime.now().isoformat(),
                'build_platform': self.get_current_platform(),
                'checksum': None  # Will be calculated later
            }
            
            # Create settings.json
            settings_file = os.path.join(temp_dir, 'settings.json')
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)
            
            # Create code file
            code_file = os.path.join(temp_dir, 'code.four-code')
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(self.main_code)
            
            # Create Windows wrapper if needed
            if platform.system() == 'Windows' and self.config['platform'].startswith('windows'):
                wrapper_file = self.create_windows_executable_wrapper(temp_dir)
                settings_data['wrapper'] = wrapper_file
            
            # Copy folders and files
            for folder in self.folders:
                folder_path = os.path.join(temp_dir, folder)
                os.makedirs(folder_path, exist_ok=True)
                self.console.print_colored(f"Created folder: {folder}", 'green')
            
            for src, dest in self.files:
                if os.path.exists(src):
                    dest_path = os.path.join(temp_dir, dest)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(src, dest_path)
                    self.console.print_colored(f"Copied: {src} -> {dest}", 'green')
                else:
                    self.console.print_colored(f"Warning: Source file not found: {src}", 'yellow')
            
            # Calculate checksum
            checksum = hashlib.md5()
            checksum.update(self.main_code.encode('utf-8'))
            settings_data['checksum'] = checksum.hexdigest()
            
            # Update settings with checksum
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)
            
            # Create .app file
            with open(output_file, 'wb') as app_file:
                app_file.write(b'LOVE-APP-WIN')  # Windows-specific header
                
                import io
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                    # Add all files from temp directory
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(full_path, temp_dir)
                            zipf.write(full_path, rel_path)
                
                zip_buffer.seek(0)
                app_file.write(zip_buffer.read())
        
        build_time = time.time() - start_time
        self.console.print_colored(f"Done! Built in {build_time:.2f} seconds ❤️", 'green')
        self.console.print_colored(f"Output: {output_file}", 'magenta')

    def run_app(self, app_file):
        """Run application with Windows-specific enhancements"""
        try:
            self.console.print_colored(f"Running {app_file} with love.. ❤️", 'cyan')
            
            with open(app_file, 'rb') as f:
                header = f.read(12)  # Read longer header
                if not (header.startswith(b'LOVE-APP') or header.startswith(b'LOVE-APP-WIN')):
                    raise FourError("Error with love: Invalid .app file (incorrect header) ❤️")
                
                # Adjust for different header lengths
                if header.startswith(b'LOVE-APP-WIN'):
                    f.seek(12)
                else:
                    f.seek(8)
                
                zip_content = f.read()
            
            with tempfile.TemporaryDirectory(dir=self.windows_paths['temp']) as temp_dir:
                zip_path = os.path.join(temp_dir, 'temp.zip')
                with open(zip_path, 'wb') as zip_file:
                    zip_file.write(zip_content)
                
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    zipf.extractall(temp_dir)
                
                # Load settings
                settings_file = os.path.join(temp_dir, 'settings.json')
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Platform compatibility check
                app_platform = settings.get('platform', 'all')
                current_platform = self.get_current_platform()
                
                if app_platform != 'all' and not app_platform.startswith('windows') and current_platform.startswith('windows'):
                    if app_platform != current_platform:
                        raise FourError(f"Error with love: This application is for {app_platform}, but you're on {current_platform} ❤️")
                
                # Show app info
                self.console.print_colored(f"Project: {settings.get('project', 'Unknown')}", 'blue')
                self.console.print_colored(f"Version: {settings.get('version', '1.0')}", 'blue')
                if settings.get('author'):
                    self.console.print_colored(f"Author: {settings['author']}", 'blue')
                print()
                
                # Run the application
                run_command = settings['run'].split()
                
                # Use wrapper if available
                if 'wrapper' in settings and os.path.exists(os.path.join(temp_dir, settings['wrapper'])):
                    if platform.system() == 'Windows':
                        result = subprocess.run([settings['wrapper']], 
                                              capture_output=False, 
                                              cwd=temp_dir,
                                              shell=True)
                        return result.returncode
                
                # Standard execution
                run_command.append('code.four-code')
                result = subprocess.run(run_command, 
                                      capture_output=True, 
                                      text=True, 
                                      cwd=temp_dir,
                                      shell=True if platform.system() == 'Windows' else False)
                
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    print(result.stderr, end='', file=sys.stderr)
                
                return result.returncode
                
        except FileNotFoundError:
            raise FourError(f"Error with love: File {app_file} not found ❤️")
        except zipfile.BadZipFile:
            raise FourError("Error with love: Corrupted .app file ❤️")
        except json.JSONDecodeError:
            raise FourError("Error with love: Corrupted .app configuration ❤️")

    def show_info(self, app_file):
        """Show detailed information about a .app file"""
        try:
            with open(app_file, 'rb') as f:
                header = f.read(12)
                if not (header.startswith(b'LOVE-APP') or header.startswith(b'LOVE-APP-WIN')):
                    raise FourError("Error with love: Invalid .app file ❤️")
                
                if header.startswith(b'LOVE-APP-WIN'):
                    f.seek(12)
                else:
                    f.seek(8)
                
                zip_content = f.read()
            
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, 'temp.zip')
                with open(zip_path, 'wb') as zip_file:
                    zip_file.write(zip_content)
                
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    zipf.extractall(temp_dir)
                
                settings_file = os.path.join(temp_dir, 'settings.json')
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Display information
                self.console.print_colored("═" * 50, 'cyan')
                self.console.print_colored("Four Application Information ❤️", 'cyan')
                self.console.print_colored("═" * 50, 'cyan')
                
                self.console.print_colored(f"Project: {settings.get('project', 'Unknown')}", 'white')
                self.console.print_colored(f"Version: {settings.get('version', '1.0')}", 'white')
                self.console.print_colored(f"Platform: {settings.get('platform', 'Unknown')}", 'white')
                self.console.print_colored(f"Run Command: {settings.get('run', 'Unknown')}", 'white')
                
                if settings.get('author'):
                    self.console.print_colored(f"Author: {settings['author']}", 'white')
                if settings.get('description'):
                    self.console.print_colored(f"Description: {settings['description']}", 'white')
                if settings.get('build_time'):
                    self.console.print_colored(f"Build Time: {settings['build_time'][:19]}", 'white')
                if settings.get('checksum'):
                    self.console.print_colored(f"Checksum: {settings['checksum']}", 'white')
                
                self.console.print_colored("═" * 50, 'cyan')
                
                # Show contents
                print("\nContents:")
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    for file_info in zipf.filelist:
                        size = file_info.file_size
                        print(f"  {file_info.filename} ({size} bytes)")
                
        except Exception as e:
            raise FourError(f"Error with love: {str(e)} ❤️")

def main():
    if len(sys.argv) < 2:
        print("Four Programming Language - Windows Complete Version")
        print("Made with love ❤️")
        print()
        print("Usage:")
        print("  four build <file.four>       - Compile project")
        print("  four run <file.app>          - Execute application")
        print("  four info <file.app>         - Show application info")
        print("  four version                 - Show version")
        print("  four help                    - Show this help")
        return

    command = sys.argv[1].lower()

    try:
        if command in ("-v", "--version", "version"):
            print("Four Programming Language v2.0 (Windows Complete)")
            print("Made with love ❤️")
            print(f"Running on: {platform.system()} {platform.release()}")
            return

        elif command in ("-h", "--help", "help"):
            print("Four Programming Language - Complete Help")
            print("Made with love ❤️")
            print()
            print("Commands:")
            print("  build <file.four>    - Compile a .four project into a .app file")
            print("  run <file.app>       - Execute a compiled .app application")
            print("  info <file.app>      - Display detailed information about a .app file")
            print("  version              - Show version information")
            print("  help                 - Show this help message")
            print()
            print("File Extensions:")
            print("  .four               - Four source code files")
            print("  .app                - Compiled Four applications")
            print()
            print("Examples:")
            print("  four build myproject.four")
            print("  four run myproject.app")
            print("  four info myproject.app")
            return

        elif command == "build":
            if len(sys.argv) != 3:
                print("Error with love: Usage: four build <file.four> ❤️")
                return
            four_file = sys.argv[2]
            if not four_file.endswith('.four'):
                print("Error with love: File must have .four extension ❤️")
                return
            interpreter = FourInterpreter()
            interpreter.parse_file(four_file)
            app_file = f"{interpreter.project_name}.app"
            interpreter.build(app_file)

        elif command == "run":
            if len(sys.argv) != 3:
                print("Error with love: Usage: four run <file.app> ❤️")
                return
            app_file = sys.argv[2]
            if not app_file.endswith('.app'):
                print("Error with love: File must have .app extension ❤️")
                return
            interpreter = FourInterpreter()
            exit_code = interpreter.run_app(app_file)
            sys.exit(exit_code)

        elif command == "info":
            if len(sys.argv) != 3:
                print("Error with love: Usage: four info <file.app> ❤️")
                return
            app_file = sys.argv[2]
            if not app_file.endswith('.app'):
                print("Error with love: File must have .app extension ❤️")
                return
            interpreter = FourInterpreter()
            interpreter.show_info(app_file)

        else:
            print(f"Error with love: Command '{command}' not recognized ❤️")
            print("Use 'four help' for available commands")

    except FourError as e:
        WindowsConsole.print_colored(str(e), 'red')
        sys.exit(1)
    except KeyboardInterrupt:
        WindowsConsole.print_colored("\nOperation cancelled with love ❤️", 'yellow')
        sys.exit(1)
    except Exception as e:
        WindowsConsole.print_colored(f"Unexpected error with love: {str(e)} ❤️", 'red')
        sys.exit(1)

if __name__ == "__main__":
    main()
