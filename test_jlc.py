#!/usr/bin/env python3
from jlc2kicadlib import JLCKicad

def test_jlc2kicad():
    try:
        converter = JLCKicad()
        print("Successfully imported JLCKicad")
        return True
    except Exception as e:
        print(f"Error importing JLCKicad: {e}")
        return False

if __name__ == "__main__":
    test_jlc2kicad()