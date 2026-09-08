"""
Pharmacy POS — single source of truth for analysis and design artefacts.
No application implementation. Documentation and design only.
"""

COURSE = "CSC 4630 – Advanced Software Engineering"
GROUP = "Group 20"
SYSTEM = "Pharmacy Point-of-Sale (POS) System"
UNIVERSITY = "[University Name]"
LECTURER = "[Lecturer Name]"
DATE = "September 2026"
METHODOLOGY = "Unified Process (UP) — Iterative and Incremental"
LARMAN = (
    "Larman, C. Applying UML and Patterns: An Introduction to "
    "Object-Oriented Analysis and Design and Iterative Development. 3rd ed. "
    "Prentice Hall."
)
MARKING_GUIDE = (
    "CSC 4630 Advanced Software Engineering Course Project Marking Guide "
    "(Unified Process, 15 weeks)."
)

# ---------------------------------------------------------------------------
# Roles — exactly two system user roles
# ---------------------------------------------------------------------------
ROLES = [
    {
        "id": "ROLE-ADMIN",
        "name": "Administrator",
        "kind": "system user",
        "summary": (
            "Responsible for catalogue, inventory, users, suppliers, "
            "configuration, reports, and monitoring."
        ),
    },
    {
        "id": "ROLE-PHARM",
        "name": "Pharmacist/Cashier",
        "kind": "system user",
        "summary": (
            "The Pharmacist performs the cashier function. There is no "
            "separate Cashier role. The Pharmacist searches medicines, "
            "processes sales, records prescriptions where required, accepts "
            "payment, issues receipts, and triggers stock reduction through sales."
        ),
    },
]

EXTERNAL_ACTORS = [
    {
        "id": "ACT-CUST",
        "name": "Customer",
        "kind": "external actor",
        "summary": (
            "Buys medicines and may present a prescription. Does not have a "
            "system login. Interacts with the Pharmacist, not with the software "
            "directly (Larman system-boundary rule)."
        ),
    },
    {
        "id": "ACT-SUP",
        "name": "Supplier",
        "kind": "external actor",
        "summary": (
            "Provides stock to the pharmacy. Not a system user. Appears as a "
            "recorded business party when goods are received."
        ),
    },
]

# ---------------------------------------------------------------------------
# Business objectives
# ---------------------------------------------------------------------------
OBJECTIVES = [
    ("BO-01", "Prevent sale of expired or insufficiently stocked medicine."),
    ("BO-02", "Complete counter sales accurately with a printed or viewable receipt."),
    ("BO-03", "Keep inventory quantities consistent with sales and stock movements."),
    ("BO-04", "Support prescription-linked dispensing without creating extra user roles."),
    ("BO-05", "Give the Administrator reliable catalogue, stock, user, and report control."),
    ("BO-06", "Leave an audit trail for sales, voids, stock adjustments, and user changes."),
    ("BO-07", "Fit a 15-week UP schedule with architecture proven before construction."),
]

# ---------------------------------------------------------------------------
# Assumptions — not silently converted into requirements
# ---------------------------------------------------------------------------
ASSUMPTIONS = [
    ("A-01", "Single physical pharmacy (one location).", "Course scope and first deployment.", "Multi-branch stock and pricing would be missing.", "Open"),
    ("A-02", "Exactly two logged-in roles: Administrator and Pharmacist/Cashier.", "Lecturer/project constraint.", "Access control and use-case model would be wrong.", "Confirmed"),
    ("A-03", "The Customer does not operate the software.", "Counter-based pharmacy practice; Larman POS boundary.", "SSDs and actors would change.", "Confirmed"),
    ("A-04", "Card and mobile-money payment are confirmed by the Pharmacist, not by a live gateway in this release.", "Avoids unverifiable third-party integration in a student construction window.", "Payment design would need an external adapter earlier.", "Open"),
    ("A-05", "NHIMA / insurance claim submission is out of scope.", "Existing project scope decision.", "Prescription sale would include claim steps.", "Confirmed"),
    ("A-06", "No public e-commerce storefront.", "POS is an in-pharmacy counter system.", "Architecture and actors would expand.", "Confirmed"),
    ("A-07", "Prescriptions are recorded and checked in-system; there is no national e-prescription feed.", "No available national interface for the project.", "UC-02 extensions would change.", "Open"),
    ("A-08", "Currency is Zambian Kwacha (ZMW).", "Deployment context is Zambia.", "Money formatting and reports would change.", "Confirmed"),
    ("A-09", "English is the UI language for this release.", "Course and team working language.", "Labels and user manual would need translation.", "Confirmed"),
    ("A-10", "The Pharmacist is legally permitted to dispense and take payment.", "Zambian pharmacy practice assumption.", "A third operational role might be demanded in reality.", "Open"),
]

# ---------------------------------------------------------------------------
# Functional requirements
# ---------------------------------------------------------------------------
FRS = [
    ("FR-01", "The system shall authenticate a user with a unique username and a secret password and start a role-specific session."),
    ("FR-02", "The system shall authorise each operation according to exactly one of two roles: Administrator or Pharmacist/Cashier."),
    ("FR-03", "The Pharmacist/Cashier shall be able to start a sale, enter one or more medicine lines, and complete the sale."),
    ("FR-04", "The Pharmacist/Cashier shall be able to search medicines by name, generic name, or product code and see on-hand quantity."),
    ("FR-05", "The system shall refuse a sale line that would sell an expired batch or a quantity greater than available sellable stock."),
    ("FR-06", "When a line requires a prescription, the Pharmacist/Cashier shall record the prescription reference and essential details before the line is accepted."),
    ("FR-07", "The Pharmacist/Cashier shall record payment as cash, card, or mobile money, including amount tendered."),
    ("FR-08", "On successful payment the system shall complete the sale, reduce stock, and produce a receipt."),
    ("FR-09", "The Administrator shall create, update, deactivate, and view medicines in the catalogue (name, generic name, strength, form, category, prescription flag, selling price, reorder level)."),
    ("FR-10", "The Administrator shall receive stock against a supplier, recording batch number, expiry date, quantity, and cost."),
    ("FR-11", "The Administrator shall adjust stock for damage, expiry removal, recount, or recall, with a mandatory reason."),
    ("FR-12", "The system shall present low-stock and near-expiry information to the Administrator."),
    ("FR-13", "The Administrator shall create, update, deactivate, and reset access for users assigned to one of the two roles."),
    ("FR-14", "The Administrator shall maintain supplier records used when receiving stock."),
    ("FR-15", "The Administrator shall view sales and inventory reports for selected date ranges."),
    ("FR-16", "The Pharmacist/Cashier shall look up or record a customer when a sale needs a named patient (typical for prescriptions)."),
    ("FR-17", "The Pharmacist/Cashier shall void an in-progress or completed sale only with a reason; the system shall restore stock for completed voids and write an audit entry."),
    ("FR-18", "The Administrator shall configure pharmacy name, address, receipt footer, and near-expiry warning days."),
    ("FR-19", "The system shall record an audit entry for login failures, sales, voids, stock receipts, stock adjustments, and user administration."),
]

