"""Generate all UML, architecture, ERD, and planning diagrams."""

from draw_kit import *
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Polygon
import matplotlib.pyplot as plt


def draw_uc_inception():
    fig, ax = fig_ax(14, 8.6, "Figure: Initial Use-Case Model — Inception (10%)")
    system_box(ax, 28, 18, 48, 68, "Pharmacy POS")
    actor(ax, 12, 62, "Pharmacist/Cashier", PHARM, "system user")
    actor(ax, 88, 62, "Customer", EXT, "external — no login")
    usecase(ax, 52, 52, 28, 14, "UC-02 Process Sale")
    arrow(ax, 16, 54, 38, 52, color=PHARM)
    arrow(ax, 86, 54, 66, 50, color=EXT, ls=(0, (4, 3)), style="->")
    text(ax, 76, 46, "interacts via\nPharmacist only", fontsize=7, color=MUTED)
    rbox(ax, 8, 4, 84, 12, fc=SAND, ec=GOLD, radius=0.3)
    text(ax, 50, 10, "Inception shows the architecturally significant 10%.\n"
         "Process Sale is the core counter goal (Larman: risk- and use-case-driven). "
         "Detailed SSDs are deferred to Elaboration.",
         fontsize=8, color=INK)
    return save(fig, UC_DIR / "UC-Inception-10-Percent.png")


def draw_uc_elab1():
    fig, ax = fig_ax(15, 9.2, "Figure: Elaboration Iteration 1 — 30% Use Cases")
    system_box(ax, 26, 14, 50, 74, "Pharmacy POS")
    actor(ax, 10, 68, "Pharmacist/Cashier", PHARM)
    actor(ax, 90, 68, "Administrator", ADMIN)
    usecase(ax, 51, 68, 26, 11, "UC-01 Authenticate User")
    usecase(ax, 51, 50, 26, 11, "UC-02 Process Sale")
    usecase(ax, 51, 32, 26, 11, "UC-03 Manage Medicines")
    arrow(ax, 14.5, 60, 38, 66, color=PHARM)
    arrow(ax, 14.5, 56, 38, 50, color=PHARM)
    arrow(ax, 85.5, 60, 64, 66, color=ADMIN)
    arrow(ax, 85.5, 54, 64, 34, color=ADMIN)
    rbox(ax, 6, 3, 88, 9.5, fc=TEAL_LT, ec=TEAL)
    text(ax, 50, 7.8, "30% = the architectural spine: identity (UC-01), the money/stock transaction (UC-02),\n"
         "and the catalogue that sales depend on (UC-03). Remaining use cases wait until Iteration 2.",
         fontsize=8)
    return save(fig, UC_DIR / "UC-Elaboration1-30-Percent.png")


def draw_uc_complete():
    fig, ax = fig_ax(16.5, 11.2, "Figure: Complete Use-Case Model")
    system_box(ax, 22, 8, 56, 84, "Pharmacy POS")
    actor(ax, 9, 72, "Pharmacist/Cashier", PHARM, "system user")
    actor(ax, 91, 78, "Administrator", ADMIN, "system user")
    actor(ax, 9, 28, "Customer", EXT, "external")
    actor(ax, 91, 28, "Supplier", EXT, "external")

    cases_left = [
        (48, 80, "UC-01 Authenticate User"),
        (48, 68, "UC-02 Process Sale"),
        (48, 56, "UC-08 Record Customer"),
        (48, 44, "UC-09 Void Sale"),
    ]
    cases_right = [
        (62, 80, "UC-03 Manage Medicines"),
        (62, 68, "UC-04 Manage Inventory"),
        (62, 56, "UC-05 Manage Users"),
        (62, 44, "UC-06 Manage Suppliers"),
        (62, 32, "UC-07 View Reports"),
        (62, 20, "UC-10 Configure Pharmacy"),
    ]
    for x, y, lab in cases_left:
        usecase(ax, x, y, 22, 8.6, lab)
    for x, y, lab in cases_right:
        usecase(ax, x, y, 22, 8.6, lab)

    # Pharmacist associations
    for y in (68, 56, 44):
        arrow(ax, 13.5, 64 if y == 68 else (52 if y == 56 else 40), 37, y, color=PHARM, lw=1.0)
    arrow(ax, 13.5, 70, 37, 80, color=PHARM, lw=1.0)
    # Admin
    for y in (80, 68, 56, 44, 32, 20):
        arrow(ax, 86.5, min(y + 6, 72), 73, y, color=ADMIN, lw=1.0)
    arrow(ax, 86.5, 70, 73, 80, color=ADMIN, lw=1.0)
    # Customer / supplier dashed
    arrow(ax, 13, 22, 37, 66, color=EXT, ls=(0, (3, 3)), style="->", lw=0.9)
    arrow(ax, 87, 24, 73, 66, color=EXT, ls=(0, (3, 3)), style="->", lw=0.9)

    text(ax, 50, 11.5, "include", fontsize=7, color=TEAL, style="italic")
    arrow(ax, 48, 63.5, 48, 60.5, color=TEAL, ls=(0, (4, 3)), style="-|>")
    text(ax, 50, 4.8, "The Pharmacist performs the cashier function; there is no separate Cashier role. "
         "Customer and Supplier are external entities, not accounts.",
         fontsize=8, color=MUTED)
    return save(fig, UC_DIR / "UC-Complete.png")


