"""UI prototypes for major Pharmacy POS workflows. Design artefacts only."""

from draw_kit import *
from matplotlib.patches import Rectangle, Circle
import matplotlib.pyplot as plt


def chrome(ax, title, role, user="Chileshe Banda"):
    ax.add_patch(Rectangle((0, 0), 100, 100, facecolor="#E8EEF0", edgecolor="none"))
    rbox(ax, 2, 4, 96, 92, fc=WHITE, ec=NAVY, radius=0.4, lw=1.2)
    ax.add_patch(Rectangle((2, 88), 96, 8, facecolor=NAVY, edgecolor="none", zorder=3))
    text(ax, 18, 92, "Pharmacy POS", fontsize=10, color=WHITE, fontweight="bold", ha="left")
    text(ax, 50, 92, title, fontsize=9.5, color="#D7EDE9", fontweight="bold")
    text(ax, 86, 92, f"{user}  ·  {role}", fontsize=7.2, color=WHITE, ha="right")
    # sidebar
    ax.add_patch(Rectangle((2, 4), 16, 84, facecolor="#0A303D", edgecolor="none", zorder=3))
    return 20  # content left


def nav(ax, items, active):
    y = 80
    for it in items:
        fc = TEAL if it == active else "#0A303D"
        rbox(ax, 3.2, y, 13.6, 6.4, fc=fc, ec=fc, radius=0.2, z=4)
        text(ax, 10, y + 3.2, it, fontsize=6.6, color=WHITE)
        y -= 7.4


def field(ax, x, y, w, h, label, value="", pwd=False):
    text(ax, x, y + h + 1.6, label, fontsize=6.5, color=MUTED, ha="left")
    rbox(ax, x, y, w, h, fc=WHITE, ec="#C5D0D4", radius=0.15, z=4)
    shown = "••••••••" if pwd else value
    text(ax, x + 1.2, y + h / 2, shown, fontsize=7.5, ha="left", color=INK)


def btn(ax, x, y, w, h, label, fill=TEAL, tc=WHITE):
    rbox(ax, x, y, w, h, fc=fill, ec=fill, radius=0.2, z=4)
    text(ax, x + w / 2, y + h / 2, label, fontsize=7.5, color=tc, fontweight="bold")


def table(ax, x, y, w, headers, rows, row_h=5.2):
    col_w = w / len(headers)
    ax.add_patch(Rectangle((x, y), w, 5.0, facecolor=TEAL, edgecolor=TEAL, zorder=4))
    for i, h in enumerate(headers):
        text(ax, x + col_w * i + col_w / 2, y + 2.5, h, fontsize=6.3, color=WHITE, fontweight="bold")
    yy = y - row_h
    for r, row in enumerate(rows):
        bg = "#F4FAF8" if r % 2 == 0 else WHITE
        ax.add_patch(Rectangle((x, yy), w, row_h, facecolor=bg, edgecolor="#E1E8EA", zorder=4))
        for i, cell in enumerate(row):
            text(ax, x + col_w * i + col_w / 2, yy + row_h / 2, cell, fontsize=6.2, color=INK)
        yy -= row_h


def login():
    fig, ax = fig_ax(13.5, 8.2, None)
    ax.add_patch(Rectangle((0, 0), 100, 100, facecolor=NAVY, edgecolor="none"))
    rbox(ax, 32, 18, 36, 64, fc=WHITE, ec=WHITE, radius=0.5)
    text(ax, 50, 74, "Pharmacy POS", fontsize=14, color=NAVY, fontweight="bold")
    text(ax, 50, 69, "CSC 4630  ·  Group 20", fontsize=8, color=TEAL)
    field(ax, 37, 54, 26, 6.5, "Username", "p.mwale")
    field(ax, 37, 40, 26, 6.5, "Password", "", pwd=True)
    btn(ax, 37, 28, 26, 7, "Sign in")
    text(ax, 50, 22, "Role is taken from the account.\nThere is no Cashier login type.",
         fontsize=7, color=MUTED)
    return save(fig, UI_DIR / "UI-01-Login.png")


