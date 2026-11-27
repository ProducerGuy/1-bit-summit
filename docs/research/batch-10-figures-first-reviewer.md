# The patent's drawings: first reviewer's search

Written before the second reviewer's return was seen. Subject: the drawings of US 2026/0220467 A1. No model was trained, loaded or evaluated.

## 1. Result

- No drawing of the application was seen. No route open to this reviewer returns a picture: a fetch returns text, and the workspace cannot download from outside its allowed hosts.
- Figures 6A and 6B were traced by their description to a figure already published by the same group. Figures 7A and 7B were not found in any form.
- One route to the typeset publication exists and was not completed, because it needed an approval that did not come.

## 2. What was found

| Figure | Status | Where | Basis |
|---|---|---|---|
| 6A, 6B | Not seen. Traced | Figure 6 of Azizan, Lale, Hassibi, "Stochastic Mirror Descent on Overparameterized Nonlinear Models", arXiv 1906.03830, section 5.2 | Read in text. The application describes histograms of the absolute value of the final weights, each an 11-million-weight vector that fits the training data exactly, for the power-10 potential (6A) and the 1-norm (6B). The paper's Figure 6 has the same caption in substance and the same count, for a ResNet-18 on CIFAR-10. An image search for the description returns that figure. Inferred to be the same experiment; whether the patent's sheets are the same images is not known |
| 7A, 7B | Not seen. Not found | | The application's text: one layer of a large language model, unimodal near zero before, two modes near plus and minus 0.3 after |
| 1 to 5, 8 to 10 | Not seen | | Text only: flowcharts and system diagrams by their descriptions |

What the paper's text says of its Figure 6, read and not seen: the 1-norm histogram has more weights at and near zero; the 2-norm histogram looks like the initialization; the 3-norm histogram is shifted right; the power-10 histogram is shifted far right so that almost all weights are nonzero. No axis values are given in the text.

## 3. Routes tried

| Route | Outcome |
|---|---|
| Google Patents page for the US publication | Text read in full. Its markup points to 16 drawing files named D00000 to D00015 and to 24 inline formula images |
| Those drawing files, thumbnail and full size, and one formula image | All failed at the image server with a client error. The project owner sees no figures on the page in a browser either |
| Justia page | Earlier fetch failed at the site. The owner's printout of it has no drawings |
| The patent office's typeset publication, at the address pattern its other publications use | The fetch asked for an approval and none came. Not completed |
| The same address from the workspace shell | Refused by the workspace's network rules |
| Web search by publication number, by international number, by title with inventors | No result for this application beyond Justia's inventor page |
| Image search by publication number | Unrelated results |
| Image search by description of the histograms | Returned the 2019 paper's Figure 6 |
| Image search for a language-model layer before and after | Unrelated results |
| Public discussion and repository of an outside project that cites the application | Links to Justia only. Its images are the author's own schematics, not the patent's |

## 4. Not tried, for want of an approval or a way to view

- The international publication at the international office's search site.
- Espacenet and other aggregators' pages for either publication.
- Recorded talks and slides by the inventors after January 2025.
