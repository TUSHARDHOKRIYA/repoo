import json
import ast
from pathlib import Path
import sys

# Standard library modules (don't need to be added)
STD_LIB_MODULES = {
    'json', 'os', 'sys', 'math', 'time', 'datetime', 're', 'pathlib',
    'collections', 'itertools', 'functools', 'typing', 'warnings',
    'copy', 'random', 'statistics', 'decimal', 'fractions', 'hashlib',
    'string', 'csv', 'pickle', 'pprint', 'textwrap', 'unicodedata',
    'inspect', 'enum', 'argparse', 'getpass', 'platform', 'subprocess',
    'multiprocessing', 'threading', 'queue', 'contextlib', 'abc'
}

# Already in base dependencies (check pyproject.toml)
BASE_DEPS = {
    'numpy', 'pandas', 'scipy', 'sklearn', 'scikit-learn',  # sklearn is scikit-learn
    'deprecated', 'numba', 'packaging', 'typing_extensions'
}

def extract_imports_from_code(code):
    """Extract imported modules from Python code using AST."""
    imports = set()
    
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:  # module can be None for "from . import x"
                    imports.add(node.module.split('.')[0])
    except SyntaxError:
        # Fallback to regex for notebooks with IPython magic
        import re
        patterns = [
            r'^\s*import\s+([\w\.]+(?:,\s*[\w\.]+)*)',
            r'^\s*from\s+([\w\.]+)\s+import'
        ]
        for line in code.split('\n'):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    modules = match.group(1)
                    for module in modules.split(','):
                        module = module.strip().split('.')[0]
                        if module:
                            imports.add(module)
    
    return imports

def main():
    notebook_dir = Path('examples')
    notebooks = list(notebook_dir.rglob('*.ipynb'))
    
    all_imports = set()
    notebook_imports = {}
    
    for notebook_path in sorted(notebooks):
        notebook_name = notebook_path.relative_to(notebook_dir)
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb_content = json.load(f)
            
            notebook_imports[notebook_name] = set()
            
            for cell in nb_content.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    cell_imports = extract_imports_from_code(source)
                    
                    # Filter out IPython magics and built-ins
                    cell_imports = {imp for imp in cell_imports 
                                   if not imp.startswith('IPython') 
                                   and not imp.startswith('!') 
                                   and imp not in STD_LIB_MODULES}
                    
                    notebook_imports[notebook_name].update(cell_imports)
                    all_imports.update(cell_imports)
                    
        except Exception as e:
            print(f'Error processing {notebook_path}: {e}', file=sys.stderr)
    
    # Filter out base dependencies
    needs_installation = all_imports - BASE_DEPS
    
    # Save detailed report
    with open('import_analysis.txt', 'w') as f:
        f.write("=== IMPORT ANALYSIS REPORT ===\n\n")
        f.write(f"Total notebooks analyzed: {len(notebooks)}\n")
        f.write(f"Total unique imports found: {len(all_imports)}\n")
        f.write(f"Packages needing installation: {len(needs_installation)}\n\n")
        
        f.write("=== PACKAGES NEEDED FOR BINDER ===\n")
        for package in sorted(needs_installation):
            f.write(f"- {package}\n")
        
        f.write("\n=== BREAKDOWN BY NOTEBOOK ===\n")
        for notebook, imports in sorted(notebook_imports.items()):
            if imports:
                f.write(f"\n{notebook}:\n")
                for imp in sorted(imports - BASE_DEPS):
                    f.write(f"  - {imp}\n")
    
    # Print summary to console
    print(f"\n📊 ANALYSIS COMPLETE")
    print(f"Notebooks analyzed: {len(notebooks)}")
    print(f"Unique imports: {len(all_imports)}")
    print(f"Packages needed for binder: {len(needs_installation)}")
    print("\n📦 PACKAGES TO ADD TO BINDER LIST:")
    for package in sorted(needs_installation):
        print(f"  {package}")
    
    print("\n📄 Full report saved to: import_analysis.txt")

if __name__ == '__main__':
    main()