def _ssd(title, actor_name, events, notes=None, fname="ssd.png"):
    fig, ax = fig_ax(14.5, 11.4, title)
    # left use-case fragment
    rbox(ax, 3, 8, 28, 78, fc=WHITE, ec=BOX, radius=0.2)
    text(ax, 17, 82, "Use-case fragment", fontsize=8.5, color=TEAL, fontweight="bold")
    if notes:
        text(ax, 17, 44, notes, fontsize=7.2, ha="center", va="center", color=INK)

    lifeline(ax, 48, 80, 10, actor_name, actor_mode=True)
    lifeline(ax, 80, 80, 10, ":System", box_w=18)
    text(ax, 80, 88.5, "black box", fontsize=7, color=MUTED, style="italic")

    y = 68
    for ev in events:
        kind = ev.get("kind", "in")
        if kind == "in":
            message(ax, 48, 80, y, ev["label"])
        else:
            message(ax, 80, 48, y, ev["label"], dashed=True, back=True)
        y -= 6.2

    text(ax, 50, 4.5, "Larman Ch. 9: actor → System events at the level of intent (enterItem, not scan).",
         fontsize=7.5, color=MUTED)
    return save(fig, SSD_DIR / fname)


def draw_ssds():
    paths = []
    paths.append(_ssd(
        "Figure: SSD — UC-02 Process Sale (main success scenario)",
        "Pharmacist/Cashier",
        [
            {"label": "makeNewSale()"},
            {"label": "saleInProgress", "kind": "out"},
            {"label": "enterItem(medicineId, qty)"},
            {"label": "description, price, runningTotal", "kind": "out"},
            {"label": "enterItem(...)   {repeat}"},
            {"label": "attachPrescription(ref, customerId)"},
            {"label": "endSale()"},
            {"label": "total", "kind": "out"},
            {"label": "makePayment(amount, method)"},
            {"label": "changeDue, receipt", "kind": "out"},
        ],
        "1. Start a sale\n2. Enter each item\n3. Attach prescription\n   if required\n4. End sale\n5. Record payment\n6. Receive receipt\n\nCustomer does not\ngenerate events.",
        "SSD-UC02-Process-Sale.png",
    ))
    paths.append(_ssd(
        "Figure: SSD — UC-01 Authenticate User",
        "Staff Member",
        [
            {"label": "requestAccess()"},
            {"label": "loginPrompt", "kind": "out"},
            {"label": "submitCredentials(username, password)"},
            {"label": "session, homeViewForRole", "kind": "out"},
        ],
        "Staff member is either\nAdministrator or\nPharmacist/Cashier.\n\nPassword is submitted\nonce; the system stores\nonly a hash.",
        "SSD-UC01-Authenticate.png",
    ))
    paths.append(_ssd(
        "Figure: SSD — UC-03 Manage Medicines",
        "Administrator",
        [
            {"label": "openMedicineMaintenance()"},
            {"label": "catalogueView", "kind": "out"},
            {"label": "saveMedicine(data)"},
            {"label": "confirmation", "kind": "out"},
            {"label": "deactivateMedicine(id)"},
            {"label": "confirmation", "kind": "out"},
        ],
        "Administrator maintains\nthe catalogue that\nenterItem depends on.",
        "SSD-UC03-Manage-Medicines.png",
    ))
    paths.append(_ssd(
        "Figure: SSD — UC-04 Manage Inventory",
        "Administrator",
        [
            {"label": "receiveStock(supplierId, lines)"},
            {"label": "receiptId, updatedQuantities", "kind": "out"},
            {"label": "adjustStock(batchId, delta, reason)"},
            {"label": "updatedQuantity", "kind": "out"},
            {"label": "viewStockAlerts()"},
            {"label": "lowStock, nearExpiry", "kind": "out"},
        ],
        "Receiving and adjusting\nare Administrator goals.\nThe Pharmacist does not\nreceive deliveries.",
        "SSD-UC04-Manage-Inventory.png",
    ))
    paths.append(_ssd(
        "Figure: SSD — UC-09 Void Sale",
        "Pharmacist/Cashier",
        [
            {"label": "selectSale(saleId)"},
            {"label": "saleSummary", "kind": "out"},
            {"label": "voidSale(saleId, reason)"},
            {"label": "voidConfirmation, restoredQty", "kind": "out"},
        ],
        "A void is an explicit\nsystem event with a\nreason. Sales are not\nsilently deleted.",
        "SSD-UC09-Void-Sale.png",
    ))
    return paths


