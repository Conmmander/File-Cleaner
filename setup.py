import py2exe
# python -m setup
py2exe.freeze(
    windows=["main.py"],
    options={'bundle_files': 0, 'compressed': True},
    version_info={'version': '0.1.0', 'product_name': 'File Cleaner', 'copyright': 'Ryan Dodd © 2023', 'description': 'File Cleaner'},
)