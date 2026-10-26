"""
bookfig.py -- figure formatting for
"Introduction to statistical physics for non-physicists" (Kuehn, Vivo, Zamponi).

Every figure of the book is saved through `save()`, which brings it to its
printed size so that all text prints at the same size, whatever the width at
which the figure is included in the book.

    native width  = (width in the book, as a fraction of \\textwidth) * TEXTWIDTH / SCALE
    printed text  = native text * SCALE        (12 pt ticks -> 9 pt in print)

The plotting code is left as written: `save()` resizes the finished figure,
sets the size of every piece of text according to its role (tick labels, axis
labels, legend, annotations, panel letters) and rescales line widths and
marker sizes so that the printed figure looks as it did before.

Usage (the \\includegraphics width in the .tex file must be the same number):

    import matplotlib.pyplot as plt
    from bookfig import setup, save, HALF, SINGLE, FULL
    setup()
    plt.plot(x, y)
    save('../Figs_3/gp.pdf', SINGLE)
"""
import re
import matplotlib as mpl
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- page geometry
TEXTWIDTH_IN = 131 / 25.4   # pinchcrn \textwidth = 131 mm
SCALE = 0.75                # printed size / native size

# Standard widths, as fractions of \textwidth (the \includegraphics width).
HALF = 0.49                 # two panels side by side
SINGLE = 0.70               # a single plot
FULL = 1.00                 # a multi-panel figure saved as one file
ASPECT = 0.75               # height / width of a single-axes plot

# ---------------------------------------------------------------- text sizes (native pt)
FS_TICK = 12                # -> 9 pt in print
FS_LABEL = 13               # axis labels and titles
FS_LEGEND = 11
FS_TEXT = 12                # annotations
FS_PANEL = 14               # panel letters a, b, (a), ...

# line widths and marker sizes (native pt) are kept within these bounds
LW_MIN, LW_MAX = 0.9, 2.4
MS_MIN, MS_MAX = 3.0, 8.0


def setup():
    """Book style for new figures (call once, after importing pyplot)."""
    mpl.rcParams.update({
        'pdf.fonttype': 42, 'ps.fonttype': 42,
        'font.family': 'serif', 'font.serif': ['DejaVu Serif'],
        'mathtext.fontset': 'cm',
        'font.size': FS_TEXT, 'axes.labelsize': FS_LABEL, 'axes.titlesize': FS_LABEL,
        'xtick.labelsize': FS_TICK, 'ytick.labelsize': FS_TICK,
        'legend.fontsize': FS_LEGEND,
        'figure.figsize': (HALF * TEXTWIDTH_IN / SCALE, ASPECT * HALF * TEXTWIDTH_IN / SCALE),
        'lines.linewidth': 1.5, 'axes.linewidth': 0.8,
        'savefig.dpi': 300,
    })


_PANEL = re.compile(r'^\s*(\$\{?\\bf\s*\{?\s*\(?[a-z]\)?\s*\}?\}?\$|\(?[a-z]\)?|\$\(?[a-z]\)?\$)\s*$')


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def _is_panel_letter(t, label_size):
    s = t.get_text()
    return bool(_PANEL.match(s)) or (len(s) <= 12 and '\\bf' in s and t.get_fontsize() > 1.2 * label_size)


def _format(fig, k):
    """Set text sizes by role and rescale lines/markers by k (= new/old width)."""
    texts_done = set()

    def size(t, s, **kw):
        t.set_fontsize(s)
        t.set_fontfamily('serif')
        for a, v in kw.items():
            getattr(t, 'set_' + a)(v)
        texts_done.add(id(t))

    for t in fig.texts:                                   # suptitle, figure-level text
        size(t, FS_PANEL if _is_panel_letter(t, 99) else FS_LABEL)
    for ax in fig.axes:
        label_size = ax.xaxis.label.get_fontsize()
        size(ax.xaxis.label, FS_LABEL)
        size(ax.yaxis.label, FS_LABEL)
        for t in (ax.title, ax._left_title, ax._right_title):
            size(t, FS_LABEL)
        ax.tick_params(which='major', labelsize=FS_TICK, width=0.8, length=3.5)
        ax.tick_params(which='minor', width=0.6, length=2.0)
        for t in ax.get_xticklabels(which='both') + ax.get_yticklabels(which='both'):
            t.set_fontfamily('serif')
        for t in (ax.xaxis.get_offset_text(), ax.yaxis.get_offset_text()):
            size(t, FS_TICK)
        for sp in ax.spines.values():
            sp.set_linewidth(0.8)
        for t in ax.texts:
            if _is_panel_letter(t, label_size):
                size(t, FS_PANEL)
            else:
                size(t, FS_TEXT)
        for ln in ax.lines:
            ln.set_linewidth(_clamp(ln.get_linewidth() * k, LW_MIN, LW_MAX))
            ln.set_markersize(_clamp(ln.get_markersize() * k, MS_MIN, MS_MAX))
            ln.set_markeredgewidth(_clamp(ln.get_markeredgewidth() * k, 0.5, 1.5))
        for c in ax.collections:
            lw = c.get_linewidths()
            if len(lw):
                c.set_linewidths([max(0.25, w * k) for w in lw])
            if hasattr(c, 'get_sizes') and len(c.get_sizes()):
                c.set_sizes([_clamp(s * k * k, MS_MIN ** 2, MS_MAX ** 2) for s in c.get_sizes()])
        for p in ax.patches:
            p.set_linewidth(max(0.25, p.get_linewidth() * k))
        if ax.get_legend() is not None:
            _rebuild_legend(ax, ax.get_legend())
    for leg in fig.legends:
        for t in leg.get_texts():
            size(t, FS_LEGEND)


