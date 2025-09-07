import re
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class Intent:
    kind: str                 # 'move_cm', 'turn_deg', 'goto'
    value: Optional[float] = None
    target: Optional[Tuple[int, int]] = None

_NUMBER = r"([-+]?\d+(?:\.\d+)?)"
_CM = re.compile(rf"^(?:forward|back)\s+{_NUMBER}\s*(?:cm|centimeter|centimeters)?$", re.I)
_TURN = re.compile(rf"^(?:left|right)\s+{_NUMBER}\s*(?:deg|degree|degrees)?$", re.I)
_GOTO = re.compile(r"^(?:goto|go to)\s*(\d+)\s*,\s*(\d+)$", re.I)

def parse_intent(text: str) -> Optional[Intent]:
    t = text.strip()
    # goto x,y
    m = _GOTO.match(t)
    if m:
        return Intent(kind="goto", target=(int(m.group(1)), int(m.group(2))))
    # forward/back N cm
    m = _CM.match(t)
    if m:
        n = float(m.group(1))
        if t.lower().startswith("back"):
            n = -n
        return Intent(kind="move_cm", value=n)
    # left/right N deg
    m = _TURN.match(t)
    if m:
        n = float(m.group(1))
        if t.lower().startswith("right"):
            n = -n
        return Intent(kind="turn_deg", value=n)
    # single-word primitives
    if t.lower() in ("forward", "back"):
        return Intent(kind="move_cm", value=10.0 if t.lower()=="forward" else -10.0)
    if t.lower() in ("left", "right"):
        return Intent(kind="turn_deg", value=15.0 if t.lower()=="left" else -15.0)
    return None
