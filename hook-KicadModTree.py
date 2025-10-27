from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all data files from the KicadModTree package
datas = collect_data_files('KicadModTree')

# Collect all submodules
hiddenimports = collect_submodules('KicadModTree')