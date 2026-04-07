use strict;
use warnings;

local $/;
open(my $fh, '<', 'hardware/wafel-eval-board.kicad_sym') or die $!;
my $content = <$fh>;
close($fh);

my $props = <<'PROPS';
    (property "MPN" "TJA1051T/3/1J"
      (at 0 0 0)
      (effects
        (font (size 1.27 1.27))
      )
      (hide yes)
    )
    (property "LCSC" "C38695"
      (at 0 0 0)
      (effects
        (font (size 1.27 1.27))
      )
      (hide yes)
    )
    (property "MPN_Alt1" "TCAN1042HDRQ1"
      (at 0 0 0)
      (effects
        (font (size 1.27 1.27))
      )
      (hide yes)
    )
    (property "LCSC_Alt1" "C2671057"
      (at 0 0 0)
      (effects
        (font (size 1.27 1.27))
      )
      (hide yes)
    )
PROPS

$content =~ s/(\(property "Description" "Generic 8-pin CAN Transceiver with Standby \(TCAN1042, TJA1051T, etc\.\)"\n      \(at 0 -10\.16 0\)\n      \(effects\n        \(font \(size 1\.27 1\.27\)\)\n      \)\n      \(hide yes\)\n    \))/$1\n$props/s;

open($fh, '>', 'hardware/wafel-eval-board.kicad_sym') or die $!;
print $fh $content;
close($fh);