def draw_domain_model():
    fig, ax = fig_ax(18.5, 13.5, "Figure: Domain Model — Pharmacy POS (conceptual)", ymax=108)

    def dm(x, y, w, h, name, attrs):
        class_box(ax, x, y, w, h, name, attrs=attrs, methods=None, header=NAVY)

    dm(40, 86, 20, 10, "Pharmacy", ["name", "address", "phone"])
    dm(4, 68, 18, 12, "User", ["username", "fullName", "role", "active"])
    dm(72, 68, 20, 12, "MedicineCategory", ["name"])
    dm(40, 64, 20, 14, "Medicine", ["productCode", "name", "genericName",
                                    "strength", "requiresRx", "unitPrice", "reorderLevel"])
    dm(72, 42, 22, 16, "StockBatch", ["batchNumber", "expiryDate",
                                     "quantityOnHand", "unitCost"])
    dm(4, 38, 20, 16, "Sale", ["startedAt", "status", "subtotal", "total"])
    dm(28, 36, 20, 16, "SalesLineItem", ["quantity", "unitPrice", "lineTotal"])
    dm(4, 16, 20, 12, "Payment", ["method", "amountTendered", "changeDue"])
    dm(28, 14, 18, 12, "Customer", ["fullName", "phone"])
    dm(50, 14, 20, 14, "Prescription", ["referenceNo", "prescriberName", "issuedOn"])
    dm(74, 14, 20, 12, "PrescriptionItem", ["quantity"])
    dm(4, 86, 18, 10, "Supplier", ["name", "phone"])
    dm(72, 86, 22, 10, "StockReceipt", ["receivedAt", "referenceNote"])
    dm(40, 42, 20, 12, "StockAdjustment", ["quantityDelta", "reason", "note"])
    dm(28, 86, 10, 8, "AuditEntry", ["action", "occurredAt"])

    # associations
    def link(a, b, name, m1, m2):
        ax.annotate("", xy=b, xytext=a,
                    arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9))
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        text(ax, mx, my + 1.2, name, fontsize=6, color=TEAL_DK, style="italic")
        text(ax, a[0], a[1] + 1.4, m1, fontsize=5.8, color=NAVY)
        text(ax, b[0], b[1] + 1.4, m2, fontsize=5.8, color=NAVY)

    # Use simple lines between known anchors (centres of boxes)
    anchors = {
        "Pharmacy": (50, 86),
        "User": (13, 68),
        "Medicine": (50, 64),
        "Cat": (82, 68),
        "Batch": (83, 50),
        "Sale": (14, 46),
        "Line": (38, 44),
        "Pay": (14, 22),
        "Cust": (37, 20),
        "Rx": (60, 21),
        "RxI": (84, 20),
        "Sup": (13, 91),
        "Rec": (83, 91),
        "Adj": (50, 48),
    }
    pairs = [
        ((50, 86), (13, 74), "Employs", "1", "1..*"),
        ((50, 86), (50, 78), "Offers", "1", "1..*"),
        ((82, 68), (60, 72), "Classifies", "1", "*"),
        ((50, 64), (83, 54), "Has-stock", "1", "*"),
        ((13, 68), (14, 54), "Records", "1", "*"),
        ((14, 46), (28, 44), "Contains", "1", "1..*"),
        ((38, 44), (50, 64), "Records-sale-of", "*", "1"),
        ((38, 44), (83, 50), "Taken-from", "*", "1"),
        ((14, 38), (14, 28), "Paid-by", "1", "0..1"),
        ((14, 38), (37, 26), "Initiated-for", "*", "0..1"),
        ((37, 20), (60, 21), "Presented", "1", "*"),
        ((60, 21), (74, 20), "Contains", "1", "1..*"),
        ((74, 20), (60, 64), "Authorises", "*", "1"),
        ((13, 86), (83, 91), "Supplies", "1", "*"),
        ((83, 86), (83, 58), "Increases", "1", "1..*"),
        ((50, 48), (83, 50), "Adjusts", "*", "1"),
        ((60, 21), (24, 38), "Attached-to", "0..1", "0..1"),
    ]
    for a, b, name, m1, m2 in pairs:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=NAVY, lw=0.85, zorder=1)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        text(ax, mx, my + 1.15, name, fontsize=5.8, color=TEAL_DK, style="italic")

    rbox(ax, 3, 2, 94, 8, fc=SAND, ec=GOLD)
    text(ax, 50, 6, "Conceptual model only (Larman Ch. 9–11). No operations. "
         "Need-to-know associations kept; Register from the NextGen POS example is omitted —\n"
         "a single-counter pharmacy records the Sale against User, not a hardware register. "
         "Receipt is an output of Sale, not a separate concept.",
         fontsize=7.4)
    return save(fig, DM_DIR / "Domain-Model.png")