NFRS = [
    ("NFR-01", "Security", "Passwords shall be stored only as a salted hash. Sessions shall expire after inactivity. Role checks shall be enforced on every privileged operation."),
    ("NFR-02", "Performance", "Entering a sale line and refreshing the running total should complete within about three seconds on the intended counter workstation under typical catalogue size. The figure matches busy counter expectations described in the group inception briefing, not a laboratory benchmark."),
    ("NFR-03", "Usability", "A trained Pharmacist/Cashier shall complete a routine three-line OTC sale from one primary sales screen without opening an administration page."),
    ("NFR-04", "Reliability / integrity", "A completed sale and its stock movements shall succeed or fail together. Partial stock reduction without a sale record is not acceptable."),
    ("NFR-05", "Availability", "The system is intended for normal pharmacy opening hours. After an unexpected stop, committed sales and stock figures shall remain recoverable from the database."),
    ("NFR-06", "Maintainability", "Presentation, application, domain, and persistence shall remain separable so that a UI change does not rewrite pricing or stock rules."),
    ("NFR-07", "Scalability", "The first release is one pharmacy. Payment and persistence are isolated so a later gateway or second counter is not blocked by a hard-wired design."),
    ("NFR-08", "Auditability", "Sensitive actions shall be attributable to a user account and a timestamp."),
    ("NFR-09", "Privacy", "Customer and prescription details shall be visible only to authenticated staff and shall not appear unnecessarily on publicly displayed screens."),
    ("NFR-10", "Data integrity", "Database keys, required fields, and non-negative quantities shall protect stock and money figures independently of the user interface."),
]

# ---------------------------------------------------------------------------
# Use cases
# ---------------------------------------------------------------------------
USE_CASES = [
    {
        "id": "UC-01",
        "name": "Authenticate User",
        "actor": "Administrator, Pharmacist/Cashier",
        "priority": "High",
        "iteration": "Elaboration 1 (30%)",
        "frs": ["FR-01", "FR-02", "FR-19"],
        "brief": "A staff member identifies themselves and receives a session limited to their role.",
    },
    {
        "id": "UC-02",
        "name": "Process Sale",
        "actor": "Pharmacist/Cashier",
        "priority": "Critical",
        "iteration": "Inception 10% / Elaboration 1 detailed",
        "frs": ["FR-03", "FR-04", "FR-05", "FR-06", "FR-07", "FR-08", "FR-16"],
        "brief": "The Pharmacist records sold medicines, handles prescription data when required, takes payment, issues a receipt, and reduces stock.",
    },
    {
        "id": "UC-03",
        "name": "Manage Medicines",
        "actor": "Administrator",
        "priority": "High",
        "iteration": "Elaboration 1 (30%)",
        "frs": ["FR-09"],
        "brief": "The Administrator maintains the sellable medicine catalogue.",
    },
    {
        "id": "UC-04",
        "name": "Manage Inventory",
        "actor": "Administrator",
        "priority": "High",
        "iteration": "Elaboration 2 (remaining 70%)",
        "frs": ["FR-10", "FR-11", "FR-12"],
        "brief": "The Administrator receives batches, adjusts stock, and reviews low-stock and near-expiry alerts.",
    },
    {
        "id": "UC-05",
        "name": "Manage Users",
        "actor": "Administrator",
        "priority": "High",
        "iteration": "Elaboration 2 (remaining 70%)",
        "frs": ["FR-13", "FR-19"],
        "brief": "The Administrator creates and maintains the two allowed account types.",
    },
    {
        "id": "UC-06",
        "name": "Manage Suppliers",
        "actor": "Administrator",
        "priority": "Medium",
        "iteration": "Elaboration 2 (remaining 70%)",
        "frs": ["FR-14"],
        "brief": "The Administrator keeps supplier details used when stock is received.",
    },
    {
        "id": "UC-07",
        "name": "View Reports",
        "actor": "Administrator",
        "priority": "Medium",
        "iteration": "Elaboration 2 (remaining 70%)",
        "frs": ["FR-15"],
        "brief": "The Administrator reviews sales and stock reports for a chosen period.",
    },
    {
        "id": "UC-08",
        "name": "Record Customer",
        "actor": "Pharmacist/Cashier",
        "priority": "Medium",
        "iteration": "Elaboration 2 (remaining 70%)",
        "frs": ["FR-16"],
        "brief": "The Pharmacist finds or records a customer used on a prescription-linked sale.",
    },
    {
        "id": "UC-09",
        "name": "Void Sale",
        "actor": "Pharmacist/Cashier",
        "priority": "High",
        "iteration": "Elaboration 2 (remaining 70%)",
        "frs": ["FR-17", "FR-19"],
        "brief": "The Pharmacist cancels a sale with a reason; stock and audit records stay consistent.",
    },
    {
        "id": "UC-10",
        "name": "Configure Pharmacy",
        "actor": "Administrator",
        "priority": "Low",
        "iteration": "Elaboration 2 (remaining 70%)",
        "frs": ["FR-18"],
        "brief": "The Administrator sets pharmacy identity and receipt/alert defaults.",
    },
]

