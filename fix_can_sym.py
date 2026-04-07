import re

with open('hardware/wafel-eval-board.kicad_sym', 'r') as f:
    content = f.read()

good_sym = """  (symbol "CAN_Transceiver_8Pin"
    (pin_names
      (offset 1.016)
    )
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (property "Reference" "U"
      (at -7.62 8.89 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "CAN_Transceiver_8Pin"
      (at -7.62 6.35 0)
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
    (property "MPN" "TJA1051T/3/1J"
      (at 0 0 0)
      (effects (font (size 1.27 1.27)))
      (hide yes)
    )
    (property "LCSC" "C38695"
      (at 0 0 0)
      (effects (font (size 1.27 1.27)))
      (hide yes)
    )
    (property "MPN_Alt1" "TCAN1042HDRQ1"
      (at 0 0 0)
      (effects (font (size 1.27 1.27)))
      (hide yes)
    )
    (property "LCSC_Alt1" "C2671057"
      (at 0 0 0)
      (effects (font (size 1.27 1.27)))
      (hide yes)
    )
    (property "Description" "Generic 8-pin CAN Transceiver with Standby"
      (at 0 0 0)
      (effects (font (size 1.27 1.27)))
      (hide yes)
    )
    (symbol "CAN_Transceiver_8Pin_0_1"
      (rectangle (start -10.16 5.08) (end 10.16 -5.08)
        (stroke (width 0.254) (type default)) (fill (type background))
      )
    )
    (symbol "CAN_Transceiver_8Pin_1_1"
      (pin input line (at -12.7 2.54 0) (length 2.54)
        (name "TXD" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at 0 -7.62 90) (length 2.54)
        (name "GND" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at -2.54 7.62 270) (length 2.54)
        (name "VCC" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
      (pin output line (at -12.7 0 0) (length 2.54)
        (name "RXD" (effects (font (size 1.27 1.27))))
        (number "4" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at 2.54 7.62 270) (length 2.54)
        (name "VIO" (effects (font (size 1.27 1.27))))
        (number "5" (effects (font (size 1.27 1.27))))
      )
      (pin bidirectional line (at 12.7 -2.54 180) (length 2.54)
        (name "CAN_L" (effects (font (size 1.27 1.27))))
        (number "6" (effects (font (size 1.27 1.27))))
      )
      (pin bidirectional line (at 12.7 2.54 180) (length 2.54)
        (name "CAN_H" (effects (font (size 1.27 1.27))))
        (number "7" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at -12.7 -2.54 0) (length 2.54)
        (name "STB" (effects (font (size 1.27 1.27))))
        (number "8" (effects (font (size 1.27 1.27))))
      )
    )
  )"""

# Remove the broken symbol
content = re.sub(r'  \(symbol "CAN_Transceiver_8Pin".*?^\s*\)\s*^\s*\)', good_sym, content, flags=re.MULTILINE | re.DOTALL)

with open('hardware/wafel-eval-board.kicad_sym', 'w') as f:
    f.write(content)