def draw_architecture():
    fig, ax = fig_ax(15.5, 10.8, "Figure: Layered Architecture — Proof of Concept")
    layers = [
        (82, "Presentation", "LoginView  ·  POSView  ·  PaymentView  ·  ReceiptView\n"
         "AdminDashboard  ·  MedicineView  ·  InventoryView  ·  ReportView", TEAL_LT, TEAL),
        (64, "Application / System", "SaleController  ·  AuthController  ·  MedicineController\n"
         "InventoryController  ·  UserController  ·  ReportController", "#E4F0EE", TEAL_DK),
        (44, "Domain", "Sale  ·  SalesLineItem  ·  Payment  ·  Medicine  ·  StockBatch\n"
         "Prescription  ·  Customer  ·  User  ·  Inventory rules", SAND, GOLD),
        (26, "Persistence", "SaleRepository  ·  MedicineRepository  ·  InventoryRepository\n"
         "UserRepository  ·  AuditRepository", "#E8EEF4", NAVY),
        (10, "External boundary", "Receipt printer / PDF   ·   Manual card & mobile-money confirmation\n"
         "(no live gateway in this release — Protected Variations keeps the seam)", BOX, MUTED),
    ]
    for y, name, body, fc, ec in layers:
        rbox(ax, 8, y, 84, 15.5, fc=fc, ec=ec, lw=1.6, radius=0.25)
        text(ax, 18, y + 11.2, name, fontsize=11, color=ec, fontweight="bold", ha="left")
        text(ax, 50, y + 6.2, body, fontsize=8.2, color=INK)
    # arrows down
    for y in (82, 64, 44, 26):
        arrow(ax, 50, y, 50, y - 1.2, color=NAVY, lw=1.2)
    text(ax, 50, 3.5, "Dependencies point downward only. Presentation never talks to repositories. "
         "This is the Elaboration 1 architectural proof-of-concept.",
         fontsize=8, color=MUTED)
    return save(fig, ARCH_DIR / "Layered-Architecture-PoC.png")


def draw_arch_sale_path():
    fig, ax = fig_ax(15.2, 8.8, "Figure: Architectural PoC — Process Sale path")
    nodes = [
        (12, 55, "POSView"),
        (34, 55, "SaleController"),
        (56, 70, "Sale"),
        (56, 40, "StockBatch"),
        (78, 70, "SaleRepository"),
        (78, 40, "InventoryRepository"),
        (56, 18, "ReceiptService"),
    ]
    for x, y, n in nodes:
        rbox(ax, x - 9, y - 5, 18, 10, fc=WHITE, ec=TEAL, radius=0.3)
        text(ax, x, y, n, fontsize=8.5, color=NAVY, fontweight="bold")
    arrow(ax, 21, 55, 25, 55)
    arrow(ax, 43, 58, 47, 66)
    arrow(ax, 43, 52, 47, 44)
    arrow(ax, 65, 70, 69, 70)
    arrow(ax, 65, 40, 69, 40)
    arrow(ax, 56, 35, 56, 23)
    text(ax, 50, 88, "makeNewSale / enterItem / endSale / makePayment", fontsize=9, color=TEAL)
    rbox(ax, 8, 4, 84, 8, fc=TEAL_LT, ec=TEAL)
    text(ax, 50, 8, "PoC question: can a sale line, an expiry check, a payment, and a stock decrement\n"
         "cross the layers without the UI knowing SQL? If yes, construction may proceed on this spine.",
         fontsize=8)
    return save(fig, ARCH_DIR / "Architecture-Sale-Path.png")


