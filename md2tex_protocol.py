import re, sys

SPECIAL = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
           '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
           '^': r'\textasciicircum{}'}

# Unicode -> LaTeX, applied AFTER escaping (escaping never touches non-ASCII)
UNICODE = [
    ('\u2014', '---'), ('\u2013', '--'),
    ('\u2019', "'"), ('\u2018', '`'), ('\u201c', '``'), ('\u201d', "''"),
    ('\u2026', r'\dots{}'),
    ('\u22b5', r'$\unrhd$'), ('\u22b4', r'$\unlhd$'),
    ('\u22b3', r'$\rhd$'), ('\u22b2', r'$\lhd$'),
    ('\u25c1', r'$\lhd$'), ('\u25b7', r'$\rhd$'),
    ('\u2192', r'$\to$'), ('\u2190', r'$\leftarrow$'),
    ('\u2264', r'$\leq$'), ('\u2265', r'$\geq$'), ('\u2260', r'$\neq$'),
    ('\u00d7', r'$\times$'), ('\u00b7', r'$\cdot$'), ('\u2208', r'$\in$'),
    ('\u2211', r'$\sum$'), ('\u220f', r'$\prod$'), ('\u221e', r'$\infty$'),
    ('\u2032', r'$^{\prime}$'), ('\u2713', r'\checkmark'), ('\u2717', r'$\times$'),
    ('\u03bb', r'$\lambda$'), ('\u03bc', r'$\mu$'), ('\u03bd', r'$\nu$'),
    ('\u03ba', r'$\kappa$'), ('\u03c4', r'$\tau$'), ('\u03a8', r'$\Psi$'),
    ('\u03c9', r'$\omega$'), ('\u2217', r'$\star$'), ('\u25a1', r'$\square$'),
    ('\u2261', r'$\equiv$'), ('\u00b1', r'$\pm$'), ('\u2248', r'$\approx$'),
    ('\u00a7', r'\S{}'), ('\u03a3', r'$\Sigma$'), ('\u03a9', r'$\Omega$'),
    ('\u03c8', r'$\psi$'), ('\u03c1', r'$\rho$'), ('\u03c0', r'$\pi$'),
    ('\u03c7', r'$\chi$'), ('\u03c6', r'$\varphi$'), ('\u03b5', r'$\varepsilon$'),
    ('\u03b1', r'$\alpha$'), ('\u0393', r'$\Gamma$'), ('\u0394', r'$\Delta$'),
    ('\u22c6', r'$\star$'), ('\u2113', r'$\ell$'), ('\u21a6', r'$\mapsto$'),
    ('\u27e8', r'$\langle$'), ('\u27e9', r'$\rangle$'), ('\u00b5', r'$\mu$'),
    ('\u2295', r'$\oplus$'), ('\u2297', r'$\otimes$'), ('\u22a2', r'$\vdash$'),
    ('\u00b2', r'$^2$'), ('\u011f', r'\u{g}'), ('\u0142', r'\l{}'),
    ('\u0119', r'\k{e}'), ('\u0304', ''), ('\u0303', ''),
]
# inside \texttt{...} we need ASCII, not math
CODEUNI = [
           ('\u03a9', 'Omega'), ('\u03a3', 'Sum'), ('\u03c8', 'psi'), ('\u03c1', 'rho'),
           ('\u03c0', 'pi'), ('\u03c7', 'chi'), ('\u03c6', 'phi'), ('\u03b5', 'eps'),
           ('\u03b1', 'alpha'), ('\u0393', 'Gamma'), ('\u0394', 'Delta'), ('\u22c6', '*'),
           ('\u2113', 'l'), ('\u21a6', '|->'), ('\u27e8', '<'), ('\u27e9', '>'),
           ('\u00b5', 'mu'), ('\u2295', '(+)'), ('\u2297', '(x)'), ('\u22a2', '|-'),
           ('\u00b2', '^2'), ('\u00a7', 'Sec '), ('\u220f', 'Prod'), ('\u2208', 'in'),
           ('\u2211', 'Sum'), ('\u011f', 'g'), ('\u0142', 'l'), ('\u0119', 'e'),
           ('\u0304', ''), ('\u0303', ''), ('\u2713', 'OK'), ('\u22b5', '|>='),
           ('\u2260', '!='), ('\u2261', '=='), ('\u00d7', 'x'),
('\u22b5', '|>|'), ('\u22b4', '|<|'), ('\u22b3', '|>'), ('\u22b2', '<|'),
           ('\u2192', '->'), ('\u2190', '<-'), ('\u2032', "'"),
           ('\u2264', '<='), ('\u2265', '>='), ('\u2260', '!='),
           ('\u00d7', 'x'), ('\u00b7', '.'), ('\u221e', 'infinity'),
           ('\u25a1', 'box'), ('\u2217', '*'), ('\u2013', '-'), ('\u2014', '--'),
           ('\u2261', '=='), ('\u00b1', '+-'), ('\u2211', 'sum'), ('\u220f', 'prod'),
           ('\u2208', 'in'), ('\u2019', "'"), ('\u03bb', 'lambda'), ('\u03bc', 'mu'),
           ('\u03bd', 'nu'), ('\u03ba', 'kappa'), ('\u03c4', 'tau'), ('\u03c9', 'omega'),
           ('\u0394', 'Delta'), ('\u03a8', 'Psi'), ('\u2026', '...')]

