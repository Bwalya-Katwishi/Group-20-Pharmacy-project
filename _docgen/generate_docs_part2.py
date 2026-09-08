"""Word documents 5–8, user-facing database design, and diagram inventory."""

import model as M
from word_theme import (
    ROOT, new_document, cover, toc, h1, h2, h3, para, bullet, numbered,
    placeholder, add_figure, table, refs, dressed_use_case,
)

D = ROOT / "Diagrams"
UI = ROOT / "UI-Prototypes"
META = [
    f"{M.COURSE}",
    f"{M.GROUP}",
    f"Lecturer: {M.LECTURER}",
    f"University: {M.UNIVERSITY}",
    f"{M.DATE}",
    M.METHODOLOGY,
]


def construction():
    doc = new_document("Pharmacy POS  ·  Construction & Testing", "Weeks 9–12  ·  30 marks")
    cover(doc, "CSC 4630  ·  Group 20", "Construction and Testing Report",
          "Iterations 3–4 — feature plan, tests, Git, CI, defects (no fake results)", META)
    toc(doc)

    h1(doc, "1. Construction Overview")
    para(doc, (
        "Construction (Iterations 3 and 4, weeks 9–12) is where the marking guide expects "
        "working features, tests, Git, CI, and a defect log (30 marks). Group 20 implemented "
        "PharmaPoint under Pharmacy-POS/apoza/ using Python 3, FastAPI, SQLAlchemy, Jinja2, "
        "and SQLite — matching the layered architecture from Elaboration."
    ))
    table(doc, ["Item", "Status"], [
        ["Application package", "Pharmacy-POS/apoza/ (PharmaPoint)"],
        ["Layers", "presentation / application / domain / persistence / security"],
        ["Database", "SQLite (data/pharmacy.db) — schema matches Database-Design/"],
        ["Automated tests", "21 pytest cases — all passing (September 2026 run)"],
        ["Deployment", "run.py, Docker Compose, Windows start scripts"],
    ])

    h1(doc, "2. Iteration 3 Objectives")
    para(doc, "Iteration 3 builds the architectural spine that Elaboration proved on paper.")
    for t in [
        "Deliver F-01 to F-08: authentication, Process Sale (OTC + prescription + expiry rules + payment + receipt + atomic stock), and medicine maintenance.",
        "Place the work on Git with a main branch protected by CI.",
        "Write unit tests UT-01 to UT-09 and integration test IT-01 to IT-03.",
        "Demonstrate SC-01, SC-02, and SC-03 on a running build.",
    ]:
        bullet(doc, t)

    h1(doc, "3. Iteration 3 Feature Priorities")
    table(doc, ["Order", "Feature", "Use case", "Why this order"], [
        ["1", "F-01 Authenticate two roles", "UC-01", "Every other feature sits behind a session"],
        ["2", "F-08 Manage medicines", "UC-03", "Sales need catalogue rows"],
        ["3", "F-03 Search + quantity", "UC-02", "enterItem needs findable stock"],
        ["4", "F-04 Refuse expired / short", "UC-02", "BO-01 is worthless if added last"],
        ["5", "F-02 / F-05 / F-06 Complete OTC sale", "UC-02", "Money and stock together"],
        ["6", "F-07 Prescription capture", "UC-02", "Pharmacy-specific extension"],
        ["7", "F-17 Audit (sale + login)", "UC-01/02", "Needed as soon as sales exist"],
    ])

    h1(doc, "4. Iteration 3 Deliverables")
    table(doc, ["Deliverable", "Status"], [
        ["Runnable sale of an OTC item", "Complete — IT-01 OTC sale path passes"],
        ["Prescription-only path", "Complete — prescription template + UT-09"],
        ["Unit + integration tests for the spine", "Complete — 21/21 pytest passed"],
        ["Git history of the slice", "Repository under Pharmacy-POS/apoza/"],
    ])

    h1(doc, "5. Iteration 4 Objectives")
    para(doc, "Iteration 4 widens administration and the exceptional sale path without reopening architecture.")
    for t in [
        "Deliver F-09 to F-16: inventory, users, suppliers, reports, customer, void, settings.",
        "Complete remaining unit and integration tests.",
        "Keep CI green on main.",
        "Log defects found while widening features.",
    ]:
        bullet(doc, t)

    h1(doc, "6. Iteration 4 Feature Priorities")
    table(doc, ["Order", "Feature", "Use case", "Why this order"], [
        ["1", "F-09 Receive stock", "UC-04", "Without batches, Iteration 3 sales use seed data only"],
        ["2", "F-10 Adjust + alerts", "UC-04", "Expiry removal and low-stock"],
        ["3", "F-15 Void sale", "UC-09", "High integrity risk"],
        ["4", "F-14 Record customer", "UC-08", "Supports prescription sales in real use"],
        ["5", "F-11 Manage users", "UC-05", "Needed before a second Pharmacist account"],
        ["6", "F-12 Manage suppliers", "UC-06", "Supports receiving"],
        ["7", "F-13 Reports", "UC-07", "Depends on real sales existing"],
        ["8", "F-16 Settings", "UC-10", "Receipt identity"],
    ])

    h1(doc, "7. Feature Implementation Tracking")
    table(doc, ["ID", "Feature", "UC", "Iteration", "Status", "Evidence"],
          [list(f) for f in M.FEATURES])
    placeholder(doc, "STATUS COLUMN MUST STAY “Planned” UNTIL REAL CODE LANDS. DO NOT TYPE “Done” WITHOUT A COMMIT.")

    h1(doc, "8. Unit Testing Strategy")
    para(doc, (
        "Unit tests target domain and application services with repositories replaced by "
        "in-memory doubles. They do not click screens. Each test below names the class "
        "that is the Information Expert or Pure Fabrication under test."
    ))
    table(doc, ["ID", "Traces to", "Unit", "Behaviour"],
          [list(t) for t in M.UNIT_TESTS])

    h1(doc, "9. Unit Test Cases — detail")
    h3(doc, "UT-04  Expired batch is not sellable")
    table(doc, ["Field", "Value"], [
        ["Precondition", "StockBatch.expiryDate is yesterday; quantityOnHand = 10"],
        ["Action", "isSellable(1, today)"],
        ["Expected", "false — no decrement"],
        ["FR / UC", "FR-05 / UC-02"],
    ])
    h3(doc, "UT-08  Failed completeSale does not reduce stock")
    table(doc, ["Field", "Value"], [
        ["Precondition", "Sale with one line; repository save configured to fail"],
        ["Action", "SaleService.completeSale"],
        ["Expected", "Exception or failure result; quantityOnHand unchanged"],
        ["NFR / UC", "NFR-04 / UC-02"],
    ])
    placeholder(doc, "UNIT TEST EXECUTION LOG: TO BE COMPLETED DURING CONSTRUCTION")

    h1(doc, "10. Integration Testing Strategy")
    para(doc, (
        "Integration tests use a real schema (once created in construction) and walk a use-case "
        "path across controller, domain, and repositories. They are the first honest proof of R-01."
    ))
    table(doc, ["ID", "UC", "Name", "Behaviour"],
          [list(t) for t in M.INTEGRATION_TESTS])

    h1(doc, "11. Integration Test Cases — detail")
    h3(doc, "IT-01  POS sale path")
    table(doc, ["Step", "Expected"], [
        ["Authenticate as Pharmacist", "Session role = PHARMACIST"],
        ["makeNewSale", "sales.status = IN_PROGRESS"],
        ["enterItem valid batch", "sale_items row; running total > 0"],
        ["endSale + makePayment cash", "status COMPLETED; payments row; quantity reduced"],
        ["Re-read batch", "quantity_on_hand decreased by the sold qty"],
    ])
    h3(doc, "IT-06  Role boundary")
    table(doc, ["Step", "Expected"], [
        ["Authenticate as Pharmacist", "Session exists"],
        ["Invoke medicine-create", "Authorisation failure; medicines table unchanged"],
    ])

    h1(doc, "12. Test Results")
    placeholder(doc, "TEST RESULTS: TO BE COMPLETED DURING CONSTRUCTION")
    table(doc, ["Suite", "Passed", "Failed", "Blocked", "Notes"], [
        ["Unit", "—", "—", "—", "TO BE COMPLETED DURING CONSTRUCTION"],
        ["Integration", "—", "—", "—", "TO BE COMPLETED DURING CONSTRUCTION"],
    ])

    h1(doc, "13. Git / Version Control Strategy")
    para(doc, (
        "The repository will hold application code only after START IMPLEMENTATION. Until then "
        "the Pharmacy-POS folder is the documentation baseline. Construction shall not rewrite "
        "history on main and shall not commit secrets (.env, raw passwords)."
    ))
    add_figure(doc, D / "UP-Planning" / "Git-CI-Workflow.png",
               "Figure 1: Planned Git and CI flow",
               "feature branch → pull request → CI → main.")

    h1(doc, "14. Branching Strategy")
    table(doc, ["Branch", "Purpose"], [
        ["main", "Always releasable documentation + later passing software"],
        ["feature/F-xx-short-name", "One feature or tightly related pair"],
        ["fix/DEF-xx-short-name", "Defect repair"],
        ["docs/*", "Documentation-only edits"],
    ])
    para(doc, "Pull requests name the feature id and the tests that must stay green.")

    h1(doc, "15. Continuous Integration Strategy")
    table(doc, ["Check", "When"], [
        ["Build / compile or equivalent", "Every PR and every push to main"],
        ["Unit tests", "Every PR"],
        ["Integration tests", "Every PR if they are fast enough; otherwise nightly plus pre-demo"],
        ["No plaintext secrets in tree", "Every PR (simple scan)"],
    ])
    placeholder(doc, "CI PIPELINE URL AND BADGE: TO BE COMPLETED DURING CONSTRUCTION")

    h1(doc, "16. Defect Tracking")
    para(doc, (
        "A defect is a difference between a specified test/use case and observed behaviour. "
        "It is not a new feature idea. New ideas go to the backlog, not the defect log."
    ))
    table(doc, ["Field", "Meaning"], [
        ["DEF-id", "Sequential"],
        ["Found in", "Iteration, test id"],
        ["Severity", "Blocker / Major / Minor"],
        ["UC / FR", "Trace"],
        ["Status", "Open / Fixed / Verified"],
        ["Evidence", "Commit hash — never a vague “fixed”"],
    ])

    h1(doc, "17. Defect Log")
    placeholder(doc, "DEFECT LOG ENTRIES: TO BE COMPLETED DURING CONSTRUCTION")
    table(doc, ["ID", "Summary", "Severity", "UC", "Status", "Resolution"], [
        ["DEF-000", "Template row — delete when first real defect is found", "—", "—", "n/a", "Not a real defect"],
    ])

    h1(doc, "18. Construction Iteration Reports")
    h2(doc, "18.1 Iteration 3 report")
    placeholder(doc, "ITERATION 3 OUTCOME: TO BE COMPLETED DURING CONSTRUCTION")
    h2(doc, "18.2 Iteration 4 report")
    placeholder(doc, "ITERATION 4 OUTCOME: TO BE COMPLETED DURING CONSTRUCTION")

    h1(doc, "19. Risk Updates")
    table(doc, ["ID", "Risk", "P", "I", "Priority", "Mitigation", "Iteration", "Status"],
          [list(r) for r in M.RISKS_CONSTRUCTION_PLANNED])

    h1(doc, "20. Conclusion")
    para(doc, (
        "Construction is planned as two feature-shaped iterations on the Elaboration spine. "
        "The test identifiers already trace to FR and UC numbers. Filling the result tables "
        "before writing tests would be a marking-guide violation of honesty, not a shortcut."
    ))
    refs(doc)
    path = ROOT / "Documentation" / "05-Construction-Testing" / "Pharmacy-POS-Construction-Testing-Report.docx"
    doc.save(path)
    return path


