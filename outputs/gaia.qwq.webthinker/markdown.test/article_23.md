Question: How many High Energy Physics - Lattice articles listed in January 2020 on Arxiv had ps versions available?

# Analysis of PostScript Version Availability in High Energy Physics - Lattice (hep-lat) Articles Submitted to ArXiv in January 2020  

## Introduction  
ArXiv, a pioneering open-access repository for preprints in physics, mathematics, computer science, and related disciplines, has long served as a critical platform for rapid scholarly communication. Since its inception in 1991, arXiv has evolved to accommodate changing technological and academic needs, including the transition from legacy document formats like PostScript (PS) to modern standards such as Portable Document Format (PDF). While PDF became the dominant format by the 2010s due to its cross-platform compatibility and digital-first design, PS remained a supported option for backward compatibility, particularly for researchers accustomed to traditional workflows or institutions requiring specific file types.  

This study focuses on quantifying the availability of PS versions for High Energy Physics - Lattice (hep-lat) articles submitted to arXiv in January 2020. The hep-lat category, which encompasses theoretical and computational studies of lattice field theories, represents a domain historically reliant on precise mathematical and graphical representations. Understanding PS retention in this category during the early 2020s provides insights into the persistence of legacy formats in specialized academic communities. January 2020 is a particularly relevant timeframe: by this period, PDF had solidified as the primary format for arXiv submissions, yet PS was still listed as an option for many articles, reflecting a transitional phase in digital publishing practices.  

The analysis employs two complementary approaches. First, manual inspection of arXiv’s monthly archive page for hep-lat submissions in January 2020 (accessible via `https://arxiv.org/list/hep-lat/202001`) allows direct observation of format availability. Each entry on this page lists available formats (e.g., `[pdf, ps.gz, other]`), enabling a straightforward count of articles with PS versions. Second, programmatic queries via arXiv’s Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH) API provide structured metadata for all submissions in the specified timeframe and category. This method ensures comprehensive coverage, particularly for large datasets, by extracting format information from XML records containing explicit tags like `<format>application/postscript</format>`.  

Three key questions guide this investigation:  
1. **Total submissions**: What was the total number of hep-lat articles submitted to arXiv in January 2020? This baseline quantifies the scope of the dataset.  
2. **PS availability**: How many of these articles included a PS version alongside other formats? This reveals the proportion of submissions retaining legacy support.  
3. **Influencing factors**: What technical, institutional, or user-driven factors might explain the persistence of PS in this category, despite the broader shift to PDF?  

The findings contribute to a broader understanding of format transition dynamics in academic publishing. They highlight the interplay between technological evolution, researcher preferences, and institutional inertia, offering a case study for how legacy systems coexist with modern standards. Such insights are critical for repository managers and researchers aiming to balance innovation with accessibility, ensuring that evolving platforms continue to serve diverse scholarly needs.  

---

## Methodology  

The methodology employed a multi-step approach to quantify the number of High Energy Physics - Lattice (hep-lat) articles submitted to arXiv in January 2020 that included PostScript (PS) versions. This approach combined manual inspection of arXiv’s public interfaces with programmatic queries via its OAI-PMH API, ensuring robustness and accuracy.  

### **1. Manual Web Search of Monthly Archive Pages**  
The first step involved accessing arXiv’s monthly archive page for hep-lat submissions in January 2020:  
`https://arxiv.org/list/hep-lat/202001`.  

| **Step** | **Action** |  
|----------|------------|  
| **1** | Navigated to the monthly archive page to list all submissions. |  
| **2** | Counted the total number of articles displayed, with each entry representing a unique submission. |  
| **3** | Inspected the format links for each article (e.g., `[pdf, ps.gz, other]`). |  
| **4** | Tallyied articles explicitly listing PS formats (`ps.gz` or `ps`), excluding those with only `pdf` or `other` links. |  

This method leveraged arXiv’s public interface to directly observe format availability. However, it required manual effort and was limited by the page’s display capacity (e.g., pagination or truncated listings).  

---

### **2. Programmatic Query via OAI-PMH API**  
To systematically retrieve metadata, the **Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH)** was used. The API query was structured as follows:  

| **Parameter** | **Value/Description** |  
|---------------|-----------------------|  
| `verb` | `ListRecords` (to fetch records). |  
| `from` | `2020-01-01` (start date). |  
| `until` | `2020-01-31` (end date). |  
| `set` | `hep-lat` (category filter). |  
| `metadataPrefix` | `arXivRaw` (to access detailed format metadata). |  

The endpoint URL was:  