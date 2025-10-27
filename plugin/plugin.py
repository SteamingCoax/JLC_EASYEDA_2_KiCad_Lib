import os
import pcbnew
import wx

from easyeda2kicad.easyeda2kicad import EasyEda2KiCad
from easyeda2kicad.processors.kicad6 import KiCad6SymbolProcessor, KiCad6FootprintProcessor
from easyeda2kicad.processors.models import WRLModelProcessor

class EasyEda2KiCadDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="EasyEDA to KiCad Converter", size=(400, 300))
        
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Part Number input
        part_box = wx.BoxSizer(wx.HORIZONTAL)
        part_label = wx.StaticText(self.panel, label="EasyEDA Part Number:")
        self.part_input = wx.TextCtrl(self.panel)
        part_box.Add(part_label, 0, wx.ALL, 5)
        part_box.Add(self.part_input, 1, wx.EXPAND | wx.ALL, 5)

        # Output directory selection
        dir_box = wx.BoxSizer(wx.HORIZONTAL)
        dir_label = wx.StaticText(self.panel, label="Output Directory:")
        self.dir_input = wx.TextCtrl(self.panel)
        dir_button = wx.Button(self.panel, label="Browse...")
        dir_button.Bind(wx.EVT_BUTTON, self.on_browse)
        dir_box.Add(dir_label, 0, wx.ALL, 5)
        dir_box.Add(self.dir_input, 1, wx.EXPAND | wx.ALL, 5)
        dir_box.Add(dir_button, 0, wx.ALL, 5)

        # Progress display
        self.progress = wx.Gauge(self.panel, range=100, style=wx.GA_HORIZONTAL)
        self.status = wx.StaticText(self.panel, label="")

        # Convert button
        self.convert_button = wx.Button(self.panel, label="Convert")
        self.convert_button.Bind(wx.EVT_BUTTON, self.on_convert)

        # Add all elements to main sizer
        self.sizer.Add(part_box, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(dir_box, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.progress, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.status, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.convert_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(self.sizer)
        self.Center()

    def on_browse(self, event):
        dlg = wx.DirDialog(self, "Choose output directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.dir_input.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_convert(self, event):
        part_number = self.part_input.GetValue()
        output_dir = self.dir_input.GetValue()

        if not part_number:
            wx.MessageBox("Please enter a part number", "Error", wx.OK | wx.ICON_ERROR)
            return
        if not output_dir:
            wx.MessageBox("Please select an output directory", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            self.status.SetLabel("Converting...")
            self.progress.SetValue(0)
            
            # Initialize converter
            converter = EasyEda2KiCad(
                symbol_processor=KiCad6SymbolProcessor(),
                footprint_processor=KiCad6FootprintProcessor(),
                model_processor=WRLModelProcessor()
            )

            # Set up output directories
            symbol_dir = os.path.join(output_dir, "symbols")
            footprint_dir = os.path.join(output_dir, "footprints")
            model_dir = os.path.join(output_dir, "3dmodels")

            os.makedirs(symbol_dir, exist_ok=True)
            os.makedirs(footprint_dir, exist_ok=True)
            os.makedirs(model_dir, exist_ok=True)

            # Convert component
            component = converter.convert_lcsc(
                part_number,
                symbol_dir=symbol_dir,
                footprint_dir=footprint_dir,
                model_dir=model_dir
            )

            self.progress.SetValue(100)
            self.status.SetLabel("Conversion completed successfully!")
            
            wx.MessageBox(
                f"Component converted successfully!\n\nFiles saved in:\n{output_dir}",
                "Success",
                wx.OK | wx.ICON_INFORMATION
            )

        except Exception as e:
            self.status.SetLabel(f"Error: {str(e)}")
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

class EasyEda2KiCadPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "EasyEDA to KiCad Converter"
        self.category = "Conversion"
        self.description = "Convert EasyEDA components to KiCad format"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        dialog = EasyEda2KiCadDialog(None)
        dialog.ShowModal()
        dialog.Destroy()

EasyEda2KiCadPlugin().register()