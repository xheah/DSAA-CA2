"""
UML Class Diagram Generator for DASK Expression Evaluator Project
Generates a class diagram using graphviz (included in Anaconda)

Usage: python class_diagram.py
Output: class_diagram.png
"""

import ast
import os
from pathlib import Path

try:
    from graphviz import Digraph
except ImportError:
    print("graphviz not found. Install with: pip install graphviz")
    print("You also need Graphviz binaries: conda install graphviz")
    exit(1)


def get_python_files(root_dir: str, exclude_dirs: set = None) -> list:
    """Get all Python files in the project, excluding test files."""
    if exclude_dirs is None:
        exclude_dirs = {'__pycache__', '.git', 'venv', 'tests'}
    
    python_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        
        for filename in filenames:
            if filename.endswith('.py') and not filename.startswith('test_'):
                python_files.append(os.path.join(dirpath, filename))
    
    return python_files


def extract_class_info(filepath: str) -> list:
    """Extract class information from a Python file using AST."""
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return []
    
    classes = []
    module_name = Path(filepath).stem
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_info = {
                'name': node.name,
                'module': module_name,
                'filepath': filepath,
                'bases': [],
                'methods': [],
                'attributes': []
            }
            
            # Extract base classes
            for base in node.bases:
                if isinstance(base, ast.Name):
                    class_info['bases'].append(base.id)
                elif isinstance(base, ast.Attribute):
                    class_info['bases'].append(base.attr)
            
            # Extract methods and attributes
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    # Determine visibility
                    if item.name.startswith('__') and not item.name.endswith('__'):
                        visibility = '-'  # private
                    elif item.name.startswith('_'):
                        visibility = '#'  # protected
                    else:
                        visibility = '+'  # public
                    
                    # Get parameters
                    params = []
                    for arg in item.args.args:
                        if arg.arg != 'self':
                            params.append(arg.arg)
                    
                    method_str = f"{visibility} {item.name}({', '.join(params)})"
                    class_info['methods'].append(method_str)
                    
                elif isinstance(item, ast.Assign):
                    # Class-level attributes
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            visibility = '-' if target.id.startswith('_') else '+'
                            class_info['attributes'].append(f"{visibility} {target.id}")
            
            # Extract instance attributes from __init__
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                    for stmt in ast.walk(item):
                        if isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                                    if target.value.id == 'self':
                                        attr_name = target.attr
                                        visibility = '-' if attr_name.startswith('_') else '+'
                                        attr_str = f"{visibility} {attr_name}"
                                        if attr_str not in class_info['attributes']:
                                            class_info['attributes'].append(attr_str)
            
            classes.append(class_info)
    
    return classes


def create_uml_diagram(classes: list, output_file: str = 'class_diagram'):
    """Create a UML class diagram using graphviz."""
    dot = Digraph(comment='DASK Expression Evaluator - Class Diagram')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.5', ranksep='1.0')
    dot.attr('node', shape='record', fontname='Helvetica', fontsize='10')
    dot.attr('edge', fontname='Helvetica', fontsize='9')
    
    # Group classes by package/module
    packages = {}
    for cls in classes:
        # Determine package from filepath
        filepath = Path(cls['filepath'])
        parts = filepath.parts
        
        # Find package name
        if 'dask_core' in parts:
            if 'data_structures' in parts:
                package = 'dask_core.data_structures'
            else:
                package = 'dask_core'
        elif 'features' in parts:
            package = 'features'
        elif 'io_utils' in parts:
            package = 'io_utils'
        elif 'ui' in parts:
            package = 'ui'
        else:
            package = 'root'
        
        if package not in packages:
            packages[package] = []
        packages[package].append(cls)
    
    # Create subgraphs for each package
    for package, pkg_classes in packages.items():
        with dot.subgraph(name=f'cluster_{package.replace(".", "_")}') as sub:
            sub.attr(label=package, style='rounded', color='gray')
            
            for cls in pkg_classes:
                # Build the label for the class node
                name = cls['name']
                
                # Attributes section (limit to first 5)
                attrs = cls['attributes'][:5]
                if len(cls['attributes']) > 5:
                    attrs.append('...')
                attrs_str = '\\l'.join(attrs) + '\\l' if attrs else ''
                
                # Methods section (limit to first 8)
                methods = cls['methods'][:8]
                if len(cls['methods']) > 8:
                    methods.append('...')
                methods_str = '\\l'.join(methods) + '\\l' if methods else ''
                
                # Create UML-style label
                label = f"{{{name}|{attrs_str}|{methods_str}}}"
                
                sub.node(name, label=label)
    
    # Track which classes exist in our diagram
    class_names = {cls['name'] for cls in classes}
    
    # Add inheritance relationships
    for cls in classes:
        for base in cls['bases']:
            if base in class_names:
                dot.edge(base, cls['name'], arrowhead='empty', style='solid')
    
    # Add composition/association relationships based on type hints and attributes
    associations = [
        ('ExpressionManager', 'ExpressionParser', 'has'),
        ('ExpressionManager', 'DaskExpression', 'manages'),
        ('DaskExpression', 'ParseTree', 'has'),
        ('ParseTree', 'TreeNode', 'has'),
        ('ParseTree', 'Evaluator', 'uses'),
        ('ExpressionParser', 'Stack', 'uses'),
        ('ExpressionParser', 'ParseTree', 'creates'),
        ('Evaluator', 'Operator', 'uses'),
        ('Menu', 'ExpressionManager', 'has'),
        ('Menu', 'FileHandler', 'uses'),
        ('Menu', 'CostAnalyser', 'uses'),
        ('Menu', 'History', 'uses'),
        ('CostAnalyser', 'ParseTree', 'analyses'),
        ('Differentiator', 'ParseTree', 'creates'),
    ]
    
    for source, target, label in associations:
        if source in class_names and target in class_names:
            dot.edge(source, target, label=label, style='dashed', arrowhead='vee')
    
    # Render the diagram
    dot.render(output_file, format='png', cleanup=True)
    print(f"Class diagram saved to {output_file}.png")
    
    # Also save as SVG for better quality
    dot.render(output_file, format='svg', cleanup=True)
    print(f"Class diagram saved to {output_file}.svg")
    
    return dot