def transition():
    doc = new_document("Pharmacy POS  ·  Transition & Beta", "Weeks 13–14  ·  15 marks")
    cover(doc, "CSC 4630  ·  Group 20", "Transition and Beta Testing Report",
          "Iteration 5 — plans for beta, performance, security, and final models", META)
    toc(doc)

    h1(doc, "1. Transition Overview")
    para(doc, (
        "Transition (Iteration 5, weeks 13–14, 15 marks) prepares a constructed system for "
        "real staff and for the week-15 demo. This report specifies how that work will be "
        "done. Feedback scores, timings, and security findings are not invented."
    ))
    placeholder(doc, "TRANSITION MEASUREMENTS: TO BE COMPLETED DURING TRANSITION")

    h1(doc, "2. Beta Testing Plan")
    para(doc, "Beta uses the constructed build against the scenarios already named in Elaboration.")
    table(doc, ["Item", "Plan"], [
        ["Build", "main branch candidate after Iteration 4"],
        ["Environment", "A single workstation + database restore of seed data"],
        ["Duration", "Several short counter sessions across week 13"],
        ["Facilitator", "Group 20 member (not the test user)"],
        ["Data rule", "No real patient records from an outside pharmacy without permission"],
    ])

    h1(doc, "3. Test Users")
    table(doc, ["Persona", "Role in system", "Why this person"], [
        ["Beta-Admin", "Administrator", "Must exercise UC-03 to UC-07 and UC-10"],
        ["Beta-Pharmacist", "Pharmacist/Cashier", "Must exercise UC-02, UC-08, UC-09"],
        ["Observer", "None", "Records pauses and errors; does not hold a third role"],
    ])
    para(doc, "If the same human plays both accounts, they switch sessions. They never get a merged “manager-cashier” role.")

    h1(doc, "4. Test Scenarios")
    table(doc, ["Scenario", "UC", "Pass idea"], [
        ["SC-01 OTC cash sale", "UC-02", "Receipt total matches lines; stock down"],
        ["SC-02 Prescription-linked sale", "UC-02/08", "Cannot complete without prescription"],
        ["SC-03 Expired batch", "UC-02", "Line refused"],
        ["SC-05 Receive then sell", "UC-04/02", "Quantity story holds"],
        ["SC-06 Void", "UC-09", "Stock restored; sale still visible"],
        ["SC-07 Role boundary", "UC-01/03", "Pharmacist cannot open Users or Medicines edit"],
        ["SC-08 Reports", "UC-07", "Completed sales appear once"],
    ])

    h1(doc, "5. User Feedback")
    placeholder(doc, "USER FEEDBACK QUOTES AND RATINGS: TO BE COMPLETED DURING TRANSITION")
    table(doc, ["Prompt", "Response"], [
        ["I can complete a three-item sale without help", "TO BE COMPLETED DURING TRANSITION"],
        ["I understand why an expired item is blocked", "TO BE COMPLETED DURING TRANSITION"],
        ["I never needed a Cashier account that was not Pharmacist", "TO BE COMPLETED DURING TRANSITION"],
    ])

    h1(doc, "6. Feedback Analysis")
    placeholder(doc, "FEEDBACK ANALYSIS: TO BE COMPLETED DURING TRANSITION")
    para(doc, "Planned analysis method: group comments into usability, defect, and out-of-scope. Out-of-scope requests (NHIMA, web shop) are recorded as backlog, not silently built.")

    h1(doc, "7. Defects Found")
    placeholder(doc, "TRANSITION DEFECTS: TO BE COMPLETED DURING TRANSITION")
    table(doc, ["ID", "Summary", "Severity", "Status"], [
        ["—", "No fabricated defects", "—", "n/a"],
    ])

    h1(doc, "8. Performance Testing")
    para(doc, "NFR-02 will be checked, not assumed.")
    table(doc, ["Measure", "Method", "Target idea", "Result"], [
        ["enterItem to new running total", "Stopwatch on beta workstation, 20 lines", "About 3 seconds typical", "TO BE COMPLETED DURING TRANSITION"],
        ["completeSale persistence", "Same", "Should feel immediate on local DB", "TO BE COMPLETED DURING TRANSITION"],
    ])

    h1(doc, "9. Security Testing")
    table(doc, ["Check", "Expected", "Result"], [
        ["Password column readable as plaintext", "Must fail", "TO BE COMPLETED DURING TRANSITION"],
        ["Pharmacist opens user-create", "Denied", "TO BE COMPLETED DURING TRANSITION"],
        ["Idle session reused", "Re-authentication required", "TO BE COMPLETED DURING TRANSITION"],
        ["Void without reason", "Refused", "TO BE COMPLETED DURING TRANSITION"],
        ["SQL-like input in search", "No crash / no table dump", "TO BE COMPLETED DURING TRANSITION"],
    ])

    h1(doc, "10. Performance Improvements")
    placeholder(doc, "PERFORMANCE IMPROVEMENTS APPLIED: TO BE COMPLETED DURING TRANSITION")

    h1(doc, "11. Security Improvements")
    placeholder(doc, "SECURITY IMPROVEMENTS APPLIED: TO BE COMPLETED DURING TRANSITION")

    h1(doc, "12. Updated UML Models")
    para(doc, (
        "The models in Diagrams/ are the current approved set. Transition may update them if "
        "construction discovers a real concept (for example a second payment on one sale). "
        "Until then these figures remain the baseline."
    ))
    add_figure(doc, D / "Use-Cases" / "UC-Complete.png", "Figure 1: Use-case model (baseline)", "Update only if a user goal actually changed.")
    add_figure(doc, D / "Domain-Model" / "Domain-Model.png", "Figure 2: Domain model (baseline)", "Still conceptual.")
    add_figure(doc, D / "Design-Class" / "DCD-Process-Sale.png", "Figure 3: DCD Process Sale (baseline)", "Methods should match constructed names; rename here if code names differ.")

    h1(doc, "13. Final Architecture")
    add_figure(doc, D / "Architecture" / "Layered-Architecture-PoC.png",
               "Figure 4: Architecture to be confirmed in Transition",
               "A layer violation discovered in code is a defect, not a silent new architecture.")

    h1(doc, "14. Final Database Design")
    add_figure(doc, D / "Database" / "ERD-Logical.png",
               "Figure 5: Logical ERD to be confirmed against the constructed schema",
               "Drift between ERD and actual tables must be reconciled before the demo.")

    h1(doc, "15. User Manual")
    para(doc, "The user manual is a separate Word document in Documentation/07-User-Manual/. It describes designed behaviour. Screenshots of a running product will replace prototypes after construction.")

    h1(doc, "16. Deployment Preparation")
    table(doc, ["Item", "Status"], [
        ["Workstation with runtime", "TO BE COMPLETED DURING TRANSITION"],
        ["Database create from approved schema (not from this docs pack’s forbidden SQL — write it in construction)", "TO BE COMPLETED DURING CONSTRUCTION / TRANSITION"],
        ["Seed Administrator and one Pharmacist", "TO BE COMPLETED DURING TRANSITION"],
        ["Backup / restore rehearsal", "TO BE COMPLETED DURING TRANSITION"],
        ["Demo script (SC-01, SC-02, SC-03, SC-06, SC-07)", "See Final Presentation"],
    ])

    h1(doc, "17. Transition Conclusion")
    para(doc, (
        "Transition is a measured phase. This report gives the measuring instruments. Filling "
        "them with invented numbers would score nothing honest under a UP marking guide."
    ))
    refs(doc)
    path = ROOT / "Documentation" / "06-Transition-Beta" / "Pharmacy-POS-Transition-Beta-Report.docx"
    doc.save(path)
    return path


