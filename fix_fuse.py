import re

with open('hardware/wafel-eval-board.kicad_sym', 'r') as f:
    content = f.read()

fuse_sym = """  (symbol "Fuse_3Terminal"
    (pin_names
      (offset 1.016)
      (hide yes)
    )
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (property "Reference" "F"
      (at -2.54 3.81 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "Fuse_3Terminal"
      (at -2.54 -3.81 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" ""
      (at 0 0 0)
      (effects (font (size 1.27 1.27)))
      (hide yes)
    )
    (property "Datasheet" "~"
      (at 0 0 0)
      (effects (font (size 1.27 1.27)))
      (hide yes)
    )
    (property "Description" "3-Terminal Battery Protection Fuse"
      (at 0 0 0)
      (effects (font (size 1.27 1.27)))
      (hide yes)
    )
    (symbol "Fuse_3Terminal_0_1"
      (rectangle (start -3.81 2.54) (end 3.81 -2.54)
        (stroke (width 0.254) (type default)) (fill (type background))
      )
      (polyline (pts (xy -3.81 0) (xy -2.54 0) (xy -1.27 1.27) (xy 0 0) (xy 1.27 1.27) (xy 2.54 0) (xy 3.81 0))
        (stroke (width 0.254) (type default)) (fill (type none))
      )
      (polyline (pts (xy 0 2.54) (xy 0 0))
        (stroke (width 0.254) (type default)) (fill (type none))
      )
    )
    (symbol "Fuse_3Terminal_1_1"
      (pin passive line (at 6.35 0 180) (length 2.54)
        (name "1" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 5.08 270) (length 2.54)
        (name "2" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at -6.35 0 0) (length 2.54)
        (name "3" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
  )"""

content = re.sub(r'  \(symbol "Fuse_3Terminal".*?^\s*\)\s*^\s*\)', fuse_sym, content, flags=re.MULTILINE | re.DOTALL)

with open('hardware/wafel-eval-board.kicad_sym', 'w') as f:
    f.write(content)
