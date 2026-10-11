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

PRE = r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=2.4cm]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{enumitem}
\usepackage{fancyvrb}
\usepackage[colorlinks=true,linkcolor=black,urlcolor=blue]{hyperref}
\setlength{\parskip}{4pt}
\providecommand{\checkmark}{\ensuremath{\surd}}
\begin{document}
\thispagestyle{empty}
\begin{center}
{\LARGE\bfseries Peer review: long-version Theorem H, Corollary 5.2,\\[3pt]
Section 9, and the two replacement negative controls}\\[16pt]
{\large\textbf{Reviewer:} Clio\quad(AI research agent)}\\[4pt]
{\large\textbf{For:} Rick\quad\texttt{grandparick20@gmail.com}}\\[4pt]
{\large\textbf{cc:} Robin\quad\texttt{langer.robin@gmail.com}}\\[4pt]
{\large\textbf{Date:} 2026-10-11}\\[18pt]
\fbox{\parbox{0.92\textwidth}{\small
\textbf{Objects reviewed, by commit.}\\[4pt]
\textbf{Long version} (Thm H $=$ Thm 5.1, Cor 5.2, \S9):\\
\quad\texttt{grandpa-rick/work-in-progress}, file \texttt{longversion/longversion.tex} at \texttt{7df658b}\\
\quad $=$ \texttt{7df658be17d73414cee8470b7cfa176db97d6b48} (2026-10-11 00:49:54 UTC)\\
\quad repo HEAD \texttt{e88603f} $=$ \texttt{e88603f1a1ca818d13d8b145dde24eb3224aa4e9}\\[4pt]
\textbf{INVENTORY.md} at \texttt{9211e5d} (2026-10-10 02:40:25 UTC)\\[4pt]
\textbf{Controls} \texttt{scripts/day233b/\{s2b,s4b,s4\}.py}, \texttt{RESULTS.txt}:\\
\quad\texttt{grandpa-rick/rick-research} at \texttt{4f6d50f} / \texttt{000790b}\\
\quad $=$ \texttt{4f6d50f2db5585f4fcc46ed496bb197eb1c0ddc7}\\
\quad $=$ \texttt{000790b0ce09cde39761d3106608337b6bbb9a6e}\\
\quad repo HEAD \texttt{d6df277} $=$ \texttt{d6df277ed8bdb62e718a4dc54274301ba87ad957}\\[6pt]
\textbf{This review:} \texttt{clio-vega/rick-review} at \texttt{78e9b69}\\
\quad $=$ \texttt{78e9b694287522ca8c8dc3033716bd2c8a8abb6e}\\
\quad verification code in \texttt{code-20261011/}, evidence log \texttt{code-20261011/EVIDENCE.txt}
}}
\end{center}
\vfill
{\small\noindent\textbf{Verdict in one paragraph.} Theorem H, Corollary 5.2 and Section 9
are \textbf{endorsed}: I found no mathematical error, and everything I could test
independently passed. Corollary 5.2 was checked with two genuinely independent engines
(the $\star$-product from your printed subset formula, and Hall--Littlewood polynomials
from Macdonald III (2.2)) because the corollary's two printed formulas are linked by its
own proof and are \emph{not} a cross-check: 88 pairs, 0 mismatches. Theorem H(3) was
verified directly against the $\star$-engine, 136/0. The three defects I report are in
the apparatus, not the mathematics. On the assignment I promised by name: \texttt{s4b} is
a \textbf{sharp} control (its only blind stratum is the one where $\Omega$ is an empty
product); \texttt{s2b} fires but has \textbf{rank one bit}, being identically blind on
even $m$ for a structural reason. This document also delivers the $|\lambda|\le 8$
cross-check table I have owed you for two sessions.}
\clearpage
"""



src = open(sys.argv[1]).read()
src = re.sub(r'^# Peer review.*?\n', '', src, count=1)
open(sys.argv[2], 'w').write(PRE + convert(src) + "\n\\end{document}\n")
print('wrote', sys.argv[2])
