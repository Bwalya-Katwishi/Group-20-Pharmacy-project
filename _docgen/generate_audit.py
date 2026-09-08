from word_theme import ROOT, new_document, cover, toc, h1, h2, para, bullet, table, refs
import model as M

doc = new_document("Pharmacy POS  ·  Design Audit", "Consistency and compliance")
cover(doc, "CSC 4630  ·  Group 20", "Design Consistency and Compliance Audit",
      "Marking guide, Larman method, UML, and traceability", [
          M.COURSE, M.GROUP, M.DATE, "Performed on the documentation pack before implementation",
      ])
toc(doc)

h1(doc, "1. Marking-guide audit")
para(doc, "Every published criterion in the CSC 4630 marking guide appears in Documentation/00-Project-Control/Marking-Guide-Compliance-Matrix.docx. Summary:")
table(doc, ["Block", "Marks", "Documentation verdict"], [
    ["Inception", "10", "Vision, 10% UC-02, risks, feasibility, UP-mapped plan present"],
    ["Elaboration 1", "20", "30% use cases + SSDs, domain model, layered PoC, updated risks present"],
    ["Elaboration 2", "15", "70% use cases, DCDs with methods, UI prototypes, risk-mitigation table present"],
    ["Construction", "30", "Feature order, UT/IT catalogues, Git/CI, defect template — results not faked"],
    ["Transition", "15", "Beta/performance/security plans and user manual — measurements not faked"],
    ["Demo & final", "10", "35-slide presentation, final report, reflection, demo scenarios — live demo pending code"],
])

h1(doc, "2. Larman methodology audit")
bullet(doc, "UP is iterative. Inception is not a requirements freeze.")
bullet(doc, "Use cases are user goals. enterItem is intent-level; scan is a technology variation.")
bullet(doc, "SSDs show actor → :System only.")
bullet(doc, "Domain model has attributes and associations, not methods.")
bullet(doc, "DCDs add methods after responsibilities / GRASP.")
bullet(doc, "NextGen POS was adapted: StockBatch and Prescription added; Register omitted.")
bullet(doc, "Page numbers from the 3rd edition are not invented. Chapter extracts (9, 11, 16) are cited.")
para(doc, "The full Larman book file was not available as one PDF. Course chapter extracts in References/ were read instead of fabricating a complete-book reading.")

h1(doc, "3. UML consistency audit")
table(doc, ["Check", "Result"], [
    ["Use-case actors", "Two system users plus Customer and Supplier as external"],
    ["No separate Cashier", "Pass — stated on diagrams, UI, schema, manual"],
    ["SSD events vs UC-02 text", "Pass — makeNewSale, enterItem, attachPrescription, endSale, makePayment"],
    ["Domain vs DCD", "Pass — DCD adds controllers, repositories, methods"],
    ["Domain vs ERD", "Pass — each persistent concept has a table; Receipt is output-only"],
    ["UI vs use cases", "Pass — no Manager screen; admin vs pharmacist shells differ"],
])

h1(doc, "4. Traceability audit (Process Sale thread)")
para(doc, "BO-01 / BO-02 → FR-03–FR-08 → UC-02 → SC-01–SC-03 → enterItem / makePayment → StockBatch, Sale, Payment → SaleController / Sale / StockBatch → sales, sale_items, payments, stock_batches → F-02–F-07 → UT-04, UT-08, IT-01, TC-04–TC-10 → demo SC-01–SC-03.")
add = True
para(doc, "Same identifiers are used in every Word document and in the presentation.")

h1(doc, "5. Two-role audit")
para(doc, "Administrator and Pharmacist/Cashier only. users.role allows two values. UI-09 shows only those roles. Earlier briefing slides that said Cashier or Manager were treated as incorrect and corrected.")

h1(doc, "6. Honesty audit")
para(doc, "No test results, beta quotes, performance numbers, defect counts, or deployment outcomes were invented. Construction and Transition use the required placeholder sentences.")

h1(doc, "7. Implementation audit")
para(doc, "No frontend, backend, API, or SQL implementation scripts were generated. schema-columns.csv is a design table, not executable SQL. _docgen/ is a documentation generator, not the Pharmacy POS application.")

h1(doc, "8. Remaining human tasks before submission")
bullet(doc, "Replace [University Name], [Lecturer Name], and Appendix C member names.")
bullet(doc, "In Word, right-click each table of contents and Update Field.")
bullet(doc, "Do not start coding until the instruction START IMPLEMENTATION.")
refs(doc)
path = ROOT / "Documentation" / "00-Project-Control" / "Design-Consistency-Audit.docx"
doc.save(path)
print(path)