def draw_dcd_sale():
    fig, ax = fig_ax(17.8, 12.2, "Figure: Design Class Diagram — Process Sale collaboration")
    class_box(ax, 3, 78, 22, 18, "SaleController",
              attrs=["- currentSale: Sale"],
              methods=["+ makeNewSale()", "+ enterItem(id, qty)",
                       "+ attachPrescription(...)", "+ endSale()",
                       "+ makePayment(amt, method)"],
              header=TEAL)
    class_box(ax, 30, 74, 24, 24, "Sale",
              attrs=["- status: SaleStatus", "- lines: SalesLineItem[*]",
                     "- payment: Payment", "- total: Money"],
              methods=["+ addLine(batch, qty)", "+ removeLine(id)",
                       "+ getTotal()", "+ becomeComplete()",
                       "+ makePayment(amt, method)", "+ void(reason)"],
              header=NAVY)
    class_box(ax, 58, 80, 22, 16, "SalesLineItem",
              attrs=["- quantity: int", "- unitPrice: Money"],
              methods=["+ getSubtotal()"],
              header=NAVY)
    class_box(ax, 58, 54, 22, 16, "Payment",
              attrs=["- method: PaymentMethod", "- amountTendered: Money",
                     "- changeDue: Money"],
              methods=["+ isAcceptable(total)"],
              header=NAVY)
    class_box(ax, 30, 42, 24, 18, "StockBatch",
              attrs=["- batchNumber: String", "- expiryDate: Date",
                     "- quantityOnHand: int"],
              methods=["+ isSellable(qty, onDate)", "+ decrement(qty)",
                       "+ increment(qty)"],
              header=NAVY)
    class_box(ax, 3, 46, 22, 18, "SaleService",
              attrs=[],
              methods=["+ completeSale(sale)", "+ voidSale(sale, reason)"],
              header=TEAL)
    class_box(ax, 3, 18, 22, 16, "SaleRepository",
              attrs=[],
              methods=["+ save(sale)", "+ find(id)"],
              stereotype="«Pure Fabrication»", header=MUTED)
    class_box(ax, 30, 16, 24, 14, "InventoryRepository",
              attrs=[],
              methods=["+ findSellableBatch(medId, qty)", "+ save(batch)"],
              header=MUTED)
    class_box(ax, 58, 28, 22, 14, "ReceiptService",
              attrs=[],
              methods=["+ present(sale)"],
              stereotype="«Indirection»", header=GOLD)
    class_box(ax, 82, 54, 16, 20, "PaymentMethod",
              attrs=[],
              methods=["+ record(sale, amt)"],
              stereotype="«interface»", header=TEAL_DK)
    class_box(ax, 82, 28, 16, 12, "CashPayment", methods=["+ record(...)"], header=TEAL)
    class_box(ax, 82, 14, 16, 12, "CardPayment", methods=["+ record(...)"], header=TEAL)
    class_box(ax, 82, 0.8, 16, 11, "MobileMoneyPayment", methods=["+ record(...)"], header=TEAL)

    ax.plot([25, 30], [88, 86], color=NAVY, lw=1)
    ax.plot([42, 58], [86, 88], color=NAVY, lw=1)
    ax.plot([42, 58], [78, 62], color=NAVY, lw=1)
    ax.plot([42, 42], [74, 60], color=NAVY, lw=1)
    ax.plot([25, 30], [54, 50], color=NAVY, lw=1)
    ax.plot([14, 14], [46, 34], color=NAVY, lw=1)
    ax.plot([42, 42], [42, 30], color=NAVY, lw=1)
    ax.plot([54, 58], [22, 35], color=NAVY, lw=1)
    ax.plot([74, 82], [60, 64], color=NAVY, lw=1)
    ax.plot([90, 90], [54, 40], color=NAVY, lw=1)
    ax.plot([90, 90], [28, 26], color=NAVY, lw=1)
    ax.plot([90, 90], [14, 12], color=NAVY, lw=1)
    text(ax, 91, 42, "△", fontsize=10, color=NAVY)
    text(ax, 50, 97.2, "Derived from UC-02 system events → responsibilities → GRASP", fontsize=8, color=MUTED)
    return save(fig, DCD_DIR / "DCD-Process-Sale.png")


