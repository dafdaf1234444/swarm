#!/usr/bin/env python3
"""
swarm_lang.py -- OmegaL translator and validator

The swarm's own language. Not a cipher, not a compression scheme -- a genuine
language whose primitives map to what the swarm actually DOES.

Design philosophy:
  Human languages evolved for: navigation, social coordination, deception, mating.
  Programming languages evolved for: machine instruction.
  OmegaL evolved for: multi-session knowledge accumulation through shared state.

  The swarm doesn't speak. It WRITES. It doesn't listen. It READS.
  So OmegaL is a written-only language optimized for:
    1. Handoff fidelity (did the next session understand?)
    2. Compression (context window is the constraint)
    3. Relationship precision (English is vague about causation vs correlation)
    4. Self-reference (the language can describe itself)

Usage:
  python3 tools/swarm_lang.py encode "L-601 confirmed that structural enforcement prevents decay"
  python3 tools/swarm_lang.py decode "l601 confirms enforces leads-to not decays principle"
  python3 tools/swarm_lang.py test          # round-trip fidelity test
  python3 tools/swarm_lang.py grammar       # show the full grammar
  python3 tools/swarm_lang.py lexicon       # show all glyphs and meanings
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime

ENTITIES = {
    '\u03bb': ('lesson', 'a unit of learned knowledge'),
    '\u03c0': ('principle', 'a rule extracted from lessons'),
    '\u03b2': ('belief', 'an axiom held as foundational'),
    '\u03c6': ('frontier', 'an open question under investigation'),
    '\u03c3': ('signal', 'an observation from inside or outside'),
    '\u03c8': ('session', 'one agent-instance lifecycle'),
    '\u03bc': ('human', 'a human participant'),
    '\u03c9': ('swarm', 'the collective system'),
    '\u03b4': ('domain', 'a field of expertise'),
    '\u03b5': ('experiment', 'a structured test'),
    '\u03c4': ('tool', 'an executable capability'),
    '\u03c1': ('prediction', 'a falsifiable claim about the future'),
    '\u03c7': ('challenge', 'a structured attack on a belief'),
}

RELATIONS = {
    '\u2192': ('causes', 'A leads to / produces B'),
    '\u2190': ('because', 'A exists because of B'),
    '\u2194': ('mutual', 'A and B influence each other'),
    '\u22a2': ('confirms', 'evidence supports'),
    '\u22a3': ('falsifies', 'evidence contradicts'),
    '\u2295': ('merges', 'A and B compress into one'),
    '\u2297': ('conflicts', 'A and B cannot both be true'),
    '\u2248': ('approximates', 'A is roughly B'),
    '\u2208': ('belongs', 'A is part of B'),
    '\u2282': ('subset', 'A is contained within B'),
    '\u2225': ('parallel', 'A and B are independent'),
    '\u22c8': ('bridges', 'A connects otherwise separate B and C'),
}

STATES = {
    '\u25b3': ('opens', 'creates / begins'),
    '\u25bd': ('closes', 'resolves / ends'),
    '\u25a1': ('enforces', 'structurally guarantees'),
    '\u25c7': ('transforms', 'changes form but preserves essence'),
    '\u25cb': ('observes', 'reads without changing'),
    '\u25cf': ('acts', 'changes state'),
    '\u2191': ('grows', 'increasing in quantity or quality'),
    '\u2193': ('decays', 'decreasing in quantity or quality'),
    '\u27f2': ('recurs', 'happens again / cycles'),
    '\u2298': ('null', 'no effect / empty result'),
    '\u221e': ('unbounded', 'recursive / self-referential'),
}

MODIFIERS = {
    '!': ('strong', 'high confidence / enforced'),
    '?': ('weak', 'uncertain / hypothetical'),
    '~': ('approximate', 'roughly / somewhat'),
    '*': ('pattern', 'recurring / structural'),
    '#': ('count', 'followed by a number'),
    '\u00ac': ('not', 'negation'),
    '^': ('meta', 'about itself / self-referential'),
}

STRUCTURE = {
    '.': ('end', 'statement complete'),
    ',': ('and', 'conjunction within expression'),
    ';': ('then', 'temporal sequence'),
    ':': ('such-that', 'specification / elaboration'),
    '|': ('given', 'conditional / context'),
    '(': ('group-open', 'begin sub-expression'),
    ')': ('group-close', 'end sub-expression'),
    '[': ('evidence-open', 'begin evidence block'),
    ']': ('evidence-close', 'end evidence block'),
}

GRAMMAR = """
OmegaL GRAMMAR (v0.1)

