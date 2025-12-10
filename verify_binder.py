import re

# Read pyproject.toml to verify dependencies
with open('pyproject.toml', 'r') as f:
    content = f.read()

# Extract binder section
binder_match = re.search(r'binder = \[(.*?)\]', content, re.DOTALL)
if binder_match:
    binder_section = binder_match.group(1)
    print('✅ UPDATED BINDER SECTION:')
    print('binder = [')
    packages = []
    for line in binder_section.strip().split('\n'):
        if line.strip() and line.strip().startswith('"'):
            print(f'    {line.strip()}')
            pkg = line.strip().strip('"').split('>')[0].split('<')[0].split('=')[0].split(';')[0].strip()
            packages.append(pkg)
    print(']')
    
    # Verify no conflicts with base dependencies
    base_deps = {'numpy', 'pandas', 'scipy', 'scikit-learn', 'deprecated', 'numba', 'packaging', 'typing-extensions'}
    
    print(f'\n✅ VERIFICATION:')
    print(f'   Total packages in binder: {len(packages)}')
    print(f'   Packages: {", ".join(packages)}')
    
    conflicts = set(packages) & base_deps
    print(f'   Conflicts with base dependencies: {len(conflicts) == 0}')
    if conflicts:
        print(f'   WARNING: Conflicting packages: {conflicts}')
    
    print(f'\n✅ ANALYSIS SUMMARY:')
    print(f'   - matplotlib: For plotting in multiple example notebooks')
    print(f'   - seaborn: For advanced visualization')
    print(f'   - statsmodels: For time series forecasting examples')
    print(f'   - pyod: For anomaly detection examples')
    print(f'   - tensorflow: For deep learning examples (Python < 3.13)')