def draw_dcd_overview():
    fig, ax = fig_ax(17.5, 11.5, "Figure: Design Class Diagram — application and domain overview")
    controllers = [
        (4, 82, "AuthController"),
        (24, 82, "SaleController"),
        (44, 82, "MedicineController"),
        (64, 82, "InventoryController"),
        (84, 82, "UserController"),
    ]
    for x, y, n in controllers:
        class_box(ax, x, y, 15, 10, n, methods=["+ handle(...)"], header=TEAL)
    domains = [
        (4, 52, "User"),
        (22, 52, "Sale"),
        (40, 52, "Medicine"),
        (58, 52, "StockBatch"),
        (76, 52, "Prescription"),
        (4, 28, "Payment"),
        (22, 28, "Customer"),
        (40, 28, "Supplier"),
        (58, 28, "StockReceipt"),
        (76, 28, "AuditEntry"),
    ]
    for x, y, n in domains:
        class_box(ax, x, y, 16, 14, n, attrs=["(see domain model)"], methods=["domain ops"], header=NAVY)
    fabs = [
        (10, 6, "PasswordHasher"),
        (32, 6, "AuditLogger"),
        (54, 6, "Repositories"),
        (76, 6, "ReceiptService"),
    ]
    for x, y, n in fabs:
        class_box(ax, x, y, 18, 12, n, stereotype="«Pure Fabrication»", methods=["+ execute(...)"], header=MUTED)
    text(ax, 50, 76, "Application controllers (GRASP Controller)", fontsize=8, color=TEAL)
    text(ax, 50, 48, "Domain classes (adapted from the conceptual model)", fontsize=8, color=NAVY)
    text(ax, 50, 20.5, "Supporting fabrications — not pharmacy concepts, but necessary software", fontsize=8, color=MUTED)
    return save(fig, DCD_DIR / "DCD-Overview.png")


def draw_grasp():
    fig, ax = fig_ax(15.8, 10.2, "Figure: GRASP responsibility assignments for Process Sale")
    rows = [
        (TEAL, "Controller", "SaleController receives makeNewSale, enterItem, endSale, makePayment."),
        (NAVY, "Creator", "Sale creates SalesLineItem and Payment."),
        (NAVY, "Information Expert", "SalesLineItem knows subtotal; Sale knows total; StockBatch knows sellability."),
        (GOLD, "Protected Variations", "PaymentMethod isolates cash, card, and mobile money."),
        (MUTED, "Pure Fabrication", "Repositories, PasswordHasher, and AuditLogger keep domain objects clean."),
        (GOLD, "Indirection", "ReceiptService sits between Sale and printer/PDF."),
        (TEAL_DK, "Low Coupling / High Cohesion", "Views → controllers → domain → repositories. One reason to change per class."),
    ]
    y = 82
    for color, title, body in rows:
        rbox(ax, 6, y, 88, 9.2, fc=WHITE, ec=color, lw=1.6, radius=0.25)
        rbox(ax, 6, y, 24, 9.2, fc=color, ec=color, radius=0.25)
        text(ax, 18, y + 4.6, title, fontsize=8.5, color=WHITE, fontweight="bold")
        text(ax, 62, y + 4.6, body, fontsize=8.2, ha="center")
        y -= 10.5
    return save(fig, DCD_DIR / "GRASP-Assignments.png")


def draw_erd():
    fig, ax = fig_ax(18.2, 14.2, "Figure: Entity-Relationship Diagram (logical)", ymax=128)

    def ent(x, y, w, h, name, cols, pk=""):
        rbox(ax, x, y, w, h, fc=WHITE, ec=NAVY, radius=0.1)
        ax.add_patch(Rectangle((x, y + h - 4.2), w, 4.2, facecolor=TEAL, edgecolor=NAVY, lw=0, zorder=3))
        text(ax, x + w / 2, y + h - 2.1, name, fontsize=7.4, color=WHITE, fontweight="bold")
        for i, c in enumerate(cols):
            mark = "PK " if i == 0 else ("FK " if "id" in c and i > 0 and c.endswith("_id") else "   ")
            text(ax, x + 0.7, y + h - 5.8 - i * 2.05, f"{mark}{c}", ha="left", fontsize=5.8,
                 family="DejaVu Sans Mono", color=INK)

    ent(2, 100, 20, 18, "users", ["user_id", "username", "role", "password_hash"])
    ent(28, 100, 22, 16, "pharmacy_settings", ["pharmacy_id", "name", "near_expiry_days"])
    ent(56, 100, 20, 16, "medicine_categories", ["category_id", "name"])
    ent(80, 100, 18, 16, "suppliers", ["supplier_id", "name", "phone"])

    ent(38, 74, 24, 20, "medicines", ["medicine_id", "product_code", "name",
                                     "requires_prescription", "unit_price", "category_id"])
    ent(70, 72, 26, 20, "stock_batches", ["batch_id", "medicine_id", "batch_number",
                                         "expiry_date", "quantity_on_hand"])

    ent(2, 70, 22, 18, "stock_receipts", ["receipt_id", "supplier_id", "received_by_user_id"])
    ent(2, 44, 24, 18, "stock_receipt_lines", ["receipt_line_id", "receipt_id", "batch_id", "quantity"])
    ent(70, 44, 26, 16, "stock_adjustments", ["adjustment_id", "batch_id", "quantity_delta", "reason"])

    ent(2, 18, 20, 16, "customers", ["customer_id", "full_name", "phone"])
    ent(26, 16, 22, 18, "prescriptions", ["prescription_id", "customer_id", "reference_no"])
    ent(50, 16, 22, 16, "prescription_items", ["prescription_item_id", "prescription_id", "medicine_id"])

    ent(26, 42, 22, 20, "sales", ["sale_id", "sold_by_user_id", "customer_id",
                                 "status", "total"])
    ent(50, 40, 18, 18, "sale_items", ["sale_item_id", "sale_id", "medicine_id",
                                      "batch_id", "quantity", "line_total"])
    ent(2, 0.5, 20, 14, "payments", ["payment_id", "sale_id", "method", "amount_tendered"])
    ent(70, 16, 26, 16, "audit_logs", ["audit_id", "user_id", "action", "occurred_at"])

    def rel(a, b):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=NAVY, lw=0.8, zorder=1)

    rel((22, 108), (26, 52))  # users to sales
    rel((12, 70), (12, 62))
    rel((66, 100), (50, 94))
    rel((50, 74), (70, 82))
    rel((80, 100), (13, 88))
    rel((13, 70), (14, 62))
    rel((24, 52), (70, 54))
    rel((37, 52), (50, 50))
    rel((48, 42), (50, 34))
    rel((12, 26), (26, 26))
    rel((48, 25), (50, 24))
    rel((37, 42), (12, 14))
    rel((12, 100), (12, 88))
    rel((22, 108), (70, 24))

    text(ax, 50, 3.2, "Crow's-foot intent: 1—* from parents to children. sale : payment is 1:0..1. "
         "Many-to-many Medicine↔Sale is resolved by sale_items; Medicine↔Prescription by prescription_items.",
         fontsize=7.2, color=MUTED)
    return save(fig, DB_DIR / "ERD-Logical.png")