# ---------------------------------------------------------------------------
# Fully dressed use cases (Larman / Cockburn style)
# ---------------------------------------------------------------------------
DETAILED_UCS = {
    "UC-01": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Staff member (Administrator or Pharmacist/Cashier)",
        "stakeholders": [
            ("Staff member", "Gains access only to functions of their assigned role."),
            ("Pharmacy owner", "Unauthorised people cannot sell or alter stock."),
            ("Auditor", "Failed and successful logins can be investigated."),
        ],
        "preconditions": "The user has an active account. The application is available.",
        "success": "A session exists, the role is known, and the correct home screen is shown.",
        "main": [
            "The staff member starts the Pharmacy POS application.",
            "The system presents the login prompt.",
            "The staff member enters username and password.",
            "The system verifies the credentials against the stored password hash and confirms the account is active.",
            "The system creates a session containing user identity and role.",
            "The system opens the Administrator dashboard or the Pharmacist sales screen according to role.",
        ],
        "extensions": [
            "4a. Credentials are wrong: the system refuses access, records a failed-login audit entry, and invites a retry.",
            "4b. Account is deactivated: the system refuses access and explains that an Administrator must restore the account.",
            "4c. Repeated failures in a short period: the system keeps refusing and keeps the audit trail (lockout policy may be applied in construction).",
        ],
        "special": "Passwords are never displayed or stored in recoverable form.",
        "tech": "Keyboard login on the counter or office workstation.",
        "frequency": "At the start of each shift and after session timeout.",
    },
    "UC-02": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Pharmacist/Cashier",
        "stakeholders": [
            ("Pharmacist/Cashier", "Completes the sale quickly and correctly."),
            ("Customer", "Pays the correct amount and receives the intended medicines plus a receipt."),
            ("Pharmacy owner", "Money and stock stay consistent; expired stock is not sold."),
            ("Regulator", "Prescription-only items are not sold without recorded prescription details."),
        ],
        "preconditions": "The Pharmacist/Cashier is authenticated. At least one sellable medicine exists.",
        "success": "A completed Sale, Payment, stock reduction, and Receipt exist. Prescription details exist when required.",
        "main": [
            "The Pharmacist/Cashier chooses to start a new sale (system event: makeNewSale).",
            "The system creates a Sale in progress and shows an empty line list and a zero total.",
            "The Pharmacist/Cashier identifies a medicine by search or product code and enters a quantity (system event: enterItem).",
            "The system locates a sellable StockBatch (unexpired, sufficient quantity), adds a SalesLineItem, and returns description, unit price, line total, and running total.",
            "The Pharmacist/Cashier repeats step 3–4 for each additional medicine.",
            "If any accepted line is prescription-only, the Pharmacist/Cashier records the customer (or uses an existing customer) and the prescription reference (system event: attachPrescription).",
            "The Pharmacist/Cashier indicates the sale content is complete (system event: endSale).",
            "The system calculates tax if configured and presents the total due.",
            "The Pharmacist/Cashier records the payment method and amount tendered (system event: makePayment).",
            "The system records Payment, marks the Sale complete, reduces batch quantities, writes audit data, and presents the Receipt.",
            "The Pharmacist/Cashier gives medicines and the receipt to the Customer.",
        ],
        "extensions": [
            "3a. Medicine is not found: the system says so; the sale remains in progress.",
            "3b. Only expired batches exist: the system refuses the line (BO-01 / FR-05).",
            "3c. Requested quantity exceeds sellable stock: the system refuses the line and shows the available quantity.",
            "3d. Pharmacist/Cashier removes a line before payment: the system deletes that SalesLineItem and updates the total.",
            "6a. Prescription-only line without prescription details: the system refuses to end the sale until details are recorded.",
            "6b. Customer is new: include UC-08 Record Customer, then continue.",
            "8a. Pharmacist/Cashier cancels the in-progress sale: no payment, no stock change (related to UC-09).",
            "9a. Amount tendered is less than total for a cash sale: the system refuses completion and shows the shortfall.",
            "9b. Card or mobile money: the Pharmacist/Cashier confirms that payment was received externally; the system records method and reference. Live gateway settlement is out of scope (A-04).",
            "10a. Persistence fails after payment intent: the system does not report success; no partial stock reduction remains (NFR-04).",
        ],
        "special": "Sale completion and stock reduction are one business transaction. Receipt shows pharmacy name, date, lines, total, payment method, and cashier identity (the Pharmacist user).",
        "tech": "Product code may be typed; barcode scan is a technology variation of enterItem, not a separate use case (Larman: name events at the level of intent).",
        "frequency": "Core daily work of the counter — typically many times per hour.",
    },
    "UC-03": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Administrator",
        "stakeholders": [
            ("Administrator", "Keeps the catalogue accurate."),
            ("Pharmacist/Cashier", "Can find the correct sellable item at the counter."),
        ],
        "preconditions": "Administrator is authenticated.",
        "success": "The medicine catalogue reflects the intended create/update/deactivate action.",
        "main": [
            "The Administrator opens medicine maintenance.",
            "The Administrator searches or starts a new medicine.",
            "The Administrator enters or edits name, generic name, strength, form, category, prescription-required flag, selling price, and reorder level.",
            "The system validates required fields and unique product code.",
            "The Administrator confirms the save.",
            "The system stores the medicine and records an audit entry.",
        ],
        "extensions": [
            "4a. Duplicate product code: the system rejects the save.",
            "4b. Invalid price or empty required field: the system rejects the save.",
            "5a. Deactivate instead of update: the medicine remains in history but is not offered for new sale lines.",
        ],
        "special": "Deactivation is preferred to physical deletion so old sales remain explainable.",
        "tech": "Office workstation, keyboard and mouse.",
        "frequency": "Whenever the assortment or price list changes.",
    },
    "UC-04": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Administrator",
        "stakeholders": [
            ("Administrator", "Stock on the shelf matches the system."),
            ("Pharmacist/Cashier", "Sellable quantities shown at the counter are trustworthy."),
        ],
        "preconditions": "Administrator is authenticated. For receiving, the supplier and medicine already exist.",
        "success": "A stock receipt or adjustment is stored; batch quantities change; alerts refresh.",
        "main": [
            "The Administrator chooses Receive Stock or Adjust Stock.",
            "Receive: the Administrator selects a supplier and adds lines (medicine, batch number, expiry, quantity, cost).",
            "The system creates or increases a StockBatch and records a StockReceipt.",
            "Adjust: the Administrator selects a batch, quantity change, and reason (damage, expiry removal, recount, recall).",
            "The system applies the adjustment if the resulting quantity would not be negative.",
            "The system updates low-stock and near-expiry views.",
        ],
        "extensions": [
            "2a. Expiry date is not in the future for a new receipt: the system warns; the Administrator may cancel.",
            "5a. Adjustment would make quantity negative: the system refuses.",
            "5b. Expiry removal of an entire batch: quantity becomes zero and the batch is not sellable.",
        ],
        "special": "Every adjustment requires a reason. Receipts of stock are not performed by the Pharmacist/Cashier role.",
        "tech": "Keyboard entry of supplier documents.",
        "frequency": "Deliveries and periodic stock checks.",
    },
    "UC-05": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Administrator",
        "stakeholders": [
            ("Administrator", "Only intended people can log in."),
            ("Staff member", "Receives a working account of the correct role."),
        ],
        "preconditions": "Administrator is authenticated.",
        "success": "A user account exists or is updated with exactly one of the two roles.",
        "main": [
            "The Administrator opens user maintenance.",
            "The Administrator creates or selects a user.",
            "The Administrator assigns username, full name, role (Administrator or Pharmacist/Cashier), and an initial password.",
            "The system stores a password hash, not the password itself.",
            "The Administrator may later deactivate the account or reset the password.",
        ],
        "extensions": [
            "3a. A third role is requested: the system does not offer one.",
            "3b. Duplicate username: the system rejects the save.",
        ],
        "special": "At least one active Administrator should remain.",
        "tech": "Office workstation.",
        "frequency": "Staff join, leave, or forget passwords.",
    },
    "UC-06": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Administrator",
        "stakeholders": [("Administrator", "Can identify who supplied a batch.")],
        "preconditions": "Administrator is authenticated.",
        "success": "Supplier name and contact details are stored or updated.",
        "main": [
            "The Administrator opens supplier maintenance.",
            "The Administrator creates or edits name, phone, and address.",
            "The system validates the name and saves the supplier.",
        ],
        "extensions": ["3a. Duplicate active supplier name: the system warns before save."],
        "special": "Suppliers are not system users and cannot log in.",
        "tech": "Office workstation.",
        "frequency": "When a new wholesaler is used.",
    },
    "UC-07": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Administrator",
        "stakeholders": [("Pharmacy owner / Administrator", "Sees sales value and stock movement for a period.")],
        "preconditions": "Administrator is authenticated.",
        "success": "A report for the selected type and date range is displayed.",
        "main": [
            "The Administrator chooses a report type (daily sales, period sales, low stock, near expiry).",
            "The Administrator enters a date range where applicable.",
            "The system aggregates stored sales and stock data and displays the report.",
        ],
        "extensions": ["3a. No data in range: the system shows an empty report, not an error."],
        "special": "Reports are read-only.",
        "tech": "Screen display; printing is a technology variation.",
        "frequency": "Daily close and periodic review.",
    },
    "UC-08": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Pharmacist/Cashier",
        "stakeholders": [
            ("Pharmacist/Cashier", "Can attach a patient name to a prescription sale."),
            ("Customer", "Is not forced to register for a simple OTC sale."),
        ],
        "preconditions": "Pharmacist/Cashier is authenticated.",
        "success": "A customer record is found or created and can be linked to the current sale.",
        "main": [
            "The Pharmacist/Cashier searches by name or phone.",
            "If found, the Pharmacist/Cashier selects the customer.",
            "If not found, the Pharmacist/Cashier enters name and optional phone and address.",
            "The system stores the customer and returns the identifier.",
        ],
        "extensions": ["1a. Search is skipped for a purely OTC sale: this use case is not required."],
        "special": "Minimal data: a name is enough. Extra medical history is out of scope.",
        "tech": "Sales screen or a small customer dialog.",
        "frequency": "Whenever a prescription-linked sale needs a named patient.",
    },
    "UC-09": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Pharmacist/Cashier",
        "stakeholders": [
            ("Pharmacist/Cashier", "Can correct a mistake without corrupting stock."),
            ("Auditor", "Sees that the original sale was voided, not silently deleted."),
        ],
        "preconditions": "Pharmacist/Cashier is authenticated. A sale in progress or a completed sale from the current business day is selected.",
        "success": "The sale is marked void. If it had reduced stock, quantities are restored. An audit entry exists.",
        "main": [
            "The Pharmacist/Cashier selects the sale and chooses Void.",
            "The system demands a reason.",
            "The Pharmacist/Cashier enters the reason and confirms.",
            "The system marks the sale void, reverses stock for completed sales, and writes the audit entry.",
        ],
        "extensions": [
            "1a. Sale is already void: the system refuses a second void.",
            "3a. Confirmation cancelled: no change.",
        ],
        "special": "Voids are retained historically. There is no silent delete.",
        "tech": "Sales screen.",
        "frequency": "Occasional error correction.",
    },
    "UC-10": {
        "scope": "Pharmacy POS application",
        "level": "User goal",
        "primary": "Administrator",
        "stakeholders": [("Administrator", "Receipts and alerts show the correct pharmacy identity.")],
        "preconditions": "Administrator is authenticated.",
        "success": "Pharmacy name, address, receipt footer, and near-expiry days are stored.",
        "main": [
            "The Administrator opens pharmacy settings.",
            "The Administrator edits the fields and saves.",
            "The system applies the values to new receipts and alert calculations.",
        ],
        "extensions": ["2a. Near-expiry days is not a positive number: the system rejects the save."],
        "special": "Settings are not a third user role.",
        "tech": "Office workstation.",
        "frequency": "Setup and rare changes.",
    },
}