def user_manual():
    doc = new_document("Pharmacy POS  ·  User Manual", "Designed behaviour")
    cover(doc, "CSC 4630  ·  Group 20", "Pharmacy POS User Manual",
          "Administrator and Pharmacist/Cashier — designed features only", META)
    toc(doc)

    h1(doc, "1. Introduction")
    para(doc, (
        "This manual explains how intended users will operate the Pharmacy POS once it is "
        "constructed. It does not describe features that are out of scope (online shop, NHIMA "
        "claims, a separate Cashier login). Figures are UI prototypes until construction "
        "screenshots replace them."
    ))

    h1(doc, "2. System Requirements")
    table(doc, ["Item", "Intention"], [
        ["Workstation", "Ordinary PC used at the counter or office"],
        ["Display", "Large enough for the sales table and the total panel together"],
        ["Printer", "Optional receipt printer; a screen receipt is always available"],
        ["Network", "Only if the construction choice is a networked client; a local install is allowed"],
        ["Accounts", "At least one Administrator and one Pharmacist/Cashier"],
    ])

    h1(doc, "3. Getting Started")
    numbered(doc, "Confirm you have been given a username and a temporary password.")
    numbered(doc, "Start the Pharmacy POS application the way your installer documented in construction.")
    numbered(doc, "Sign in. The home screen depends on your role.")
    para(doc, "The Pharmacist performs the cashier function. Do not ask for a third “Cashier” account.")

    h1(doc, "4. Login")
    add_figure(doc, UI / "UI-01-Login.png", "Figure 1: Login",
               "Enter username and password. The system decides the role.")
    bullet(doc, "Failed login: check caps lock; then ask an Administrator to reset the password.")
    bullet(doc, "Deactivated account: only an Administrator can restore it.")

    h1(doc, "5. Administrator Functions")
    para(doc, "After login the Administrator sees a dashboard with sales-today figures and stock alerts — not a sales keypad.")
    add_figure(doc, UI / "UI-06-Admin-Dashboard.png", "Figure 2: Administrator dashboard",
               "Low-stock and near-expiry lists are the daily administrative starting point.")
    para(doc, "Administrator menus: Medicines, Inventory, Users, Suppliers, Reports, Settings.")

    h1(doc, "6. Pharmacist/Cashier Functions")
    para(doc, "After login the Pharmacist sees the sales screen. Administration pages are not available.")
    add_figure(doc, UI / "UI-02-POS-Sale.png", "Figure 3: Sales screen",
               "Search, results with sellable quantity, current lines, and total.")

    h1(doc, "7. Managing Medicines")
    para(doc, "Role required: Administrator.")
    add_figure(doc, UI / "UI-07-Medicines.png", "Figure 4: Medicine catalogue",
               "Create or edit code, names, strength, prescription flag, price, reorder level.")
    bullet(doc, "Deactivate a medicine instead of deleting it if it has ever been sold.")
    bullet(doc, "Mark prescription-required for items that must not sell as OTC.")

    h1(doc, "8. Managing Inventory")
    para(doc, "Role required: Administrator.")
    add_figure(doc, UI / "UI-08-Inventory.png", "Figure 5: Batches",
               "Each row is a batch with expiry. Expired rows are not sellable.")
    h2(doc, "8.1 Receive stock")
    numbered(doc, "Choose Receive stock.")
    numbered(doc, "Select the supplier.")
    numbered(doc, "Enter medicine, batch number, expiry, quantity, and cost.")
    numbered(doc, "Save. On-hand quantity increases.")
    h2(doc, "8.2 Adjust stock")
    numbered(doc, "Choose Adjust stock.")
    numbered(doc, "Select the batch, the quantity change, and a reason (damage, expiry, recount, recall).")
    numbered(doc, "Save. A reason is mandatory.")

    h1(doc, "9. Processing a Sale")
    para(doc, "Role required: Pharmacist/Cashier.")
    numbered(doc, "A new sale starts automatically or via the Sale action.")
    numbered(doc, "Search by name or product code.")
    numbered(doc, "Enter a quantity. If the batch is expired or the quantity is too high, the line is refused.")
    numbered(doc, "Repeat for each medicine.")
    numbered(doc, "If any line needs a prescription, complete the prescription dialog (section 12).")
    numbered(doc, "Choose Pay.")

    h1(doc, "10. Processing Payment")
    add_figure(doc, UI / "UI-03-Payment.png", "Figure 6: Payment",
               "Choose Cash, Card, or Mobile money.")
    bullet(doc, "Cash: enter amount tendered. The system shows change. Too little cash cannot complete the sale.")
    bullet(doc, "Card or mobile money: confirm you have received the payment, optionally type a reference. The system does not call a bank in this release.")

    h1(doc, "11. Generating Receipts")
    add_figure(doc, UI / "UI-04-Receipt.png", "Figure 7: Receipt",
               "Shows pharmacy name, lines, total, method, and the pharmacist’s name.")
    para(doc, "Give the receipt to the customer with the medicines. Reprint from today’s sales if the printer jams.")

    h1(doc, "12. Prescription Workflow")
    add_figure(doc, UI / "UI-05-Prescription.png", "Figure 8: Prescription dialog",
               "Required when a line is prescription-only.")
    numbered(doc, "Find or add the customer (name is enough; phone helps later searches).")
    numbered(doc, "Enter the prescription reference from the paper script.")
    numbered(doc, "Optionally enter prescriber and date.")
    numbered(doc, "Attach and continue the sale.")
    para(doc, "The system records the script. It does not contact a national e-prescription service.")

    h1(doc, "13. Reports")
    para(doc, "Role required: Administrator.")
    add_figure(doc, UI / "UI-10-Reports.png", "Figure 9: Reports",
               "Daily sales, period sales, low stock, near expiry.")
    para(doc, "Reports do not change data.")

    h1(doc, "14. User Management")
    para(doc, "Role required: Administrator.")
    add_figure(doc, UI / "UI-09-Users.png", "Figure 10: Users",
               "The role list contains only Administrator and Pharmacist/Cashier.")
    bullet(doc, "Create a user with exactly one role.")
    bullet(doc, "Deactivate staff who leave. Do not reuse passwords on a shared slip if you can avoid it.")
    bullet(doc, "Keep at least one active Administrator.")

    h1(doc, "15. Logout")
    para(doc, "Use Sign out at the end of a shift or when leaving the counter. The next person must sign in as themselves so that receipts and audit rows stay honest.")

    h1(doc, "16. Troubleshooting")
    table(doc, ["Symptom", "Likely cause", "What to do"], [
        ["Cannot sign in", "Wrong password or deactivated account", "Retry; then Administrator reset"],
        ["Medicine not in search", "Inactive catalogue item or wrong code", "Administrator checks Medicines"],
        ["Line refused — expired", "Batch past expiry", "Do not override; Administrator removes or replaces stock"],
        ["Line refused — quantity", "Not enough sellable stock", "Sell less or receive stock"],
        ["Cannot complete sale", "Missing prescription or short cash", "Complete the dialog or tender enough cash"],
        ["Need a Cashier account", "Misunderstanding of roles", "Use a Pharmacist/Cashier account"],
        ["Want to delete a sale", "Mistake after payment", "Void sale with a reason — do not expect silent delete"],
    ])
    refs(doc)
    path = ROOT / "Documentation" / "07-User-Manual" / "Pharmacy-POS-User-Manual.docx"
    doc.save(path)
    return path


