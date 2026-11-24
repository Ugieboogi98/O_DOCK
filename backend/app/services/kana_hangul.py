"""Deterministic Japanese kana -> Hangul transliteration for proper names.

Follows the spelling conventions already used by the curated dictionary
(e.g. 우즈마키, 휴우가, 센쥬, 츠나데, 카카시): aspirated k/t/p everywhere,
つ→츠, long vowels written as they are, ン→ㄴ and ッ→ㅅ batchim.
It is only applied to readings of names. Loanwords and ordinary words are
translated by meaning, never by sound.
"""
import re
import unicodedata

# Initial consonant indices (Unicode Hangul composition order).
_I = {'g': 0, 'n': 2, 'd': 3, 'r': 5, 'm': 6, 'b': 7, 's': 9, '': 11, 'j': 12, 'ch': 14, 'k': 15, 't': 16, 'p': 17, 'h': 18}
# Vowel indices.
_V = {'a': 0, 'ya': 2, 'e': 5, 'ye': 7, 'o': 8, 'wa': 9, 'we': 15, 'wi': 16, 'wo': 14, 'yo': 12, 'u': 13, 'yu': 17, 'eu': 18, 'i': 20}
_FINAL_N, _FINAL_S = 4, 19

_BASE = {
    'ア': ('', 'a'), 'イ': ('', 'i'), 'ウ': ('', 'u'), 'エ': ('', 'e'), 'オ': ('', 'o'),
    'カ': ('k', 'a'), 'キ': ('k', 'i'), 'ク': ('k', 'u'), 'ケ': ('k', 'e'), 'コ': ('k', 'o'),
    'ガ': ('g', 'a'), 'ギ': ('g', 'i'), 'グ': ('g', 'u'), 'ゲ': ('g', 'e'), 'ゴ': ('g', 'o'),
    'サ': ('s', 'a'), 'シ': ('s', 'i'), 'ス': ('s', 'eu'), 'セ': ('s', 'e'), 'ソ': ('s', 'o'),
    'ザ': ('j', 'a'), 'ジ': ('j', 'i'), 'ズ': ('j', 'eu'), 'ゼ': ('j', 'e'), 'ゾ': ('j', 'o'),
    'タ': ('t', 'a'), 'チ': ('ch', 'i'), 'ツ': ('ch', 'eu'), 'テ': ('t', 'e'), 'ト': ('t', 'o'),
    'ダ': ('d', 'a'), 'ヂ': ('j', 'i'), 'ヅ': ('j', 'eu'), 'デ': ('d', 'e'), 'ド': ('d', 'o'),
    'ナ': ('n', 'a'), 'ニ': ('n', 'i'), 'ヌ': ('n', 'u'), 'ネ': ('n', 'e'), 'ノ': ('n', 'o'),
    'ハ': ('h', 'a'), 'ヒ': ('h', 'i'), 'フ': ('h', 'u'), 'ヘ': ('h', 'e'), 'ホ': ('h', 'o'),
    'バ': ('b', 'a'), 'ビ': ('b', 'i'), 'ブ': ('b', 'u'), 'ベ': ('b', 'e'), 'ボ': ('b', 'o'),
    'パ': ('p', 'a'), 'ピ': ('p', 'i'), 'プ': ('p', 'u'), 'ペ': ('p', 'e'), 'ポ': ('p', 'o'),
    'マ': ('m', 'a'), 'ミ': ('m', 'i'), 'ム': ('m', 'u'), 'メ': ('m', 'e'), 'モ': ('m', 'o'),
    'ヤ': ('', 'ya'), 'ユ': ('', 'yu'), 'ヨ': ('', 'yo'),
    'ラ': ('r', 'a'), 'リ': ('r', 'i'), 'ル': ('r', 'u'), 'レ': ('r', 'e'), 'ロ': ('r', 'o'),
    'ワ': ('', 'wa'), 'ヰ': ('', 'i'), 'ヱ': ('', 'e'), 'ヲ': ('', 'o'), 'ヴ': ('b', 'u'),
}
_SMALL_Y = {'ャ': 'ya', 'ュ': 'yu', 'ョ': 'yo'}
_SMALL_V = {'ァ': 'a', 'ィ': 'i', 'ゥ': 'u', 'ェ': 'e', 'ォ': 'o'}
# Consonant + small vowel combinations (ファ, ティ, ウィ ...).
_COMBO = {
    ('h', 'a'): ('h', 'wa'), ('h', 'i'): ('p', 'i'), ('h', 'e'): ('p', 'e'), ('h', 'o'): ('p', 'o'),
    ('t', 'i'): ('t', 'i'), ('d', 'i'): ('d', 'i'), ('t', 'u'): ('t', 'u'), ('d', 'u'): ('d', 'u'),
    ('', 'i'): ('', 'wi'), ('', 'e'): ('', 'we'), ('', 'o'): ('', 'wo'),
    ('s', 'e'): ('s', 'ye'), ('j', 'e'): ('j', 'e'), ('ch', 'e'): ('ch', 'e'),
    ('b', 'a'): ('b', 'a'), ('b', 'i'): ('b', 'i'), ('b', 'e'): ('b', 'e'), ('b', 'o'): ('b', 'o'),
}
KANA = re.compile(r'^[ぁ-ゖァ-ヺー・\s・=＝]+$')


def _katakana(text):
    text = unicodedata.normalize('NFKC', text)
    return ''.join(chr(ord(c) + 0x60) if 'ぁ' <= c <= 'ゖ' else c for c in text)


def _syllable(initial, vowel, final=0):
    return chr(0xAC00 + (_I[initial] * 21 + _V[vowel]) * 28 + final)


def is_kana(text):
    return isinstance(text, str) and bool(text.strip()) and bool(KANA.match(text))


def to_hangul(text):
    """Transliterate a kana reading. Returns None when a character is unsupported."""
    if not is_kana(text):
        return None
    chars = _katakana(text)
    out = []          # list of [initial, vowel, final] or separators
    i = 0
    while i < len(chars):
        c = chars[i]
        if c in ' 　・=＝':
            if out and out[-1] != ' ':
                out.append(' ')
            i += 1
            continue
        if c == 'ー':
            i += 1
            continue
        if c in 'ンッ':
            if out and isinstance(out[-1], list) and out[-1][2] == 0:
                out[-1][2] = _FINAL_N if c == 'ン' else _FINAL_S
            elif c == 'ン':
                out.append(['', 'eu', _FINAL_N])
            i += 1
            continue
        if c in _SMALL_Y or c in _SMALL_V:
            # A stray small kana is read as its full-size vowel.
            vowel = _SMALL_Y.get(c) or _SMALL_V[c]
            out.append(['', vowel, 0])
            i += 1
            continue
        if c not in _BASE:
            return None
        initial, vowel = _BASE[c]
        nxt = chars[i + 1] if i + 1 < len(chars) else ''
        if nxt in _SMALL_Y and vowel == 'i':
            vowel = _SMALL_Y[nxt]
            if initial == 'ch':
                vowel = {'ya': 'a', 'yu': 'u', 'yo': 'o'}[vowel]
            i += 1
        elif nxt in _SMALL_V:
            small = _SMALL_V[nxt]
            initial, vowel = _COMBO.get((initial, small), (initial, small))
            i += 1
        out.append([initial, vowel, 0])
        i += 1
    text = ''.join(p if p == ' ' else _syllable(*p) for p in out).strip()
    return text or None