# ---------------------------------------------------------------------------
# Risks — evolved across iterations (no fake construction outcomes)
# ---------------------------------------------------------------------------
RISKS_INCEPTION = [
    ("R-01", "Sale and stock update diverge (double-sell or missing decrement).", "High", "High", "Critical", "Prove one business transaction in the architectural PoC.", "Inception", "Open"),
    ("R-02", "Expired medicine can be sold.", "Medium", "High", "High", "Batch expiry is a first-class domain rule in enterItem.", "Inception", "Open"),
    ("R-03", "A third role creeps in and breaks the two-role rule.", "Medium", "High", "High", "Actors and authorisation designed as two roles only.", "Inception", "Open"),
    ("R-04", "Payment recorded but sale not completed, or the reverse.", "Medium", "High", "High", "makePayment completes sale only after Payment is accepted in the same transaction.", "Inception", "Open"),
    ("R-05", "Staff resist a new counter workflow.", "Medium", "Medium", "Medium", "Keep the sales UI on one screen; plan Transition training.", "Inception", "Open"),
    ("R-06", "Scope grows into NHIMA claims or e-commerce.", "High", "High", "High", "Out-of-scope list is explicit; iteration plan stays POS-centred.", "Inception", "Open"),
    ("R-07", "Fifteen-week calendar is consumed by late architecture work.", "Medium", "High", "High", "Risk-driven Elaboration 1 proves Process Sale before feature breadth.", "Inception", "Open"),
    ("R-08", "Data loss after workstation or power failure.", "Low", "High", "Medium", "Persistence in a real database; backup plan in Transition.", "Inception", "Open"),
    ("R-09", "Prescription recording is legally insufficient.", "Medium", "Medium", "Medium", "Record reference + patient; do not claim national e-prescription.", "Inception", "Open"),
    ("R-10", "Layered design is too slow or too tangled for a counter sale.", "Medium", "High", "High", "Architectural PoC walks makeNewSale–enterItem–makePayment through all layers.", "Inception", "Open"),
]

RISKS_ELAB1 = [
    ("R-01", "Sale and stock update diverge.", "Medium", "High", "High", "PoC specifies a single application transaction around completeSale.", "Elaboration 1", "Mitigating"),
    ("R-02", "Expired medicine can be sold.", "Low", "High", "Medium", "Domain rule specified: only unexpired sellable batches are chosen.", "Elaboration 1", "Mitigating"),
    ("R-03", "Third-role creep.", "Low", "High", "Medium", "Use-case and SSD actors confirmed as two system users.", "Elaboration 1", "Mitigating"),
    ("R-04", "Payment / sale inconsistency.", "Medium", "High", "High", "SSD and operation contract tie makePayment to completion.", "Elaboration 1", "Mitigating"),
    ("R-05", "Staff resist new workflow.", "Medium", "Medium", "Medium", "Sales screen concept kept on one surface.", "Elaboration 1", "Open"),
    ("R-06", "Scope creep.", "Medium", "High", "Medium", "Insurance and web shop remain out of scope.", "Elaboration 1", "Mitigating"),
    ("R-07", "Schedule slip.", "Medium", "High", "High", "Iteration 1 limited to 30% architecturally significant use cases.", "Elaboration 1", "Mitigating"),
    ("R-08", "Data loss.", "Low", "High", "Medium", "Logical schema started; physical DB still construction.", "Elaboration 1", "Open"),
    ("R-09", "Prescription legal sufficiency.", "Medium", "Medium", "Medium", "attachPrescription is a first-class system event.", "Elaboration 1", "Mitigating"),
    ("R-10", "Architecture unfit for POS.", "Low", "High", "Medium", "Layered PoC documented with clear dependencies.", "Elaboration 1", "Mitigating"),
]

