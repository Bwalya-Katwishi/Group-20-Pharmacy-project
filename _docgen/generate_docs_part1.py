"""Word documents 1–4 and the marking compliance matrix."""

from pathlib import Path
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


def _uc_row(uc):
    return [uc["id"], uc["name"], uc["actor"], uc["priority"], uc["iteration"], ", ".join(uc["frs"])]


def inception():
    doc = new_document("Pharmacy POS  ·  Inception Report", "Weeks 1–2  ·  10 marks")
    cover(doc, "CSC 4630  ·  Group 20", "Inception Report",
          "Vision, feasibility, 10% use cases, risks, and iteration plan", META)
    toc(doc)

    h1(doc, "1. Project Overview")
    para(doc, (
        f"This report is the Inception artefact for the {M.SYSTEM}. "
        "Inception, in the Unified Process as taught from Larman, is not a requirements freeze "
        "and not a mini-waterfall. Its job is to decide whether the project is worth serious "
        "investigation, to name the core problem, to expose the highest risks, and to identify "
        "the small set of use cases that will drive the first real development iteration."
    ))
    para(doc, (
        "The group is not implementing the application in this phase. The marking guide awards "
        "10 marks for vision, high-level use cases, risk list, feasibility, and a justified "
        "iteration plan mapped to UP phases."
    ))
    table(doc, ["Item", "Value"], [
        ["System", M.SYSTEM],
        ["Course", M.COURSE],
        ["Group", M.GROUP],
        ["Methodology", M.METHODOLOGY],
        ["System user roles", "Exactly two: Administrator; Pharmacist/Cashier"],
        ["Implementation status", "PharmaPoint built — Pharmacy-POS/apoza/ (see Construction report)"],
    ])

    h1(doc, "2. Problem Statement")
    para(doc, M.PROBLEM_STATEMENT)
    para(doc, (
        "A further problem is organisational: some generic POS products assume a cashier who is "
        "not the pharmacist. This project forbids that split. The Pharmacist performs the cashier "
        "function. Inventing a third role would misrepresent both the marking constraint and the "
        "intended workplace."
    ))

    h1(doc, "3. Business Case")
    h2(doc, "3.1 Operational value")
    para(doc, (
        "A correct sale that also updates the right batch reduces two expensive mistakes: giving "
        "out an expired pack and promising a medicine that is not on the shelf. Receipts that "
        "match the recorded sale reduce disputes at the counter."
    ))
    h2(doc, "3.2 Strategic and compliance value")
    para(doc, (
        "Batch and expiry data turn a later inspection from a paper hunt into a query. "
        "Prescription-only items cannot silently pass as sweets. The design does not claim to "
        "submit NHIMA claims or to connect to a national e-prescription network; those are "
        "explicitly out of scope so that the business case stays honest."
    ))
    h2(doc, "3.3 Financial argument")
    para(doc, (
        "The construction cost is student labour and ordinary hardware. The avoided cost is "
        "wasted expired stock, lost sales from false availability, and time spent reconstructing "
        "a day's takings from mixed paper and memory. No fabricated ROI percentage is offered."
    ))
    h2(doc, "3.4 Why a custom pharmacy POS rather than a supermarket till")
    para(doc, (
        "A supermarket till has Sale, Line, and Payment — the Larman NextGen shape. A pharmacy "
        "also has StockBatch (expiry), Prescription, and a legally meaningful dispenser who is "
        "the same person taking the money. Those three facts justify a pharmacy-specific model "
        "instead of copying NextGen unchanged."
    ))

    h1(doc, "4. Vision")
    para(doc, M.VISION)

    h1(doc, "5. Scope")
    h2(doc, "5.1 In scope")
    for s in M.SCOPE_IN:
        bullet(doc, s)
    h2(doc, "5.2 Out of scope")
    for s in M.SCOPE_OUT:
        bullet(doc, s)
    para(doc, (
        "Out-of-scope items are not hidden requirements. If a later stakeholder demands NHIMA "
        "claims or a web shop, that is a new project increment, not a silent expansion of UC-02."
    ))

    h1(doc, "6. Business Objectives")
    table(doc, ["ID", "Objective"], [[i, t] for i, t in M.OBJECTIVES])

    h1(doc, "7. Stakeholders")
    table(doc, ["Stakeholder", "Interest", "System account?"], [
        ["Pharmacy owner / manager (person, not a role)", "Profit, compliance, trustworthy stock figures", "May hold the Administrator account"],
        ["Administrator", "Catalogue, stock, users, reports", "Yes — ROLE-ADMIN"],
        ["Pharmacist/Cashier", "Fast correct sales; legal dispensing", "Yes — ROLE-PHARM"],
        ["Customer / patient", "Correct medicine, fair price, receipt", "No"],
        ["Supplier", "Deliveries recorded against their name", "No"],
        ["Regulator / inspector", "Traceability of batches and prescription-only sales", "No"],
        ["Course lecturer", "UP artefacts, traces, no waterfall theatre", "No"],
    ])

    h1(doc, "8. System Users")
    para(doc, (
        "There are exactly two system user roles. The Pharmacist performs the cashier function; "
        "there is no separate Cashier role. Customer and Supplier may appear as actors on use-case "
        "diagrams but they do not log in."
    ))
    table(doc, ["ID", "Role", "Kind", "Summary"],
          [[r["id"], r["name"], r["kind"], r["summary"]] for r in M.ROLES])
    table(doc, ["ID", "Actor", "Kind", "Summary"],
          [[r["id"], r["name"], r["kind"], r["summary"]] for r in M.EXTERNAL_ACTORS])

    h1(doc, "9. High-Level Requirements")
    h2(doc, "9.1 Functional requirements")
    table(doc, ["ID", "Statement"], [[i, t] for i, t in M.FRS])
    h2(doc, "9.2 Non-functional requirements")
    table(doc, ["ID", "Quality", "Statement"], [[i, q, t] for i, q, t in M.NFRS])
    h2(doc, "9.3 Assumptions")
    para(doc, "Assumptions are not requirements. If an assumption fails, the requirement set may change.")
    table(doc, ["ID", "Assumption", "Reason", "Impact if incorrect", "Status"],
          [list(a) for a in M.ASSUMPTIONS])

    h1(doc, "10. Ten Percent Use Cases")
    para(doc, (
        "Larman and the marking guide ask for about 10% of the use cases in Inception, chosen "
        "because they are architecturally significant — not because they are easy. The group "
        "identified ten user-goal use cases. Ten percent is therefore the single core goal "
        "UC-02 Process Sale, described here at a brief level. OTC and prescription-linked "
        "paths are scenarios of that one goal, not two extra Inception use cases and not "
        "button-level steps such as “click Search”."
    ))
    uc02 = next(u for u in M.USE_CASES if u["id"] == "UC-02")
    table(doc, ["ID", "Name", "Primary actor", "Why this is the 10%"], [[
        uc02["id"], uc02["name"], uc02["actor"],
        "Touches money, stock, expiry, prescription rules, payment, and receipt — the risks that will break the architecture if ignored."
    ]])
    para(doc, uc02["brief"])
    para(doc, "Brief main success scenario (Inception level, not fully dressed):", bold=True)
    for step in [
        "Pharmacist/Cashier starts a sale.",
        "Pharmacist/Cashier enters each medicine and quantity; the system refuses expired or insufficient batches.",
        "If a line is prescription-only, prescription and customer details are recorded.",
        "Pharmacist/Cashier ends the sale and records cash, card, or mobile-money payment.",
        "The system completes the sale, reduces stock, and presents a receipt.",
    ]:
        bullet(doc, step)

    h1(doc, "11. Initial Use-Case Model")
    add_figure(
        doc, D / "Use-Cases" / "UC-Inception-10-Percent.png",
        "Figure 1: Initial use-case model (Inception, 10%)",
        "Only the architecturally significant Process Sale goal is shown. The Customer does not operate the software.",
    )
    para(doc, "The remaining nine use cases are named so that the 30% and 70% cuts are not arbitrary:")
    table(doc, ["ID", "Name", "Primary actor", "Priority", "Iteration", "FR"],
          [_uc_row(u) for u in M.USE_CASES])
    add_figure(
        doc, D / "Use-Cases" / "UC-Complete.png",
        "Figure 2: Full use-case outline (names only in Inception; details come later)",
        "Showing the outline early prevents surprise actors. Detailing waits for Elaboration.",
    )

    h1(doc, "12. Initial Risk Register")
    table(doc, ["ID", "Risk", "P", "I", "Priority", "Mitigation", "Iteration", "Status"],
          [list(r) for r in M.RISKS_INCEPTION])
    para(doc, (
        "The first elaboration iteration is aimed at R-01, R-02, R-04, and R-10: the sale must "
        "move through layers, obey expiry, and complete payment and stock together."
    ))

    h1(doc, "13. Feasibility Study")
    h2(doc, "13.1 Technical feasibility")
    para(doc, (
        "A layered desktop or web application with a relational database can represent Sale, "
        "StockBatch, User, and Payment. Password hashing, role checks, and transactional "
        "updates are ordinary techniques. Live payment gateways are treated as a later "
        "variation (A-04), which keeps technical feasibility inside the course window."
    ))
    h2(doc, "13.2 Economic feasibility")
    para(doc, (
        "There is no licence purchase in the student project. Hardware is a normal workstation. "
        "The economic case for a real pharmacy is the reduction of waste and dispute time "
        "already stated; it is qualitative on purpose."
    ))
    h2(doc, "13.3 Operational feasibility")
    para(doc, (
        "The two-role model matches a small pharmacy: one person on the counter, one person "
        "(or the same person at a different time) administering the catalogue. Training risk "
        "R-05 remains and is accepted into Transition rather than denied."
    ))
    h2(doc, "13.4 Schedule feasibility")
    para(doc, (
        "The marking guide already decomposes 15 weeks. Feasibility depends on not building "
        "features during Inception and on proving Process Sale in Elaboration 1 before widening "
        "the use-case set. That is why this document forbids implementation until the group "
        "is told to start."
    ))

    h1(doc, "14. UP Methodology")
    para(doc, (
        "The Unified Process is iterative and incremental, architecture-centric, use-case-driven, "
        "and risk-driven (Larman; marking guide “Key UP Principles”). The four phases are "
        "Inception, Elaboration, Construction, and Transition. Each phase contains iterations. "
        "This project uses Iteration 1 and 2 in Elaboration, Iterations 3–4 in Construction, "
        "and Iteration 5 in Transition."
    ))
    add_figure(
        doc, D / "UP-Planning" / "UP-Phases.png",
        "Figure 3: Unified Process phases used by this project",
        "Arrows mean sequence of phases, not a single-pass waterfall of all requirements then all design then all code.",
    )

    h1(doc, "15. Iteration Plan")
    add_figure(
        doc, D / "UP-Planning" / "Iteration-Plan-15-Weeks.png",
        "Figure 4: Fifteen-week iteration plan",
        "Marks and weeks are taken from the lecturer’s marking guide, not invented by the group.",
    )
    table(doc, ["Weeks", "Phase / iteration", "Marks", "Objective"], [
        ["1–2", "Inception", "10", "Vision, 10% use cases, risks, feasibility, plan"],
        ["3–5", "Elaboration Iteration 1", "20", "30% detailed use cases, SSDs, domain model, architectural PoC"],
        ["6–8", "Elaboration Iteration 2", "15", "Remaining use cases, DCDs, GRASP, UI prototypes, schema"],
        ["9–12", "Construction Iterations 3–4", "30", "Prioritised features, unit + integration tests, Git, CI, defects"],
        ["13–14", "Transition Iteration 5", "15", "Beta, performance/security, final models, user manual"],
        ["15", "Demo and submission", "10", "Live demo, final report, repository completeness"],
    ])

    h1(doc, "16. UP Phase Mapping")
    para(doc, (
        "The mapping is justified, not decorative. Inception investigates. Elaboration attacks "
        "the risks that would make Construction a gamble. Construction grows features in "
        "priority order on a stable spine. Transition makes the system usable by real staff "
        "and submitable to the lecturer."
    ))
    table(doc, ["Marking-guide milestone", "UP idea (Larman)", "This project’s response"], [
        ["Vision & feasibility", "Is it worth serious work?", "Problem, business case, feasibility, 10% UC-02"],
        ["Core architecture & requirements", "Prove the core design", "UC-01/02/03, SSDs, domain, layered PoC"],
        ["Risk-driven design", "Design to remaining risks", "70% use cases, DCD, GRASP, UI, database design"],
        ["Feature implementation", "Increment working software", "Planned only — not executed in this documentation pack"],
        ["Polishing & deployment prep", "Make it releasable", "Beta/security/performance plans; user manual draft"],
        ["Demo & final submission", "Show scenarios and reflect", "Presentation and final report structure"],
    ])

    h1(doc, "17. Inception Conclusion")
    para(doc, (
        "The project is feasible as a 15-week UP course system if the group keeps two roles, "
        "keeps insurance and e-commerce out, and treats Process Sale as the first architecture "
        "problem. Inception has named the 10% use case, the risks, and the week map. "
        "Elaboration Iteration 1 must now dress UC-01, UC-02, and UC-03, draw SSDs, build a "
        "conceptual domain model, and show a layered proof-of-concept — still without writing "
        "the application."
    ))
    refs(doc)
    path = ROOT / "Documentation" / "01-Inception" / "Pharmacy-POS-Inception-Report.docx"
    doc.save(path)
    return path


