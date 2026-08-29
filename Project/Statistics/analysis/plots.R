# Publication-quality figures for the IPL statistics project.
# Reads data/ipl_2008_2018.csv + results.json; writes PDFs to report/figures/.
library(ggplot2)
library(jsonlite)

# Project root = parent of the directory holding this script (works for
# relative and absolute invocation paths alike).
full <- sub("^--file=", "", commandArgs(FALSE)[grepl("^--file=", commandArgs(FALSE))][1])
stopifnot(!is.na(full))
setwd(dirname(normalizePath(full)))   # .../Statistics/analysis
setwd("..")                           # .../Statistics

df <- read.csv("data/ipl_2008_2018.csv", stringsAsFactors = FALSE)
R  <- fromJSON("results.json", simplifyVector = TRUE)

dir.create("report/figures", showWarnings = FALSE)

# Shared look: serif type (pairs with Times body), muted professional palette
INK    <- "#2C3E50"
ACCENT <- "#C0392B"
STEEL  <- "#34495E"
GOLD   <- "#B7950B"

theme_set(theme_minimal(base_size = 11, base_family = "serif"))
theme_update(
  panel.grid.minor = element_blank(),
  panel.grid.major = element_line(colour = "grey90", linewidth = 0.3),
  plot.title = element_text(face = "bold", size = 12),
  plot.subtitle = element_text(colour = "grey30", size = 9.5),
  axis.title = element_text(size = 10.5),
  legend.position = "none",
  plot.caption = element_text(size = 7.5, colour = "grey40")
)

fig <- function(plot, name, w = 6.8, h = 3.9) {
  ggsave(file.path("report/figures", name), plot = plot,
         width = w, height = h, dpi = 300)
}

## 1. Distribution of target runs: histogram + density ------------------------
p1 <- ggplot(df, aes(x = target_runs)) +
  geom_histogram(aes(y = after_stat(density)), bins = 32,
                 fill = STEEL, colour = "white", alpha = 0.85) +
  geom_density(colour = ACCENT, linewidth = 0.9) +
  geom_vline(xintercept = R$descriptive$target_runs$mean,
             linetype = "dashed", colour = GOLD, linewidth = 0.7) +
  annotate("text", x = R$descriptive$target_runs$mean - 38, y = 0.0128,
           label = paste0("mean = ", round(R$descriptive$target_runs$mean, 1)),
           family = "serif", size = 3.1, colour = GOLD) +
  labs(title = "Distribution of Target Runs (n = 686)",
       subtitle = "Histogram scaled to density with kernel density overlay; dashed line marks the mean",
       x = "Target runs", y = "Density",
       caption = "IPL seasons 2008-2018; the 10 abandoned/no-result matches are excluded.")
fig(p1, "fig_target_hist.pdf")

## 2. Boxplots: margin vs target ----------------------------------------------
long <- rbind(
  data.frame(v = df$result_margin[!is.na(df$result_margin)],
             metric = "Victory margin"),
  data.frame(v = df$target_runs, metric = "Target runs"))
p2 <- ggplot(long, aes(x = metric, y = v, fill = metric)) +
  geom_boxplot(width = 0.42, outlier.size = 1.1, outlier.colour = "grey45",
               alpha = 0.9) +
  scale_fill_manual(values = c(STEEL, ACCENT)) +
  stat_summary(fun = mean, geom = "point", shape = 23, size = 2.4,
               fill = GOLD, colour = "white") +
  labs(title = "Spread and Skew: Victory Margins vs Target Runs",
       subtitle = "Boxes span Q1-Q3; median line and gold mean diamond shown.\nThe margin box is compressed, with far-out outliers.",
       x = NULL, y = "Runs",
       caption = "Margins available for 685 decided matches (the single tied match has no margin).")
fig(p2, "fig_boxplots.pdf")

