# LCSC to KiCad Converter Plugin

A KiCad plugin that converts LCSC/EasyEDA components to KiCad format, including symbols, footprints, and 3D models.

## Features

- Convert LCSC components directly within KiCad
- Support for symbols, footprints, and 3D models
- Easy-to-use graphical interface
- Progress tracking
- Custom output directory selection

## Installation

1. Download the plugin from the KiCad Plugin and Content Manager
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open KiCad
2. Click on the LCSC to KiCad Converter icon in the toolbar
3. Enter the LCSC part number
4. Select an output directory
5. Click Convert
6. The converted files will be saved in the specified directory under:
   - symbols/
   - footprints/
   - 3dmodels/

## Dependencies

- wxPython >= 4.2.0
- easyeda2kicad >= 2.0.0

## License

MIT License

## Credits

Based on the [easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py) project.