def elab1():
    doc = new_document("Pharmacy POS  ·  Elaboration Iteration 1", "Weeks 3–5  ·  20 marks")
    cover(doc, "CSC 4630  ·  Group 20", "Elaboration Iteration 1 Report",
          "30% use cases, SSDs, domain model, architectural proof-of-concept", META)
    toc(doc)

    h1(doc, "1. Introduction")
    para(doc, (
        "Elaboration Iteration 1 is the first real development iteration in Larman’s sense: "
        "not coding the whole product, but investigating the core so that Construction is not "
        "a guess. The marking guide awards 20 marks for detailed 30% use cases with SSDs, a "
        "domain model of conceptual classes, an architectural proof-of-concept, and an updated "
        "risk list."
    ))

    h1(doc, "2. Iteration Objectives")
    for t in [
        "Fully dress the 30% use cases UC-01, UC-02, and UC-03.",
        "Describe key scenarios of Process Sale (OTC success, prescription-linked, expiry refusal).",
        "Draw SSDs that treat the system as a black box.",
        "Build a conceptual domain model without methods.",
        "Propose a layered architecture and a Process Sale path as proof-of-concept.",
        "Sketch the persistence idea that later becomes the schema.",
        "Update risks now that the spine is visible.",
    ]:
        bullet(doc, t)

    h1(doc, "3. Selected 30% Use Cases")
    para(doc, (
        "Thirty percent of ten use cases is three. They are not a random third. They are the "
        "identity boundary, the money-and-stock transaction, and the catalogue the transaction "
        "depends on."
    ))
    add_figure(
        doc, D / "Use-Cases" / "UC-Elaboration1-30-Percent.png",
        "Figure 1: Elaboration 1 use-case selection",
        "Administrator and Pharmacist/Cashier both authenticate. Only the Pharmacist processes a sale. Only the Administrator maintains medicines.",
    )
    table(doc, ["ID", "Name", "Actor", "Priority", "Iteration", "FR"],
          [_uc_row(u) for u in M.USE_CASES if u["id"] in ("UC-01", "UC-02", "UC-03")])

    h1(doc, "4. Detailed Use Cases")
    for uid in ("UC-01", "UC-02", "UC-03"):
        uc = next(u for u in M.USE_CASES if u["id"] == uid)
        dressed_use_case(doc, uc, M.DETAILED_UCS[uid])

    h1(doc, "5. Key Scenarios")
    h2(doc, "5.1 SC-01  Routine OTC sale")
    para(doc, (
        "Two unexpired OTC lines, cash tendered above the total, receipt shown. This is the "
        "main success scenario of UC-02 without attachPrescription. It is the first scenario "
        "the architectural PoC must support."
    ))
    h2(doc, "5.2 SC-02  Prescription-linked sale")
    para(doc, (
        "A prescription-only medicine is entered. The system refuses endSale until a customer "
        "and prescription reference exist (FR-06). This scenario distinguishes a pharmacy POS "
        "from NextGen’s store example."
    ))
    h2(doc, "5.3 SC-03  Expired or short stock")
    para(doc, (
        "enterItem is refused. No SalesLineItem is created. This scenario is how BO-01 and "
        "FR-05 become visible system behaviour rather than a poster slogan."
    ))
    h2(doc, "5.4 SC-04  Administrator adds a medicine then Pharmacist sells it")
    para(doc, (
        "UC-03 then UC-02. Proves the catalogue is not a separate toy system."
    ))

    h1(doc, "6. System Sequence Diagrams")
    para(doc, (
        "Larman Chapter 9: an SSD shows actors and the system as a black box. Interior classes "
        "are not shown. Event names express intent (enterItem, not scan)."
    ))
    add_figure(doc, D / "SSD" / "SSD-UC02-Process-Sale.png",
               "Figure 2: SSD for UC-02 Process Sale",
               "System events: makeNewSale, enterItem, attachPrescription, endSale, makePayment. The Customer generates none of them.")
    add_figure(doc, D / "SSD" / "SSD-UC01-Authenticate.png",
               "Figure 3: SSD for UC-01 Authenticate User",
               "submitCredentials is the intent-level event. Role-specific home view is the output.")
    add_figure(doc, D / "SSD" / "SSD-UC03-Manage-Medicines.png",
               "Figure 4: SSD for UC-03 Manage Medicines",
               "saveMedicine and deactivateMedicine are Administrator system events.")

    h1(doc, "7. Domain Model")
    para(doc, (
        "The domain model is conceptual. It lists ideas the business already has, not software "
        "controllers. Methods are omitted on purpose (Larman: do not confuse the domain model "
        "with a design class diagram)."
    ))
    add_figure(doc, D / "Domain-Model" / "Domain-Model.png",
               "Figure 5: Conceptual domain model",
               "Need-to-know associations are kept. NextGen’s Register is omitted: a single-counter pharmacy records Sale against User. Receipt is an output, not a concept.")

    h1(doc, "8. Conceptual Classes")
    table(doc, ["Conceptual class", "Meaning in this pharmacy"],
          [list(x) for x in M.DOMAIN_CLASSES])
    para(doc, (
        "Medicine is the catalogue description. StockBatch is the physical, expiring quantity. "
        "That split is the pharmacy analogue of Larman’s ProductSpecification versus Item, "
        "adapted rather than copied: pharmacies care about batch number and expiry more than "
        "about serialized items."
    ))

    h1(doc, "9. Architectural Proof-of-Concept")
    para(doc, (
        "The PoC question is not “can we draw four boxes?” It is: can makeNewSale, enterItem, "
        "endSale, and makePayment travel from a view through a controller into Sale and "
        "StockBatch and back out through a repository without the view knowing SQL, and "
        "without completing a sale if stock cannot move?"
    ))
    add_figure(doc, D / "Architecture" / "Architecture-Sale-Path.png",
               "Figure 6: Process Sale path used as the proof-of-concept",
               "If this path cannot be explained, Construction of reports or user-admin would be theatre.")

    h1(doc, "10. Layered Architecture")
    add_figure(doc, D / "Architecture" / "Layered-Architecture-PoC.png",
               "Figure 7: Layered architecture",
               "Dependencies point down. Presentation never imports repositories. External payment gateways remain a seam, not a dependency of Sale.")
    table(doc, ["Layer", "Responsibility", "Depends on", "Major components"], [
        ["Presentation", "Screens and user gestures", "Application", "LoginView, POSView, PaymentView, admin views"],
        ["Application", "System events (GRASP Controller)", "Domain", "SaleController, AuthController, MedicineController"],
        ["Domain", "Pharmacy rules and totals", "nothing above", "Sale, SalesLineItem, StockBatch, Payment, Medicine"],
        ["Persistence", "Store and reconstitute aggregates", "database engine (later)", "SaleRepository, InventoryRepository"],
        ["External boundary", "Printer / manual pay confirm", "called via Indirection", "ReceiptService, PaymentMethod implementations"],
    ])

    h1(doc, "11. Architectural Decisions")
    table(doc, ["ID", "Decision", "Rationale", "Alternative rejected"], [
        ["AD-01", "Layered architecture", "Marking guide example; separates UI from rules", "Smart UI with SQL in button handlers"],
        ["AD-02", "Use-case controllers", "Larman Controller; maps 1:1 to SSDs", "One god service for the whole system"],
        ["AD-03", "Two roles as an enumeration on User", "Project rule; avoids a role table that invites a third role", "Free-text role names"],
        ["AD-04", "Batch-level stock", "Expiry and recall require it", "A single quantity on Medicine"],
        ["AD-05", "Manual confirmation of card/mobile money", "A-04; Protected Variations keeps a PaymentMethod seam", "Pretending a live gateway exists"],
        ["AD-06", "No Register class", "Single counter; User records the sale", "Copying NextGen Register without a need-to-know reason"],
        ["AD-07", "Documentation before code", "Group instruction and risk R-07", "Coding screens during Inception"],
    ])

    h1(doc, "12. Initial Database Design Concept")
    para(doc, (
        "Persistence is still a design idea. Tables that must exist later are already implied "
        "by the domain model: users, medicines, stock_batches, sales, sale_items, payments, "
        "customers, prescriptions. Passwords will be hashes. The full schema, ERD, and "
        "normalisation argument belong to Elaboration 2 so that this iteration stays on "
        "behaviour and architecture."
    ))
    add_figure(doc, D / "Database" / "Schema-Groups.png",
               "Figure 8: Intended schema groups (concept only)",
               "Groups, not CREATE TABLE scripts. Implementation SQL is forbidden until START IMPLEMENTATION.")

    h1(doc, "13. Updated Risk Register")
    table(doc, ["ID", "Risk", "P", "I", "Priority", "Mitigation", "Iteration", "Status"],
          [list(r) for r in M.RISKS_ELAB1])

    h1(doc, "14. Risk Analysis")
    para(doc, (
        "R-01 and R-04 are the same family: money and stock must move together. The PoC "
        "answers them with a single completion operation. R-02 is answered by StockBatch as "
        "Information Expert. R-10 is answered by the layer diagram. R-05 (training) is not "
        "an architecture risk and is left open for Transition. No risk is marked “closed by "
        "implementation” because implementation has not started."
    ))

    h1(doc, "15. Iteration Results")
    table(doc, ["Planned", "Result in this documentation pack"], [
        ["30% detailed use cases", "UC-01, UC-02, UC-03 fully dressed"],
        ["Key scenarios", "SC-01 to SC-04"],
        ["SSDs", "UC-01, UC-02, UC-03"],
        ["Domain model", "Conceptual classes and associations"],
        ["Architectural PoC", "Layered design + sale path"],
        ["Updated risks", "Statuses moved to Mitigating where design exists"],
        ["Working application", "Not produced — correctly out of this iteration’s documentation objective"],
    ])

    h1(doc, "16. Conclusion")
    para(doc, (
        "Iteration 1 has a behavioural spine and an architecture that can carry it. Iteration 2 "
        "must finish the use-case set, assign methods with GRASP, prototype the UI, and lock "
        "the logical database — still without writing the product."
    ))
    refs(doc)
    path = ROOT / "Documentation" / "02-Elaboration-Iteration-1" / "Pharmacy-POS-Elaboration-Iteration-1-Report.docx"
    doc.save(path)
    return path