## 3. Empirical PMF of wicket margins -----------------------------------------
w  <- df[df$result == "wickets" & !is.na(df$result_margin), ]
pm <- as.data.frame(table(margin = factor(w$result_margin, levels = 1:10)))
pm$p   <- pm$Freq / sum(pm$Freq)
pm$lab <- sprintf("%.3f", pm$p)
p3 <- ggplot(pm, aes(x = margin, y = p)) +
  geom_col(fill = STEEL, alpha = 0.92, width = 0.72) +
  geom_vline(xintercept = which.max(pm$p), linetype = "dotted",
             colour = ACCENT, linewidth = 0.7) +
  geom_text(aes(label = lab), vjust = -0.35, family = "serif", size = 2.7,
            colour = INK) +
  scale_y_continuous(expand = expansion(mult = c(0, .09))) +
  labs(title = "Empirical PMF of Winning Margins When Chasing",
       subtitle = expression(P(X == x) ~ "for wickets lost by the batting side;" ~
                               "mode at x = 6" ~ (hat(p) == 0.205)),
       x = "Wickets (margin of defeat)", y = "P(X = x)",
       caption = "All 370 chase wins, seasons 2008-2018.")
fig(p3, "fig_pmf_wickets.pdf")

## 4. Season trend: per-match scatter + season means + OLS line ---------------
means <- as.data.frame(R$regression$points)
sl <- R$regression$slope; ic <- R$regression$intercept
p4 <- ggplot() +
  geom_jitter(data = df, aes(x = season, y = target_runs),
              width = 0.14, alpha = 0.13, colour = STEEL, size = 1.05) +
  geom_point(data = means, aes(x = season, y = target_runs),
             shape = 21, fill = GOLD, colour = INK, size = 2.6) +
  geom_abline(intercept = ic, slope = sl, colour = ACCENT, linewidth = 0.85) +
  annotate("label", x = 2.1, y = 238,
           label = sprintf("hat(y) == %.2f + %.2f * x", ic, sl),
           parse = TRUE, family = "serif", size = 3.4, colour = ACCENT,
           fill = "white", alpha = 0.85, label.size = 0) +
  annotate("label", x = 2.1, y = 224,
           label = sprintf("R^2 == %.3f ~ (%.3g)", R$regression$r2,
                           R$regression$p_value),
           parse = TRUE, family = "serif", size = 3.2, colour = "grey30",
           fill = "white", alpha = 0.85, label.size = 0) +
  scale_x_continuous(breaks = 1:11, labels = 2008:2018) +
  labs(title = "Target Runs Drift Upward Across the Decade",
       subtitle = "Faded points: individual matches. Gold dots: seasonal means. Red line: least-squares fit through seasonal means.",
       x = "Season", y = "Target runs",
       caption = "OLS on 11 seasonal means: slope = 1.150 runs per season (SE 0.465).")
fig(p4, "fig_regression.pdf")

## 5. Binomial estimates with 95% CIs ------------------------------------------
b <- R$binomial
est <- rbind(
  data.frame(group = "Team batting first\nwins",      k = b$bat_first_win$k,     n = b$bat_first_win$n),
  data.frame(group = "Team chasing\nwins",            k = b$field_first_win$k,   n = b$field_first_win$n))
est$p  <- est$k / est$n
lo <- function(k, n) qbeta(0.025, k + 0.5, n - k + 0.5)   # Jeffreys interval
hi <- function(k, n) qbeta(0.975, k + 0.5, n - k + 0.5)
est$lo <- mapply(lo, est$k, est$n); est$hi <- mapply(hi, est$k, est$n)
est$lab <- sprintf("%d/%d = %.1f%%", est$k, est$n, 100 * est$p)

p5 <- ggplot(est, aes(x = group, y = p, colour = group)) +
  geom_hline(yintercept = 0.5, linetype = "dashed", colour = "grey55") +
  geom_errorbar(aes(ymin = lo, ymax = hi), width = 0.16, linewidth = 0.75) +
  geom_point(size = 3.4) +
  geom_text(aes(label = lab), vjust = -1.25, family = "serif", size = 3.1,
            show.legend = FALSE) +
  scale_colour_manual(values = c(STEEL, ACCENT)) +
  annotate("text", x = 2.42, y = 0.505, label = "fair coin (0.5)",
           family = "serif", size = 2.8, colour = "grey45") +
  coord_cartesian(ylim = c(0.3, 0.68)) +
  labs(title = "First-Innings Advantage: Binomial Proportion Estimates",
       subtitle = "Win proportions with 95% confidence intervals; chasing clears the fair-coin benchmark, batting first does not.",
       x = NULL, y = "Estimated win probability",
       caption = "Exact binomial tests: chasing p = 0.029 (significant at alpha = 0.05); batting first p = 0.188.")
fig(p5, "fig_binomial_ci.pdf")

cat("figures written:\n"); print(list.files("report/figures"))