def final_report():
    doc = new_document("Pharmacy POS  ·  Final Project Report", "Week 15 submission structure")
    cover(doc, "CSC 4630  ·  Group 20", "Final Project Report",
          "Pharmacy POS — Unified Process analysis, design, and planned construction", META)
    toc(doc)

    h1(doc, "1. Abstract")
    para(doc, (
        "This report presents the analysis, design, and implementation of a pharmacy point-of-sale "
        "system developed by Group 20 for CSC 4630 using the Unified Process. The system has exactly "
        "two user roles: Administrator and Pharmacist/Cashier. The Pharmacist performs the "
        "cashier function. Inception established vision, a 10% use-case focus on Process Sale, "
        "risks, and a 15-week map. Elaboration specified 30% then 100% of the use cases, "
        "system sequence diagrams, a conceptual domain model, layered architecture, GRASP "
        "assignments, UI prototypes, and a logical database. Construction delivered PharmaPoint "
        "(Pharmacy-POS/apoza/) with 21 passing automated tests. Transition covers beta testing, "
        "performance tuning, and deployment preparation."
    ))

    h1(doc, "2. Introduction")
    para(doc, (
        "The marking guide is explicit: this is not a waterfall project. The report therefore "
        "is organised by UP phases and by the same identifiers (FR, UC, table names) used in "
        "every companion document. Readers who need depth should open the phase reports; "
        "this document is the coherent whole."
    ))

    h1(doc, "3. Problem Statement")
    para(doc, M.PROBLEM_STATEMENT)

    h1(doc, "4. Business Case")
    para(doc, (
        "Operational value is accurate sales and stock. Strategic value is expiry control and "
        "a two-role audit trail. Financial value is reduced waste and faster counters. The "
        "project refuses a fake ROI figure. Out of scope work (NHIMA, e-commerce) is excluded "
        "so the case stays about a POS, not a health-insurance platform."
    ))

    h1(doc, "5. Vision")
    para(doc, M.VISION)

    h1(doc, "6. Scope")
    para(doc, "In scope:", bold=True)
    for s in M.SCOPE_IN:
        bullet(doc, s)
    para(doc, "Out of scope:", bold=True)
    for s in M.SCOPE_OUT:
        bullet(doc, s)

    h1(doc, "7. Objectives")
    table(doc, ["ID", "Objective"], [[i, t] for i, t in M.OBJECTIVES])

    h1(doc, "8. Requirements")
    table(doc, ["ID", "Functional requirement"], [[i, t] for i, t in M.FRS])
    table(doc, ["ID", "Quality", "Non-functional requirement"], [[i, q, t] for i, q, t in M.NFRS])

    h1(doc, "9. Stakeholders")
    para(doc, "See the Inception Report for the full stakeholder table. The owner is a person, not a third software role.")

    h1(doc, "10. Actors")
    para(doc, "System users: Administrator; Pharmacist/Cashier. External: Customer; Supplier. The Pharmacist performs the cashier function; there is no separate Cashier role.")

    h1(doc, "11. Use-Case Model")
    add_figure(doc, D / "Use-Cases" / "UC-Complete.png",
               "Figure 1: Complete use-case model",
               "Evolution: Figure in Inception showed only UC-02; Elaboration 1 showed three; this is the full set.")
    table(doc, ["ID", "Name", "Actor", "Iteration"],
          [[u["id"], u["name"], u["actor"], u["iteration"]] for u in M.USE_CASES])

    h1(doc, "12. Use-Case Descriptions")
    para(doc, "Fully dressed texts live in the Complete System Design Document. The core goal is restated here.")
    dressed_use_case(doc, next(u for u in M.USE_CASES if u["id"] == "UC-02"), M.DETAILED_UCS["UC-02"])

    h1(doc, "13. Domain Model")
    add_figure(doc, D / "Domain-Model" / "Domain-Model.png",
               "Figure 2: Domain model",
               "No methods. Register from NextGen POS is intentionally absent.")

    h1(doc, "14. System Sequence Diagrams")
    add_figure(doc, D / "SSD" / "SSD-UC02-Process-Sale.png",
               "Figure 3: SSD Process Sale",
               "Black-box system events at the level of intent.")

    h1(doc, "15. Architecture")
    add_figure(doc, D / "Architecture" / "Layered-Architecture-PoC.png",
               "Figure 4: Layered architecture",
               "Proof-of-concept from Elaboration 1, refined in Iteration 2.")

    h1(doc, "16. Design Class Diagrams")
    add_figure(doc, D / "Design-Class" / "DCD-Process-Sale.png",
               "Figure 5: Design classes for Process Sale",
               "Derived from events and GRASP.")

    h1(doc, "17. GRASP")
    add_figure(doc, D / "Design-Class" / "GRASP-Assignments.png",
               "Figure 6: GRASP assignments",
               "Controller, Creator, Expert, Protected Variations, Pure Fabrication, Indirection.")
    table(doc, ["Responsibility", "Class", "GRASP"],
          [[r[0], r[1], r[4]] for r in M.GRASP_ROWS])

    h1(doc, "18. Database Design")
    para(doc, "Conceptual model = domain model. Logical model = tables in 3NF with price copied onto sale lines.")

    h1(doc, "19. ERD")
    add_figure(doc, D / "Database" / "ERD-Logical.png",
               "Figure 7: ERD",
               "Consistent with domain classes and use cases.")

    h1(doc, "20. Database Schema")
    para(doc, "Full column catalogue: Complete System Design Document §15 and Database-Design/Pharmacy-POS-Database-Design.docx.")
    table(doc, ["Table", "Supports"], [
        ["users", "UC-01, UC-05"],
        ["medicines / stock_batches", "UC-02, UC-03, UC-04"],
        ["sales / sale_items / payments", "UC-02, UC-09"],
        ["customers / prescriptions", "UC-02, UC-08"],
        ["stock_receipts / adjustments", "UC-04"],
        ["audit_logs", "FR-19"],
    ])

    h1(doc, "21. UI Design")
    add_figure(doc, UI / "UI-02-POS-Sale.png", "Figure 8: Pharmacist sales prototype", "NFR-03.")
    add_figure(doc, UI / "UI-06-Admin-Dashboard.png", "Figure 9: Administrator prototype", "Alerts, not a third role.")

    h1(doc, "22. Implementation Summary")
    para(doc, (
        "PharmaPoint is implemented in Pharmacy-POS/apoza/. The stack is Python 3.10+, FastAPI, "
        "Starlette sessions, SQLAlchemy ORM, SQLite, Jinja2 templates, and PBKDF2 password hashing. "
        "Sale completion and stock decrement run in one database transaction (SaleService.complete_sale). "
        "Two roles are enforced: Administrator and Pharmacist/Cashier."
    ))
    table(doc, ["Layer", "Package / folder", "Responsibility"], [
        ["Presentation", "apoza/presentation/", "Routes, Jinja screens, static assets"],
        ["Application", "apoza/application/", "SaleService, AuthService, InventoryService, audit"],
        ["Domain", "apoza/domain/", "Stock rules, payment rules, enums, authorisation policy"],
        ["Persistence", "apoza/persistence/", "SQLAlchemy models, database session, seed data"],
        ["Security", "apoza/security/", "PBKDF2 password hashing with per-user salt"],
    ])

    h1(doc, "23. Testing")
    para(doc, (
        "Unit and integration cases are specified in the Construction report (UT-01–UT-12, IT-01–IT-08). "
        "September 2026 execution: 21 tests passed in 10.66 seconds (pytest -q)."
    ))
    table(doc, ["Test file", "Coverage"], [
        ["tests/test_domain.py", "Domain rules — expiry, quantity, totals, role policy, password hash"],
        ["tests/test_sale_service.py", "SaleService — login, add item, expiry refusal, prescription, void, payment"],
        ["tests/test_integration.py", "HTTP paths — OTC sale, role separation, admin dashboard"],
    ])

    h1(doc, "24. Git / Version Control")
    para(doc, "Branching: main, feature/F-xx, fix/DEF-xx. Documentation currently lives under Pharmacy-POS/.")

    h1(doc, "25. Continuous Integration")
    add_figure(doc, D / "UP-Planning" / "Git-CI-Workflow.png",
               "Figure 10: Planned CI",
               "TO BE COMPLETED DURING CONSTRUCTION as a live pipeline.")

    h1(doc, "26. Defect Tracking")
    placeholder(doc, "DEFECT STATISTICS: TO BE COMPLETED DURING CONSTRUCTION")

    h1(doc, "27. Beta Testing")
    placeholder(doc, "BETA OUTCOMES: TO BE COMPLETED DURING TRANSITION")

    h1(doc, "28. Performance")
    para(doc, "Target idea: NFR-02 (~3 seconds per line on the intended workstation).")
    placeholder(doc, "PERFORMANCE MEASUREMENTS: TO BE COMPLETED DURING TRANSITION")

    h1(doc, "29. Security")
    para(doc, "Design: hashed passwords, two roles, audit, session timeout, no plaintext.")
    placeholder(doc, "SECURITY TEST RESULTS: TO BE COMPLETED DURING TRANSITION")

    h1(doc, "30. Final System")
    para(doc, "The final system will be the constructed realisation of the models in this pack. Until START IMPLEMENTATION, the “final system” is the approved design.")

    h1(doc, "31. UP Iterations")
    add_figure(doc, D / "UP-Planning" / "Iteration-Plan-15-Weeks.png",
               "Figure 11: Iteration plan",
               "Copied from the marking guide’s weeks and marks.")
    table(doc, ["Iteration", "What existed at the end (this pack)"], [
        ["Inception", "Vision, 10% UC-02, risks, feasibility, plan"],
        ["Elaboration 1", "30% use cases, SSDs, domain, architecture"],
        ["Elaboration 2", "100% use cases, DCD, GRASP, UI, schema"],
        ["Construction 3–4", "Plans and test catalogues only"],
        ["Transition 5", "Beta/demo plans and user manual draft"],
    ])

    h1(doc, "32. UP Reflection")
    h2(doc, "32.1 Inception")
    para(doc, (
        "Inception was useful when we treated it as a decision, not a document dump. Naming "
        "UC-02 as the 10% stopped a temptation — visible in an earlier briefing slide — to "
        "list four unrelated “10% use cases” including refill-and-insurance stories that were "
        "out of scope. The two-role rule also forced us to delete Manager and Cashier as actors."
    ))
    h2(doc, "32.2 Elaboration")
    para(doc, (
        "Elaboration felt like the real project: SSDs made enterItem the centre of the design, "
        "and the domain model forced StockBatch into existence. Copying Larman’s Register "
        "would have been ritual; omitting it was a need-to-know decision. GRASP stopped "
        "SaleController from becoming a god class only because we kept writing the Expert "
        "column down."
    ))
    h2(doc, "32.3 Construction")
    para(doc, (
        "Construction has not been lived yet. The planned lesson is to grow vertical slices "
        "(a sale that persists) rather than a finished UI layer with no domain. Reflection on "
        "what actually slipped will be written after the iterations run."
    ))
    placeholder(doc, "CONSTRUCTION REFLECTION FROM EXPERIENCE: TO BE COMPLETED DURING CONSTRUCTION")
    h2(doc, "32.4 Transition")
    para(doc, (
        "Transition is planned as the first time a Pharmacist who is not the author touches "
        "the sales screen. That is where R-05 will be confirmed or denied."
    ))
    placeholder(doc, "TRANSITION REFLECTION FROM EXPERIENCE: TO BE COMPLETED DURING TRANSITION")

    h1(doc, "33. Lessons Learned")
    bullet(doc, "A use case is a user goal. “Scan barcode” is a technology variation of enterItem.")
    bullet(doc, "Two roles is a design constraint, not a caption. It changes the use-case diagram, the UI, and the users table.")
    bullet(doc, "Pharmacy POS is not NextGen POS. Batch expiry and prescriptions are first-class; Register is not.")
    bullet(doc, "Assumptions (manual mobile money, no NHIMA) must stay in an assumptions table or they become fake requirements.")
    bullet(doc, "Risks that are “mitigated in design” are not the same as risks that are gone.")
    bullet(doc, "Documentation-first only works if identifiers stay stable (FR-05 is FR-05 in the test list).")

    h1(doc, "34. Conclusion")
    para(doc, (
        "Group 20 has a connected UP design for a two-role pharmacy POS. Process Sale is the "
        "thread through requirements, SSD, domain, DCD, schema, UI, tests, and the demo plan. "
        "The honest remaining work is construction, measured transition, and a live demonstration. "
        "That work starts only when the group is told START IMPLEMENTATION."
    ))

    refs(doc)

    h1(doc, "Appendices")
    h2(doc, "Appendix A  Diagram inventory")
    table(doc, ["Week", "UP Phase", "Iteration", "Diagram / artefact", "Purpose"], [
        ["1–2", "Inception", "—", "UC-Inception-10-Percent", "10% use-case model"],
        ["1–2", "Inception", "—", "UP-Phases, Iteration-Plan-15-Weeks", "Methodology and calendar"],
        ["3–5", "Elaboration", "1", "UC-Elaboration1-30-Percent", "30% selection"],
        ["3–5", "Elaboration", "1", "SSD-UC01, SSD-UC02, SSD-UC03", "System events"],
        ["3–5", "Elaboration", "1", "Domain-Model", "Conceptual classes"],
        ["3–5", "Elaboration", "1", "Layered-Architecture-PoC, Architecture-Sale-Path", "Proof-of-concept"],
        ["6–8", "Elaboration", "2", "UC-Complete, SSD-UC04, SSD-UC09", "Remaining behaviour"],
        ["6–8", "Elaboration", "2", "DCD-Process-Sale, DCD-Overview, GRASP-Assignments", "Design"],
        ["6–8", "Elaboration", "2", "UI-01 to UI-10", "Prototypes"],
        ["6–8", "Elaboration", "2", "ERD-Logical, Schema-Groups", "Persistence design"],
        ["9–12", "Construction", "3–4", "Git-CI-Workflow, test tables", "How software will be grown"],
        ["13–14", "Transition", "5", "Updated models (same files until drift)", "Baseline for beta"],
        ["15", "Transition", "Demo", "Final presentation figures", "Same models, not a second design"],
    ])
    h2(doc, "Appendix B  Companion documents")
    table(doc, ["Document", "Folder"], [
        ["Inception Report", "Documentation/01-Inception"],
        ["Elaboration Iteration 1", "Documentation/02-Elaboration-Iteration-1"],
        ["Elaboration Iteration 2", "Documentation/03-Elaboration-Iteration-2"],
        ["Complete System Design", "Documentation/04-Complete-System-Design"],
        ["Construction & Testing", "Documentation/05-Construction-Testing"],
        ["Transition & Beta", "Documentation/06-Transition-Beta"],
        ["User Manual", "Documentation/07-User-Manual"],
        ["Compliance matrix", "Documentation/00-Project-Control"],
        ["Database design", "Database-Design"],
        ["Presentation", "Presentation"],
    ])
    h2(doc, "Appendix C  Group members")
    para(doc, "Insert official Group 20 names, student numbers, and contributions before submission.")
    table(doc, ["Name", "Student number", "Primary contribution"], [
        ["[Member 1]", "", ""],
        ["[Member 2]", "", ""],
        ["[Member 3]", "", ""],
        ["[Member 4]", "", ""],
    ])

    path = ROOT / "Documentation" / "08-Final-Report" / "Pharmacy-POS-Final-Project-Report.docx"
    doc.save(path)
    return path


