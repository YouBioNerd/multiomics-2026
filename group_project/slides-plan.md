# Slide plan — Study B (workshop talk structure)

Built to the required shape: question → what we did → 2–3 figures with
read-aloud captions → a "choice we made" slide per sub-question → the
answer → what we do not believe about our own result.

Figures live in `group_project/figures/` (regenerate with
`Rscript group_project/make_slide_figures.R`).

---

## Slide 1 — Title and the question, in one sentence

> **Do the vaginal communities of people on the pill, the injectable and
> the ring differ from each other?**

Study B, 93 participants, one sample each; 220 species; both count tables.

## Slide 2 — What we did, including what we filtered and why

- Quality-checked both tables first (`01-qc.qmd`).
- **Filtered: nothing deleted from the main test.** We *flagged* nine
  samples with fewer than 15,000 reads (read off the gap in the library
  size histogram) and ran a sensitivity analysis without them; the rule
  was picked from depth alone, never from the test result.
- Main analysis: PCoA + PERMANOVA on Bray-Curtis distance of **relative
  abundances** (so shallow samples are not punished for being shallow).
- Confounder check: BV prevalence by arm, Fisher's exact test.
- Pairwise arm comparisons with Holm correction (three tests = three
  chances to be fooled).

## Slide 3 — Figure 1: `pcoa-arm.png` ← TALK FIGURE

*Caption to read out:* "Each point is one participant's vaginal community,
mapped so that close points have similar communities. The three colours are
the three contraceptive methods — and they overlap far more than they
separate. Arm explains about 3% of the variation, p ≈ 0.15."

## Slide 4 — Figure 2: `pcoa-bv.png` ← TALK FIGURE

*Caption to read out:* "The same map, coloured by BV status instead of
method. Now the map makes sense: BV-negative communities sit in the top
left, BV-positive in the bottom right. What separates these samples is BV
— about 14% of the variation, p = 0.001 — not the contraceptive method."

## Slide 5 — Figure 3: `bv-by-arm.png` ← TALK FIGURE (the confounder check)

*Caption to read out:* "If BV clustered in one arm, that arm would look
compositionally different for a boring reason. It doesn't: roughly half of
every arm is BV-positive, and the differences are within chance — Fisher's
p ≈ 0.45. BV is a rival explanation, not a confounder."

## Slide 6 — Choice we made: sub-question 1 "Do the arms differ?"

- **Route A:** Bray-Curtis on **relative abundances** (compositional
  transform).
- **Route B:** Bray-Curtis on **raw counts** — the route our first draft
  took, while the text wrongly claimed it was relative abundances.
- **Kept: Route A.** On raw counts, a shallow sample looks different just
  for being shallow; with nine shallow samples that could fake a community
  difference. Here the nine happened to be spread across arms, so the
  verdict survived by luck — we chose not to rely on luck.
- **Source we opened and read:** Anderson (2001), the PERMANOVA paper —
  <https://doi.org/10.1111/j.1442-9993.2001.01070.pp.x>
  *(open it before the talk and skim the abstract)*.

## Slide 7 — Choice we made: sub-question 2 "Is BV more common in one arm?"

- **Route A:** Fisher's exact test — exact probabilities, valid with the
  two cells that held fewer than 5 samples.
- **Route B:** chi-square approximation — simpler, but unreliable with
  small cells (R warns about exactly this).
- **Kept: Route A** — and we ran the test *both* ways: three BV
  categories, and any-BV-vs-none collapsed to two. Both give the same
  verdict (p ≈ 0.45 and p ≈ 0.90), which is why we trust it.
- **Source we opened and read:** the R documentation page for
  `fisher.test` — type `?fisher.test` in the console, or read
  <https://stat.ethz.ch/R-manual/R-patched/library/stats/html/fisher.test.html>.

## Slide 8 — Choice we made: sub-question 3 "Is pill vs injectable real?"

- **Route A:** report the raw pairwise p-value (0.03) as the headline.
- **Route B:** Holm-correct it across the three pairwise tests (→ ≈ 0.10)
  and call it suggestive.
- **Kept: Route B.** Three tests mean three chances to be fooled by
  chance; 0.03 is one uncorrected draw. It agrees with the biology check
  (median Lactobacillus share 85% pill vs ~45% other arms), so it stays
  on the agenda — but as a lead for the gene table, not a finding.