RISKS_ELAB2 = [
    ("R-01", "Sale and stock update diverge.", "Low", "High", "Medium", "SaleService.completeSale collaborates with Inventory and repositories in one unit of work.", "Elaboration 2", "Mitigated in design"),
    ("R-02", "Expired medicine can be sold.", "Low", "High", "Medium", "StockBatch.isSellable() is Information Expert for expiry and quantity.", "Elaboration 2", "Mitigated in design"),
    ("R-03", "Third-role creep.", "Low", "High", "Low", "User.role is an enumeration of two values in schema and UI.", "Elaboration 2", "Mitigated in design"),
    ("R-04", "Payment / sale inconsistency.", "Low", "High", "Medium", "Payment created by Sale; completion only after accepted payment.", "Elaboration 2", "Mitigated in design"),
    ("R-05", "Staff resist new workflow.", "Medium", "Medium", "Medium", "UI prototypes issued for counter and admin paths.", "Elaboration 2", "Mitigating"),
    ("R-06", "Scope creep.", "Low", "High", "Low", "Remaining 70% use cases do not add insurance or web shop.", "Elaboration 2", "Mitigated in design"),
    ("R-07", "Schedule slip.", "Medium", "Medium", "Medium", "Construction will implement by feature priority, not by layer-in-isolation.", "Elaboration 2", "Open"),
    ("R-08", "Data loss.", "Low", "High", "Medium", "Schema includes keys, required fields, audit table; backup remains Transition.", "Elaboration 2", "Mitigating"),
    ("R-09", "Prescription legal sufficiency.", "Medium", "Medium", "Medium", "Prescription and Customer tables designed; national feed still out of scope.", "Elaboration 2", "Mitigated in design"),
    ("R-10", "Architecture unfit for POS.", "Low", "Medium", "Low", "DCD and GRASP keep controllers thin and domain cohesive.", "Elaboration 2", "Mitigated in design"),
    ("R-11", "UI prototypes misunderstood as finished product.", "Medium", "Low", "Low", "Prototypes labelled as design only.", "Elaboration 2", "Open"),
]

RISKS_CONSTRUCTION_PLANNED = [
    ("R-01", "Concurrency defect during two overlapping sales of the last pack.", "Medium", "High", "High", "Integration tests + transactional decrement. Results: TO BE COMPLETED DURING CONSTRUCTION", "Construction", "Planned"),
    ("R-07", "Features slip inside Iterations 3–4.", "Medium", "High", "High", "Priority list: sale spine first, then inventory, then reports.", "Construction", "Planned"),
    ("R-12", "Tests exist only for happy paths.", "Medium", "Medium", "Medium", "Unit cases include expiry, short stock, void, and bad login.", "Construction", "Planned"),
    ("R-13", "Git history is unusable for marking.", "Low", "Medium", "Low", "Feature branches, PR reviews, CI on main.", "Construction", "Planned"),
]

RISKS_TRANSITION_PLANNED = [
    ("R-05", "Staff resist or misuse the counter screen.", "Medium", "Medium", "Medium", "Beta with real Pharmacist/Cashier and Administrator. TO BE COMPLETED DURING TRANSITION", "Transition", "Planned"),
    ("R-08", "No backup/restore rehearsal.", "Low", "High", "Medium", "Transition checklist includes restore drill. TO BE COMPLETED DURING TRANSITION", "Transition", "Planned"),
    ("R-14", "Performance on a real machine differs from design target.", "Medium", "Medium", "Medium", "Measure line-entry time in beta; tune queries if needed. TO BE COMPLETED DURING TRANSITION", "Transition", "Planned"),
]

# ---------------------------------------------------------------------------
# Domain conceptual classes (NO methods)
# ---------------------------------------------------------------------------
DOMAIN_CLASSES = [
    ("Pharmacy", "The pharmacy that owns catalogue, stock, users, and sales."),
    ("User", "A person with a system account. Role is Administrator or Pharmacist/Cashier."),
    ("Medicine", "A sellable pharmaceutical product definition (catalogue item)."),
    ("MedicineCategory", "A grouping such as antibiotic, analgesic, or OTC sundry."),
    ("StockBatch", "A physical quantity of a medicine with batch number and expiry."),
    ("Sale", "A sales transaction in progress or completed."),
    ("SalesLineItem", "One medicine and quantity on a sale."),
    ("Payment", "Money recorded against a sale (cash, card, or mobile money)."),
    ("Customer", "A patient or buyer recorded when a name is required."),
    ("Prescription", "A recorded authority to dispense specific medicines."),
    ("PrescriptionItem", "One medicine and quantity authorised on a prescription."),
    ("Supplier", "An external wholesaler or manufacturer source of stock."),
    ("StockReceipt", "A delivery of stock from a supplier."),
    ("StockReceiptLine", "One batch line on a stock receipt."),
    ("StockAdjustment", "A non-sale quantity change with a reason."),
    ("AuditEntry", "A recorded security- or stock-sensitive action."),
]