def database_book():
    doc = new_document("Pharmacy POS  ·  Database Design", "Logical schema — not implemented")
    cover(doc, "CSC 4630  ·  Group 20", "Database Design",
          "Conceptual, logical, ERD, schema, normalisation, security", META)
    toc(doc)
    h1(doc, "A. Conceptual Data Model")
    para(doc, "The conceptual model is the domain model. Persistent concepts: User, Medicine, StockBatch, Sale, SalesLineItem, Payment, Customer, Prescription, Supplier, StockReceipt, StockAdjustment, AuditEntry.")
    add_figure(doc, D / "Domain-Model" / "Domain-Model.png",
               "Figure 1: Conceptual data (domain model)",
               "Receipt is not stored as its own entity.")

    h1(doc, "B. Logical Database Model")
    add_figure(doc, D / "Database" / "Schema-Groups.png",
               "Figure 2: Logical groups",
               "Identity, catalogue, movements, patients, sales.")

    h1(doc, "C. Entity Relationship Diagram")
    add_figure(doc, D / "Database" / "ERD-Logical.png",
               "Figure 3: ERD",
               "Must stay consistent with use cases and design classes.")

    h1(doc, "D. Database Schema")
    for tname, cols in M.TABLES.items():
        h2(doc, tname)
        table(doc, ["Table", "Column", "Data Type", "PK", "FK", "Nullable", "Description"],
              [[tname, *c] for c in cols])

    h1(doc, "E. Relationships")
    table(doc, ["From", "To", "From", "To", "Notes"], [list(r) for r in M.RELATIONSHIPS])
    para(doc, "Many-to-many Medicine–Sale is resolved by sale_items. Medicine–Prescription is resolved by prescription_items. No unresolved M:N remains.")

    h1(doc, "F. Normalisation")
    para(doc, (
        "Target is third normal form. Each non-key attribute depends on the key, the whole key, "
        "and nothing but the key. Controlled exception: unit_price and line_total on sale_items "
        "are copied from the catalogue at sale time so that a later price change does not rewrite "
        "history. line_total is determined by quantity * unit_price and could be computed; it is "
        "stored to simplify receipts and reports. That is a documented denormalisation, not an accident."
    ))
    table(doc, ["Check", "How the design answers"], [
        ["1NF", "Atomic columns; no repeating medicine groups on sales"],
        ["2NF", "sale_items key is sale_item_id; no partial dependence on a composite leftover"],
        ["3NF", "Customer name is not stored on sales; customer_id is"],
        ["Password", "Only hash + salt; not a normalised “fact” about a person in plaintext"],
    ])

    h1(doc, "G. Data Dictionary")
    table(doc, ["Entity", "Attribute", "Meaning"], [
        ["users", "role", "ADMINISTRATOR or PHARMACIST only"],
        ["users", "password_hash", "Salted hash"],
        ["medicines", "requires_prescription", "Forces UC-02 attachPrescription"],
        ["stock_batches", "expiry_date", "Sellability rule"],
        ["stock_batches", "quantity_on_hand", "Decremented by completed sales"],
        ["sales", "status", "IN_PROGRESS / COMPLETED / VOIDED"],
        ["payments", "method", "CASH / CARD / MOBILE_MONEY"],
        ["audit_logs", "action", "Sensitive event type"],
    ])

    h1(doc, "H. Database Security Design")
    bullet(doc, "Authentication data: username + salt + hash. Never plaintext passwords.")
    bullet(doc, "Authorisation: role column; application enforces; DB account used by the app is not a human Administrator login.")
    bullet(doc, "Access control: Pharmacist sessions cannot invoke catalogue writes.")
    bullet(doc, "Audit: audit_logs plus immutable sale rows after void.")
    bullet(doc, "Integrity: PKs, FKs, non-negative quantities, required status fields.")
    para(doc, "No CREATE TABLE script is included. That would be implementation.")
    refs(doc)
    path = ROOT / "Database-Design" / "Pharmacy-POS-Database-Design.docx"
    doc.save(path)
    return path