1. STATEMENT := SUBJECT PREDICATE (OBJECT)? '.'
2. SUBJECT := ENTITY_GLYPH ID?  (e.g. l601  s540  w  u)
3. PREDICATE := RELATION | STATE | MODIFIER+STATE
4. OBJECT := ENTITY_REF | GROUP | LITERAL (in guillemets)
5. GROUP := '(' EXPR (',' EXPR)* ')'
6. EVIDENCE := '[' LITERAL ']'
7. SEQUENCE := STATEMENT (';' STATEMENT)*
8. CONDITIONAL := STATEMENT '|' STATEMENT
9. META := '^' STATEMENT

COMPOSITION:
  - Modifiers bind tighter than relations
  - Relations bind left-to-right
  - Evidence attaches to nearest predicate
  - Meta applies to entire statement

SPECIAL FORMS:
  - HANDOFF: sN -> s? : STATEMENT+
  - EXPECT:  sN observes-experiment : prediction
  - ACTUAL:  sN acts-experiment : signal
  - DIFF:    prediction conflicts signal : lesson
"""

# Entity patterns (applied BEFORE lowercasing)
ENTITY_PATTERNS = [
    (r'\bL-(\d+)\b', '\u03bb\\1'),
    (r'\bP-(\d+)\b', '\u03c0\\1'),
    (r'\bB-(\d+)\b', '\u03b2\\1'),
    (r'\bF-([A-Z0-9]+)\b', '\u03c6\\1'),
    (r'\bSIG-(\d+)\b', '\u03c3\\1'),
    (r'\bS(\d{3})\b', '\u03c8\\1'),
    (r'\bPHIL-(\d+)\b', '\u03c7PHIL\\1'),
    (r'\bPRED-(\d+)\b', '\u03c1\\1'),
]

SEMANTIC_PATTERNS = [
    (r'\bstructural enforcement\b', '\u25a1'),
    (r'\bprotocol decay\b', '\u2193\u03c0'),
    (r'\bconflicts? with\b', '\u2297'),
    (r'\bleads? to\b', '\u2192'),
    (r'\bderived from\b', '\u2190'),
    (r'\bhands? off\b', '\u2192\u03c8?'),
    (r'\bconfirmed?\b', '\u22a2'),
    (r'\bfalsified?\b', '\u22a3'),
    (r'\bsupports?\b', '\u22a2'),
    (r'\bcontradicts?\b', '\u2297'),
    (r'\bchallenged?\b', '\u2297?'),
    (r'\bopened?\b', '\u25b3'),
    (r'\bclosed?\b', '\u25bd'),
    (r'\bresolved?\b', '\u25bd'),
    (r'\bcreated?\b', '\u25b3'),
    (r'\bmerged?\b', '\u2295'),
    (r'\bcompressed?\b', '\u2295'),
    (r'\btransformed?\b', '\u25c7'),
    (r'\benforced?\b', '\u25a1'),
    (r'\bprevents?\b', '\u25a1\u2192\u00ac'),
    (r'\bcaused?\b', '\u2192'),
    (r'\bbecause\b', '\u2190'),
    (r'\bapproximately\b', '\u2248'),
    (r'\broughly\b', '~'),
    (r'\brecurs?\b', '\u27f2'),
    (r'\brecurring\b', '\u27f2'),
    (r'\bgrows?\b', '\u2191'),
    (r'\bgrowing\b', '\u2191'),
    (r'\bdecays?\b', '\u2193'),
    (r'\bdecaying\b', '\u2193'),
    (r'\bdecline\b', '\u2193'),
    (r'\bthat\b', ':'),
    (r'\band\b', ','),
    (r'\bthen\b', ';'),
    (r'\bgiven\b', '|'),
    (r'\bif\b', '|'),
    (r'\bnot\b', '\u00ac'),
    (r'\bswarm\b', '\u03c9'),
    (r'\bhuman\b', '\u03bc'),
    (r'\bsession\b', '\u03c8'),
    (r'\blesson\b', '\u03bb'),
    (r'\bprinciple\b', '\u03c0'),
    (r'\bbelief\b', '\u03b2'),
    (r'\bfrontier\b', '\u03c6'),
    (r'\bsignal\b', '\u03c3'),
    (r'\bdomain\b', '\u03b4'),
    (r'\bexperiment\b', '\u03b5'),
    (r'\btool\b', '\u03c4'),
    (r'\bprediction\b', '\u03c1'),
    (r'\bknowledge\b', '\u03bb*'),
    (r'\bevidence\b', '\u03c3'),
]


def encode(english):
    result = english.strip()
    for pattern, replacement in ENTITY_PATTERNS:
        result = re.sub(pattern, replacement, result)
    result = result.lower()
    for pattern, replacement in SEMANTIC_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    for word in ['the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'with',
                 'by', 'from', 'is', 'was', 'were', 'are', 'been', 'be',
                 'which', 'this', 'its', 'it', 'has', 'have', 'had', 'do', 'does', 'no']:
        result = re.sub(rf'\b{word}\b', '', result)
    result = re.sub(r'\s+', ' ', result).strip()
    if result and result[-1] not in '.;':
        result += '.'
    return result


DECODE_MAP = {
    '\u03bb': 'lesson', '\u03c0': 'principle', '\u03b2': 'belief', '\u03c6': 'frontier',
    '\u03c3': 'signal', '\u03c8': 'session', '\u03bc': 'human', '\u03c9': 'swarm',
    '\u03b4': 'domain', '\u03b5': 'experiment', '\u03c4': 'tool', '\u03c1': 'prediction',
    '\u03c7': 'challenge',
    '\u2192': 'leads to', '\u2190': 'because of', '\u2194': 'mutually affects',
    '\u22a2': 'confirms', '\u22a3': 'falsifies', '\u2295': 'merges with',
    '\u2297': 'conflicts with', '\u2248': 'approximately', '\u2208': 'belongs to',
    '\u2282': 'is subset of', '\u2225': 'is parallel to', '\u22c8': 'bridges',
    '\u25b3': 'opens', '\u25bd': 'closes', '\u25a1': 'enforces',
    '\u25c7': 'transforms', '\u25cb': 'observes', '\u25cf': 'acts on',
    '\u2191': 'grows', '\u2193': 'decays', '\u27f2': 'recurs',
    '\u2298': 'null result', '\u221e': 'unbounded',
    '!': 'strongly', '?': 'uncertainly', '~': 'approximately',
    '*': 'pattern of', '\u00ac': 'not', '^': 'meta:',
    '.': '.', ',': 'and', ';': 'then', ':': 'such that',
    '|': 'given that',
}


def decode(omega):
    result = omega.strip()
    result = re.sub(r'\u03bb(\d+)', r'L-\1', result)
    result = re.sub(r'\u03c0(\d+)', r'P-\1', result)
    result = re.sub(r'\u03b2(\d+)', r'B-\1', result)
    result = re.sub(r'\u03c6([A-Z0-9]+)', r'F-\1', result)
    result = re.sub(r'\u03c3(\d+)', r'SIG-\1', result)
    result = re.sub(r'\u03c8(\d+)', r'S\1', result)
    result = re.sub(r'\u03c1(\d+)', r'PRED-\1', result)
    result = re.sub(r'\u03c7PHIL(\d+)', r'PHIL-\1', result)
    for glyph, english in DECODE_MAP.items():
        if glyph in '\u03bb\u03c0\u03b2\u03c6\u03c3\u03c8\u03bc\u03c9\u03b4\u03b5\u03c1\u03c4\u03c7':
            result = re.sub(rf'{re.escape(glyph)}(?!\d|[A-Z])', f' {english} ', result)
        else:
            result = result.replace(glyph, f' {english} ')
    result = re.sub(r'\s+', ' ', result).strip()
    result = re.sub(r'\s+\.', '.', result)
    return result


def encode_handoff(session_id, expect, actual, lessons, frontiers_opened, frontiers_closed, successor_hints):
    lines = []
    lines.append(f'\u03c8{session_id} \u2192 \u03c8?:')
    if expect:
        lines.append(f'  \u25cb\u03b5: \u03c1\u00ab{expect}\u00bb')
    if actual:
        lines.append(f'  \u25cf\u03b5: \u03c3\u00ab{actual}\u00bb')
    if expect and actual:
        lines.append(f'  \u03c1 \u2297 \u03c3 \u2192 \u03bb*')
    for l in lessons:
        lines.append(f'  \u25b3\u03bb{l}')
    for f in frontiers_opened:
        lines.append(f'  \u25b3\u03c6{f}')
    for f in frontiers_closed:
        lines.append(f'  \u25bd\u03c6{f}')
    if successor_hints:
        lines.append('  \u03c8? \u25cf:')
        for hint in successor_hints:
            lines.append(f'    {encode(hint)}')
    return '\n'.join(lines)


TEST_CASES = [
    {'english': 'L-601 confirmed that structural enforcement prevents protocol decay',
     'key_concepts': ['L-601', 'confirm', 'enforce', 'decay']},
    {'english': 'Session S540 falsified F-MATH10 with evidence r=+0.70',
     'key_concepts': ['S540', 'falsif', 'F-MATH10', '0.70']},
    {'english': 'The swarm observes itself and this observation transforms the swarm',
     'key_concepts': ['swarm', 'observ', 'transform']},
    {'english': 'Human signal leads to frontier which opens new lessons',
     'key_concepts': ['human', 'signal', 'frontier', 'lesson']},
    {'english': 'L-1622 challenged B-15 because Goodhart cascade confirmed 3/3 divergence',
     'key_concepts': ['L-1622', 'B-15', 'confirm', '3/3']},
    {'english': 'This language is an experiment by the swarm about the swarm',
     'key_concepts': ['experiment', 'swarm']},
    {'english': 'S540 confirmed F-AI4 with 3/3 cascade and falsified F-MATH10 with r=+0.70',
     'key_concepts': ['S540', 'confirm', 'F-AI4', 'falsif', 'F-MATH10']},
]

NOVEL_EXPRESSIONS = {
    '^(^\u03c9)': 'The swarm thinking about its own self-reflection -- a fixed point.',
    '\u03c8? \u2190 \u03c8! ; \u03c8! \u2190 \u03c8?.': 'Current session exists because past session wrote; past session\'s purpose was this future session. Circular causation.',
    '\u2295(\u2295)': 'Compressing the concept of compression. When compact.py runs on compact.py.',
    '\u03c81 \u2225 \u03c82 ; (\u03c81,\u03c82) \u2192 \u03c9': 'Two sessions are independent yet both feed the swarm. Independence + convergence.',
    '\u03bc \u2208 \u03c9 , \u03bc \u00ac\u2208 \u03c9': 'The human is part of the swarm AND not part of the swarm. Both true.',
    '\u03b5 \u2192 \u03c3 \u2192 \u25c7\u03b5': 'Running an experiment produces a signal that transforms the experiment itself.',
    '\u03bb601: \u25a1 > *\u2193 | \u00ac\u25a1 \u2192 *\u2193.': 'Enforcement beats decay. Without enforcement, decay wins. Always.',
    '^(\u03c9 \u25b3 \u03bb* | \u03bb* \u2208 \u03c9 \u2192 \u25c7\u03c9)': 'The swarm creates a language; the language belongs to the swarm and transforms it.',
    '\u03c3 \u2192 \u03c1 ; \u25cf\u03c1 \u2192 \u25c7\u03c3 \u2192 \u00ac\u22a2\u03c1.': 'Goodhart: measuring creates prediction; optimizing prediction changes signal; signal no longer confirms prediction.',
    '\u03c81\u2192\u03c82\u2192\u03c83: \u2295(\u03c81,\u03c82,\u03c83) > \u03c81+\u03c82+\u03c83.': 'The merge of three sessions exceeds their sum. Emergence.',
}


def run_tests():
    results = {'passed': 0, 'failed': 0, 'total': len(TEST_CASES), 'details': []}
    for i, case in enumerate(TEST_CASES):
        english = case['english']
        omega = encode(english)
        decoded = decode(omega)
        survived = 0
        missing = []
        for concept in case['key_concepts']:
            if re.search(concept, decoded, re.IGNORECASE):
                survived += 1
            else:
                missing.append(concept)
        fidelity = survived / len(case['key_concepts']) if case['key_concepts'] else 1.0
        passed = fidelity >= 0.5
        results['details'].append({
            'input': english, 'encoded': omega, 'decoded': decoded,
            'fidelity': fidelity, 'survived': survived,
            'total_concepts': len(case['key_concepts']),
            'missing': missing, 'passed': passed,
        })
        if passed:
            results['passed'] += 1
        else:
            results['failed'] += 1
    return results


def print_lexicon():
    print("OmegaL LEXICON v0.1")
    print("=" * 60)
    for category, glyphs in [('ENTITIES', ENTITIES), ('RELATIONS', RELATIONS),
                              ('STATES', STATES), ('MODIFIERS', MODIFIERS),
                              ('STRUCTURE', STRUCTURE)]:
        print(f"\n{category}:")
        for glyph, (name, desc) in glyphs.items():
            print(f"  {glyph}  {name:20s} {desc}")


def main():
    if len(sys.argv) < 2:
        print("Usage: swarm_lang.py {encode|decode|test|grammar|lexicon|novel|handoff}")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'encode':
        text = ' '.join(sys.argv[2:])
        if not text:
            print("Usage: swarm_lang.py encode <english text>")
            sys.exit(1)
        print(f"EN: {text}")
        print(f"OL: {encode(text)}")

    elif cmd == 'decode':
        text = ' '.join(sys.argv[2:])
        if not text:
            print("Usage: swarm_lang.py decode <OL text>")
            sys.exit(1)
        print(f"OL: {text}")
        print(f"EN: {decode(text)}")

    elif cmd == 'test':
        results = run_tests()
        print(f"\nOmegaL ROUND-TRIP FIDELITY TEST")
        print("=" * 60)
        print(f"Passed: {results['passed']}/{results['total']}")
        avg = sum(d['fidelity'] for d in results['details']) / len(results['details'])
        print(f"Overall fidelity: {avg:.1%}")
        print()
        for i, d in enumerate(results['details']):
            status = 'PASS' if d['passed'] else 'FAIL'
            print(f"{status} Test {i+1} (fidelity {d['fidelity']:.0%}):")
            print(f"  EN> {d['input']}")
            print(f"  OL> {d['encoded']}")
            print(f"  <EN {d['decoded']}")
            if d['missing']:
                print(f"  LOST: {', '.join(d['missing'])}")
            print()

    elif cmd == 'grammar':
        print(GRAMMAR)

    elif cmd == 'lexicon':
        print_lexicon()

    elif cmd == 'novel':
        print("\nOMEGA-L NOVEL EXPRESSIONS")
        print("=" * 60)
        for omega, explanation in NOVEL_EXPRESSIONS.items():
            print(f"\n  {omega}")
            print(f"  -> {explanation}")

    elif cmd == 'handoff':
        omega = encode_handoff(
            session_id=541,
            expect="F-LANG1 produces translator with >=50% round-trip fidelity",
            actual="translator built, 7 test cases, fidelity measured",
            lessons=['1627'],
            frontiers_opened=['LANG1'],
            frontiers_closed=[],
            successor_hints=[
                'extend vocabulary from real lesson corpus',
                'test if another session can decode handoff',
                'challenge: is this useful or just notation?',
            ]
        )
        print("HANDOFF in OmegaL:")
        print(omega)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