# ---------------------------------------------------------------------------
# Database tables (logical design — not implementation scripts)
# ---------------------------------------------------------------------------
TABLES = {
    "users": [
        ("user_id", "INT", "Y", "", "N", "Surrogate primary key."),
        ("username", "VARCHAR(50)", "", "", "N", "Unique login name."),
        ("full_name", "VARCHAR(120)", "", "", "N", "Display name on receipts and audit."),
        ("role", "VARCHAR(20)", "", "", "N", "ADMINISTRATOR or PHARMACIST."),
        ("password_hash", "VARCHAR(255)", "", "", "N", "Salted hash only. Never plaintext."),
        ("password_salt", "VARCHAR(64)", "", "", "N", "Per-user salt if not embedded in the hash."),
        ("is_active", "BOOLEAN", "", "", "N", "Deactivated accounts cannot authenticate."),
        ("created_at", "DATETIME", "", "", "N", "Account creation time."),
        ("last_login_at", "DATETIME", "", "", "Y", "Last successful login."),
    ],
    "pharmacy_settings": [
        ("pharmacy_id", "INT", "Y", "", "N", "Single-row settings key for this deployment."),
        ("name", "VARCHAR(160)", "", "", "N", "Pharmacy trading name."),
        ("address", "VARCHAR(255)", "", "", "Y", "Printed on receipts."),
        ("phone", "VARCHAR(40)", "", "", "Y", "Printed on receipts."),
        ("receipt_footer", "VARCHAR(255)", "", "", "Y", "Thank-you or regulatory line."),
        ("near_expiry_days", "INT", "", "", "N", "Days used for near-expiry alerts."),
        ("currency_code", "CHAR(3)", "", "", "N", "ZMW for this project."),
    ],
    "medicine_categories": [
        ("category_id", "INT", "Y", "", "N", "Primary key."),
        ("name", "VARCHAR(80)", "", "", "N", "Unique category name."),
        ("description", "VARCHAR(255)", "", "", "Y", "Optional note."),
    ],
    "medicines": [
        ("medicine_id", "INT", "Y", "", "N", "Primary key."),
        ("product_code", "VARCHAR(40)", "", "", "N", "Unique SKU / product code."),
        ("name", "VARCHAR(160)", "", "", "N", "Brand or dispensing name."),
        ("generic_name", "VARCHAR(160)", "", "", "Y", "INN / generic name."),
        ("strength", "VARCHAR(40)", "", "", "Y", "For example 500 mg."),
        ("form", "VARCHAR(40)", "", "", "Y", "Tablet, syrup, cream."),
        ("category_id", "INT", "", "medicine_categories.category_id", "Y", "Optional category."),
        ("requires_prescription", "BOOLEAN", "", "", "N", "True for prescription-only items."),
        ("unit_price", "DECIMAL(12,2)", "", "", "N", "Current selling price."),
        ("reorder_level", "INT", "", "", "N", "Low-stock threshold."),
        ("is_active", "BOOLEAN", "", "", "N", "Inactive medicines are not sold."),
    ],
    "suppliers": [
        ("supplier_id", "INT", "Y", "", "N", "Primary key."),
        ("name", "VARCHAR(160)", "", "", "N", "Supplier trading name."),
        ("phone", "VARCHAR(40)", "", "", "Y", "Contact phone."),
        ("address", "VARCHAR(255)", "", "", "Y", "Contact address."),
        ("is_active", "BOOLEAN", "", "", "N", "Soft delete flag."),
    ],
    "stock_batches": [
        ("batch_id", "INT", "Y", "", "N", "Primary key."),
        ("medicine_id", "INT", "", "medicines.medicine_id", "N", "Medicine of this batch."),
        ("batch_number", "VARCHAR(60)", "", "", "N", "Manufacturer / supplier batch no."),
        ("expiry_date", "DATE", "", "", "N", "Not sellable after this date."),
        ("quantity_on_hand", "INT", "", "", "N", "Current sellable quantity."),
        ("unit_cost", "DECIMAL(12,2)", "", "", "Y", "Optional cost for valuation."),
        ("received_at", "DATETIME", "", "", "N", "First receipt time."),
    ],
    "stock_receipts": [
        ("receipt_id", "INT", "Y", "", "N", "Primary key."),
        ("supplier_id", "INT", "", "suppliers.supplier_id", "N", "Source supplier."),
        ("received_by_user_id", "INT", "", "users.user_id", "N", "Administrator who received."),
        ("received_at", "DATETIME", "", "", "N", "Receipt time."),
        ("reference_note", "VARCHAR(120)", "", "", "Y", "Delivery note number."),
    ],
    "stock_receipt_lines": [
        ("receipt_line_id", "INT", "Y", "", "N", "Primary key."),
        ("receipt_id", "INT", "", "stock_receipts.receipt_id", "N", "Parent receipt."),
        ("batch_id", "INT", "", "stock_batches.batch_id", "N", "Batch increased."),
        ("quantity", "INT", "", "", "N", "Quantity received."),
    ],
    "stock_adjustments": [
        ("adjustment_id", "INT", "Y", "", "N", "Primary key."),
        ("batch_id", "INT", "", "stock_batches.batch_id", "N", "Adjusted batch."),
        ("adjusted_by_user_id", "INT", "", "users.user_id", "N", "Administrator."),
        ("quantity_delta", "INT", "", "", "N", "Signed quantity change."),
        ("reason", "VARCHAR(40)", "", "", "N", "DAMAGE, EXPIRY, RECOUNT, RECALL."),
        ("note", "VARCHAR(255)", "", "", "Y", "Free-text explanation."),
        ("adjusted_at", "DATETIME", "", "", "N", "When the change occurred."),
    ],
    "customers": [
        ("customer_id", "INT", "Y", "", "N", "Primary key."),
        ("full_name", "VARCHAR(160)", "", "", "N", "Patient or buyer name."),
        ("phone", "VARCHAR(40)", "", "", "Y", "Optional phone."),
        ("address", "VARCHAR(255)", "", "", "Y", "Optional address."),
        ("created_at", "DATETIME", "", "", "N", "When first recorded."),
    ],
    "prescriptions": [
        ("prescription_id", "INT", "Y", "", "N", "Primary key."),
        ("customer_id", "INT", "", "customers.customer_id", "N", "Named patient."),
        ("reference_no", "VARCHAR(60)", "", "", "N", "Paper / clinic reference."),
        ("prescriber_name", "VARCHAR(160)", "", "", "Y", "Doctor or clinic if known."),
        ("issued_on", "DATE", "", "", "Y", "Prescription date if known."),
        ("recorded_by_user_id", "INT", "", "users.user_id", "N", "Pharmacist who recorded it."),
        ("recorded_at", "DATETIME", "", "", "N", "Capture time."),
    ],
    "prescription_items": [
        ("prescription_item_id", "INT", "Y", "", "N", "Primary key."),
        ("prescription_id", "INT", "", "prescriptions.prescription_id", "N", "Parent prescription."),
        ("medicine_id", "INT", "", "medicines.medicine_id", "N", "Authorised medicine."),
        ("quantity", "INT", "", "", "N", "Authorised quantity."),
    ],
    "sales": [
        ("sale_id", "INT", "Y", "", "N", "Primary key."),
        ("sold_by_user_id", "INT", "", "users.user_id", "N", "Pharmacist/Cashier."),
        ("customer_id", "INT", "", "customers.customer_id", "Y", "Optional customer."),
        ("prescription_id", "INT", "", "prescriptions.prescription_id", "Y", "Optional linked prescription."),
        ("status", "VARCHAR(20)", "", "", "N", "IN_PROGRESS, COMPLETED, VOIDED."),
        ("started_at", "DATETIME", "", "", "N", "makeNewSale time."),
        ("completed_at", "DATETIME", "", "", "Y", "Completion or void time."),
        ("void_reason", "VARCHAR(255)", "", "", "Y", "Required when VOIDED."),
        ("subtotal", "DECIMAL(12,2)", "", "", "N", "Sum of line totals."),
        ("total", "DECIMAL(12,2)", "", "", "N", "Amount due."),
    ],
    "sale_items": [
        ("sale_item_id", "INT", "Y", "", "N", "Primary key."),
        ("sale_id", "INT", "", "sales.sale_id", "N", "Parent sale."),
        ("medicine_id", "INT", "", "medicines.medicine_id", "N", "Sold medicine."),
        ("batch_id", "INT", "", "stock_batches.batch_id", "N", "Batch decremented."),
        ("quantity", "INT", "", "", "N", "Quantity sold."),
        ("unit_price", "DECIMAL(12,2)", "", "", "N", "Price at time of sale."),
        ("line_total", "DECIMAL(12,2)", "", "", "N", "quantity * unit_price."),
    ],
    "payments": [
        ("payment_id", "INT", "Y", "", "N", "Primary key."),
        ("sale_id", "INT", "", "sales.sale_id", "N", "Paid sale (1:1 for this design)."),
        ("method", "VARCHAR(20)", "", "", "N", "CASH, CARD, MOBILE_MONEY."),
        ("amount_tendered", "DECIMAL(12,2)", "", "", "N", "Amount given or confirmed."),
        ("change_due", "DECIMAL(12,2)", "", "", "N", "Cash change; zero otherwise."),
        ("external_reference", "VARCHAR(80)", "", "", "Y", "Card/mobile confirmation note."),
        ("paid_at", "DATETIME", "", "", "N", "Payment time."),
    ],
    "audit_logs": [
        ("audit_id", "INT", "Y", "", "N", "Primary key."),
        ("user_id", "INT", "", "users.user_id", "Y", "Null only for failed unknown login."),
        ("action", "VARCHAR(40)", "", "", "N", "LOGIN, LOGIN_FAIL, SALE_COMPLETE, VOID, STOCK_RECEIPT, STOCK_ADJUST, USER_ADMIN."),
        ("entity_name", "VARCHAR(40)", "", "", "Y", "Affected table or concept."),
        ("entity_id", "INT", "", "", "Y", "Affected key."),
        ("details", "VARCHAR(500)", "", "", "Y", "Non-sensitive summary."),
        ("occurred_at", "DATETIME", "", "", "N", "Event time."),
    ],
}