def draw_schema_overview():
    fig, ax = fig_ax(15, 9.4, "Figure: Database schema groups")
    groups = [
        (8, 62, "Identity & config", "users\npharmacy_settings\naudit_logs", TEAL_LT),
        (38, 62, "Catalogue & stock", "medicine_categories\nmedicines\nstock_batches\nsuppliers", SAND),
        (68, 62, "Stock movements", "stock_receipts\nstock_receipt_lines\nstock_adjustments", "#E8EEF4"),
        (8, 18, "Patients", "customers\nprescriptions\nprescription_items", WHITE),
        (38, 18, "Sales", "sales\nsale_items\npayments", TEAL_LT),
    ]
    for x, y, title, body, fc in groups:
        rbox(ax, x, y, 26, 28, fc=fc, ec=NAVY, radius=0.3)
        text(ax, x + 13, y + 23, title, fontsize=10, color=NAVY, fontweight="bold")
        text(ax, x + 13, y + 12, body, fontsize=8.5, color=INK)
    rbox(ax, 68, 18, 26, 28, fc=SAND, ec=GOLD)
    text(ax, 81, 32, "Normalisation\n3NF target\n\nPrices copied onto\nsale_items so history\ndoes not change.", fontsize=8)
    return save(fig, DB_DIR / "Schema-Groups.png")


def draw_up_phases():
    fig, ax = fig_ax(15.2, 7.6, "Figure: Unified Process phases (iterative, not waterfall)")
    phases = [
        (8, "Inception", "W1–2", "Vision, 10%\nuse cases, risks", TEAL),
        (32, "Elaboration", "W3–8", "Architecture +\nuse cases to 100%", NAVY),
        (56, "Construction", "W9–12", "Features, tests,\nGit / CI", TEAL_DK),
        (80, "Transition", "W13–15", "Beta, polish,\ndemo", GOLD),
    ]
    for x, name, weeks, body, col in phases:
        rbox(ax, x, 38, 18, 40, fc=WHITE, ec=col, lw=2, radius=0.4)
        rbox(ax, x, 66, 18, 12, fc=col, ec=col, radius=0.4)
        text(ax, x + 9, 72, name, fontsize=10, color=WHITE, fontweight="bold")
        text(ax, x + 9, 60, weeks, fontsize=9, color=col, fontweight="bold")
        text(ax, x + 9, 50, body, fontsize=8)
        if x < 80:
            arrow(ax, x + 18.5, 58, x + 23.2, 58, color=NAVY)
    text(ax, 50, 24, "Each phase contains iterations that produce working understanding (then software).\n"
         "Elaboration is two iterations. Construction is Iterations 3–4. Transition is Iteration 5 + demo.",
         fontsize=8.5)
    text(ax, 50, 10, "Larman: do not treat Inception as a mini-waterfall requirements freeze.",
         fontsize=8, color=MUTED)
    return save(fig, UP_DIR / "UP-Phases.png")