def _rebuild_legend(ax, leg):
    """Re-create a legend at FS_LEGEND, keeping its placement and options.
    (A legend's spacings are fixed in units of the font size it was created with,
    so only changing its text size would leave a box of the old size.)"""
    texts = [t.get_text() for t in leg.get_texts()]
    handles = list(getattr(leg, 'legend_handles', None) or leg.legendHandles)
    # use the plotted artists themselves where possible (they carry the new line widths)
    hl, ll = ax.get_legend_handles_labels()
    lookup = dict(zip(ll, hl))
    handles = [lookup.get(t, h) for t, h in zip(texts, handles)]
    bb = leg.get_bbox_to_anchor().transformed(ax.transAxes.inverted())
    anchor = (bb.x0, bb.y0, bb.width, bb.height)
    kw = dict(loc=leg._loc, bbox_to_anchor=anchor, ncols=leg._ncols,
              frameon=leg.get_frame_on(), fontsize=FS_LEGEND,
              title=leg.get_title().get_text() or None, title_fontsize=FS_LEGEND,
              handlelength=min(leg.handlelength, 1.6), handletextpad=leg.handletextpad,
              labelspacing=leg.labelspacing, columnspacing=leg.columnspacing,
              borderpad=leg.borderpad, borderaxespad=leg.borderaxespad)
    if leg.get_frame_on():
        kw['framealpha'] = leg.get_frame().get_alpha()
    leg.remove()
    new = ax.legend(handles, texts, **kw)
    for t in new.get_texts():
        t.set_fontfamily('serif')


def _thin_ticks(fig):
    """Ask for fewer ticks on linear axes whose tick labels overlap (larger fonts need more room)."""
    fig.canvas.draw()                       # tick-label texts exist only after a draw
    r = fig.canvas.get_renderer()
    for ax in fig.axes:
        for name, axis, lo, hi in (('x', ax.xaxis, 'x0', 'x1'), ('y', ax.yaxis, 'y0', 'y1')):
            if axis.get_scale() != 'linear' or not isinstance(axis.get_major_locator(), mpl.ticker.MaxNLocator):
                continue
            for _ in range(4):
                bb = sorted((t.get_window_extent(r) for t in axis.get_ticklabels() if t.get_visible() and t.get_text()),
                            key=lambda b: getattr(b, lo))
                if all(getattr(a, hi) + 3 < getattr(b, lo) for a, b in zip(bb, bb[1:])):
                    break
                ax.locator_params(axis=name, nbins=max(2, len(bb) - 2))
                fig.canvas.draw()


def save(path, width, aspect=None, fig=None, layout=True, close=False):
    """Bring `fig` (default: the current figure) to its printed size and save it.

    path   : output file, e.g. '../Figs_7/fmT2.pdf'
    width  : width at which the figure is included in the book, as a fraction of
             \\textwidth (HALF, SINGLE, FULL or any number); must match the .tex file
    aspect : height/width; default ASPECT for a single-axes plot, otherwise the
             figure's own aspect ratio
    layout : apply tight_layout (set False if the figure has a hand-made layout)
    """
    fig = fig or plt.gcf()
    w0, h0 = fig.get_size_inches()
    W = width * TEXTWIDTH_IN / SCALE                  # target width of the saved file
    if aspect is None:
        axes = [a for a in fig.axes if a.get_visible() and a.axison]
        single = len(axes) == 1 and not axes[0].images
        aspect = ASPECT if single else h0 / w0
    _format(fig, min(1.0, W / w0))   # shrink lines of large legacy figures, never thicken

    # fit the *cropped* figure to exactly W inches, so that SCALE holds in print
    pad = 0.02
    fw, fh = W, W * aspect
    for _ in range(6):
        fig.set_size_inches(fw, fh)
        if layout:
            try:
                fig.tight_layout(pad=0.3)
            except Exception:
                pass
        bb = fig.get_tightbbox(fig.canvas.get_renderer())
        r = W / (bb.width + 2 * pad)
        if abs(r - 1) < 0.003:
            break
        fw, fh = fw * r, fh * r
    _thin_ticks(fig)
    fig.savefig(path, bbox_inches='tight', pad_inches=pad,
                metadata={'CreationDate': None, 'ModDate': None, 'Creator': 'bookfig.py'})
    if close:
        plt.close(fig)
    return path