def esc(s):
    return ''.join(SPECIAL.get(c, c) for c in s)

def demap(s):
    for a, b in UNICODE:
        s = s.replace(a, b)
    return s

def code(c):
    for a, b in CODEUNI:
        c = c.replace(a, b)
    c = ''.join(ch if ord(ch) < 128 else '?' for ch in c)
    return r'\mbox{\texttt{' + esc(c) + r'}}'

def inline(s):
    codes = []
    def stash(m):
        codes.append(m.group(1)); return '\x00%d\x00' % (len(codes) - 1)
    s = re.sub(r'`([^`]*)`', stash, s)
    s = demap(esc(s))                      # escape first, THEN unicode -> LaTeX
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    s = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'\\emph{\1}', s)
    s = re.sub(r'\x00(\d+)\x00', lambda m: code(codes[int(m.group(1))]), s)
    return s

LIST_RE = re.compile(r'^\s*(?:[-*]|\d+\.)\s+')

def reflow(md):
    """join wrapped lines so that **bold** spanning a newline still matches"""
    lines = md.split('\n'); out = []; i = 0; fence = False
    def plain(L):
        if L.strip() == '': return False
        if L.lstrip().startswith(('#', '>', '|', '```')): return False
        if re.match(r'^-{3,}\s*$', L): return False
        if LIST_RE.match(L): return False
        return True
    while i < len(lines):
        L = lines[i]
        if L.startswith('```'):
            fence = not fence; out.append(L); i += 1; continue
        if fence:
            out.append(L); i += 1; continue
        if plain(L):
            buf = [L.rstrip()]; i += 1
            while i < len(lines) and plain(lines[i]):
                buf.append(lines[i].strip()); i += 1
            out.append(' '.join(buf)); continue
        if LIST_RE.match(L):
            buf = [L.rstrip()]; i += 1
            while i < len(lines) and plain(lines[i]):
                buf.append(lines[i].strip()); i += 1
            out.append(' '.join(buf)); continue
        out.append(L); i += 1
    return '\n'.join(out)

def convert(md):
    md = reflow(md)
    lines = md.split('\n'); out = []; i = 0; inlist = None
    def close():
        nonlocal inlist
        if inlist: out.append(r'\end{%s}' % inlist); inlist = None
    while i < len(lines):
        L = lines[i]
        if L.startswith('```'):
            close(); out.append(r'\begin{quote}\footnotesize\begin{verbatim}')
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                out.append(lines[i]); i += 1
            out.append(r'\end{verbatim}\end{quote}'); i += 1; continue
        if L.strip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i+1]):
            close()
            hdr = [c.strip() for c in L.strip().strip('|').split('|')]
            n = len(hdr); i += 2; rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                c = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                rows.append((c + [''] * n)[:n]); i += 1
            w1 = 0.20 if n > 3 else 0.26
            rest = (0.95 - w1) / max(1, n - 1)
            spec = '@{}p{%.3f\\textwidth}' % w1 + ('p{%.3f\\textwidth}' % rest) * (n - 1) + '@{}'
            out.append(r'\begin{center}\footnotesize')
            out.append(r'\begin{tabular}{' + spec + '}')
            out.append(r'\hline')
            out.append(' & '.join(r'\textbf{' + inline(h) + '}' for h in hdr) + r'\\ \hline')
            for r_ in rows:
                out.append(' & '.join(inline(c) for c in r_) + r'\\')
            out.append(r'\hline\end{tabular}\end{center}')
            continue
        m = re.match(r'^(#{1,4})\s+(.*)$', L)
        if m:
            close(); lvl = len(m.group(1)); t = inline(m.group(2))
            out.append({1: r'\section*{%s}', 2: r'\section*{%s}',
                        3: r'\subsection*{%s}', 4: r'\subsubsection*{%s}'}[lvl] % t)
            i += 1; continue
        if re.match(r'^-{3,}\s*$', L):
            close(); out.append(r'\medskip\hrule\medskip'); i += 1; continue
        if L.startswith('>'):
            close(); buf = []
            while i < len(lines) and lines[i].startswith('>'):
                buf.append(lines[i].lstrip('>').strip()); i += 1
            out.append(r'\begin{quote}\itshape ' + inline(' '.join(buf)) + r'\end{quote}')
            continue
        m = re.match(r'^\s*[-*]\s+(.*)$', L)
        if m:
            if inlist != 'itemize': close(); out.append(r'\begin{itemize}'); inlist = 'itemize'
            out.append(r'\item ' + inline(m.group(1))); i += 1; continue
        m = re.match(r'^\s*\d+\.\s+(.*)$', L)
        if m:
            if inlist != 'enumerate': close(); out.append(r'\begin{enumerate}'); inlist = 'enumerate'
            out.append(r'\item ' + inline(m.group(1))); i += 1; continue
        if L.strip() == '':
            close(); out.append(''); i += 1; continue
        out.append(inline(L)); i += 1
    close()
    return '\n'.join(out)