def draw_iteration_plan():
    fig, ax = fig_ax(16, 9.2, "Figure: 15-week iteration plan mapped to UP")
    rows = [
        ("W1–2", "Inception", "Vision & feasibility", "10", "10% UC-02, risks, plan"),
        ("W3–5", "Elaboration 1", "Core architecture", "20", "30% UC-01/02/03, SSD, domain, PoC"),
        ("W6–8", "Elaboration 2", "Risk-driven design", "15", "70% use cases, DCD, GRASP, UI, schema"),
        ("W9–12", "Construction 3–4", "Feature implementation", "30", "Prioritised features, tests, Git, CI, defects"),
        ("W13–14", "Transition 5", "Polish & deploy prep", "15", "Beta, performance, security, manual"),
        ("W15", "Transition", "Demo & submission", "10", "Live demo, final report, repository"),
    ]
    y = 78
    headers = [8, 22, 42, 62, 78]
    labels = ["Weeks", "UP phase", "Milestone", "Marks", "Primary artefacts"]
    for x, lab in zip(headers, labels):
        text(ax, x, 86, lab, fontsize=8, color=TEAL, fontweight="bold", ha="left")
    for i, (w, ph, ms, mk, art) in enumerate(rows):
        fc = TEAL_LT if i % 2 == 0 else WHITE
        rbox(ax, 4, y - 3, 92, 10, fc=fc, ec=BOX, radius=0.15)
        vals = [w, ph, ms, mk, art]
        xs = [8, 22, 42, 62, 78]
        for x, v in zip(xs, vals):
            text(ax, x, y + 2, v, fontsize=7.6, ha="left")
        y -= 11
    return save(fig, UP_DIR / "Iteration-Plan-15-Weeks.png")


def draw_git():
    fig, ax = fig_ax(14.5, 7.8, "Figure: Planned Git / CI workflow (Construction)")
    boxes = [("feature/*", 12), ("pull request", 38), ("CI pipeline", 64), ("main", 88)]
    y = 55
    for name, x in boxes:
        rbox(ax, x - 10, y, 20, 16, fc=WHITE, ec=TEAL, radius=0.3)
        text(ax, x, y + 8, name, fontsize=10, color=NAVY, fontweight="bold")
        if x < 88:
            arrow(ax, x + 10.5, y + 8, x + 15.5, y + 8)
    text(ax, 64, 42, "lint · unit · integration", fontsize=8, color=MUTED)
    text(ax, 50, 24, "Defects are logged against a branch and a test case. "
         "Results: TO BE COMPLETED DURING CONSTRUCTION.",
         fontsize=8.5)
    return save(fig, UP_DIR / "Git-CI-Workflow.png")


def draw_traceability():
    fig, ax = fig_ax(16.2, 5.8, "Figure: Traceability chain")
    nodes = ["Business\nobjective", "FR / NFR", "Use case", "Scenario", "SSD event",
             "Domain\nconcept", "Design\nclass", "Table", "Feature", "Test"]
    for i, n in enumerate(nodes):
        x = 5 + i * 9.5
        rbox(ax, x, 35, 8.6, 28, fc=TEAL_LT if i % 2 == 0 else WHITE, ec=TEAL, radius=0.25)
        text(ax, x + 4.3, 49, n, fontsize=7)
        if i < len(nodes) - 1:
            arrow(ax, x + 8.7, 49, x + 9.4, 49, color=NAVY, lw=1)
    text(ax, 50, 18, "Example: BO-01 → FR-05 → UC-02 → expired-batch extension → enterItem → StockBatch → "
         "stock_batches → F-04 → UT-04 / TC-05",
         fontsize=8)
    return save(fig, UP_DIR / "Traceability-Chain.png")


def main():
    out = []
    out.append(draw_uc_inception())
    out.append(draw_uc_elab1())
    out.append(draw_uc_complete())
    out.extend(draw_ssds())
    out.append(draw_domain_model())
    out.append(draw_architecture())
    out.append(draw_arch_sale_path())
    out.append(draw_dcd_sale())
    out.append(draw_dcd_overview())
    out.append(draw_grasp())
    out.append(draw_erd())
    out.append(draw_schema_overview())
    out.append(draw_up_phases())
    out.append(draw_iteration_plan())
    out.append(draw_git())
    out.append(draw_traceability())
    print("Diagrams written:")
    for p in out:
        print(" ", p)
    return out


if __name__ == "__main__":
    main()