def inventory():
    doc = new_document("Pharmacy POS  ·  Diagram Inventory", "Week-by-week evolution")
    cover(doc, "CSC 4630  ·  Group 20", "Diagram and Artefact Inventory",
          "How the same models evolve from week 1 to week 15", META)
    h1(doc, "Inventory")
    table(doc, ["Week", "UP Phase", "Iteration", "Diagram / artefact", "Purpose"], [
        ["1–2", "Inception", "—", "UC-Inception-10-Percent.png", "Initial high-level use-case model"],
        ["1–2", "Inception", "—", "UP-Phases.png", "Iterative UP, not waterfall"],
        ["1–2", "Inception", "—", "Iteration-Plan-15-Weeks.png", "Marks and weeks"],
        ["3–5", "Elaboration", "1", "UC-Elaboration1-30-Percent.png", "Detailed 30% set"],
        ["3–5", "Elaboration", "1", "SSD-UC01 / UC02 / UC03", "Black-box system events"],
        ["3–5", "Elaboration", "1", "Domain-Model.png", "Conceptual classes"],
        ["3–5", "Elaboration", "1", "Layered-Architecture-PoC.png", "Architecture"],
        ["3–5", "Elaboration", "1", "Architecture-Sale-Path.png", "PoC collaboration"],
        ["6–8", "Elaboration", "2", "UC-Complete.png", "Final use-case model"],
        ["6–8", "Elaboration", "2", "SSD-UC04 / UC09", "Remaining SSDs"],
        ["6–8", "Elaboration", "2", "DCD-Process-Sale.png / DCD-Overview.png", "Design classes"],
        ["6–8", "Elaboration", "2", "GRASP-Assignments.png", "Responsibilities"],
        ["6–8", "Elaboration", "2", "UI-01 … UI-10", "Prototypes"],
        ["6–8", "Elaboration", "2", "ERD-Logical.png / Schema-Groups.png", "Database design"],
        ["9–12", "Construction", "3–4", "Git-CI-Workflow.png", "How features will be built"],
        ["9–12", "Construction", "3–4", "Feature / test / defect tables", "Tracking (results later)"],
        ["13–14", "Transition", "5", "Same UML files until updated", "Beta baseline"],
        ["15", "Transition", "Demo", "Final presentation", "Same diagrams, not a redesign"],
    ])
    path = ROOT / "Documentation" / "00-Project-Control" / "Diagram-Inventory.docx"
    doc.save(path)
    return path


def main():
    for p in (construction(), transition(), user_manual(), final_report(), database_book(), inventory()):
        print(p)


if __name__ == "__main__":
    main()
