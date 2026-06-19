# CP437 character table.
# Entries are the UTF-8 equivalents of IBM Code Page 437 (not the actual
# code-page bytes). Index into CP437 with a CP437 code to get the
# corresponding Unicode character.
# fmt: off
CP437: tuple[str, ...] = (
    "\0", "☺", "☻", "♥", "♦", "♣", "♠", "•", "◘", "○", "◙", "♂", "♀", "♪", "♫", "☼",    # 0x00
    "►", "◄", "↕", "‼", "¶", "§", "▬", "↨", "↑", "↓", "→", "←", "∟", "↔", "▲", "▼",     # 0x10
    " ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",    # 0x20
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",     # 0x30
    "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",     # 0x40
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_",    # 0x50
    "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",     # 0x60
    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "⌂",     # 0x70
    "Ç", "ü", "é", "â", "ä", "à", "å", "ç", "ê", "ë", "è", "ï", "î", "ì", "Ä", "Å",     # 0x80
    "É", "æ", "Æ", "ô", "ö", "ò", "û", "ù", "ÿ", "Ö", "Ü", "¢", "£", "¥", "₧", "ƒ",     # 0x90
    "á", "í", "ó", "ú", "ñ", "Ñ", "ª", "º", "¿", "⌐", "¬", "½", "¼", "¡", "«", "»",     # 0xa0
    "░", "▒", "▓", "│", "┤", "╡", "╢", "╖", "╕", "╣", "║", "╗", "╝", "╜", "╛", "┐",     # 0xb0
    "└", "┴", "┬", "├", "─", "┼", "╞", "╟", "╚", "╔", "╩", "╦", "╠", "═", "╬", "╧",     # 0xc0
    "╨", "╤", "╥", "╙", "╘", "╒", "╓", "╫", "╪", "┘", "┌", "█", "▄", "▌", "▐", "▀",     # 0xd0
    "α", "ß", "Γ", "π", "Σ", "σ", "µ", "τ", "Φ", "Θ", "Ω", "δ", "∞", "φ", "ε", "∩",     # 0xe0
    "≡", "±", "≥", "≤", "⌠", "⌡", "÷", "≈", "°", "∙", "·", "√", "ⁿ", "²", "■", "\xa0",  # 0xf0
)
# fmt: on

# Named constants for glyphs used by the renderer.
# Add entries here as new glyphs are needed; never scatter CP437 literals
# elsewhere in the codebase — always reference via this module.

FULL_BLOCK: str = CP437[0xDB]  # █

BOX_DBL_HORIZONTAL: str = CP437[0xCD]  # ═
BOX_DBL_VERTICAL: str = CP437[0xBA]  # ║
BOX_DBL_DOWN_RIGHT: str = CP437[0xC9]  # ╔
BOX_DBL_DOWN_LEFT: str = CP437[0xBB]  # ╗
BOX_DBL_UP_RIGHT: str = CP437[0xC8]  # ╚
BOX_DBL_UP_LEFT: str = CP437[0xBC]  # ╝

# Menu / UI glyphs
TRIANGLE_RIGHT: str = CP437[0x10]  # ► (selection cursor)

# Terrain glyphs
WAVE: str = CP437[0xF7]  # ≈ (deep ocean)
TILDE: str = CP437[0x7E]  # ~ (coast / river)
DOT: str = CP437[0x2E]  # . (plain)
CLUB: str = CP437[0x05]  # ♣ (forest)
LOWER_N: str = CP437[0x6E]  # n (hill)
CARET: str = CP437[0x5E]  # ^ (mountain)
MIDDLE_DOT: str = CP437[0xFA]  # · (desert)
UNDERSCORE: str = CP437[0x5F]  # _ (tundra)