def pos():
    fig, ax = fig_ax(16, 9.4, None)
    chrome(ax, "Point of sale", "Pharmacist/Cashier", "P. Mwale")
    nav(ax, ["Sale", "Find customer", "Today's sales", "Void sale", "Sign out"], "Sale")
    field(ax, 21, 78, 28, 5.5, "Search medicine / product code", "para")
    btn(ax, 50.5, 78, 10, 5.5, "Search")
    rbox(ax, 21, 48, 40, 26, fc="#F7FBFA", ec="#D5E3E0")
    text(ax, 41, 70, "Search results  ·  sellable qty shown", fontsize=7, color=TEAL, fontweight="bold")
    table(ax, 22.5, 63, 37, ["Code", "Name", "Price", "Qty"], [
        ["PAR-500", "Paracetamol 500mg", "12.00", "84"],
        ["PAR-SYR", "Paracetamol syrup", "28.50", "12"],
        ["AMOX-500", "Amoxicillin 500mg", "35.00", "40"],
    ], row_h=4.4)
    table(ax, 21, 40, 52, ["Item", "Batch", "Qty", "Price", "Line"], [
        ["Paracetamol 500mg", "B19-04", "2", "12.00", "24.00"],
        ["Cough syrup 100ml", "C02-11", "1", "45.00", "45.00"],
    ], row_h=5.0)
    rbox(ax, 75, 22, 21, 58, fc=SAND, ec=GOLD)
    text(ax, 85.5, 74, "Current sale", fontsize=9, color=NAVY, fontweight="bold")
    text(ax, 85.5, 66, "Lines   2", fontsize=8)
    text(ax, 85.5, 60, "Subtotal   ZMW 69.00", fontsize=8)
    text(ax, 85.5, 54, "Total   ZMW 69.00", fontsize=11, fontweight="bold", color=NAVY)
    text(ax, 85.5, 46, "Customer  (optional)", fontsize=7, color=MUTED)
    text(ax, 85.5, 41, "Walk-in / OTC", fontsize=8)
    btn(ax, 77, 30, 17, 6, "Pay")
    btn(ax, 77, 23, 17, 5.2, "Cancel sale", fill=WHITE, tc=ROSE)
    return save(fig, UI_DIR / "UI-02-POS-Sale.png")


def payment():
    fig, ax = fig_ax(14.5, 8.6, None)
    chrome(ax, "Record payment", "Pharmacist/Cashier", "P. Mwale")
    nav(ax, ["Sale", "Find customer", "Today's sales", "Void sale", "Sign out"], "Sale")
    text(ax, 40, 80, "Amount due", fontsize=8, color=MUTED, ha="left")
    text(ax, 40, 75, "ZMW 69.00", fontsize=16, color=NAVY, fontweight="bold", ha="left")
    for i, (lab, on) in enumerate([("Cash", True), ("Card", False), ("Mobile money", False)]):
        fc = TEAL if on else WHITE
        tc = WHITE if on else NAVY
        rbox(ax, 21 + i * 18, 58, 16.5, 8, fc=fc, ec=TEAL, radius=0.25)
        text(ax, 29.25 + i * 18, 62, lab, fontsize=8, color=tc, fontweight="bold")
    field(ax, 21, 44, 24, 6, "Amount tendered", "100.00")
    field(ax, 48, 44, 24, 6, "Change due", "31.00")
    field(ax, 21, 30, 51, 6, "External reference (card / mobile money)", "")
    btn(ax, 21, 16, 22, 7, "Complete sale")
    btn(ax, 45, 16, 16, 7, "Back", fill=WHITE, tc=NAVY)
    text(ax, 72, 32, "Card and mobile money\nare confirmed by the\nPharmacist (A-04).\nNo live gateway.",
         fontsize=7, color=MUTED, ha="left")
    return save(fig, UI_DIR / "UI-03-Payment.png")