- **Source we opened and read:** the R documentation for `p.adjust`
  (`?p.adjust`), which explains the Holm method and when to use it.

## Slide 9 — The answer, stated as plainly as the data allow

> **No.** Contraceptive method explains about 3% of the variation in
> these vaginal communities (p ≈ 0.15). What separates samples is BV
> status — about 14%, p = 0.001 — and BV is spread evenly across the
> three arms (p ≈ 0.45). The only hint of an arm effect is pill vs
> injectable (p ≈ 0.03, ≈ 0.10 after correction), and we are not calling
> that a finding.

## Slide 10 — What we do *not* believe about our own result

- **We do not believe "no difference" means "no difference exists."**
  26–39 people per arm is enough to miss a modest effect; p ≈ 0.15 is
  absence of evidence, not evidence of absence.
- **We do not fully believe the pill-vs-injectable hint.** It is one of
  three comparisons, it does not survive Holm correction, and dropping
  the nine shallow samples strengthened it — flattering, but it also
  shows how sensitive a borderline result is to one filter.
- **We do not believe our distance choice sees everything.** Bray-Curtis
  is dominated by the most abundant organisms; a real but small arm
  effect could hide under the BV signal. (Aitchison and Jaccard agreed,
  which helps but does not close the question.)
- **We do not believe the arms were comparable at baseline.** This is
  observational, not randomised: any unmeasured difference between the
  three groups travels with the method label.

## Slide 11 — Questions we would ask next

Pick three for the slide; the rest can be one spoken line ("we also wrote
down…"). All are answerable from the Study B tables we already have.

1. **Does the gene table agree with the composition hint?** Test pill vs
   injectable directly in the gene counts with DESeq2. This is the chase
   slide 8 promised — define nothing new, just test the two arms.
2. **Does BV show up in the immune data?** The `06_cytokines.csv` table
   has not been touched. BV-positive samples should, if the biology
   story is right, carry more inflammatory signalling. BV comes from the
   Nugent score (metadata), so testing cytokines by BV breaks no rule.
3. **Which Lactobacillus species dominates?** *L. crispatus* and
   *L. iners* mean different things biologically — iners-dominated
   communities are less stable. A one-table summary of the two species'
   shares by arm and by BV would sharpen the slide-3 map.
4. **Does composition shift gradually with the Nugent score?** Instead of
   the three BV categories, treat Nugent as a 0–10 number: does the map
   slide along a gradient? A dose–response pattern is harder to dismiss
   than a three-group split.
5. **Do cytokines differ by arm?** The immune readout is the one place a
   contraceptive-method effect could appear even if the species table
   shows none — hormones can act on tissue without reshaping the
   community. Arm is metadata, cytokines are their own table, so the
   cross-table rule is satisfied.
6. **Is pH the middleman?** pH differs sharply between BV states; a
   simple summary of pH by arm (and pH by BV) would show whether the
   hormone could only act *through* the environment rather than directly.

The cross-table habit still applies: define the group from one table,
test the other (e.g. BV labels from metadata → test cytokines; community
labels from the species table → test genes). Never define and test on
the same table.

## Backup slides (only if asked)

- `library-size-histogram.png` — "Nine shallow samples; kept in the main
  test, sensitivity analysis without them strengthened the signal."
- `gene-library-by-batch.png` — "Sequencing batch: negligible (R² ≈ 0.5%)."

## How to check the deck is right

- The two maps show 93 points; the bar chart's segments sum to 93 per arm
  column in `03-bv-by-arm.qmd`.
- Numbers on slides 3–9 match the recomputed evidence table in
  `04-summary.html`.
- The "all robustness checks agree" claim: rerun the §4 robustness table
  in `02-community-composition.qmd` — every row shows arm R² ≈ 3% with
  p > 0.1 (except the low-depth-dropped row, reported separately).
- The three sources on slides 6–8: actually open each one once before
  the talk — that is what "read it yourself" means.
- Slide 11's promises are checkable in the data: `06_cytokines.csv` and
  the gene table are in `data/2-workshop2/group_b_contraception/`, and
  the two Lactobacillus species can be counted straight from the
  taxonomy table.