def elab2():
    doc = new_document("Pharmacy POS  ·  Elaboration Iteration 2", "Weeks 6–8  ·  15 marks")
    cover(doc, "CSC 4630  ·  Group 20", "Elaboration Iteration 2 Report",
          "Remaining use cases, design classes, GRASP, UI prototypes, schema", META)
    toc(doc)

    h1(doc, "1. Introduction")
    para(doc, (
        "Elaboration Iteration 2 is risk-driven design. The marking guide awards 15 marks for "
        "the remaining 70% of use cases, refined design class diagrams with methods, UI "
        "prototypes, and risk-mitigation progress. The group still does not implement the "
        "application."
    ))

    h1(doc, "2. Iteration Objectives")
    for t in [
        "Fully dress UC-04 through UC-10.",
        "Add SSDs where the system events are not obvious from Iteration 1.",
        "Produce design class diagrams derived from events → responsibilities → GRASP.",
        "Prototype Administrator and Pharmacist/Cashier screens that match the use cases.",
        "Publish the logical database schema and ERD.",
        "Show how risks moved from “open” to “mitigated in design”.",
    ]:
        bullet(doc, t)

    h1(doc, "3. Remaining Use Cases")
    para(doc, "Seventy percent of ten use cases is seven. They widen administration and the exceptional sale path.")
    table(doc, ["ID", "Name", "Actor", "Priority", "Iteration", "FR"],
          [_uc_row(u) for u in M.USE_CASES if u["id"] not in ("UC-01", "UC-02", "UC-03")])
    add_figure(doc, D / "Use-Cases" / "UC-Complete.png",
               "Figure 1: Complete use-case model",
               "Same model as Inception’s outline, now with fully dressed descriptions below.")

    h1(doc, "4. Detailed Use Cases")
    for uid in ("UC-04", "UC-05", "UC-06", "UC-07", "UC-08", "UC-09", "UC-10"):
        uc = next(u for u in M.USE_CASES if u["id"] == uid)
        dressed_use_case(doc, uc, M.DETAILED_UCS[uid])

    h1(doc, "5. Additional System Sequence Diagrams")
    add_figure(doc, D / "SSD" / "SSD-UC04-Manage-Inventory.png",
               "Figure 2: SSD for UC-04 Manage Inventory",
               "receiveStock, adjustStock, and viewStockAlerts are Administrator events.")
    add_figure(doc, D / "SSD" / "SSD-UC09-Void-Sale.png",
               "Figure 3: SSD for UC-09 Void Sale",
               "voidSale(saleId, reason) is the intent-level event. There is no deleteSale event.")

    h1(doc, "6. Refined Design")
    para(doc, (
        "Design starts from the SSD events, not from a pile of tables. UC-02 events become "
        "SaleController methods. Those methods delegate to Sale and SaleService. Persistence "
        "objects are fabrications. Payment kinds vary behind an interface."
    ))
    add_figure(doc, D / "UP-Planning" / "Traceability-Chain.png",
               "Figure 4: How a requirement becomes a class and a test",
               "The chain is the quality rule for this project: Process Sale is one story in every artefact.")

    h1(doc, "7. Design Class Diagrams")
    add_figure(doc, D / "Design-Class" / "DCD-Process-Sale.png",
               "Figure 5: Design classes for Process Sale",
               "Methods come from SSDs and GRASP, not from inventing getters for every column.")
    add_figure(doc, D / "Design-Class" / "DCD-Overview.png",
               "Figure 6: Application, domain, and fabrication overview",
               "Controllers for the other use cases follow the same shape as SaleController.")

    h1(doc, "8. Class Responsibilities")
    table(doc, ["Class", "Responsibility", "Collaborators"], [
        ["SaleController", "Accept UC-02 system events; keep a current sale", "SaleService, views"],
        ["Sale", "Hold lines, total, status; create lines and payment", "SalesLineItem, Payment"],
        ["SalesLineItem", "Quantity, price, line total", "Medicine (price copied)"],
        ["StockBatch", "Expiry, quantity, sellability, increment/decrement", "InventoryRepository"],
        ["SaleService", "Complete or void a sale as one unit of work", "Sale, repositories, AuditLogger"],
        ["PaymentMethod", "Record a specific tender type", "Payment"],
        ["AuthController", "UC-01 events", "AuthenticationService, PasswordHasher"],
        ["MedicineController", "UC-03 events", "Medicine, MedicineRepository"],
        ["InventoryController", "UC-04 events", "StockReceipt, StockAdjustment, StockBatch"],
        ["UserController", "UC-05 events", "User, PasswordHasher"],
        ["ReceiptService", "Present a receipt without Sale knowing the device", "Sale, pharmacy settings"],
    ])

    h1(doc, "9. GRASP Analysis")
    add_figure(doc, D / "Design-Class" / "GRASP-Assignments.png",
               "Figure 7: GRASP map for the sale collaboration",
               "Each important operation has a principle, not just a class name.")
    table(doc, ["Responsibility", "Class", "Collaborators", "Why", "GRASP"],
          [list(r) for r in M.GRASP_ROWS])

    h1(doc, "10. UI Prototypes")
    para(doc, (
        "Prototypes are design, not a product. They exist so that UC-02 can be performed on "
        "one sales surface and so that Administrator work never appears as extra roles."
    ))
    for fname, cap, exp in [
        ("UI-01-Login.png", "Figure 8: Login", "Role is an account attribute, not a third login type."),
        ("UI-02-POS-Sale.png", "Figure 9: Pharmacist sales screen", "Search, cart, batch, and total on one screen (NFR-03)."),
        ("UI-03-Payment.png", "Figure 10: Payment", "Cash, card, mobile money. Manual confirmation for non-cash (A-04)."),
        ("UI-04-Receipt.png", "Figure 11: Receipt", "Output of Sale, including pharmacist identity."),
        ("UI-05-Prescription.png", "Figure 12: Attach prescription", "Shown only when a line requires it."),
        ("UI-06-Admin-Dashboard.png", "Figure 13: Administrator dashboard", "Alerts for low stock and near expiry."),
        ("UI-07-Medicines.png", "Figure 14: Medicine maintenance", "Supports UC-03."),
        ("UI-08-Inventory.png", "Figure 15: Inventory", "Expired batches visible but not sellable."),
        ("UI-09-Users.png", "Figure 16: Users", "Two roles only."),
        ("UI-10-Reports.png", "Figure 17: Reports", "Read-only Administrator view."),
    ]:
        add_figure(doc, UI / fname, cap, exp, width=14.5)

    h1(doc, "11. Database Schema Design")
    para(doc, (
        "The logical schema is the persistent form of the domain model. It is not an "
        "implemented database. No SQL scripts are supplied."
    ))
    add_figure(doc, D / "Database" / "ERD-Logical.png",
               "Figure 18: Logical ERD",
               "Associative entities sale_items and prescription_items resolve many-to-many pairs.")
    add_figure(doc, D / "Database" / "Schema-Groups.png",
               "Figure 19: Schema groups",
               "Identity, catalogue, movements, patients, sales.")
    para(doc, "Column-level specification is repeated in the Complete System Design Document and in Database-Design/.")
    for tname, cols in M.TABLES.items():
        h3(doc, tname)
        table(doc, ["Column", "Type", "PK", "FK", "Null", "Description"],
              [[c[0], c[1], c[2], c[3], c[4], c[5]] for c in cols])

    h1(doc, "12. Architecture Refinement")
    para(doc, (
        "Iteration 1 proposed layers. Iteration 2 names the classes inside them and the GRASP "
        "reasons they exist. The downward dependency rule is unchanged. Construction should "
        "implement by feature (a vertical slice of Process Sale) rather than finishing one "
        "layer completely before the next — that would be waterfall in disguise."
    ))

    h1(doc, "13. Updated Risk Register")
    table(doc, ["ID", "Risk", "P", "I", "Priority", "Mitigation", "Iteration", "Status"],
          [list(r) for r in M.RISKS_ELAB2])

    h1(doc, "14. Risk Mitigation Progress")
    table(doc, ["Risk", "Inception", "Elaboration 1", "Elaboration 2"], [
        ["R-01 stock/sale split", "Named", "PoC transaction", "SaleService unit of work in DCD"],
        ["R-02 expired sale", "Named", "Domain rule", "StockBatch.isSellable in DCD"],
        ["R-03 third role", "Named", "Actor model", "role enumeration + UI"],
        ["R-04 payment split", "Named", "SSD makePayment", "Payment + PaymentMethod"],
        ["R-05 user resistance", "Named", "Still open", "UI prototypes ready for beta"],
        ["R-06 scope creep", "Named", "Scope held", "70% use cases stay inside POS"],
        ["R-10 architecture", "Named", "Layers drawn", "Responsibilities assigned"],
    ])
    para(doc, "No row claims that code has been measured. Mitigation here means design mitigation.")

    h1(doc, "15. Iteration Results")
    table(doc, ["Marking item", "Artefact"], [
        ["Remaining 70% use cases", "UC-04–UC-10 fully dressed"],
        ["Design class diagrams with methods", "DCD-Process-Sale, DCD-Overview"],
        ["UI prototypes", "Ten screens covering both roles"],
        ["Risk mitigation progress", "Register + progress table"],
    ])

    h1(doc, "16. Conclusion")
    para(doc, (
        "Design is now rich enough to construct from. The next documents record how "
        "Construction and Transition will be run, and the Complete System Design Document "
        "binds every identifier together. Coding still waits for START IMPLEMENTATION."
    ))
    refs(doc)
    path = ROOT / "Documentation" / "03-Elaboration-Iteration-2" / "Pharmacy-POS-Elaboration-Iteration-2-Report.docx"
    doc.save(path)
    return path