def receipt():
    fig, ax = fig_ax(12.5, 9.2, None)
    ax.add_patch(Rectangle((0, 0), 100, 100, facecolor="#E8EEF0", edgecolor="none"))
    rbox(ax, 30, 6, 40, 88, fc=WHITE, ec=NAVY, radius=0.2)
    text(ax, 50, 88, "KABWATA FAMILY PHARMACY", fontsize=8.5, color=NAVY, fontweight="bold")
    text(ax, 50, 84, "Plot 12, Cairo Road  ·  Lusaka", fontsize=7, color=MUTED)
    text(ax, 50, 80, "RECEIPT  #S-1042", fontsize=8, color=TEAL, fontweight="bold")
    text(ax, 50, 76, "07 Sep 2026  14:22   ·   Pharmacist: P. Mwale", fontsize=6.5, color=MUTED)
    ax.plot([34, 66], [73, 73], color="#D0D5D7", lw=0.8)
    lines = [
        ("Paracetamol 500mg x2", "24.00"),
        ("Cough syrup 100ml x1", "45.00"),
        ("Subtotal", "69.00"),
        ("Total", "69.00"),
        ("Cash tendered", "100.00"),
        ("Change", "31.00"),
    ]
    y = 68
    for lab, amt in lines:
        text(ax, 36, y, lab, fontsize=7, ha="left")
        text(ax, 64, y, amt, fontsize=7, ha="right")
        y -= 5
    text(ax, 50, 28, "Batch numbers printed for\ntraceability. Thank you.", fontsize=7, color=MUTED)
    text(ax, 50, 18, "Not a tax invoice unless configured.", fontsize=6.5, color=MUTED)
    return save(fig, UI_DIR / "UI-04-Receipt.png")


def prescription():
    fig, ax = fig_ax(14.5, 8.4, None)
    chrome(ax, "Attach prescription", "Pharmacist/Cashier", "P. Mwale")
    nav(ax, ["Sale", "Find customer", "Today's sales", "Void sale", "Sign out"], "Sale")
    text(ax, 40, 80, "Amoxicillin 500mg requires a prescription (FR-06).",
         fontsize=8, color=ROSE, ha="left")
    field(ax, 21, 64, 30, 6, "Customer", "Mutale Phiri  ·  0977 111 222")
    btn(ax, 52, 64, 14, 6, "Find / add", fill=NAVY)
    field(ax, 21, 50, 22, 6, "Prescription reference", "UTH-24-8891")
    field(ax, 45, 50, 22, 6, "Prescriber (optional)", "Dr. Tembo")
    field(ax, 21, 36, 22, 6, "Issued on", "2026-09-06")
    btn(ax, 21, 20, 20, 7, "Attach & continue")
    return save(fig, UI_DIR / "UI-05-Prescription.png")


def admin_dash():
    fig, ax = fig_ax(16, 9.2, None)
    chrome(ax, "Administrator dashboard", "Administrator", "A. Bwalya")
    nav(ax, ["Dashboard", "Medicines", "Inventory", "Users", "Suppliers", "Reports", "Settings"], "Dashboard")
    cards = [
        (21, 70, "Sales today", "ZMW 4,820"),
        (42, 70, "Transactions", "37"),
        (63, 70, "Low-stock items", "6"),
        (79, 70, "Near expiry", "4"),
    ]
    for x, y, lab, val in cards:
        rbox(ax, x, y, 15.5, 14, fc=TEAL_LT, ec=TEAL, radius=0.25)
        text(ax, x + 7.75, y + 10, lab, fontsize=6.8, color=TEAL)
        text(ax, x + 7.75, y + 5.5, val, fontsize=10, color=NAVY, fontweight="bold")
    text(ax, 40, 64, "Alerts require Administrator action (UC-04). The Pharmacist sees stock on the sale screen only.",
         fontsize=7, color=MUTED, ha="left")
    table(ax, 21, 52, 73, ["Alert", "Medicine", "Batch", "Detail"], [
        ["LOW", "ORS sachets", "—", "On hand 8 / reorder 20"],
        ["EXPIRY", "Amoxicillin 250mg", "A03-02", "Expires 2026-10-12"],
        ["EXPIRY", "Insulin (fridge)", "I11-08", "Expires 2026-10-02"],
    ])
    return save(fig, UI_DIR / "UI-06-Admin-Dashboard.png")


