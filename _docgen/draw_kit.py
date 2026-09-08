"""Shared visual language for Pharmacy POS diagrams and UI prototypes."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyBboxPatch,
    FancyArrowPatch,
    Circle,
    Rectangle,
    Ellipse,
    RegularPolygon,
    Arc,
    Polygon,
)
from matplotlib.lines import Line2D

NAVY = "#0D3B4C"
TEAL = "#1A7A6D"
TEAL_DK = "#145E54"
TEAL_LT = "#D7EDE9"
SAND = "#F4EFE6"
GOLD = "#C4A35A"
INK = "#1A2332"
MUTED = "#5B6770"
PAPER = "#F7FAF9"
WHITE = "#FFFFFF"
ROSE = "#B85C38"
BOX = "#E8EEF0"
ADMIN = "#1A7A6D"
PHARM = "#0D3B4C"
EXT = "#6B7280"

ROOT = Path(r"C:\Users\bwaly\Desktop\Group 20 Pharmacy-project\Pharmacy-POS")
UC_DIR = ROOT / "Diagrams" / "Use-Cases"
SSD_DIR = ROOT / "Diagrams" / "SSD"
DM_DIR = ROOT / "Diagrams" / "Domain-Model"
DCD_DIR = ROOT / "Diagrams" / "Design-Class"
ARCH_DIR = ROOT / "Diagrams" / "Architecture"
DB_DIR = ROOT / "Diagrams" / "Database"
UP_DIR = ROOT / "Diagrams" / "UP-Planning"
UI_DIR = ROOT / "UI-Prototypes"


def fig_ax(w=16, h=10, title=None, ymax=100):
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(w, h), dpi=160)
    fig.patch.set_facecolor(PAPER)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    ax.set_facecolor(PAPER)
    if title:
        ax.text(50, ymax - 3.2, title, ha="center", va="center", fontsize=15,
                color=NAVY, fontweight="bold")
    return fig, ax


def save(fig, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def rbox(ax, x, y, w, h, fc=WHITE, ec=NAVY, lw=1.4, radius=0.8, z=2):
    p = FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0.15,rounding_size={radius}",
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z,
    )
    ax.add_patch(p)
    return p


def text(ax, x, y, s, **kw):
    defaults = dict(ha="center", va="center", color=INK, fontsize=9, zorder=4)
    defaults.update(kw)
    ax.text(x, y, s, **defaults)


def arrow(ax, x1, y1, x2, y2, color=NAVY, lw=1.3, style="-|>", rad=0, ls="-"):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle=style, mutation_scale=12, linewidth=lw,
            color=color, linestyle=ls,
            connectionstyle=f"arc3,rad={rad}", zorder=3,
        )
    )


def actor(ax, x, y, label, color=NAVY, sub=None):
    """UML stick figure. (x,y) is head centre."""
    ax.add_patch(Circle((x, y), 1.35, fill=False, edgecolor=color, lw=1.6, zorder=4))
    ax.plot([x, x], [y - 1.35, y - 5.1], color=color, lw=1.6, zorder=4)
    ax.plot([x - 2.0, x + 2.0], [y - 2.6, y - 2.6], color=color, lw=1.6, zorder=4)
    ax.plot([x, x - 1.7], [y - 5.1, y - 7.6], color=color, lw=1.6, zorder=4)
    ax.plot([x, x + 1.7], [y - 5.1, y - 7.6], color=color, lw=1.6, zorder=4)
    text(ax, x, y - 9.2, label, color=color, fontsize=8.5, fontweight="bold")
    if sub:
        text(ax, x, y - 11.0, sub, color=MUTED, fontsize=7)


def usecase(ax, x, y, w, h, label, fc=TEAL_LT, ec=TEAL):
    e = Ellipse((x, y), w, h, facecolor=fc, edgecolor=ec, lw=1.5, zorder=3)
    ax.add_patch(e)
    text(ax, x, y, label, fontsize=8, color=NAVY, fontweight="medium")


def system_box(ax, x, y, w, h, title="Pharmacy POS"):
    rbox(ax, x, y, w, h, fc="#FBFDFC", ec=TEAL, lw=1.8, radius=0.4)
    text(ax, x + w / 2, y + h - 2.4, title, fontsize=11, color=TEAL, fontweight="bold")


def class_box(ax, x, y, w, h, name, attrs=None, methods=None, stereotype=None, header=TEAL):
    """UML class: name / attributes / methods. (x,y) bottom-left."""
    rbox(ax, x, y, w, h, fc=WHITE, ec=NAVY, lw=1.2, radius=0.15)
    name_h = 6.2 if not stereotype else 8.2
    ax.add_patch(Rectangle((x, y + h - name_h), w, name_h, facecolor=header, edgecolor=NAVY, lw=0, zorder=3))
    cy = y + h - 3.1
    if stereotype:
        text(ax, x + w / 2, y + h - 2.2, stereotype, fontsize=6.5, color=WHITE, style="italic")
        cy = y + h - 5.2
    text(ax, x + w / 2, cy, name, fontsize=8.2, color=WHITE, fontweight="bold")
    # divider lines
    body_top = y + h - name_h
    mid = body_top
    if attrs:
        ah = min(len(attrs) * 2.15 + 0.8, body_top - y - (8 if methods else 1))
        mid = body_top - ah
        ax.plot([x, x + w], [mid, mid], color=NAVY, lw=0.7, zorder=4)
        for i, a in enumerate(attrs):
            text(ax, x + 1.1, body_top - 1.6 - i * 2.15, a, ha="left", fontsize=6.4, color=INK, family="DejaVu Sans Mono")
    if methods:
        ax.plot([x, x + w], [mid, mid] if attrs else [body_top, body_top], color=NAVY, lw=0.7, zorder=4)
        start = (mid if attrs else body_top) - 1.6
        for i, m in enumerate(methods):
            text(ax, x + 1.1, start - i * 2.15, m, ha="left", fontsize=6.4, color=INK, family="DejaVu Sans Mono")


def assoc(ax, x1, y1, x2, y2, name="", m1="", m2="", color=NAVY):
    ax.plot([x1, x2], [y1, y2], color=color, lw=1.05, zorder=2)
    if name:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        text(ax, mx, my + 1.3, name, fontsize=6.3, color=TEAL_DK, style="italic")
    if m1:
        text(ax, x1 + (2 if x2 > x1 else -2), y1 + 1.1, m1, fontsize=6.2, color=NAVY)
    if m2:
        text(ax, x2 + (2 if x1 > x2 else -2), y2 + 1.1, m2, fontsize=6.2, color=NAVY)


def lifeline(ax, x, y0, y1, title, box_w=16, actor_mode=False):
    if actor_mode:
        actor(ax, x, y0 + 8.5, title, color=PHARM)
        ax.plot([x, x], [y0 - 2, y1], color=NAVY, ls=(0, (3, 3)), lw=1.1)
        return x, y0 - 2, y1
    rbox(ax, x - box_w / 2, y0, box_w, 6.2, fc=TEAL_LT, ec=TEAL, radius=0.2)
    text(ax, x, y0 + 3.1, title, fontsize=8.5, color=NAVY, fontweight="bold")
    ax.plot([x, x], [y0, y1], color=NAVY, ls=(0, (3, 3)), lw=1.1)
    return x, y0, y1


def message(ax, x1, x2, y, label, dashed=False, back=False):
    style = "-|>" if not back else "->"
    arrow(ax, x1, y, x2, y, color=NAVY, lw=1.15, style=style, ls=(0, (4, 3)) if dashed else "-")
    text(ax, (x1 + x2) / 2, y + 1.55, label, fontsize=7.2, color=INK, family="DejaVu Sans Mono")