def system_design():
    doc = new_document("Pharmacy POS  ·  Complete System Design", "Design baseline")
    cover(doc, "CSC 4630  ·  Group 20", "Complete System Design Document",
          "Requirements, models, architecture, schema, UI, security, traceability", META)
    toc(doc)

    h1(doc, "1. System Overview")
    para(doc, (
        f"The {M.SYSTEM} is a counter application for a single Zambian pharmacy. "
        "A Pharmacist/Cashier sells medicines; an Administrator maintains catalogue, stock, "
        "users, suppliers, and reports. The design follows UP and Larman: use-case-driven, "
        "architecture-centric, iterative."
    ))

    h1(doc, "2. Scope")
    para(doc, "In scope:", bold=True)
    for s in M.SCOPE_IN:
        bullet(doc, s)
    para(doc, "Out of scope:", bold=True)
    for s in M.SCOPE_OUT:
        bullet(doc, s)

    h1(doc, "3. Actors")
    table(doc, ["Name", "Kind", "Notes"],
          [[r["name"], r["kind"], r["summary"]] for r in M.ROLES + M.EXTERNAL_ACTORS])
    para(doc, "The Pharmacist performs the cashier function; there is no separate Cashier role.", bold=True)

    h1(doc, "4. Functional Requirements")
    table(doc, ["ID", "Statement"], [[i, t] for i, t in M.FRS])

    h1(doc, "5. Non-Functional Requirements")
    table(doc, ["ID", "Quality", "Statement"], [[i, q, t] for i, q, t in M.NFRS])

    h1(doc, "6. Complete Use-Case Model")
    add_figure(doc, D / "Use-Cases" / "UC-Complete.png",
               "Figure 1: Complete use-case model",
               "Ten user-goal use cases. No “click button” use cases.")
    table(doc, ["ID", "Name", "Actor", "Priority", "Iteration", "FR"],
          [_uc_row(u) for u in M.USE_CASES])

    h1(doc, "7. Use-Case Descriptions")
    for uc in M.USE_CASES:
        dressed_use_case(doc, uc, M.DETAILED_UCS[uc["id"]])

    h1(doc, "8. Domain Model")
    add_figure(doc, D / "Domain-Model" / "Domain-Model.png",
               "Figure 2: Domain model",
               "Conceptual classes only.")
    table(doc, ["Class", "Meaning"], [list(x) for x in M.DOMAIN_CLASSES])

    h1(doc, "9. System Sequence Diagrams")
    for fn, cap, exp in [
        ("SSD-UC02-Process-Sale.png", "Figure 3: SSD UC-02", "Core money/stock events."),
        ("SSD-UC01-Authenticate.png", "Figure 4: SSD UC-01", "Session creation."),
        ("SSD-UC03-Manage-Medicines.png", "Figure 5: SSD UC-03", "Catalogue events."),
        ("SSD-UC04-Manage-Inventory.png", "Figure 6: SSD UC-04", "Stock events."),
        ("SSD-UC09-Void-Sale.png", "Figure 7: SSD UC-09", "Compensating event."),
    ]:
        add_figure(doc, D / "SSD" / fn, cap, exp)

    h1(doc, "10. Operation Contracts")
    para(doc, (
        "Larman uses operation contracts for system operations that have non-obvious post-conditions. "
        "Two contracts are justified here: enterItem and makePayment."
    ))
    h3(doc, "Contract CO-01  enterItem")
    table(doc, ["Clause", "Text"], [
        ["Operation", "enterItem(medicineId, quantity)"],
        ["Cross-ref", "UC-02, SSD Figure 3"],
        ["Preconditions", "A Sale is in progress. The Pharmacist/Cashier is authenticated."],
        ["Postconditions", "If a sellable StockBatch exists: a SalesLineItem was created; it was associated with the Sale and the batch; quantity and unitPrice were set; Sale totals were updated. If none exists: no line was created and a refusal was returned."],
    ])
    h3(doc, "Contract CO-02  makePayment")
    table(doc, ["Clause", "Text"], [
        ["Operation", "makePayment(amount, method)"],
        ["Cross-ref", "UC-02"],
        ["Preconditions", "Sale is in progress; endSale has produced a total; prescription rules are satisfied."],
        ["Postconditions", "A Payment was created and associated with the Sale; Sale.status became COMPLETED; each line’s StockBatch quantity decreased; an AuditEntry was created; a receipt presentation was requested. On failure of persistence, none of the above remain."],
    ])

    h1(doc, "11. Architecture")
    add_figure(doc, D / "Architecture" / "Layered-Architecture-PoC.png",
               "Figure 8: Layered architecture", "Downward dependencies only.")
    add_figure(doc, D / "Architecture" / "Architecture-Sale-Path.png",
               "Figure 9: Sale path", "PoC collaboration.")

    h1(doc, "12. Design Class Diagrams")
    add_figure(doc, D / "Design-Class" / "DCD-Process-Sale.png",
               "Figure 10: DCD Process Sale", "Methods from SSDs.")
    add_figure(doc, D / "Design-Class" / "DCD-Overview.png",
               "Figure 11: DCD overview", "Controllers and fabrications.")

    h1(doc, "13. GRASP Analysis")
    add_figure(doc, D / "Design-Class" / "GRASP-Assignments.png",
               "Figure 12: GRASP", "Responsibility assignments.")
    table(doc, ["Responsibility", "Class", "Collaborators", "Why", "GRASP"],
          [list(r) for r in M.GRASP_ROWS])

    h1(doc, "14. Database Design")
    para(doc, (
        "Conceptual: the domain model. Logical: tables below in 3NF with controlled "
        "denormalisation of unit_price onto sale_items so historical receipts do not change "
        "when the catalogue price changes."
    ))
    h1(doc, "15. Database Schema")
    for tname, cols in M.TABLES.items():
        h3(doc, tname)
        table(doc, ["Table", "Column", "Data type", "PK", "FK", "Nullable", "Description"],
              [[tname, c[0], c[1], c[2], c[3], c[4], c[5]] for c in cols])

    h1(doc, "16. Entity Relationships")
    add_figure(doc, D / "Database" / "ERD-Logical.png",
               "Figure 13: ERD", "Logical relationships.")
    table(doc, ["From", "To", "From card.", "To card.", "Meaning"],
          [list(r) for r in M.RELATIONSHIPS])

    h1(doc, "17. Data Dictionary")
    table(doc, ["Term", "Kind", "Notes"], [
        ["Medicine", "Concept / table medicines", "Catalogue description"],
        ["StockBatch", "Concept / table stock_batches", "Expiring physical quantity"],
        ["Sale", "Concept / table sales", "IN_PROGRESS, COMPLETED, VOIDED"],
        ["SalesLineItem", "Concept / table sale_items", "Resolves Sale–Medicine"],
        ["Payment", "Concept / table payments", "One per completed sale"],
        ["User.role", "Attribute", "ADMINISTRATOR | PHARMACIST"],
        ["password_hash", "Attribute", "Never plaintext"],
        ["requires_prescription", "Attribute", "Drives attachPrescription"],
        ["Receipt", "Output", "Not a stored entity"],
        ["Customer", "External person / table customers", "No login"],
    ])

    h1(doc, "18. UI Design")
    para(doc, "Prototypes correspond to use cases, not to an invented third role.")
    for fn, cap in [
        ("UI-01-Login.png", "Login — UC-01"),
        ("UI-02-POS-Sale.png", "POS — UC-02"),
        ("UI-03-Payment.png", "Payment — UC-02"),
        ("UI-05-Prescription.png", "Prescription — UC-02 / UC-08"),
        ("UI-06-Admin-Dashboard.png", "Admin home — UC-04 alerts"),
        ("UI-07-Medicines.png", "Medicines — UC-03"),
        ("UI-08-Inventory.png", "Inventory — UC-04"),
        ("UI-09-Users.png", "Users — UC-05"),
        ("UI-10-Reports.png", "Reports — UC-07"),
    ]:
        add_figure(doc, UI / fn, f"Figure: {cap}", "See Elaboration 2 for commentary.", width=14.2)

    h1(doc, "19. Security Design")
    table(doc, ["Control", "Design"], [
        ["Authentication", "Username + salted password hash (NFR-01, users table)"],
        ["Authorisation", "Exactly two roles; checked on every privileged operation"],
        ["Password handling", "No plaintext, no reversible encryption"],
        ["Session", "Server-side or equivalent session; idle timeout"],
        ["Input validation", "Quantities ≥ 0; prices ≥ 0; required fields; unique codes"],
        ["Audit", "audit_logs for login, sale, void, stock, user admin"],
        ["Sensitive data", "Customer and prescription fields only on staff screens"],
        ["Database", "Least-privilege DB account in construction; no shared admin password in source"],
        ["Transport", "HTTPS if the construction choice is a web client"],
    ])

    h1(doc, "20. Performance Considerations")
    para(doc, (
        "NFR-02 asks for about three seconds to accept a line and refresh the total on the "
        "intended workstation. The design supports that by: searching on indexed product_code "
        "and name; choosing one sellable batch rather than scanning history in the UI; and "
        "keeping the sale in memory until completeSale. Measurements belong to Transition — "
        "none are invented here."
    ))

    h1(doc, "21. Integration Considerations")
    para(doc, (
        "Receipt output is isolated (ReceiptService). PaymentMethod isolates tender types. "
        "No NHIMA, no e-commerce, no live gateway. Those seams are how Protected Variations "
        "is applied without fake integrations."
    ))

    h1(doc, "22. Traceability Matrix")
    add_figure(doc, D / "UP-Planning" / "Traceability-Chain.png",
               "Figure 14: Traceability chain", "Used to build the matrix.")
    rows = []
    for uc in M.USE_CASES:
        rows.append([
            ", ".join(uc["frs"]),
            uc["id"],
            "Main + extensions",
            "SSD " + uc["id"] if uc["id"] in ("UC-01", "UC-02", "UC-03", "UC-04", "UC-09") else "Events in description",
            "See domain / DCD",
            next((f[0] for f in M.FEATURES if f[2].startswith(uc["id"])), "—"),
            next((t[0] for t in M.TEST_CASES_TRACE if t[1] == uc["id"]), "—"),
        ])
    table(doc, ["FR", "Use case", "Scenario", "SSD / events", "Design / data", "Feature", "Test"], rows)

    h2(doc, "22.1 Objectives to requirements")
    table(doc, ["Objective", "Requirements"], [
        ["BO-01", "FR-05, FR-08, FR-11"],
        ["BO-02", "FR-03, FR-07, FR-08"],
        ["BO-03", "FR-08, FR-10, FR-11, FR-17"],
        ["BO-04", "FR-06, FR-16"],
        ["BO-05", "FR-09 to FR-15, FR-18"],
        ["BO-06", "FR-17, FR-19"],
        ["BO-07", "Iteration plan (process requirement)"],
    ])

    h1(doc, "23. Design Decisions")
    para(doc, "See Elaboration 1 AD-01 to AD-07. Additional decisions:")
    table(doc, ["ID", "Decision", "Rationale"], [
        ["AD-08", "Copy unit_price onto sale_items", "Historical receipts stay stable"],
        ["AD-09", "Soft-deactivate users and medicines", "Old sales remain explainable"],
        ["AD-10", "One payment per completed sale", "Matches the counter workflow; splits can wait"],
        ["AD-11", "Void keeps the sale row", "Audit over convenience"],
    ])

    h1(doc, "24. Risks and Mitigations")
    table(doc, ["ID", "Risk", "P", "I", "Priority", "Mitigation", "Iteration", "Status"],
          [list(r) for r in M.RISKS_ELAB2])

    h1(doc, "25. Assumptions")
    table(doc, ["ID", "Assumption", "Reason", "Impact if incorrect", "Status"],
          [list(a) for a in M.ASSUMPTIONS])

    refs(doc)
    path = ROOT / "Documentation" / "04-Complete-System-Design" / "Pharmacy-POS-Complete-System-Design.docx"
    doc.save(path)
    return path


