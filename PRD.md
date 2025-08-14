# Product Requirements Document (PRD)
**Project Name:** Generatore carte Dobble con preview e PDF  
**Owner:** Solo build (you)  
**Date:** 2025-08-14  

---

## 1) Problem Statement
Creating custom Dobble (Spot It!) cards manually is time-consuming and error-prone. Users need an easy tool to generate complete, valid Dobble decks, preview cards, and export them as PDFs for printing.

---

## 2) Goals & Objectives
- **Automatically generate valid Dobble decks** with correct symbol distribution.  
- **Preview cards** visually before printing.  
- **Export to PDF** with print-ready formatting.  
- **Allow custom symbols** (images or text).  
- **Provide a simple, fast web interface** for deck creation.

---

## 3) Target Users
- Board game enthusiasts who want custom Dobble decks.  
- Teachers, educators, and event organizers creating personalized games.  
- Hobbyists designing printable card games.  

---

## 4) Core Features

### MVP
1. **Deck Generator**: Create full Dobble decks with user-defined number of symbols.  
2. **Card Preview**: Show individual cards in-browser with symbols arranged visually.  
3. **PDF Export**: Generate print-ready PDFs with all cards.  
4. **Custom Symbols**: Add text or image symbols for cards.  

### Phase 2
5. **Theme Templates**: Predefined symbol sets (animals, emojis, numbers, etc.).  
6. **Drag & Drop Symbol Editor**: Customize card layouts and symbol positions.  
7. **Deck Sharing**: Save and share decks online.  

### Phase 3
8. **Randomized Variants**: Auto-generate multiple deck versions for variety.  
9. **Mobile Preview & Export**: Responsive UI and mobile-friendly PDFs.  
10. **Community Templates**: User-submitted decks or symbol sets.  

---

## 5) Non-Functional Requirements
- **Performance:** Decks generate in <2 seconds for typical sizes (31–57 cards).  
- **Reliability:** Generated decks must respect Dobble rules (1 symbol overlap per card pair).  
- **Usability:** Simple UI for desktop and tablet users.  
- **Accessibility:** Easy to use for non-technical users; intuitive controls.

---

## 6) Constraints
- Must validate decks mathematically to avoid duplicate/missing symbol pairs.  
- Image symbols must be properly scaled to fit circular card layouts.  
- PDF formatting should fit standard print sizes (A4, Letter).  

---

## 7) Tech Stack Suggestion
- **Frontend:** React + TypeScript + Tailwind for UI.  
- **Backend:** Node.js or Python (Flask/FastAPI) for deck generation and PDF creation.  
- **PDF Library:** jsPDF, PDFKit, or ReportLab.  
- **Image Handling:** Canvas API or Pillow (Python) for symbol rendering.  
- **Randomization/Algorithm:** Dobble combinatorial logic for valid deck generation.  

---

## 8) Success Metrics
- 100% of generated decks follow Dobble rules.  
- ≥80% of users successfully export PDFs without errors.  
- High user satisfaction with preview and customization features (>4/5).  
- Low page load times (<3 seconds).  

---

## 9) Roadmap

| Phase     | Duration  | Key Deliverables |
|-----------|-----------|------------------|
| **MVP**   | 3–4 weeks | Deck generator, card preview, PDF export, custom symbols |
| **Phase 2** | +4 weeks | Theme templates, drag & drop editor, deck sharing |
| **Phase 3** | +6 weeks | Randomized variants, mobile preview, community templates |

---

## 10) Risks & Mitigation
- **Deck generation errors:** Use tested combinatorial algorithms and automated validation.  
- **Performance issues with large decks:** Optimize symbol rendering and PDF generation.  
- **Complex UI for beginners:** Provide pre-configured templates and tooltips.

---

## 11) Open Questions
- Should the app allow **custom card shapes** or only standard circles?  
- How many symbols should a user be able to upload per deck?  
- Should PDFs include optional **coloring versions** for educational purposes?  

---
