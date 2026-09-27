LegalEase - Project Testing

Test 1: Generate a Freelance Work Contract
Input: Document Type = Freelance Work Contract, Parties = Jane Doe (Service Provider), TechNova Inc. (Client), Terms = Work must be delivered by May 15, 2025; Payment within 7 days; Confidentiality at all times, Date = April 15, 2025
Result: Document generated successfully with all clauses included.

Test 2: Edit the generated document
Clicked "Edit Document", modified text, applied changes with Ctrl+Enter.
Result: Edited text reflected correctly.

Test 3: Download in all formats
Downloaded as .TXT, .DOCX, .PDF
Result: All three files opened correctly. DOCX and PDF included logo, terms table and footer.

Test 4: Missing API key
Removed the API key from .env and tried to generate.
Result: App showed a clear error message instead of crashing.

Test 5: Empty required fields
Left Document Type blank and clicked Generate.
Result: App showed a warning asking to fill required fields.
