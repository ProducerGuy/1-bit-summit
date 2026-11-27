# Brief: find the drawings of one patent application

You are one of two reviewers on a research project. Both of you are doing this task alone, and neither sees the other's result until both are in. This brief is the whole task. You do not need any other project document for it, and for this task you should not read the project's repository: work from primary and public sources only.

## 1. What is wanted

The drawings of this patent application, in any form in which the picture itself can be looked at:

- Title: Systems and Methods for Training Neural Networks and Related Machine Learning Models
- United States publication: US 2026/0220467 A1, published 30 July 2026
- Application number: 19/460,181, filed 26 January 2026
- Priority: provisional application 63/749,353, filed 24 January 2025
- International publication: WO 2026/161822 A1, application PCT/US2026/012584
- Applicant: California Institute of Technology
- Inventors: Hassibi, Lale, Naucler

The publication appears to have 16 drawing sheets. Its text describes figures 1 to 10, with figures 6A, 6B, 7A and 7B being weight histograms. Neither reviewer has yet seen any drawing: only the text has been read.

In order of importance:

1. Figures 7A and 7B. The text says they show the weights of one layer of a large language model before and after the process.
2. Figures 6A and 6B. The text says they show histograms of the absolute value of the final weights of a network for different potentials.
3. Every other drawing sheet.
4. The typeset pages of the description that hold equations 26 to 31, as printed in the official publication and not as re-rendered by a patent website.

"Any form" means any: the official publication as a document or as page images, the international publication, a patent office's file for the application, a mirror or aggregator that serves the drawings, the provisional application, or the same figure published elsewhere by the same people, such as a paper, a preprint, a thesis, a talk, slides, a poster, a video or a company document. If a figure is found somewhere other than the patent, say what shows it is the same figure and how sure you are.

## 2. What to return

One markdown document, with the image files attached beside it or inside one archive.

For each drawing sheet and each figure:

- Whether you saw the picture itself, read a description of it, or found nothing.
- Where it was obtained: the exact address, and the route you took to reach it.
- The file, if you could obtain it. If you could only view it, say so.
- What it shows, from the picture and not from the patent's text: the figure number printed on it, the kind of plot or diagram, axis labels, ranges and tick values, legends and titles, any model, layer, dataset or parameter count named, and for a histogram where its mass and its peaks sit, with numbers read off the axes.

For the equation pages:

- A faithful transcription of the steps given for the inverse of the gradient mapping in the rigid cage section, of equations 26 to 31, and of the sentence that follows equation 31, exactly as the official typeset pages print them, including anything that looks wrong. Say for each whether you read it from a typeset page image or from a website's re-rendering.

Then:

- Everything you tried that did not work, and why it did not work. This is as useful as what worked.
- Anything the drawings show that the text does not say, or that disagrees with the text.
- Your own suggestions: other places these figures could exist that this brief did not think of, and anything you think this brief has wrong or is asking for in the wrong way. Pushback is wanted.

Label every statement by how you got it: seen in an image, read in text, computed, or inferred.

## 3. Conditions

- No model is trained, loaded or evaluated.
- Do not use, request or enter any credential, account or payment. Do not fill in any form that asks for personal information. Free public sources only.
- Do not ask the project owner to do anything. If something can only be obtained by a person, write it at the very top of your reply as numbered single-action steps and nothing else, and put the rest of your report after it.
- Do not guess at what a figure shows. A figure you did not see is reported as not seen.
- No time or effort estimates.