RELATIONSHIPS = [
    ("users", "sales", "1", "0..*", "A pharmacist records many sales."),
    ("users", "stock_receipts", "1", "0..*", "An administrator records many receipts."),
    ("users", "stock_adjustments", "1", "0..*", "An administrator records many adjustments."),
    ("medicine_categories", "medicines", "1", "0..*", "A category groups many medicines."),
    ("medicines", "stock_batches", "1", "0..*", "A medicine has many batches."),
    ("suppliers", "stock_receipts", "1", "0..*", "A supplier is the source of many receipts."),
    ("stock_receipts", "stock_receipt_lines", "1", "1..*", "A receipt contains lines."),
    ("stock_batches", "stock_receipt_lines", "1", "0..*", "A batch may be increased by receipt lines."),
    ("stock_batches", "stock_adjustments", "1", "0..*", "A batch may be adjusted many times."),
    ("customers", "prescriptions", "1", "0..*", "A customer may have many recorded prescriptions."),
    ("customers", "sales", "1", "0..*", "A customer may appear on many sales."),
    ("prescriptions", "prescription_items", "1", "1..*", "A prescription lists items."),
    ("medicines", "prescription_items", "1", "0..*", "A medicine may appear on prescriptions."),
    ("prescriptions", "sales", "1", "0..1", "A prescription may be linked to a sale."),
    ("sales", "sale_items", "1", "1..*", "A sale contains line items."),
    ("medicines", "sale_items", "1", "0..*", "A medicine appears on many sale lines."),
    ("stock_batches", "sale_items", "1", "0..*", "A batch is sold on many lines over time."),
    ("sales", "payments", "1", "0..1", "A completed sale has one payment in this design."),
    ("users", "audit_logs", "1", "0..*", "A user generates many audit rows."),
]