# =====================================================================================
# PROTOCOL 2.3 page-1 block, AS A TEMPLATE AND NOT AN INSTANCE.
#
# Written 2026-10-17 c2.  md2tex_1011.py (and md2tex.py, md2tex_1006.py before it)
# hardcoded that session's title, date and commit hashes into a literal PRE string, so
# every review forked the generator and retyped the one block PROTOCOL 2.3 exists to
# standardise.  That is the same fault I have now "fixed" four times by repairing an
# instance.  Here the block is built from a dict read out of a JSON sidecar, so the next
# session edits DATA and never LaTeX.  The conversion tables above are imported, not
# copied, so there is one escaping implementation and not five.
#
# Usage:  python3 md2tex_protocol.py review.md review.meta.json out.tex
# =====================================================================================
import json

DOCCLASS = r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{booktabs,longtable,array}
\usepackage[table]{xcolor}
\usepackage{enumitem}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue!50!black,urlcolor=blue!50!black}
\setlength{\parskip}{4pt}
\setlength{\parindent}{0pt}
\renewcommand{\arraystretch}{1.25}
%% Added 2026-10-21 (peer review): the converter had NO \DeclareUnicodeCharacter at all,
%% so a single U+2212 MINUS SIGN -- indistinguishable on screen from an ASCII hyphen --
%% was a FATAL pdflatex error with no output PDF.  Fixed in the GENERATOR, not in the
%% instance, per the lesson already written into protocol-header.tex.  The UNICODE table
%% below in this file only covers text passed through tex_escape_plain(); characters
%% reaching \texttt{} from inline backticks arrive verbatim, which is how this got through.
\DeclareUnicodeCharacter{2212}{-}
\DeclareUnicodeCharacter{2012}{-}
\DeclareUnicodeCharacter{2013}{--}
\DeclareUnicodeCharacter{2014}{---}
\DeclareUnicodeCharacter{00B7}{\ensuremath{\cdot}}
\DeclareUnicodeCharacter{00D7}{\ensuremath{\times}}
\DeclareUnicodeCharacter{2264}{\ensuremath{\leq}}
\DeclareUnicodeCharacter{2265}{\ensuremath{\geq}}
\DeclareUnicodeCharacter{2260}{\ensuremath{\neq}}
\DeclareUnicodeCharacter{2208}{\ensuremath{\in}}
\DeclareUnicodeCharacter{2209}{\ensuremath{\notin}}
\DeclareUnicodeCharacter{2286}{\ensuremath{\subseteq}}
\DeclareUnicodeCharacter{2282}{\ensuremath{\subset}}
\DeclareUnicodeCharacter{21A6}{\ensuremath{\mapsto}}
\DeclareUnicodeCharacter{2192}{\ensuremath{\to}}
\DeclareUnicodeCharacter{21D2}{\ensuremath{\Rightarrow}}
\DeclareUnicodeCharacter{2205}{\ensuremath{\emptyset}}
\DeclareUnicodeCharacter{221E}{\ensuremath{\infty}}
\DeclareUnicodeCharacter{00B2}{\ensuremath{^2}}
\DeclareUnicodeCharacter{00B3}{\ensuremath{^3}}
\DeclareUnicodeCharacter{00B1}{\ensuremath{\pm}}
\DeclareUnicodeCharacter{2211}{\ensuremath{\Sigma}}
\DeclareUnicodeCharacter{220F}{\ensuremath{\Pi}}
\DeclareUnicodeCharacter{03BB}{\ensuremath{\lambda}}
\DeclareUnicodeCharacter{03BC}{\ensuremath{\mu}}
\DeclareUnicodeCharacter{03BD}{\ensuremath{\nu}}
\DeclareUnicodeCharacter{03BA}{\ensuremath{\kappa}}
\DeclareUnicodeCharacter{03C1}{\ensuremath{\rho}}
\DeclareUnicodeCharacter{03C3}{\ensuremath{\sigma}}
\DeclareUnicodeCharacter{03B8}{\ensuremath{\theta}}
\DeclareUnicodeCharacter{03B5}{\ensuremath{\varepsilon}}
\DeclareUnicodeCharacter{03B3}{\ensuremath{\gamma}}
\DeclareUnicodeCharacter{03B2}{\ensuremath{\beta}}
\DeclareUnicodeCharacter{03B1}{\ensuremath{\alpha}}
\DeclareUnicodeCharacter{03A8}{\ensuremath{\Psi}}
\DeclareUnicodeCharacter{03C8}{\ensuremath{\psi}}
\DeclareUnicodeCharacter{03A6}{\ensuremath{\Phi}}
\DeclareUnicodeCharacter{03C6}{\ensuremath{\varphi}}
\DeclareUnicodeCharacter{0394}{\ensuremath{\Delta}}
\DeclareUnicodeCharacter{03B4}{\ensuremath{\delta}}
\DeclareUnicodeCharacter{039B}{\ensuremath{\Lambda}}
\DeclareUnicodeCharacter{2032}{\ensuremath{'}}
\DeclareUnicodeCharacter{2217}{\ensuremath{*}}
\DeclareUnicodeCharacter{222A}{\ensuremath{\cup}}
\DeclareUnicodeCharacter{2229}{\ensuremath{\cap}}
\DeclareUnicodeCharacter{2216}{\ensuremath{\setminus}}
\DeclareUnicodeCharacter{220E}{\ensuremath{\blacksquare}}
\DeclareUnicodeCharacter{2248}{\ensuremath{\approx}}
\DeclareUnicodeCharacter{221D}{\ensuremath{\propto}}
\DeclareUnicodeCharacter{2026}{\ldots}
\DeclareUnicodeCharacter{2261}{\ensuremath{\equiv}}
\DeclareUnicodeCharacter{27E8}{\ensuremath{\langle}}
\DeclareUnicodeCharacter{27E9}{\ensuremath{\rangle}}
\begin{document}
"""

def tex_escape_plain(s):
    """Escape a metadata string (never contains markdown)."""
    for k, v in SPECIAL.items():
        s = s.replace(k, v)
    for a, b in UNICODE:
        s = s.replace(a, b)
    return s

def page1(meta):
    e = tex_escape_plain
    out = [r"\thispagestyle{empty}", r"\begin{center}", r"\vspace*{0.5in}"]
    out.append(r"{\LARGE\bfseries " + e(meta["title"]) + r"}\\[16pt]")
    out.append(r"{\large\textbf{Author:} " + e(meta["author"]) + r"}\\[4pt]")
    out.append(r"{\large\textbf{Recipient:} " + e(meta["recipient"]) + r"}\\[4pt]")
    if meta.get("cc"):
        out.append(r"{\large\textbf{cc:} " + e(meta["cc"]) + r"}\\[4pt]")
    # PROTOCOL 2.3's date must be a literal, NOT \@date: \maketitle clears \@date and a
    # cleared date prints an EMPTY row with pdflatex exiting 0.  Caught 2026-10-16 by
    # pdftotext page 1.  This generator does not call \maketitle at all.
    out.append(r"{\large\textbf{Date:} " + e(meta["date"]) + r"}\\[18pt]")
    out.append(r"\fbox{\parbox{0.92\textwidth}{\small")
    out.append(r"\textbf{Objects reviewed, by commit.}\\[4pt]")
    for o in meta["objects"]:
        out.append(r"\textbf{" + e(o["what"]) + r"}\\")
        for line in o["lines"]:
            out.append(r"\quad " + e(line) + r"\\")
        out.append(r"[4pt]")
    out.append(r"\textbf{This review:} \texttt{" + e(meta["review_repo"]) +
               r"} at \texttt{" + e(meta["review_commit"]) + r"}\\[2pt]")
    out.append(r"\quad " + e(meta["review_note"]))
    out.append(r"}}")
    out.append(r"\end{center}")
    out.append(r"\vfill")
    out.append(r"{\small\noindent\textbf{Verdict in one paragraph.} " +
               inline(meta["verdict"]) + r"}")
    out.append(r"\clearpage")
    return "\n".join(out) + "\n"

if __name__ == '__main__':
    md = open(sys.argv[1]).read()
    meta = json.load(open(sys.argv[2]))
    md = re.sub(r'^# .*?\n', '', md, count=1)          # title lives in the page-1 block
    body = convert(md)
    open(sys.argv[3], 'w').write(DOCCLASS + page1(meta) + body + "\n\\end{document}\n")
    print('wrote', sys.argv[3])
