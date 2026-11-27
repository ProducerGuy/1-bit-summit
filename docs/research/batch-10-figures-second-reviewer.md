# Independent patent drawing retrieval audit

US 2026/0220467 A1 | WO 2026/161822 A1 | 26 November 2026

## 1. Result and provenance

**[Read in text]** The [US application transcription](https://patents.justia.com/patent/20260220467) identifies California Institute of Technology, Babak Hassibi, Ali Sahin Lale and Gustav Naucler, application 19/460,181, filing 26 January 2026, publication 30 July 2026 and priority to US provisional 63/749,353 (24 January 2025). The [PCT listing](https://patent-i.com/report/wo_en/applicant/0000486/) independently identifies WO 2026/161822, the same title, inventors and dates. These are public transcriptions/indexes of the application, not official page images.

**[Seen in an image]** I located and visually inspected the original research plots of the 11-million-parameter experiment described in the patent's discussion of Figures 6A–6B. They appear in the 2019 Azizan, Lale and Hassibi preprint, *Stochastic Mirror Descent on Overparameterized Nonlinear Models: Convergence, Implicit Regularization, and Generalization*, and in the later author-hosted journal manuscript. The standalone PNG URLs below opened and displayed the images. This is substantially more evidence than a figure caption alone.

**[Inferred]** The distinctive experimental description, sample size, potential choices and narrative make these very strong candidates for the underlying plots of Figures 6A–6B. I estimate 95% confidence in the same underlying experiment, and 80% confidence that at least one of the plots inspected is reproduced or adapted in the patent's drawings. These are subjective provenance assessments, not measured probabilities. I cannot assign an individual plot to 6A or 6B or certify pixel identity without seeing those patent sheets.

**[Read in text / retrieval result]** No official US or PCT drawing sheet was successfully retrieved or viewed. Figures 7A and 7B, the highest-priority LLM plots, remain unseen. No authenticated alternative copy of either was found. No official typeset description page containing equations 26–31 was obtained. The equations below are explicitly provisional readings of the Justia website's mathematical rendering. The proposed 16-sheet total remains unverified. No source was opened from the project's repository; no model was loaded, evaluated or trained; no account or credentials were used.

**[Retrieval result]** The standalone research PNGs and PDF pages were viewable in the web reader, but file-download attempts for the overlay PNG, the l10 PNG, the arXiv PDF and the author-hosted PDF failed. Accordingly this document supplies the exact verified image URLs, rather than falsely attaching reconstructed or unverified images. No local image file is claimed. The Markdown image links reference the actual source images remotely.

## 2. Highest priority: Figures 7A and 7B

**[Read in text]** Source: https://patents.justia.com/patent/20260220467 , sections II, compression, quantization-directed q-norm applications, immediately following equation 18. The patent describes 7A as a distribution for one layer of a conventionally trained LLM, centered at approximately zero; 7B is described as a distribution for an LLM layer trained using the proposed methods, with modes near −0.3 and +0.3. The description places these figures in the large-q discussion, before the rigid cage section. It does not establish from these passages that they are produced using the rigid cage specifically.

| Requested figure | Actual patent picture seen? | Source file obtained? | What is known |
|---|---|---|---|
| 7A | No | No | [Read in text] Conventional LLM layer distribution, unimodal near zero. No visual confirmation of axes, units, tick spacing, vertical frequency, model or layer identity. |
| 7B | No | No | [Read in text] LLM layer described as bimodal, near ±0.3. No visual confirmation of peak locations, spread, population, labels, scale or model. |

**[Inferred]** The brief's description of a before/after experiment goes beyond what the accessible text securely establishes. A conventional training result and a proposed-method result are not necessarily a matched checkpoint pair, the same exact layer, or the same initialization. No claim of identical model, layer, data, training or preserved scores follows until those details are obtained. Do not identify either as Qwen, a transformer of any particular size, or an actual strict one-bit deployed model based solely on the prose. Do not confuse these signed distributions around ±0.3 with the unsigned magnitude plots in Section 3 below, whose axes extend only to 0.05.

## 3. Figures 6A and 6B: strong alternative-source recovery

### 3A. Source chain and identification

**[Read in text]** The patent's discussion reports an 11 × 10^6-dimensional weight vector interpolating the training data for each histogram, with a common initialization and differing stochastic mirror descent potentials. It specifically references the l10 histogram in 6A, and describes its mass moving away from zero. [Patent text](https://patents.justia.com/patent/20260220467).

**[Read in text]** The 2019 preprint, [arXiv:1906.03830v1](https://arxiv.org/html/1906.03830v1), section 5.2 and Appendix B.3, describes exactly this experiment. Appendix B.2 identifies the network as ResNet-18 on CIFAR-10 (50,000 training examples). It is a vision classification experiment, not a language model. The four potentials are l1, l2 (SGD), l3 and l10. The authors report interpolation of the same data. The manuscript's printed page 11, Figure 6, and printed page 34, Figure 12, supply the pictures. The later journal version by the same authors, [author-hosted PDF](https://azizan.mit.edu/papers/SMD_deep.pdf), also contains the same four-panel Figure 2 and Appendix Figure 12. I visually inspected its printed page 23, Figure 12, which agrees with the preprint's plots. The [Caltech doctoral thesis](https://thesis.library.caltech.edu/14001/3/Navid_Azizan_2020_Thesis.pdf), Figures 9.2 and 9.12, provides another text-identified copy; I did not inspect those thesis figure pages themselves.

**[Inferred]** The coincidence is unusually specific: not merely a histogram of neural-network weights, but exactly 11 million dimensions, exact interpolation, common initialization, a comparison of SMD potentials, and the distinctive l10 shift. The prior paper is coauthored by two of the patent inventors. Nonetheless, the patent's labels 6A and 6B cannot be mapped to these individual figures until the patent drawings are seen. This is a recovered candidate source, not recovery of the original patent sheet.

### 3B. Image inventory and visual measurements

**[Seen in an image]** All six standalone PNGs below were actually displayed via the arXiv HTML article's linked images. The standalone plots have axis and legend labels but no printed figure number; the figure numbers are established by the surrounding PDF page. I separately inspected the PDF page images of Figures 6, 11 and 12 to confirm the mapping. The standalone links are the original authors' image files, not a redraw or an AI-generated illustration. No model name, dataset or parameter count is printed inside the plot axes. Those facts are supplied by the paper text and captions.

**[Seen in an image]** Shared horizontal axis: `Absolute Value of Weights`, from 0.00 to 0.05, labeled ticks every 0.01. Vertical axis: `Frequency`. These are counts per bin, not normalized density, percentage or signed weight. No independent plot title appears above the axes. The estimates below are approximate visual readings; no integration of raw counts was possible.

| Paper figure and panel | Direct image | Legend/color | Vertical ticks | Visual distribution and approximate peak |
|---|---|---|---|---|
| Figure 6 and 12(e) | [comparison.png](https://arxiv.org/html/1906.03830v1/comparison.png) | l1-norm grey; l2-norm blue; l3-norm red; l10-norm green | 0 to 300,000, every 50,000 | Overlay: grey/blue concentrated near zero, red peak near 0.006, green strongest spike near 0.0243. Green and other curves overlap substantially. |
| Figure 12(a) | [l1.png](https://arxiv.org/html/1906.03830v1/l1.png) | l1-norm, grey | 0 to 300,000, every 50,000 | Irregular high near-zero bins; largest spike around 0.0023, about 290,000. Much mass below 0.015; diminishing tail through about 0.03. |
| Figure 12(b) | [l2.png](https://arxiv.org/html/1906.03830v1/l2.png) | l2-norm, blue | 0 to 180,000, every 20,000 | Maximum near zero, about 169,000; smoothly declining envelope, around 35,000 near 0.018 and a small tail beyond 0.03. |
| Figure 12(c) | [l3.png](https://arxiv.org/html/1906.03830v1/l3.png) | l3-norm, red | 0 to 180,000, every 20,000 | Peak near 0.006, about 160,000; notable near-zero mass and right tail to 0.05. |
| Figure 12(d) | [l10.png](https://arxiv.org/html/1906.03830v1/l10.png) | l10-norm, green | 0 to 300,000, every 50,000 | Near-zero bins small; rise around 0.006–0.01; shoulder near 0.011 (~48,000), broad main concentration about 0.018–0.03, tallest narrow bin ~0.0243 and ~288,000. Secondary bumps around 0.033–0.035 (~40,000–50,000). Tail nearly vanishes around 0.04–0.043. |
| Figure 11 (initialization; not a final-weight histogram) | [Initial.png](https://arxiv.org/html/1906.03830v1/Initial.png) | Initial, magenta | 0 to 200,000, every 50,000 | Peak near zero, about 178,000; monotonically declining envelope to near zero around 0.033. |

**[Seen in an image]** The overlay plot and the individual l10 panel are especially useful. They are embedded here by reference to the original online images. If the Markdown viewer does not load remote images, use the source links above or view the PDF's printed pages 11 and 34 directly.

![Original overlay of four potentials (paper Fig. 6 / Fig. 12e; candidate patent source, not an authenticated patent sheet)](https://arxiv.org/html/1906.03830v1/comparison.png)

![Original l10 panel (paper Fig. 12d; candidate patent source)](https://arxiv.org/html/1906.03830v1/l10.png)

**[Computed, approximate]** The peak estimate in the l10 PNG can be checked with a linear interpolation on the displayed 580×377 image: the horizontal plot spans roughly x=90 to 555 pixels for 0 to 0.05; the tallest spike at x≈316 gives 0.05(316−90)/(555−90)≈0.0243. The vertical plot spans y≈327 to 16 for 0 to 300,000; spike top y≈28 gives 300,000(327−28)/(327−16)≈288,000. This is a graphical estimate, not an exact count retrieved from data. The l1 maximum is similarly at x≈111, giving 0.0023, with y≈25 giving about 291,000. The l3 maximum at x≈146 gives 0.0060; y≈48 gives roughly 161,000 on its 180,000 vertical scale. These estimates are reproducible from the visible originals and are not measurements of patent Figures 6A or 6B themselves.

### 3C. What the candidate pictures add

**[Seen in an image]** The l10 distribution is unmistakably shifted away from zero, but spread across many magnitude bins. There is a prominent thin spike on a broad distribution. It is not a single spike, and neither the signs nor the within-group spread can be seen. The figure does not show a binary checkpoint, two signed peaks or a measured retention score. The two low-power distributions and the initial histogram have very different shapes from l10.

**[Inferred]** Eliminating small weights is not sufficient to establish exact equal-magnitude binarization. The observed green distribution could be consistent with mixtures of groups each having their own scale, but the plot does not identify any groups, so neither equality within groups nor its failure can be inferred from the pooled histogram alone. A quantization method using per-group scales needs separate groupwise evidence. These plots also do not establish post-quantization accuracy or conversion of an existing pretrained language model. This is the most important scientific distinction revealed by the alternative-source recovery.

## 4. Complete patent figure and sheet inventory

**[Read in text]** All descriptions in this table are from the patent's `BRIEF DESCRIPTION OF THE DRAWINGS` at https://patents.justia.com/patent/20260220467 . They are paraphrased and are not visual readings. No exact printed drawing-sheet-to-figure mapping was found; sheet numbers must not be assigned by guessing from figure order.

| Patent figure | Patent image | Alternative figure | Text-only identification |
|---|---|---|---|
| 1 | Not seen | None found | Network model for responding to queries |
| 2 | Not seen | None found | Model-training process |
| 3A | Not seen | None found | Quantization process, original weights |
| 3B | Not seen | None found | Quantization process, concentration of weights |
| 3C | Not seen | None found | Quantization process, binary representation |
| 4A | Not seen | None found | Pruning process |
| 4B | Not seen | None found | Pruning process |
| 5 | Not seen | None found | Training-concurrent compression with mirror descent |
| 6A | Not seen | Strong candidate experiment, see Section 3 | Final absolute-weight histograms; l10 explicitly referenced |
| 6B | Not seen | Strong candidate experiment, see Section 3 | Final absolute-weight histograms; precise panel assignment unknown |
| 7A | Not seen | None found | Conventional LLM layer histogram |
| 7B | Not seen | None found | Proposed-method LLM layer histogram |
| 8 | Not seen | None found | Training system |
| 9 | Not seen | None found | Training element |
| 10 | Not seen | None found | Training application |

**[Inferred]** The caption list comprises 15 distinct figure labels. This does not establish 15 sheets: one figure can occupy multiple sheets, multiple figures can occupy one sheet, and a front-page representative drawing may repeat a figure. The brief's 16 sheets are plausible but not independently verified. Per requested sheet, the honest status is:

| Sheet number (as proposed in brief) | Image seen | Figure mapping | File |
|---|---|---|---|
| 1 | No | Unknown | None |
| 2 | No | Unknown | None |
| 3 | No | Unknown | None |
| 4 | No | Unknown | None |
| 5 | No | Unknown | None |
| 6 | No | Unknown | None |
| 7 | No | Unknown | None |
| 8 | No | Unknown | None |
| 9 | No | Unknown | None |
| 10 | No | Unknown | None |
| 11 | No | Unknown | None |
| 12 | No | Unknown | None |
| 13 | No | Unknown | None |
| 14 | No | Unknown | None |
| 15 | No | Unknown | None |
| 16 | No | Unknown | None |

**[Inferred]** No visual axis, legend, symbol or model detail is asserted for any unseen patent figure. The actual official sheet header, publication number and `Sheet x of y` labels must be checked against the eventual image file.

## 5. Equations 26–31: website-rendered fallback, not an official transcription

**[Read in text]** Source: https://patents.justia.com/patent/20260220467 , sections `1. Rigid Cage Quantization` and `2. Kurtosis Quantization`. The website's MathML/LaTeX-like rendering was read. The following normalizes its typographical notation into readable mathematical markup while deliberately preserving the suspicious terms. None of the six equations or the subsequent sentence was seen on an official patent page image. Thus the requested exact typeset transcription is not fulfilled. In particular the later three equations are in the kurtosis section, not the rigid cage section.

### 5A. Rigid cage

**[Read in text; website rendering]** Equation (26):

$$\psi(w)=\|w\|_\infty+\frac{\epsilon}{2}\|w\|^2=\max_{i=1,\dots,p}|w|_i+\frac{\epsilon}{2}\sum_{i=1}^p w_i^2.$$

**[Read in text; website rendering]** Equation (27):

$$\nabla\psi=s+\epsilon w,\quad\text{where }\|s\|_1=1\text{ and }s_i=0,\text{ if }|w_i|<\|w\|_\infty.$$

**[Read in text; website rendering]** The inverse-mapping steps, in mathematical form (prose summarized):

1. Sort the magnitudes of x in descending order: $|x_{i_1}|\ge |x_{i_2}|\ge\cdots,|x_{i_p}|$.
2. Select the largest k satisfying $\sum_{j=1}^k|x_{i_j}|>k|x_{i_{k+1}}|+1$.
3. Set $\alpha=(\sum_{j=1}^k|x_{i_j}|-1)/k$.

**[Read in text; website rendering]** Equation (28):

$$[\nabla^{-1}\psi(x)]_{i_j}=\begin{cases}\frac{\alpha}{\epsilon}\cdot\operatorname{sign}(x_{i_j})&j=1,\dots,k\\x_{i_j}&j=k+1,\dots,p.\end{cases}$$

**[Read in text]** The second branch is displayed as $x_{i_j}$, not $x_{i_j}/\epsilon$. The sorting rule as rendered refers to $x_{i_{k+1}}$ without specifying what happens when $k=p$. No all-zero inverse branch is displayed in the three steps. None of these can be ascribed definitively to the original published patent rather than transcription errors.

### 5B. Kurtosis quantization

**[Read in text; website rendering]** Equation (29):

$$\ell_{kur}(w)=\sum_{i=1}^k\sum_{j=1}^{p_i}\left(|w_j^{(i)}|^4-\left(\frac{1}{p_i}\sum_{j=1}^{p_i}|w_j^{(i)}|\right)^4\right)^2.$$

The text defines $p_i$ as the number of weights in layer i and $\sum_{i=1}^k p_i=p$.

**[Read in text; website rendering]** Equation (30), preserving the displayed trailing comma in the argument of f:

$$\ell(f(x,w,),y)+\delta\ell_{kur}(w).$$

**[Read in text; website rendering]** The sentence following (30) specifies a small positive $\delta$.

**[Read in text; website rendering]** Equation (31), preserving the indexed norm and the final magnitude multiplier rather than silently correcting them:

$$[\nabla\ell_{kur}(w)]_j^{(i)}=8\left(|w_j^{(i)}|^4-\left(\frac{1}{p_i}\|w_j^{(i)}\|_1\right)^4\right)\cdot\left(|w_j^{(i)}|^3-\frac{1}{p_i^4}\cdot\|w_j^{(i)}\|_1^3\cdot|w_j^{(i)}|\right)\operatorname{sign}(w_j^{(i)}).$$

**[Read in text; website rendering]** The sentence after (31) says that the gradient, with a positive weighting denoted by beta, may be added to the ordinary loss gradient used in equations (9), (10), (14) and/or (15). The following sentence permits the one-step or two-step update. This is a paraphrase, not a faithful typeset transcription. The apparent delta/beta notation discrepancy is preserved as a question for the official page. The exact sentence and its original typography remain outstanding.

### 5C. Independent checks identifying why the original page matters

**[Computed]** A mathematically correct inverse of the potential in (26), for epsilon > 0, can be computed by maximizing $x^T w-\|w\|_\infty-\epsilon\|w\|^2/2$. Introduce $t=\|w\|_\infty$. For fixed t, the maximizing coordinate is

$$w_i=\operatorname{sign}(x_i)\min(|x_i|/\epsilon,t).$$

If $\|x\|_1\le1$, the maximizer is zero, because zero satisfies $x\in\partial\|0\|_\infty$, the unit l1 ball. Otherwise write $\alpha=\epsilon t>0$. Differentiating the optimized objective with respect to the active cap t gives

$$\sum_i(|x_i|-\alpha)_+=1.$$

For the k active magnitudes above alpha this implies $\alpha=(\sum_{j=1}^k|x_{i_j}|-1)/k$. The inverse in the unclipped branch is $x_i/\epsilon$, not $x_i$. An illustrative two-coordinate example is $x=(2,0.2)$ and $\epsilon=0.1$: alpha=1, and the correct inverse is $(10,2)$. The rendered second branch instead yields $(10,0.2)$, whose second coordinate fails $x_2=\epsilon w_2$ since it gives 0.02 rather than 0.2. This is a mathematical discrepancy in the website rendering, not proof of an error in the official publication.

**[Computed]** A further boundary issue in (27): for nonzero w the l1 subgradient of the infinity norm has unit l1 norm on the maximizers with matching signs; at w=0 the full subdifferential is the closed unit l1 ball. The official text should be checked for whether that qualification appears elsewhere.

**[Computed]** Equation (29) also permits an independent differentiation check. For one layer let $a_j=|w_j|$, $m=p_i^{-1}\sum_j a_j$, $d_j=a_j^4-m^4$ and $K=\sum_jd_j^2$. For nonzero weights, $\partial m/\partial w_l=\operatorname{sign}(w_l)/p_i$. Consequently

$$\partial K/\partial w_l=8\operatorname{sign}(w_l)\left[a_l^3d_l-\frac{m^3}{p_i}\sum_jd_j\right].$$

The dependence on the shared mean creates a sum over all coordinates. The displayed equation (31) lacks that explicit cross-coordinate sum and uses the suspicious indexed norm. This again makes the typeset page a priority. These checks do not replace the requested transcription or demonstrate that an inventor wrote an erroneous formula.

## 6. Retrieval ledger: failed, incomplete and successful routes

**[Read in text / retrieval result]** The following ledger gives exact attempted addresses and observed outcomes. An inaccessible response is not proof of a non-existent record, and a blocked web reader is not proof a normal public browser cannot retrieve it. No login, key, access form or payment was used. No attempt was made to bypass authentication or access private records.

| Route | Exact URL / query | Observed result |
|---|---|---|
| USPTO direct official PDF | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20260220467 | Web reader inaccessible; container HTTP request failed DNS resolution; separate download tool rejected the URL because no successful view was registered. No PDF. |
| Alternative USPTO domain | https://ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20260220467 | Web reader inaccessible. |
| USPTO Basic search | https://ppubs.uspto.gov/basic/ | Public instructions/search interface indexed; no submitted interactive query or retrieved target document. |
| USPTO external query candidate | https://ppubs.uspto.gov/pubwebapp/external.html?q=20260220467 | Inaccessible; this candidate permalink not established. |
| USPTO historical PDF viewer candidate | https://pdfaiw.uspto.gov/.aiw?docid=20260220467 | Inaccessible. Historical endpoint, not verified as operational. |
| Patent Center application | https://patentcenter.uspto.gov/applications/19460181 | Inaccessible. |
| Patent Center document wrapper | https://patentcenter.uspto.gov/applications/19460181/ifw/docs | Inaccessible. Prosecution drawings not obtained. |
| Open Data Portal candidate detail URL | https://data.uspto.gov/patent-file-wrapper/search/details/19460181 | Inaccessible. No API key requested or used. |
| Official bulk PDF dataset | https://data.uspto.gov/bulkdata/datasets/appmp2 | HTML page with zero readable lines in this reader; archive member not retrieved. Dataset's existence verified through https://catalog.data.gov/dataset/patent-application-multi-page-pdf-images-2001-present?from_hint=eyJxIjoiYXBwbGljYXRpb24ifQ%3D%3D . |
| Legacy USPTO bulk archive candidate | https://bulkdata.uspto.gov/data/patent/application/redbook/2026/ | Inaccessible. |
| Google historical bulk files | https://www.google.com/googlebooks/uspto-patents-applications-text-with-embedded-images.html | Successfully read, but archive explicitly discontinued in 2015; not a 2026 source. |
| Google Patents US | https://patents.google.com/patent/US20260220467A1/en ; https://patents.google.com/patent/US20260220467A1 ; https://patents.google.com/patent/US20260220467 ; https://patents.google.com/patent/US20260220467A1/en?oq=US20260220467A1 | All inaccessible. No Google storage PDF hash or drawing asset URL obtained. |
| Google Patents WO | https://patents.google.com/patent/WO2026161822A1/en ; https://patents.google.com/patent/WO2026161822A1 ; https://patents.google.com/patent/WO2026161822 | All inaccessible. |
| Google-hosted patent image search | Exact publication identifiers, `site:patentimages.storage.googleapis.com`, plus PDF searches | No matching file located. Do not guess hashed image-storage paths. |
| WIPO PATENTSCOPE | https://patentscope.wipo.int/search/en/WO2026161822 ; https://patentscope.wipo.int/search/en/detail.jsf?docId=WO2026161822 | HTTP 403 on both. Second URL's document-ID syntax is also unverified for this record. |
| Espacenet | https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026161822A1 | Inaccessible. |
| EPO Register candidate | https://register.epo.org/application?number=WOUS26012584 | Inaccessible; no verified EP regional entry. |
| EPO OPS image endpoint | https://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/WO2026161822/images | Inaccessible; no credential attempted. |
| EPO publication-server candidates | https://data.epo.org/publication-server/rest/v1.0/publication-dates/20260730/patents/WO2026161822NWA1/document.html ; https://data.epo.org/publication-server/rest/v1.0/publication-dates/20260730/patents/WO2026161822NWA1/document.pdf | Both inaccessible; endpoint may not support this WO document type. |
| Justia | https://patents.justia.com/patent/20260220467 | Successful for description, captions, re-rendered equations and publication metadata; no drawing images exposed in retrieved record. |
| FreePatentsOnline | https://www.freepatentsonline.com/20260220467.pdf ; https://www.freepatentsonline.com/20260220467.html | Inaccessible. |
| PAT2PDF | https://www.pat2pdf.org/pat2pdf/foo.pl?number=20260220467 | Inaccessible. Its public home page documents the lookup syntax, not this file's availability. |
| PatentGuru candidates | https://www.patentguru.com/US20260220467A1 ; https://www.patentguru.com/WO2026161822A1 | Inaccessible. |
| Lens candidate | https://www.lens.org/lens/patent/US_20260220467_A1 | Inaccessible; candidate record URL not verified. |
| DownloadPatent candidate | https://www.downloadpatent.com/patent/US20260220467A1 | Inaccessible; only service coverage page was available, not actual target PDF. |
| Patents-review | https://www.patents-review.com/inventor/1553933-babak-hassibi-san-marino-ca-us.html ; https://www.patents-review.com/a/20260220467-systems-methods-training-neural-networks-related-machine.html | Inventor listing indexed exact US application; direct listing fetch 403 and candidate article URL inaccessible. |
| Patent-i international index | https://patent-i.com/report/wo_en/applicant/0000486/ ; followed exact WO listing link to https://patent-i.com/summaria/offer/WO2026/161822 | Bibliographic listing read; destination provided no usable drawing. |
| IPqwery international index | https://www.ipqwery.com/ipowner/en/owner/ip/1112-california-institute-of-technology.html?rgk=IPType&rgk=Jurisdiction&rvk=Patent&rvk=WIPO ; followed actual application link https://www.ipqwery.com/ipowner/en/ip/ptwo/US2026012584.html | Bibliographic listing read; target record HTTP 403. |
| Image search | `"US20260220467" "WO2026161822" patent drawings` | Returned unrelated patent picture, explicitly rejected. |
| Provisional | `"63/749,353" provisional`; cross-reference and Patent Center wrapper route | Reference verified in public text, no provisional document or drawing returned. |
| Inventor/figure search | `"rigid cage" "Naucler" weights quantization`; `Gustav Naucler Hassibi quantization mirror descent histograms LLM`; `"Gustav Naucler" mirror descent quantization thesis`; `"Gustav Naucler" Hassibi quantization slides`; `"Gustav Nauclér" "quantization" mirror`; `"Hassibi" "Naucler" "quantization" LLM`; `Caltech technology transfer "Hassibi" "Naucler" quantization training neural networks`; `"large language model" "mirror descent" "bimodal" weights quantization Hassibi`; `"mirror descent" "bimodal" "Hassibi" quantization large language model` | No verified Figure 7A/7B copy found. Unrelated works and generic results rejected. |
| Earlier experimental source | `Hassibi Lale Azizan "histograms" "weights" "potentials" mirror descent 11 million`; `Hassibi mirror descent "histogram" "11" "weights" ResNet` | Found the matching experimental description and successfully opened the primary arXiv and author-hosted paper images. ResearchGate was a discovery route, not the visual authority used. |
| ArXiv PDF and HTML | https://arxiv.org/pdf/1906.03830 ; https://arxiv.org/html/1906.03830 | PDF pages 11, 33, 34 visually inspected; six standalone PNG links opened. PDF and two PNG download attempts failed. |
| Author-hosted manuscript | https://azizan.mit.edu/papers/SMD_deep.pdf | Page 23 visually inspected; download attempt failed. |
| Related RMD preprint | https://arxiv.org/pdf/2202.10788 | Accessible text; not established as source of requested figures. No figure identity claimed. |
| Caltech thesis | https://thesis.library.caltech.edu/14001/3/Navid_Azizan_2020_Thesis.pdf | Text and figure list identify analogous plots; thesis drawings not separately visually inspected. |
| Related fellowship record | https://www.control.lth.se/surf ; https://sfp.caltech.edu/documents/25667/Summer_Abstracts_23_compiled.pdf ; https://sfp.caltech.edu/documents/25669/Summer_Seminar_Day_23_-_List_of_Presentations.pdf | Search results identify Nauclér's 2023 work with Hassibi. No poster picture or LLM histogram authenticated. |

## 7. Other plausible retrieval paths and pushback

**[Read in text]** The USPTO [PDF link guide](https://www.uspto.gov/sites/default/files/documents/PDF-links-QRG-Patent-Public-Search.pdf) confirms the exact direct PDF URL pattern used in Section 6. The [official public search page](https://www.uspto.gov/patents/search/patent-public-search) currently says an account will be required for PPUBS beginning 4 December 2026. This is a notice about future access, not evidence the present failures are login walls. The WIPO [PATENTSCOPE FAQ](https://www.wipo.int/en/web/patentscope/faqs_patentscope) identifies its Drawings tab as a source of actual figures. Neither ordinary public browser workflow could be completed by this reader. The correct target remains the published document, not a browser print of the HTML transcription.

**[Inferred]** Highest-value alternative is retrieval from a free public browser session of the exact official USPTO PDF or WIPO published document. A normal browser's network panel can reveal the actual PDF/image request if the site serves a viewer rather than a downloadable file. This is a route suggestion, not an assertion that only a human can obtain the file. No request is made of the project owner. Any future access must comply with the no-credential condition.

**[Inferred]** The weekly USPTO multi-page PDF and single-page TIFF datasets offer a separate path from the interactive viewer. The release week is 30 July 2026; identify the publication member using `US20260220467A1` and the archive's naming/index convention rather than guessing a specific filename. A ZIP central-directory or indexed archive lookup could retrieve just the relevant member where public HTTP byte ranges are supported. An official XML-with-embedded-images distribution may also have drawing TIFFs and formula images as separate files. The text-only XML dataset is not sufficient. A current archive listing, exact archive URL, and access that does not require credentials remain unverified. Do not claim this alternative succeeded.

**[Inferred]** The public prosecution wrapper may have original or replacement drawings, which could differ from the published version. An original-file image should be recorded with its document date and identity; compare with the US and PCT publications before transcribing. The priority provisional may have a different figure order. A Caltech technology-transfer disclosure, an inventor's conference slide deck, an institutional repository item or the full 2023 SURF poster could provide further candidates. The fellowship record predates the filing and could be relevant to the vision experiments, but no authenticated LLM figure was obtained from it. Author-generated copies of the four SMD plots already provide a promising precedent for this approach.

**[Inferred]** Once an authentic PDF is acquired, preserve its original bytes, hash, and all numbered sheets. Render the original page images at sufficient resolution, rotate only for reading, retain uncropped originals alongside any crops, and compare the US/WO versions. The key figure identity check for 6A/6B is whether the plot range, ticks, legend and the distinctive bin/spike positions match the plots in Section 3. For 7A/7B, identify the exact model, layer, weight count, dataset, signed axis, binning, and whether the plots are from a matched training experiment. Check for any caption that establishes before/after rather than two separate runs. For (26)–(31), preserve the printed punctuation, subscripts, coefficients and branch definitions before proposing corrections.

**[Inferred]** The claim of 16 drawing sheets, the characterization of 7A/7B as matched before/after, and the supposition that the figures demonstrate rigid-cage training are not yet supported by image evidence. A failure to find pictures is not evidence that they were never published. The strongest positive finding is the primary-source recovery of the likely Figure 6 experiment; the highest-priority LLM figures and official equation pages are still unresolved.
