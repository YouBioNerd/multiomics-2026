# Regenerates the slide figures from the raw data, at high resolution.
# Why regenerate instead of copying the report PNGs: this guarantees the
# CORRECT version of each figure (e.g. the BV map computed on relative
# abundances, not raw counts) and gives slide-friendly resolution.
#
# Run:  Rscript group_project/make_slide_figures.R

library(tidyverse)
library(here)
library(microViz)
library(phyloseq)

source(here("R/count_tables.R"))

fig_dir <- here("group_project", "figures")
dir.create(fig_dir, showWarnings = FALSE)

dd  <- read_counts("group_b")
ps  <- as_counts("group_b", "microbiome", data = dd)
psb <- ps |> tax_transform("compositional") |> dist_calc("bray")

# 1. The headline map: PCoA coloured by contraceptive arm
p <- psb |> ord_calc("PCoA") |> ord_plot(colour = "arm") +
  labs(title = "Bray-Curtis PCoA, coloured by contraceptive method")
ggsave(file.path(fig_dir, "pcoa-arm.png"), p, width = 8, height = 6, dpi = 300)

# 2. The same map coloured by what actually separates the samples: BV status
p <- psb |> ord_calc("PCoA") |> ord_plot(colour = "bv") +
  labs(title = "… coloured by BV status")
ggsave(file.path(fig_dir, "pcoa-bv.png"), p, width = 8, height = 6, dpi = 300)

# 3. The confounder check: BV prevalence by arm
p <- dd$metadata |>
  count(arm, bv) |>
  ggplot(aes(arm, n, fill = bv)) +
  geom_col(position = "fill") +
  scale_y_continuous(labels = scales::percent) +
  labs(x = NULL, y = "Share of samples", fill = "BV status",
       title = "BV status by contraceptive arm")
ggsave(file.path(fig_dir, "bv-by-arm.png"), p, width = 8, height = 6, dpi = 300)

# BACKUP 1: library sizes — justifies the 15,000-read rule
lib <- tibble(sample_id = dd$metadata$sample_id,
              arm       = dd$metadata$arm,
              reads     = colSums(dd$species))
p <- ggplot(lib, aes(reads)) +
  geom_histogram(bins = 30, fill = "grey70", colour = "white") +
  labs(x = "Reads per sample (species table)", y = "Samples",
       title = "Library sizes: a clear gap below ~15,000 reads")
ggsave(file.path(fig_dir, "library-size-histogram.png"), p,
       width = 8, height = 6, dpi = 300)

# BACKUP 2: gene library size by sequencing batch — batch was negligible
gene_lib <- tibble(batch = dd$metadata$rnaseq_batch,
                   reads = colSums(dd$genes))
p <- ggplot(gene_lib, aes(batch, reads, fill = batch)) +
  geom_boxplot(show.legend = FALSE) +
  geom_jitter(width = 0.15, alpha = 0.4) +
  labs(title = "Gene library size by sequencing batch",
       x = "Batch", y = "Library size (reads)")
ggsave(file.path(fig_dir, "gene-library-by-batch.png"), p,
       width = 8, height = 6, dpi = 300)

cat("Saved:", list.files(fig_dir, "\\.png$", full.names = FALSE), sep = "\n  ")