def main():
    # Get project root (where this script is located)
    project_root = Path(__file__).parent
    
    print("Scanning project for Python files...")
    python_files = get_python_files(str(project_root))
    
    print(f"Found {len(python_files)} Python files")
    
    # Extract class information
    all_classes = []
    for filepath in python_files:
        classes = extract_class_info(filepath)
        all_classes.extend(classes)
        if classes:
            print(f"  {filepath}: {[c['name'] for c in classes]}")
    
    print(f"\nFound {len(all_classes)} classes total")
    
    # Filter out operator subclasses for cleaner diagram (keep base Operator)
    operator_subclasses = {'AddOperator', 'SubOperator', 'MulOperator', 
                          'DivOperator', 'SumOperator', 'DivSumOperator', 'PowOperator'}
    filtered_classes = [c for c in all_classes if c['name'] not in operator_subclasses]
    
    print(f"Generating diagram with {len(filtered_classes)} main classes...")
    print("(Operator subclasses grouped under base Operator class)")
    
    # Create the diagram
    dot = create_uml_diagram(filtered_classes)
    
    # Also generate PlantUML code for alternative rendering
    print("\nGenerating PlantUML code...")
    generate_plantuml(filtered_classes)


def generate_plantuml(classes: list):
    """Generate PlantUML code as an alternative."""
    lines = ['@startuml', 'skinparam classAttributeIconSize 0', '']
    
    # Group by package
    packages = {}
    for cls in classes:
        filepath = Path(cls['filepath'])
        parts = filepath.parts
        
        if 'dask_core' in parts:
            if 'data_structures' in parts:
                package = 'dask_core.data_structures'
            else:
                package = 'dask_core'
        elif 'features' in parts:
            package = 'features'
        elif 'io_utils' in parts:
            package = 'io_utils'
        elif 'ui' in parts:
            package = 'ui'
        else:
            package = 'root'
        
        if package not in packages:
            packages[package] = []
        packages[package].append(cls)
    
    for package, pkg_classes in packages.items():
        lines.append(f'package "{package}" {{')
        for cls in pkg_classes:
            lines.append(f'  class {cls["name"]} {{')
            for attr in cls['attributes'][:5]:
                lines.append(f'    {attr}')
            for method in cls['methods'][:6]:
                lines.append(f'    {method}')
            lines.append('  }')
        lines.append('}')
        lines.append('')
    
    # Inheritance
    class_names = {c['name'] for c in classes}
    for cls in classes:
        for base in cls['bases']:
            if base in class_names:
                lines.append(f'{base} <|-- {cls["name"]}')
    
    lines.append('')
    lines.append("' Associations")
    associations = [
        ('ExpressionManager', 'DaskExpression', '*--'),
        ('DaskExpression', 'ParseTree', 'o--'),
        ('ParseTree', 'TreeNode', 'o--'),
        ('Menu', 'ExpressionManager', 'o--'),
    ]
    for source, target, arrow in associations:
        if source in class_names and target in class_names:
            lines.append(f'{source} {arrow} {target}')
    
    lines.append('@enduml')
    
    with open('class_diagram.puml', 'w') as f:
        f.write('\n'.join(lines))
    
    print("PlantUML code saved to class_diagram.puml")
    print("You can render it at: https://www.plantuml.com/plantuml/uml/")


if __name__ == '__main__':
    main()