def medicines():
    fig, ax = fig_ax(16, 9.2, None)
    chrome(ax, "Manage medicines", "Administrator", "A. Bwalya")
    nav(ax, ["Dashboard", "Medicines", "Inventory", "Users", "Suppliers", "Reports", "Settings"], "Medicines")
    btn(ax, 21, 78, 16, 5.5, "+ New medicine")
    field(ax, 39, 78, 28, 5.5, "", "Search catalogue")
    table(ax, 21, 68, 73, ["Code", "Name", "Rx?", "Price", "Active"], [
        ["PAR-500", "Paracetamol 500mg", "No", "12.00", "Yes"],
        ["AMOX-500", "Amoxicillin 500mg", "Yes", "35.00", "Yes"],
        ["INS-R", "Insulin regular", "Yes", "180.00", "Yes"],
    ])
    rbox(ax, 21, 8, 54, 28, fc="#F7FBFA", ec=TEAL)
    text(ax, 48, 32, "Edit medicine", fontsize=8, color=TEAL, fontweight="bold")
    field(ax, 23, 20, 24, 5, "Product code", "AMOX-500")
    field(ax, 49, 20, 24, 5, "Unit price (ZMW)", "35.00")
    field(ax, 23, 10, 16, 5, "Rx required", "Yes")
    btn(ax, 49, 10, 12, 5, "Save")
    return save(fig, UI_DIR / "UI-07-Medicines.png")


def inventory():
    fig, ax = fig_ax(16, 9.2, None)
    chrome(ax, "Manage inventory", "Administrator", "A. Bwalya")
    nav(ax, ["Dashboard", "Medicines", "Inventory", "Users", "Suppliers", "Reports", "Settings"], "Inventory")
    btn(ax, 21, 78, 16, 5.5, "Receive stock")
    btn(ax, 38.5, 78, 16, 5.5, "Adjust stock", fill=NAVY)
    table(ax, 21, 68, 73, ["Medicine", "Batch", "Expiry", "On hand", "Sellable?"], [
        ["Paracetamol 500mg", "B19-04", "2027-03-01", "84", "Yes"],
        ["Amoxicillin 250mg", "A03-02", "2026-10-12", "16", "Yes"],
        ["Cough syrup", "C88-01", "2026-08-20", "3", "No — expired"],
    ])
    text(ax, 57.5, 22, "Expired batches stay visible for audit but cannot be chosen by enterItem.",
         fontsize=7.5, color=MUTED)
    return save(fig, UI_DIR / "UI-08-Inventory.png")


def users():
    fig, ax = fig_ax(15, 8.6, None)
    chrome(ax, "Manage users", "Administrator", "A. Bwalya")
    nav(ax, ["Dashboard", "Medicines", "Inventory", "Users", "Suppliers", "Reports", "Settings"], "Users")
    text(ax, 40, 80, "Only two roles can be assigned.", fontsize=8, color=TEAL, ha="left")
    table(ax, 21, 70, 73, ["Username", "Full name", "Role", "Active"], [
        ["a.bwalya", "A. Bwalya", "Administrator", "Yes"],
        ["p.mwale", "P. Mwale", "Pharmacist/Cashier", "Yes"],
        ["j.phiri", "J. Phiri", "Pharmacist/Cashier", "No"],
    ])
    rbox(ax, 21, 12, 40, 26, fc=SAND, ec=GOLD)
    text(ax, 41, 33, "There is no Cashier, Manager,\nor Inventory Clerk role.",
         fontsize=8, color=NAVY)
    return save(fig, UI_DIR / "UI-09-Users.png")


def reports():
    fig, ax = fig_ax(15, 8.6, None)
    chrome(ax, "Reports", "Administrator", "A. Bwalya")
    nav(ax, ["Dashboard", "Medicines", "Inventory", "Users", "Suppliers", "Reports", "Settings"], "Reports")
    for i, lab in enumerate(["Daily sales", "Period sales", "Low stock", "Near expiry"]):
        on = i == 0
        btn(ax, 21 + i * 18, 76, 16.5, 6, lab, fill=TEAL if on else WHITE, tc=WHITE if on else NAVY)
    field(ax, 21, 64, 18, 5.5, "From", "2026-09-07")
    field(ax, 41, 64, 18, 5.5, "To", "2026-09-07")
    table(ax, 21, 54, 73, ["Time", "Sale", "Pharmacist", "Total", "Method"], [
        ["14:22", "S-1042", "P. Mwale", "69.00", "Cash"],
        ["13:05", "S-1041", "P. Mwale", "180.00", "Mobile money"],
        ["11:40", "S-1040", "P. Mwale", "35.00", "Card"],
    ])
    return save(fig, UI_DIR / "UI-10-Reports.png")


def main():
    out = [login(), pos(), payment(), receipt(), prescription(),
           admin_dash(), medicines(), inventory(), users(), reports()]
    print("UI prototypes written:")
    for p in out:
        print(" ", p)


if __name__ == "__main__":
    main()