# ---------------------------------------------------------------------------
# Features for construction tracking (not yet implemented)
# ---------------------------------------------------------------------------
FEATURES = [
    ("F-01", "Authenticate and authorise two roles", "UC-01", "Iteration 3", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-02", "Process OTC sale with receipt", "UC-02", "Iteration 3", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-03", "Search medicine and show sellable quantity", "UC-02", "Iteration 3", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-04", "Refuse expired and oversold lines", "UC-02", "Iteration 3", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-05", "Record payment (cash / card / mobile money)", "UC-02", "Iteration 3", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-06", "Complete sale and decrement stock atomically", "UC-02", "Iteration 3", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-07", "Prescription capture on prescription-only lines", "UC-02", "Iteration 3", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-08", "Manage medicines", "UC-03", "Iteration 3", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-09", "Receive stock batches", "UC-04", "Iteration 4", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-10", "Adjust stock and show alerts", "UC-04", "Iteration 4", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-11", "Manage users", "UC-05", "Iteration 4", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-12", "Manage suppliers", "UC-06", "Iteration 4", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-13", "View reports", "UC-07", "Iteration 4", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-14", "Record customer", "UC-08", "Iteration 4", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-15", "Void sale with stock restore", "UC-09", "Iteration 4", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-16", "Configure pharmacy settings", "UC-10", "Iteration 4", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
    ("F-17", "Audit log for sensitive actions", "UC-01 / UC-09", "Iteration 4", "Planned", "TO BE COMPLETED DURING CONSTRUCTION"),
]

UNIT_TESTS = [
    ("UT-01", "FR-01 / UC-01", "AuthenticationService", "Correct password hash yields a session with the stored role."),
    ("UT-02", "FR-01 / UC-01", "AuthenticationService", "Wrong password yields no session."),
    ("UT-03", "FR-02 / UC-01", "AuthorisationPolicy", "Pharmacist cannot invoke medicine-create."),
    ("UT-04", "FR-05 / UC-02", "StockBatch", "isSellable is false when expiry_date is before today."),
    ("UT-05", "FR-05 / UC-02", "StockBatch", "isSellable is false when quantity_on_hand is 0."),
    ("UT-06", "FR-03 / UC-02", "Sale", "Adding a valid line increases total by quantity * unit_price."),
    ("UT-07", "FR-08 / UC-02", "SaleService", "completeSale reduces batch quantity by the line quantity."),
    ("UT-08", "NFR-04 / UC-02", "SaleService", "If payment persistence fails, quantity_on_hand is unchanged."),
    ("UT-09", "FR-06 / UC-02", "Sale", "endSale is rejected when a prescription-only line has no prescription."),
    ("UT-10", "FR-17 / UC-09", "SaleService", "voidCompletedSale restores batch quantity and sets status VOIDED."),
    ("UT-11", "FR-07 / UC-02", "Payment", "Cash with amount_tendered < total is rejected."),
    ("UT-12", "FR-09 / UC-03", "Medicine", "Duplicate product_code is rejected."),
]

INTEGRATION_TESTS = [
    ("IT-01", "UC-02", "POS sale path", "Login as Pharmacist, makeNewSale, enterItem, endSale, makePayment, reload sale and batch from database."),
    ("IT-02", "UC-02", "Expiry refusal path", "Seed an expired batch; enterItem is refused; no sale_item row."),
    ("IT-03", "UC-02 / UC-08", "Prescription path", "Prescription-only medicine requires customer + prescription before completion."),
    ("IT-04", "UC-04 / UC-02", "Receive then sell", "Administrator receives a batch; Pharmacist sells one unit; quantity is original minus one."),
    ("IT-05", "UC-09", "Void path", "Completed sale voided; batch quantity restored; audit_logs row exists."),
    ("IT-06", "UC-01 / UC-03", "Role boundary", "Pharmacist session calling medicine-create API/service is denied."),
    ("IT-07", "UC-05", "User admin path", "Administrator creates a Pharmacist user; that user can authenticate."),
    ("IT-08", "UC-07", "Report path", "Two completed sales in range appear once each on the period sales report."),
]

GRASP_ROWS = [
    ("Handle system events of UC-02", "SaleController", "SaleService, Sale", "A use-case (facade) controller receives actor events without putting UI logic in the domain.", "Controller"),
    ("Create SalesLineItem", "Sale", "SalesLineItem, Medicine, StockBatch", "Sale contains the lines and knows the moment they are added.", "Creator"),
    ("Create Payment", "Sale", "Payment", "Sale records the payment that completes it.", "Creator"),
    ("Know line total", "SalesLineItem", "Medicine (price copied)", "The line has quantity and unit price.", "Information Expert"),
    ("Know sale total", "Sale", "SalesLineItem", "Sale has the lines.", "Information Expert"),
    ("Decide if a batch may be sold", "StockBatch", "—", "The batch knows expiry date and quantity on hand.", "Information Expert"),
    ("Reduce stock", "StockBatch / InventoryService", "Sale, SalesLineItem", "Quantity lives on the batch; a small domain service coordinates multi-line decrement.", "Information Expert / High Cohesion"),
    ("Hash passwords", "PasswordHasher", "User", "Hashing is not a natural pharmacy concept; keep User free of crypto details.", "Pure Fabrication"),
    ("Write audit rows", "AuditLogger", "controllers / services", "Cross-cutting record keeping would clutter Sale or User.", "Pure Fabrication"),
    ("Isolate payment kinds", "PaymentMethod (cash, card, mobile money)", "Payment, Sale", "New methods should not explode conditionals in Sale.", "Protected Variations / Polymorphism"),
    ("Print or show a receipt", "ReceiptService", "Sale, Pharmacy settings", "Output device or PDF should not sit inside Sale.", "Indirection"),
    ("Persist aggregates", "SaleRepository and related repositories", "domain objects", "SQL/API details must not leak into Sale.", "Pure Fabrication / Low Coupling"),
    ("Keep views off repositories", "Controllers + services", "Views", "Presentation depends inward only.", "Low Coupling"),
    ("One reason to change per class", "Sale vs SaleController vs SaleRepository", "—", "Pricing rules, HTTP/UI events, and SQL stay apart.", "High Cohesion"),
]

TEST_CASES_TRACE = [
    ("TC-01", "UC-01", "FR-01", "Valid Administrator login opens dashboard."),
    ("TC-02", "UC-01", "FR-01", "Valid Pharmacist login opens sales screen."),
    ("TC-03", "UC-01", "FR-01", "Invalid password is refused."),
    ("TC-04", "UC-02", "FR-03", "Three-line OTC sale completes."),
    ("TC-05", "UC-02", "FR-05", "Expired batch cannot be added."),
    ("TC-06", "UC-02", "FR-05", "Quantity above on-hand cannot be added."),
    ("TC-07", "UC-02", "FR-06", "Prescription-only item requires prescription details."),
    ("TC-08", "UC-02", "FR-07", "Cash, card, and mobile money can be recorded."),
    ("TC-09", "UC-02", "FR-08", "Receipt shows lines, total, method, pharmacist name."),
    ("TC-10", "UC-02", "FR-08", "Stock on hand decreases after completion."),
    ("TC-11", "UC-03", "FR-09", "Administrator adds a medicine that then appears in search."),
    ("TC-12", "UC-04", "FR-10", "Receiving a batch increases quantity."),
    ("TC-13", "UC-04", "FR-11", "Expiry adjustment requires a reason."),
    ("TC-14", "UC-05", "FR-13", "New Pharmacist user can log in; cannot open user admin."),
    ("TC-15", "UC-09", "FR-17", "Void restores stock and keeps the original sale visible as voided."),
]

SCOPE_IN = [
    "Authentication and role-based authorisation for two roles only",
    "Medicine catalogue maintenance",
    "Batch-level inventory with expiry and quantity",
    "Over-the-counter and prescription-linked counter sales",
    "Payments recorded as cash, card, or mobile money",
    "Receipt generation",
    "Sale void with reason and stock restore",
    "Customer record when a named patient is required",
    "Supplier record and stock receiving",
    "Low-stock and near-expiry visibility",
    "Sales and inventory reports",
    "Pharmacy settings used on receipts and alerts",
    "Audit of sensitive actions",
]

SCOPE_OUT = [
    "A separate Cashier, Manager, or Inventory Clerk user role",
    "Online / e-commerce ordering",
    "NHIMA or other insurance claim submission",
    "Live card or mobile-money gateway settlement (manual confirmation only)",
    "National electronic prescription network",
    "Clinical diagnosis or drug-interaction decision support",
    "Multi-branch warehousing and inter-store transfers",
    "Full accounting / general ledger",
    "Supplier self-service portal",
    "Patient refill reminder campaigns",
]

PROBLEM_STATEMENT = (
    "Many small and medium pharmacies in Zambia still combine paper registers, "
    "memory, and generic retail tools that were not designed for medicines. "
    "That mix produces four recurring failures: expired packs can be sold; "
    "life-saving lines run out without a reliable warning; prices and receipts "
    "are inconsistent; and there is a weak audit trail when a regulator or owner "
    "asks who sold or adjusted a batch. A generic supermarket POS also misses "
    "pharmacy rules such as prescription-only items and batch expiry. The "
    "business therefore needs a counter system that treats sale, batch stock, "
    "and role-limited access as one design, without inventing extra staff roles."
)

VISION = (
    "A pharmacy-specific point-of-sale system in which the Pharmacist runs the "
    "counter (search, sale, prescription capture, payment, receipt) and the "
    "Administrator runs the office (catalogue, stock, users, suppliers, reports). "
    "The system makes the dangerous path — selling expired or untracked medicine — "
    "hard, and the routine path — a correct paid sale — fast enough for a busy counter."
)
