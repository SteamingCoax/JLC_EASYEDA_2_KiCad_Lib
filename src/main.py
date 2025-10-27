#!/usr/bin/env python3
import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread


class EasyEda2KiCadGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EasyEDA to KiCad Converter")
        self.root.geometry("600x400")
        
        # Output directory selection
        dir_frame = ttk.Frame(root)
        dir_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(dir_frame, text="Output Directory:").pack(side=tk.LEFT)
        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(dir_frame, text="Browse", command=self.browse_directory).pack(side=tk.RIGHT)
        
        # Part numbers input
        ttk.Label(root, text="Part Numbers (One per line):").pack(anchor=tk.W, padx=5)
        
        self.parts_text = tk.Text(root, height=10)
        self.parts_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Convert button
        self.convert_btn = ttk.Button(root, text="Convert", command=self.start_conversion)
        self.convert_btn.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(root, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=5, pady=5)
        
        # Status label
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=5)
        
        self.conversion_thread = None
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def start_conversion(self):
        output_dir = self.dir_entry.get().strip()
        part_numbers = self.parts_text.get("1.0", tk.END).strip().split('\n')
        
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return
            
        if not part_numbers or not part_numbers[0]:
            messagebox.showerror("Error", "Please enter at least one part number")
            return
        
        # Disable controls during conversion
        self.convert_btn.configure(state='disabled')
        self.progress.start()
        self.status_label.configure(text="Converting...")
        
        # Start conversion in a separate thread
        self.conversion_thread = Thread(target=self.convert_parts, 
                                     args=(output_dir, part_numbers))
        self.conversion_thread.start()
        
        # Check progress periodically
        self.root.after(100, self.check_conversion)
    
    def convert_parts(self, output_dir, part_numbers):
        try:
            # Convert to absolute path
            abs_output_dir = os.path.abspath(output_dir)
            os.makedirs(abs_output_dir, exist_ok=True)
            
            # Create a fixed library name that won't change based on directory
            lib_name = "easyeda2kicad"
            lib_path = os.path.join(abs_output_dir, lib_name)
            
            # Setup conversion command
            python_executable = sys.executable
            script_cmd = [python_executable, "-m", "easyeda2kicad"]
            
            total_parts = len([p for p in part_numbers if p.strip()])
            converted = 0
            
            for part_number in part_numbers:
                if part_number.strip():
                    # Update status
                    self.status_label.configure(text=f"Converting part {converted + 1}/{total_parts}: {part_number.strip()}")
                    
                    # Build command for easyeda2kicad
                    cmd = script_cmd + [
                        "--full",  # Convert symbol, footprint, and 3D model
                        f"--lcsc_id={part_number.strip()}",
                        "--output", lib_path,
                        "--overwrite"  # Update if component already exists
                    ]
                    
                    # Run the conversion command
                    result = subprocess.run(cmd, 
                                         capture_output=True, 
                                         text=True,
                                         check=False)
                    
                    if result.returncode != 0:
                        raise Exception(f"Conversion failed: {result.stderr}")
                    
                    # Show the output in the status label
                    if result.stdout:
                        self.status_label.configure(text=result.stdout.strip())
                    
                    converted += 1
            
            self.conversion_success = True
            self.conversion_error = None
            
        except Exception as e:
            self.conversion_success = False
            self.conversion_error = str(e)
    
    def check_conversion(self):
        if self.conversion_thread and not self.conversion_thread.is_alive():
            self.progress.stop()
            self.convert_btn.configure(state='normal')
            
            if getattr(self, 'conversion_success', False):
                self.status_label.configure(text="✓ Conversion completed successfully!")
            else:
                error_msg = getattr(self, 'conversion_error', "Unknown error occurred")
                self.status_label.configure(text=f"❌ Error: {error_msg}")
                messagebox.showerror("Error", f"Conversion failed: {error_msg}")
        else:
            self.root.after(100, self.check_conversion)


def main():
    root = tk.Tk()
    app = EasyEda2KiCadGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
