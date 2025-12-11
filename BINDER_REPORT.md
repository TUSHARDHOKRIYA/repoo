Bindder REPORT: Binder Examples - Issue, Fixes, Verification
Date: December 11, 2025

1) Executive summary
- Issue found: The Binder environment for the Aeon Toolkit example notebooks was failing with ModuleNotFoundError because the `binder` extra in `pyproject.toml` only listed Jupyter packages (`notebook`, `jupyterlab`) and omitted additional packages required by the example notebooks.
- While launching Binder (Dockerfile uses `pip install .[binder]`) could not run many example notebooks; notebooks crashed at import time.
- Fix applied: Added the missing runtime packages (with version constraints copied from the existing `all_extras`) to the `binder` extra. Verified all example notebooks now have their imports covered by the base Binder image + the updated binder extras.

2) What I found during analysis
- Notebooks analyzed: 62 example notebooks under.
- Main missing packages detected (from `import_analysis.txt` and notebook scans):
  - `matplotlib` 
  - `seaborn` 
  - `statsmodels` 
  - `pyod` 
  - `tensorflow` 
  - `aeon` 
- Base image note: Binder uses `jupyter/scipy-notebook:python-3.11`, which already includes `numpy`, `pandas`, `scipy`, `scikit-learn` (so these were not added to binder extras).

3) Exact changes made (files and diff summary)
- Modified: `pyproject.toml` — added packages to the `binder` optional dependency list (lines ~97-106):
  binder = [
    "notebook",
    "jupyterlab",
    "matplotlib>=3.3.2",
    "seaborn>=0.11.0",
    "statsmodels>=0.12.1",
    "pyod>=1.1.3",
    "tensorflow>=2.14; python_version < '3.13'",
  ]

End of report.
