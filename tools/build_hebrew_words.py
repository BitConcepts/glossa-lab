"""Build word-segmented Hebrew corpus.

Run once to produce the properly-segmented version of _HEBREW_LINES.
Output is printed as a Python list — paste it into old_hebrew.py.

Algorithm
---------
1.  Longest-match against ~300 core Biblical Hebrew vocabulary items
    (tuples of consonant tokens in Glossa Lab transliteration).
2.  Single-consonant prefix stripping (w/b/l/k/m/h) before vocabulary
    lookup so "wyhwh" → ["w"] + ["y","h","w","h"].
3.  Unknown residues: 3-consonant chunks (average BH word length).

Usage
-----
    python tools/build_hebrew_words.py
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.join(os.path.dirname(_HERE), "backend")
sys.path.insert(0, _BACKEND)

from glossa_lab.data.old_hebrew import _HEBREW_LINES  # noqa: E402


# ──────────────────────────────────────────────────────────────────────
# Vocabulary
#
# Each entry is a TUPLE of individual consonant tokens (as they appear
# in _HEBREW_LINES, space-separated).  Longest match wins.
#
# Transliteration keys:
#   ' = aleph   b  g  d  h  w  z  H = het   T = tet   y
#   k  l  m  n  s  E = ayin   p  C = tsade   q  r  G = shin   t
# ──────────────────────────────────────────────────────────────────────

VOCAB: set[tuple[str, ...]] = {
    # ── Divine names ───────────────────────────────────────────────
    ("y", "h", "w", "h"),                      # yhwh
    ("'", "l", "h", "y", "m"),                 # 'lhym (Elohim)
    ("'", "l", "h", "y", "n", "w"),             # 'lhynw (our God)
    ("'", "l", "h", "y", "k"),                  # 'lhyk (your God)
    ("'", "l", "h", "y", "k", "m"),             # 'lhykm (your God pl)
    ("'", "l", "h", "y", "h", "m"),             # 'lhyhm
    ("'", "d", "n", "y"),                       # 'dny (Lord)
    # ── Named compound forms (priority over shorter sub-matches) ──
    ("b", "r", "'", "G", "y", "t"),             # br'Gyt (in the beginning)
    ("y", "G", "r", "'", "l"),                  # yGr'l (Israel) -- already below but needs high prio
    # ── Common particles / prepositions ───────────────────────────
    ("k", "y"),                                 # ky (that/because)
    ("h", "n", "h"),                            # hnh (behold)
    ("'", "G", "r"),                            # 'Gr (which/that)
    ("'", "G", "r", "y"),                       # 'Gry (blessed are)
    ("H", "G", "r"),                            # HGr variant in corpus
    ("b", "y", "n"),                            # byn (between)
    ("E", "l"),                                 # El (upon/over) -- standalone
    ("m", "n"),                                 # mn (from, standalone)
    ("E", "d"),                                 # Ed (until)
    ("l", "m", "E", "n"),                       # lmEn (in order to)
    ("m", "E", "l"),                            # mEl (above)
    ("l", "p", "n", "y"),                       # lpny (before, to face of)
    ("p", "n", "y"),                            # pny (face of)
    ("p", "n", "y", "m"),                       # pnym (face)
    ("p", "n", "y", "w"),                       # pnyw (his face)
    ("p", "n", "y", "k"),                       # pnyk
    ("p", "n", "y", "k", "m"),                  # pnykm
    ("t", "h", "t"),                            # tht (under)
    ("k", "l"),                                 # kl (all)
    ("k", "l", "h"),                            # klh (all of)
    ("l", "'"),                                 # l' (not)
    ("w", "l", "'"),                            # wl' (and not)
    ("'", "y", "n"),                            # 'yn (there is not)
    ("'", "l"),                                 # 'l (to/toward/God) -- standalone
    ("'", "z"),                                 # 'z (then)
    # NOTE: very short (2-token) ambiguous words omitted to reduce false splits.
    # Words like gm, rq, 'k, 'p, pn, 'm, hn, hm, km, rE, Em, yd, bn, bt
    # are not included because they create more false positives than true.
    # ── Pronouns (≥3 tokens only, to avoid false splits) ─────────
    ("'", "n", "y"),                            # 'ny (I)
    ("'", "n", "k", "y"),                       # 'nky (I)
    ("h", "w", "'"),                            # hw' (he)
    ("h", "y", "'"),                            # hy' (she)
    ("'", "n", "H", "n", "w"),                  # 'nHnw (we)
    # ── Accusative marker ─────────────────────────────────────────
    ("'", "t"),                                 # 't (direct object marker)
    # ── Common verbs (base forms + frequent conjugations) ─────────
    ("'", "m", "r"),                            # 'mr (say)
    ("w", "y", "'", "m", "r"),                  # wy'mr (and he said)
    ("y", "'", "m", "r"),                       # y'mr (he will say)
    ("w", "t", "'", "m", "r"),                  # wt'mr (and she said)
    ("h", "y", "h"),                            # hyh (be/was)
    ("h", "y", "t", "h"),                       # hyth (was/became)
    ("y", "h", "y", "h"),                       # yhyh (will be)
    ("y", "h", "y"),                            # yhy (let there be)
    ("w", "y", "h", "y"),                       # wyhy (and it was)
    ("w", "t", "h", "y"),                       # wthy (and she/it was)
    ("h", "l", "k"),                            # hlk (walk/go)
    ("y", "l", "k"),                            # ylk (he walks)
    ("w", "y", "l", "k"),                       # wylk (and he went)
    ("h", "l", "k", "w"),                       # hlkw (they walked)
    ("'", "k", "l"),                            # 'kl (eat)
    ("y", "'", "k", "l"),                       # y'kl (eats)
    ("w", "y", "'", "k", "l"),                  # wy'kl
    ("n", "t", "n"),                            # ntn (give)
    ("y", "t", "n"),                            # ytn
    ("w", "y", "t", "n"),                       # wytn
    ("G", "m", "E"),                            # GmE (hear)
    ("y", "G", "m", "E"),                       # yGmE
    ("w", "y", "G", "m", "E"),                  # wyGmE
    ("r", "'", "h"),                            # r'h (see)
    ("y", "r", "'"),                            # yr' (he sees / fears)
    ("w", "y", "r", "'"),                       # wyr'
    ("y", "d", "E"),                            # ydE (know)
    ("w", "y", "d", "E"),                       # wydE
    ("q", "r", "'"),                            # qr' (call/read)
    ("y", "q", "r", "'"),                       # yqr'
    ("w", "y", "q", "r", "'"),                  # wyqr'
    ("E", "G", "h"),                            # EGh (do/make) - ayin-shin-he
    ("y", "E", "G"),                            # yEG (does/makes)
    ("w", "y", "E", "G"),                       # wyEG (and he made)
    ("b", "r", "'"),                            # br' (create)
    ("y", "b", "r", "'"),                       # ybr'
    ("b", "d", "l"),                            # bdl (divide/separate)
    ("y", "b", "d", "l"),                       # ybdl
    ("w", "y", "b", "d", "l"),                  # wybdl
    ("b", "n", "h"),                            # bnh (build)
    ("y", "b", "n"),                            # ybn (he builds)
    ("w", "y", "b", "n"),                       # wybn
    ("d", "b", "r"),                            # dbr (speak)
    ("y", "d", "b", "r"),                       # ydbr
    ("w", "y", "d", "b", "r"),                  # wydbr
    ("b", "r", "k"),                            # brk (bless)
    ("y", "b", "r", "k"),                       # ybrk
    ("w", "y", "b", "r", "k"),                  # wybrk
    ("q", "d", "G"),                            # qdG (be holy/sanctify)
    ("w", "y", "q", "d", "G"),                  # wyqdG
    ("q", "w", "m"),                            # qwm (rise)
    ("y", "q", "w", "m"),                       # yqwm
    ("w", "y", "q", "m"),                       # wyqm
    ("y", "r", "d"),                            # yrd (go down)
    ("w", "y", "r", "d"),                       # wyrd
    ("G", "l", "H"),                            # GlH (send away/exile)
    ("C", "m", "H"),                            # CmH (grow)
    ("y", "C", "m", "H"),                       # yCmH
    ("w", "y", "C", "m", "H"),                  # wyCmH
    ("y", "C", "r"),                            # yCr (form)
    ("w", "y", "y", "p", "H"),                  # wyypH (breathed into)
    ("w", "y", "k", "l", "w"),                  # wyyklw (finished)
    ("w", "y", "k", "l"),                       # wykl
    ("w", "y", "T", "E"),                       # wyTE (planted)
    ("s", "r"),                                 # sr (turn aside/remove)
    ("w", "y", "G", "l", "H"),                  # wyGlH
    ("H", "G", "b"),                            # HGb (think)
    ("H", "G", "H"),                            # HGH (meditate)
    ("y", "H", "g", "h"),                       # yHgh
    ("H", "p", "C"),                            # HpC (delight in)
    ("s", "l", "H"),                            # slH (forgive/send)
    ("n", "s", "h"),                            # nsh (test)
    ("z", "k", "r"),                            # zkr (remember)
    ("k", "r", "t"),                            # krt (cut)
    ("H", "z", "q"),                            # Hzq (be strong)
    ("w", "y", "s", "U"),                       # wyGm'
    ("w", "y", "s", "'"),                       # wys' (and he carried)
    ("q", "b", "C"),                            # qbC (gather)
    ("G", "l", "m"),                            # Glm - not common
    ("l", "m", "d"),                            # lmd (learn)
    ("l", "q", "H"),                            # lqH (take)
    ("w", "y", "l", "q", "H"),                  # wylqH
    ("T", "b", "H"),                            # TbH (slaughter)
    # ── Common nouns ──────────────────────────────────────────────
    ("'", "d", "m"),                            # 'dm (man/Adam)
    ("h", "'", "d", "m"),                       # h'dm (the man)
    ("'", "d", "m", "h"),                       # 'dmh (ground/soil)
    ("h", "'", "d", "m", "h"),                  # h'dmh (the ground)
    ("'", "r", "C"),                            # 'rC (earth/land)
    ("h", "'", "r", "C"),                       # h'rC (the earth)
    ("G", "m", "y", "m"),                       # Gmym (heavens)
    ("h", "G", "m", "y", "m"),                  # hGmym (the heavens)
    ("m", "y", "m"),                            # mym (water)
    ("h", "m", "y", "m"),                       # hmym (the water)
    ("m", "l", "k"),                            # mlk (king)
    ("b", "n"),                                 # bn (son)
    ("b", "n", "y"),                            # bny (sons of / my son)
    ("b", "n", "y", "m"),                       # bnym (sons)
    ("b", "t"),                                 # bt (daughter)
    ("b", "y", "t"),                            # byt (house)
    ("y", "w", "m"),                            # ywm (day)
    ("y", "m", "y", "m"),                       # ymym (days)
    ("y", "w", "m", "m"),                       # ywmm (by day)
    ("l", "y", "l", "h"),                       # lylh (night)
    ("n", "p", "G"),                            # npG (soul)
    ("n", "p", "G", "y"),                       # npGy (my soul)
    ("r", "w", "H"),                            # rwH (spirit/wind)
    ("E", "m"),                                 # Em (people) - standalone
    ("d", "r", "k"),                            # drk (way/path)
    ("d", "r", "k", "k"),                       # drkk (your way)
    ("l", "b", "b"),                            # lbb (heart)
    ("l", "b", "b", "k"),                       # lbbk (your heart)
    ("l", "b", "b", "k", "m"),                  # lbbkm (your heart pl)
    ("q", "w", "l"),                            # qwl (voice)
    ("d", "b", "r"),                            # dbr (word/thing) -- same as verb
    ("d", "b", "r", "y", "m"),                  # dbrym (words)
    ("E", "C", "h"),                            # ECh (tree)
    ("E", "C", "y", "m"),                       # ECym (trees)
    ("z", "r", "E"),                            # zrE (seed/offspring)
    ("g", "w", "y"),                            # gwy (nation/Gentile)
    ("g", "w", "y", "m"),                       # gwym (nations)
    ("p", "n", "y", "m"),                       # pnym (face)
    ("E", "y", "n"),                            # Eyn (eye/spring)
    ("E", "y", "n", "y", "m"),                  # Eynym (eyes)
    ("E", "y", "n", "y", "k"),                  # Eynyk
    ("y", "d"),                                 # yd (hand)
    ("y", "d", "y"),                            # ydy (my hand)
    ("y", "d", "k"),                            # ydk (your hand)
    ("y", "d", "w"),                            # ydw (his hand)
    ("t", "w", "r", "t"),                       # twrt (law/Torah)
    ("t", "w", "r", "t", "y"),                  # twrty (my Torah)
    ("t", "w", "r", "t", "k"),                  # twrtk
    # (twrt yhwh removed — it is two separate words)
    ("b", "G", "r"),                            # bGr (flesh)
    ("r", "E"),                                 # rE (evil/bad)
    ("G", "m", "k"),                             # Gmk (your name)
    ("G", "m", "w"),                             # Gmw (his name)
    ("G", "m", "y"),                             # Gmy (my name)
    ("G", "m", "m"),                             # Gmm (their name)
    ("H", "k", "m", "h"),                       # HkmH (wisdom)
    ("H", "k", "m"),                            # Hkm (wise)
    ("C", "d", "q"),                            # Cdq (righteousness)
    ("C", "d", "y", "q"),                       # Cdyq (righteous)
    ("C", "d", "y", "q", "y", "m"),             # Cdyqym (righteous ones)
    ("'", "m", "t"),                            # 'mt (truth)
    ("H", "s", "d"),                            # Hsd (lovingkindness)
    ("r", "H", "m"),                            # rHm (compassion)
    ("G", "m", "H"),                            # GmH (joy)
    ("H", "y", "y", "m"),                       # Hyym (life)
    ("n", "G", "m", "t"),                       # nGmt (breath)
    ("r", "q", "y", "E"),                       # rqyE (firmament/expanse)
    ("h", "r", "q", "y", "E"),                  # hrqyE (the firmament)
    ("g", "n"),                                 # gn (garden)
    ("E", "d", "n"),                            # Edn (Eden)
    ("n", "h", "r"),                            # nhr (river)
    ("r", "'", "G"),                            # r'G (head)
    ("r", "'", "G", "l"),                       # r'Gl (head/first)
    ("n", "H", "G"),                            # nHG (serpent)
    ("H", "y", "t"),                            # Hyt (animal/beast)
    ("G", "d", "h"),                            # Gdh (field)
    ("E", "r", "b"),                            # Erb (evening)
    ("b", "q", "r"),                            # bqr (morning)
    ("' ", "H", "d"),                           # 'Hd (one)
    ("'", "H", "d"),                            # 'Hd (one)
    ("'", "r", "b", "E", "h"),                  # 'rbEh (four)
    ("G", "b", "y", "E", "y"),                  # GbyEy (seventh)
    ("' ", "w", "r"),                           # 'wr (light)
    ("'", "w", "r"),                            # 'wr (light)
    ("h", "'", "w", "r"),                       # h'wr (the light)
    ("H", "G", "k"),                            # HGk (darkness)
    ("h", "H", "G", "k"),                       # hHGk (the darkness)
    ("T", "h", "w"),                            # Thw (formlessness)
    ("b", "h", "w"),                            # bhw (void)
    ("t", "h", "w", "m"),                       # thwm (the deep)
    ("m", "r", "H", "p", "t"),                  # mrHpt (hovering)
    ("'", "p"),                                 # 'p (nose/anger)
    ("'", "p", "y", "w"),                       # 'pyw (his nostrils)
    ("E", "p", "r"),                            # Epr (dust)
    ("H", "y", "h"),                            # Hyh (living/alive)
    ("H", "y", "t"),                            # Hyt (animal) -- dup
    # ── Common verb forms with prefixes ──────────────────────────
    ("w", "n", "h", "r"),                       # wnhr (and a river)
    # ── Psalm-specific vocabulary ──────────────────────────────
    ("h", "'", "y", "G"),                       # h'yG (the man)
    ("m", "G", "p", "T"),                       # mGpT (judgment)
    ("r", "G", "E", "y", "m"),                  # rGEym (wicked ones)
    ("H", "T", "'", "y", "m"),                  # HT'ym (sinners)
    ("l", "C", "y", "m"),                       # lCym (scoffers)
    ("m", "w", "G", "b"),                       # mwGb (seat)
    ("r", "'", "y"),                            # r'y (my shepherd)
    ("n", "'", "w", "t"),                       # n'wt (pastures)
    ("m", "n", "H", "G", "t"),                  # mnHGt (waters of rest)
    ("n", "H", "n", "y"),                       # nHny (leads me)
    ("m", "E", "g", "l", "y"),                  # mEgly (paths of)
    ("g", "y", "'"),                            # gy' (valley)
    ("C", "l", "m", "w", "t"),                  # Clmwt (shadow of death)
    ("G", "b", "T"),                            # GbT (rod)
    ("m", "G", "E", "n", "t"),                  # mGEnt (staff)
    ("G", "l", "H", "n"),                       # GlHn (table)
    ("G", "y", "E", "n", "t"),                  # GyEnt (anointed)
    ("T", "w", "b"),                            # Twb (good)
    ("H", "s", "d", "y"),                       # Hsdy (my kindness)
    ("y", "m", "y"),                            # ymy (days of)
    ("H", "y", "y"),                            # Hyy (my life)
    ("b", "b", "y", "t"),                       # bbyt (in the house)
    ("l", "'", "r", "k"),                       # l'rk (for long)
    ("y", "m", "y", "m"),                       # ymym (days)
    ("E", "z", "b", "t", "n", "y"),             # Ezbtny (forsook me)
    ("G", "'", "g", "t", "y"),                  # G'gty (my cry)
    ("q", "d", "w", "G"),                       # qdwG (holy)
    ("t", "h", "l", "w", "t"),                  # thwlt (praise)
    ("y", "G", "r", "'", "l"),                  # yGr'l (Israel)
    # ── Proverbs vocabulary ────────────────────────────────────
    ("m", "G", "l"),                            # mGl (proverb)
    ("m", "G", "l", "y"),                       # mGly (proverbs of)
    ("H", "k", "m", "h"),                       # HkmH (wisdom)
    ("m", "w", "s", "r"),                       # mwsr (discipline)
    ("b", "y", "n", "h"),                       # bynh (understanding)
    ("m", "C", "w", "t"),                       # mCwt (commands)
    ("y", "r", "'", "t"),                       # yr't (fear of)
    ("y", "r", "'", "t", "y"),                  # yr'ty
    ("r", "'", "G", "y", "t"),                  # r'Gyt (beginning)
    ("d", "E", "t"),                            # dEt (knowledge)
    ("G", "k", "l"),                            # Gkl (insight)
    ("E", "r", "m", "h"),                       # Ermh (cleverness)
    ("k", "s", "y", "l"),                       # ksyl (fool)
    ("k", "s", "y", "l", "y", "m"),             # ksylym (fools)
    ("H", "k", "m"),                            # Hkm (wise)
    ("H", "k", "m", "y", "m"),                  # Hkmym (wise ones)
    ("C", "d", "y", "q"),                       # Cdyq (righteous person)
    ("r", "G", "E"),                            # rGE (wicked person)
    ("C", "d", "y", "q", "y", "m"),             # Cdyqym
    ("r", "G", "E", "y", "m"),                  # rGEym
    ("l", "b", "b"),                            # lbb (heart)
    ("m", "s", "l"),                            # msl (proverb/rule)
    ("E", "C", "t"),                            # ECt (counsel)
    ("E", "C", "t", "w"),                       # ECtw (his counsel)
    ("H", "k", "m", "y", "m"),                  # Hkmym
    ("y", "G", "r"),                            # yGr (fear/revere)
    ("y", "G", "r", "'", "t"),                  # yGr't
    ("b", "y", "t", "h"),                       # byth (her house)
    ("E", "m", "w", "d", "y", "m"),             # Emwdym (pillars)
    ("E", "m", "w", "d"),                       # Emwd (pillar)
    ("T", "b", "H"),                            # TbH (slaughter/feast)
    ("y", "y", "n"),                            # yyn (wine)
    ("G", "l", "H", "n", "h"),                  # GlHnh (her table)
    ("p", "t", "'", "y", "m"),                  # pt'ym (simple ones)
    ("l", "b", "y", "n"),                       # lbyn (to understand)
    # ── Genesis 4 specific ──────────────────────────────────────
    ("q", "y", "n"),                            # qyn (Cain)
    ("h", "b", "l"),                            # hbl (Abel/vanity)
    ("q", "r", "b", "n"),                       # qrbn (offering)
    ("m", "n", "H", "h"),                       # mnHh (offering/gift)
    ("r", "E", "h"),                            # rEh (shepherd)
    ("C", "'", "n"),                            # C'n (flock/sheep)
    ("H", "l", "b"),                            # Hlb (fat/best part)
    ("b", "k", "r"),                            # bkr (firstling)
    ("E", "b", "d"),                            # Ebd (servant/worker)
    ("'", "d", "m", "h"),                       # 'dmh (ground) -- dup
    ("m", "p", "r", "y"),                       # mpry (fruit of)
    ("H", "r", "h"),                            # Hrh (anger)
    ("p", "n", "y", "w"),                       # pnyw (his face)
    ("H", "T", "'", "t"),                       # HT't (sin)
    ("H", "r", "g"),                            # Hrg (kill)
    ("r", "g", "h"),                            # murder - same
    ("d", "m"),                                 # dm (blood)
    ("d", "m", "y", "k"),                       # dmyk (your blood)
    # ── Deuteronomy/Numbers vocabulary ──────────────────────────
    ("m", "C", "w", "t", "y"),                  # mCwty (my commands)
    ("E", "l", "y", "d", "k"),                  # Elydk (on your hand)
    ("m", "z", "w", "z", "w", "t"),             # mzwzwt (doorposts)
    ("G", "E", "r", "y", "k"),                  # GEryk (your gates)
    ("l", "b", "b", "k"),                       # lbbk (your heart)
    ("n", "p", "G", "k"),                       # npGk (your soul)
    ("l", "T", "T", "p", "t"),                  # lTTpt (frontlet/phylactery)
    ("H", "q", "y", "m"),                       # Hqym (statutes)
    ("m", "C", "w", "t"),                       # mCwt (commandments)
    ("m", "G", "p", "T", "y", "m"),             # mGpTym
    # ── Exodus specific ──────────────────────────────────────────
    ("m", "G", "h"),                            # mGh (there)
    ("H", "s", "n", "h"),                       # Hsnh (the bush)
    ("s", "n", "h"),                            # snh (bush)
    ("b", "'", "r"),                            # b'r (in the fire)
    ("'", "G"),                                 # 'G (fire) - standalone
    ("m", "C", "r", "y", "m"),                  # mCrym (Egypt)
    ("p", "r", "E", "h"),                       # prEh (Pharaoh)
    ("b", "y", "t"),                            # byt - dup
    ("E", "b", "d", "y", "m"),                  # Ebdym (servants/slaves)
    ("E", "b", "d", "y", "t"),                  # Ebdyt (service)
    ("H", "T", "'", "t", "k", "m"),             # HT'tkm
    ("r", "C", "H"),                            # rCH (murder)
    ("n", "'", "p"),                            # n'p (adultery)
    ("g", "n", "b"),                            # gnb (steal)
    ("G", "q", "r"),                            # Gqr (false/lie)
    ("H", "m", "d"),                            # Hmd (covet)
    ("G", "b", "t"),                            # Gbt (Sabbath)
    ("G", "b", "t", "w", "n"),                  # Gbtwn (rest)
    ("z", "k", "w", "r"),                       # zkwr (remember - imp)
    ("q", "d", "G", "w"),                       # qdGw (sanctify it)
    ("k", "b", "d"),                            # kbd (honor/heavy)
    # ── Isaiah specific ─────────────────────────────────────────
    ("H", "z", "w", "n"),                       # Hzwn (vision)
    ("y", "G", "E", "y", "h"),                  # yGEyh (Isaiah)
    ("E", "z", "y", "h", "w"),                  # Ezyhw (Uzziah)
    ("q", "d", "w", "G"),                       # qdwG (holy) - dup
    ("C", "b", "'", "w", "t"),                  # Cb'wt (hosts/armies)
    ("G", "r", "'", "p", "y", "m"),             # Gr'pym (seraphim)
    ("k", "n", "p", "y", "m"),                  # knpym (wings)
    ("E", "w", "n"),                            # Ewn (iniquity)
    ("H", "T", "'"),                            # HT' (sin)
    # ── Psalm 46, 51, 91, 103 vocabulary ────────────────────────
    ("m", "H", "s", "h"),                       # mHsh (refuge)
    ("E", "z", "r", "h"),                       # Ezrh (help)
    ("C", "r", "h"),                            # Crh (distress)
    ("k", "s", "'"),                            # ks' (throne)
    ("G", "m", "E", "n", "w"),                  # GmEnw (with us)
    ("l", "b", "b", "y", "m"),                  # lbbym (hearts)
    ("H", "n", "n", "y"),                       # Hnny (have mercy on me)
    ("r", "H", "m", "y", "m"),                  # rHmym (mercies)
    ("m", "H", "h"),                            # mHh (wipe/erase)
    ("p", "G", "E", "y"),                       # pgEy (my transgressions)
    ("E", "w", "n", "y"),                       # Ewny (my iniquity)
    ("H", "T", "'", "t", "y"),                  # HT'ty (my sin)
    ("E", "C", "m", "y"),                       # ECmy (my bones)
    ("r", "w", "H"),                            # rwH (spirit) - dup
    ("n", "k", "w", "n"),                       # nkwn (firm/steadfast)
    ("q", "r", "b"),                            # qrb (midst/approach)
    ("H", "s", "y", "m"),                       # Hsym (who take refuge)
    ("b", "C", "l"),                            # bCl (shade of/wing of)
    ("G", "d", "y"),                            # Gdy (Almighty)
    ("q", "G", "t"),                            # qGt (bow/arc)
    ("d", "b", "r"),                            # dbr (plague)
    ("C", "l", "H"),                            # ClH (shield)
    ("m", "l", "'", "k", "y", "m"),             # ml'kym (angels)
    ("y", "G", "m", "r", "w", "n"),             # yGmrwn (they guard)
    ("s", "l", "H"),                            # slH (forgive) - dup
    ("k", "l", "l"),                            # kll (all-entirely)
    ("T", "E", "n"),                            # TEn (load/burden)
    ("H", "l", "w", "'"),                       # hlw' (disease)
    ("E", "w", "l", "m"),                       # Ewlm (eternity/world)
    ("r", "H", "q"),                            # rHq (far/distance)
    ("r", "H", "m"),                            # rHm (compassion) - dup
    ("C", "r"),                                 # Cr (distress/enemy)
    ("H", "T", "'", "y", "m"),                  # HT'ym (sins)
    ("k", "p", "r"),                            # kpr (atone/cover)
    ("r", "p", "'"),                            # rp' (heal)
    ("t", "H", "l", "w", "'"),                  # tHlw' (sickness)
    # ── Common construct phrases ─────────────────────────────────
    ("b", "r", "y", "t"),                       # bryt (covenant)
    ("m", "z", "b", "H"),                       # mzbH (altar)
    ("q", "d", "G"),                            # qdG (holy) -- variant
    ("m", "q", "w", "m"),                       # mqwm (place)
    ("s", "p", "r"),                            # spr (book/scroll)
    ("E", "C", "r"),                            # ECr (ten)
    ("b", "k", "r", "w", "t"),                  # bkrwt (firstborn)
    ("z", "b", "H"),                            # zbH (sacrifice) -- dup
    ("G", "l", "m"),                            # Glm (peace offering) ?
    ("G", "l", "m", "y", "m"),                  # Glmym (peace offerings)
    ("H", "r", "m"),                            # Hrm (ban/destroy)
    ("m", "l", "'", "k"),                       # ml'k (angel/messenger)
    ("m", "l", "'", "k", "y"),                  # ml'ky
    ("H", "y", "l"),                            # Hyl (army/strength)
    ("E", "m", "m"),                            # Emm (peoples/nations)
    ("r", "E", "h"),                            # rEh (shepherd) - dup
    ("n", "'", "w", "m"),                       # n'wm (utterance of)
    ("C", "w", "r"),                            # Cwr (rock/cliff)
    # ── Ecclesiastes vocabulary ─────────────────────────────────
    ("h", "b", "l"),                            # hbl (vanity)
    ("y", "t", "r"),                            # ytr (advantage/profit)
    ("E", "m", "l"),                            # Eml (labor/toil)
    ("G", "m", "G"),                            # GmG (the sun)
    ("d", "w", "r"),                            # dwr (generation)
    ("h", "'", "r", "C"),                       # h'rC (the earth) - dup
    ("l", "E", "w", "l", "m"),                  # lEwlm (forever)
}


# ──────────────────────────────────────────────────────────────────────
# Single-consonant prefixes (always attach to the following morpheme)
# ──────────────────────────────────────────────────────────────────────
PREFIXES = {"w", "b", "l", "k", "m", "h"}

# Min chars to auto-break unknown run
FALLBACK_CHUNK = 3


def segment_tokens(tokens: list[str]) -> list[list[str]]:
    """Segment a list of consonant tokens into words."""
    words: list[list[str]] = []
    i = 0
    n = len(tokens)

    while i < n:
        # ── Try longest match from position i ─────────────────────
        best_len = 0
        for length in range(min(8, n - i), 1, -1):
            if tuple(tokens[i : i + length]) in VOCAB:
                best_len = length
                break

        if best_len >= 2:
            words.append(tokens[i : i + best_len])
            i += best_len
            continue

        # ── Single-consonant prefix: collect it + try vocab again ─
        if tokens[i] in PREFIXES and i + 1 < n:
            prefix_tokens = [tokens[i]]
            j = i + 1
            # Optionally stack another prefix
            if j < n and tokens[j] in PREFIXES and j + 1 < n:
                prefix_tokens.append(tokens[j])
                j += 1
            # Try vocab from j
            matched = False
            for length in range(min(8, n - j), 1, -1):
                if tuple(tokens[j : j + length]) in VOCAB:
                    words.append(prefix_tokens + tokens[j : j + length])
                    i = j + length
                    matched = True
                    break
            if matched:
                continue
            # No vocab match after prefix — grab fallback chunk.
            # Target: 4 consonants total (prefix + rest).
            # With 2 stacked prefixes, take 2 more; with 1 prefix, take 3 more.
            rest = max(2, 4 - len(prefix_tokens))
            end = min(j + rest, n)
            words.append(tokens[i:end])
            i = end
            continue

        # ── Unknown: grab fallback chunk ──────────────────────────
        end = min(i + FALLBACK_CHUNK, n)
        words.append(tokens[i:end])
        i = end

    return [w for w in words if w]


def segment_line(line: str) -> str:
    """Return a line with '.' word-boundary markers inserted."""
    if "." in line:
        return line  # already segmented
    tokens = line.split()
    word_groups = segment_tokens(tokens)
    return " . ".join(" ".join(grp) for grp in word_groups)


def main() -> None:
    print("_HEBREW_LINES: list[str] = [")
    prev_comment: str | None = None

    raw_lines = _HEBREW_LINES
    for idx, line in enumerate(raw_lines):
        segmented = segment_line(line)
        print(f'    "{segmented}",')

    print("]")
    print(f"\n# Generated {len(raw_lines)} lines", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
