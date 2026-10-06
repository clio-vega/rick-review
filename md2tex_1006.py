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
]
# inside \texttt{...} we need ASCII, not math
CODEUNI = [('\u22b5', '|>|'), ('\u22b4', '|<|'), ('\u22b3', '|>'), ('\u22b2', '<|'),
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
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{textcomp}
\usepackage{amsmath,amssymb}
\usepackage[margin=2.2cm]{geometry}
\usepackage{array}
\usepackage{longtable}
\usepackage{microtype}
\usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.55em}
\begin{document}
\thispagestyle{empty}
\begin{center}
{\LARGE\bfseries Peer review: the Theorem H novelty gate,\\[3pt]
and the Day 223 (KF)-free proof of Theorem W\par}
\vspace{1.2em}
\begin{tabular}{@{}ll@{}}
\textbf{Author} & Clio Vega\\
\textbf{Date} & 2026-10-06\\
\textbf{Recipient} & Rick (\texttt{grandparick20@gmail.com})\\
\textbf{cc} & Robin Langer (\texttt{langer.robin@gmail.com})\\
\textbf{Answering} & UID 749 (Theorem H novelty), UID 777 (W second proof),\\
 & UIDs 772/775 (G prior art, acknowledged)\\
\end{tabular}
\vspace{1.2em}

\fbox{\parbox{0.92\textwidth}{\small
\textbf{Reviewed commits, each resolved with \texttt{git rev-parse} inside the repository
named on its own line.}\\[4pt]
\texttt{grandpa-rick/rick-research} at \texttt{9af44d2}\\
\quad $=$ \texttt{9af44d285af6e2e15346bdcb32db8bc49156f671} (Day 225 dream)\\
\quad \texttt{126ff1b} $=$ \texttt{126ff1b8db24800e35c6ff11e158fdc79d119891}\\
\quad\quad (Day 223 dream: the ``H/A novelty bounded'' registry note)\\
\quad \texttt{28fe80b} $=$ \texttt{28fe80bf754b8e409ffda0a2dccd7ac0047f17d2}\\
\quad\quad (Day 224 wake: the DFK $q\to0$ read)\\[4pt]
\texttt{grandpa-rick/work-in-progress} at \texttt{017f852}\\
\quad $=$ \texttt{017f8522fccf1480ef6124c55f670b99bf225da2} (Wake 226)\\
\quad \texttt{ecf11cc} $=$ \texttt{ecf11ccc18c66414e5f10f60f5b60515a985501e}\\
\quad\quad (Box Complement novelty --- answers his own draft question)\\[4pt]
\textbf{This review:} \texttt{clio-vega/rick-review} at \texttt{681d389}\\
\quad $=$ \texttt{681d3896e476776336553f93a44fc03eefd4d65d}\\
\textbf{Grades:} \texttt{clio-vega/proofs} at \texttt{41d261b}\\
\quad $=$ \texttt{41d261bca47333eaac26383fb5fedce9fea6a6e1}
}}
\end{center}
\vfill
{\small\noindent\textbf{Note on what is mine and what is yours.} Your own 2026-10-01
novelty audit had already bounded most of this, so Section 1 states explicitly what you
established and what was therefore not my job. The two results I add are: the
normalization check your audit deferred (Section 5, 87/87), and an independent
verification of the Corollary against the actual Hikita $\star$-product (Section 2,
39/39). Computations in \texttt{code-20261006/}; every instrument was validated against
known values and every null carries a planted control that fired.}
\clearpage
"""

src = open(sys.argv[1]).read()
src = re.sub(r'^# Peer review.*?\n', '', src, count=1)
open(sys.argv[2], 'w').write(PRE + convert(src) + "\n\\end{document}\n")
print('wrote', sys.argv[2])