def compliance():
    doc = new_document("Pharmacy POS  ·  Marking Compliance Matrix", "Project control")
    cover(doc, "CSC 4630  ·  Group 20", "Marking Guide Compliance Matrix",
          "Every official criterion mapped to an artefact", META)
    toc(doc)
    h1(doc, "1. Purpose")
    para(doc, (
        "The lecturer’s marking guide, not this prompt, determines marks. This matrix lists "
        "every published criterion. Construction and Transition product evidence is planned, "
        "not fabricated."
    ))
    h1(doc, "2. Master matrix")
    table(doc, ["Requirement", "Marks", "Deliverable", "UP Phase", "Week", "Document", "Status"], [
        ["Vision document (objectives, scope)", "3", "Vision, scope, objectives", "Inception", "1–2", "Inception Report §§4–6", "Complete (docs)"],
        ["10% use cases (high-level)", "3", "UC-02 brief + Figure 1", "Inception", "1–2", "Inception Report §10–11", "Complete (docs)"],
        ["Risk list & iteration plan (UP justified)", "4", "Risk register + 15-week plan", "Inception", "1–2", "Inception Report §12, 15–16", "Complete (docs)"],
        ["Inception total", "10", "Vision & feasibility milestone", "Inception", "1–2", "01-Inception", "Complete (docs)"],
        ["30% use cases detailed, with SSDs", "6", "UC-01/02/03 + SSDs", "Elaboration 1", "3–5", "Elab 1 Report §§3–6", "Complete (docs)"],
        ["Domain model (UML class diagram)", "5", "Conceptual domain model", "Elaboration 1", "3–5", "Elab 1 Report §§7–8", "Complete (docs)"],
        ["Architectural proof-of-concept", "5", "Layers + sale path", "Elaboration 1", "3–5", "Elab 1 Report §§9–11", "Complete (docs)"],
        ["Updated risk list", "4", "Elab 1 register", "Elaboration 1", "3–5", "Elab 1 Report §§13–14", "Complete (docs)"],
        ["Elaboration 1 total", "20", "Core architecture & requirements", "Elaboration 1", "3–5", "02-Elaboration-Iteration-1", "Complete (docs)"],
        ["Remaining use cases (70%)", "5", "UC-04–UC-10", "Elaboration 2", "6–8", "Elab 2 Report §§3–4", "Complete (docs)"],
        ["Design class diagrams (refined with methods)", "5", "DCD + responsibilities", "Elaboration 2", "6–8", "Elab 2 Report §§7–9", "Complete (docs)"],
        ["UI prototype (if applicable)", "3", "Ten screens", "Elaboration 2", "6–8", "Elab 2 Report §10; UI-Prototypes/", "Complete (docs)"],
        ["Risk mitigation progress", "2", "Progress table", "Elaboration 2", "6–8", "Elab 2 Report §§13–14", "Complete (docs)"],
        ["Elaboration 2 total", "15", "Risk-driven design", "Elaboration 2", "6–8", "03-Elaboration-Iteration-2", "Complete (docs)"],
        ["Prioritised features implemented", "10", "Feature list + later code", "Construction 3–4", "9–12", "Construction Report §§3–7", "Implemented in apoza/"],
        ["Test cases (unit + integration)", "10", "UT/IT catalogues", "Construction 3–4", "9–12", "Construction Report §§8–12", "21/21 pytest passed"],
        ["Version control & CI adherence", "5", "Git/CI strategy", "Construction 3–4", "9–12", "Construction Report §§13–15", "Git repo + CI strategy documented"],
        ["Defect tracking log", "5", "Log template", "Construction 3–4", "9–12", "Construction Report §§16–17", "Template ready; populate during construction"],
        ["Construction total", "30", "Feature implementation", "Construction", "9–12", "05-Construction-Testing", "Documentation ready"],
        ["Beta testing report (user feedback)", "5", "Beta plan + later results", "Transition 5", "13–14", "Transition Report §§2–7", "Plan only"],
        ["Performance/security fixes", "5", "Test plans + later fixes", "Transition 5", "13–14", "Transition Report §§8–11", "Plan only"],
        ["Final documentation (models, user manual)", "5", "Manual + updated models", "Transition 5", "13–14", "User Manual; Transition §12–15", "Manual drafted from design"],
        ["Transition total", "15", "Polishing & deployment prep", "Transition", "13–14", "06 + 07", "Documentation ready"],
        ["Live demo (key scenarios shown)", "5", "Demo plan", "Week 15", "15", "Presentation; Final Report", "Plan only"],
        ["Final report (UP reflection, lessons)", "3", "Final report", "Week 15", "15", "08-Final-Report", "Written for design phase; construction reflection pending"],
        ["Code repository (Git) & completeness", "2", "Repository contents", "Week 15", "15", "Pharmacy-POS/ + apoza/", "Code and docs present"],
        ["Demo & submission total", "10", "Demo & final submission", "Transition", "15", "08 + Presentation", "Documentation ready"],
        ["Late submission penalty", "−10%/week", "N/A", "—", "—", "Process", "Not applied"],
        ["Plagiarism", "Zero tolerance", "Original pharmacy adaptation of Larman", "All", "All", "All docs", "Larman cited; NextGen not copied blindly"],
        ["Bonus (optional, up to 5%)", "up to 5", "GoF / CI-CD / UX", "Later", "Later", "Not claimed yet", "PaymentMethod seam may later support a GoF Strategy bonus — not claimed as done"],
    ])
    h1(doc, "3. Notes")
    para(doc, (
        "Status “Complete (docs)” means the marking artefact exists as analysis/design. "
        "It does not mean software was written. Claiming implemented features or measured "
        "beta results would violate the no-fake-results rule."
    ))
    refs(doc)
    path = ROOT / "Documentation" / "00-Project-Control" / "Marking-Guide-Compliance-Matrix.docx"
    doc.save(path)
    return path


def main():
    paths = [inception(), elab1(), elab2(), system_design(), compliance()]
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
