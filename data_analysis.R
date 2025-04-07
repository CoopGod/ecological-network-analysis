# Load packages
library(dplyr)
library(lme4)
library(ggplot2)
library(lmerTest)
library(patchwork)

# Read in the data
trophic_network_file <- "C:/Users/coopg/Desktop/SUST 410/completed_data/trophic_network/completed_network_data.csv" # nolint: line_length_linter.
combined_network_file <- "C:/Users/coopg/Desktop/SUST 410/completed_data/combined_network/completed_network_data.csv" # nolint: line_length_linter.
df_t <- read.csv(trophic_network_file)
df_tnt <- read.csv(combined_network_file)

# Remove rows for which the correlation was NA
# and Spearman's correlation is not significant
df_t <- df_t[!is.na(df_t$spearmans), ]
df_t <- df_t %>% filter(df_t$distance >= 0)
df_t <- df_t %>% filter(df_t$p_value <= 0.05)
df_t <- df_t %>% filter(df_t$p_value > 0)
nrow(df_t)
df_tnt <- df_tnt[!is.na(df_tnt$spearmans), ]
df_tnt <- df_tnt %>% filter(df_tnt$distance >= 0)
df_tnt <- df_tnt %>% filter(df_tnt$p_value <= 0.05)
df_tnt <- df_tnt %>% filter(df_tnt$p_value > 0)
nrow(df_tnt)

# Create jitter plot for trophic network
pane_a <- ggplot(
  df_t, aes(x = factor(distance), y = spearmans, fill = factor(distance))
) +
  geom_jitter(
    width = 0.2, alpha = 0.6, shape = 21, color = "black"
  ) + # Jittered points
  stat_summary(
    fun = mean, geom = "point", color = "black", size = 3
  ) + # Mean point
  scale_fill_brewer(palette = "Blues") +
  theme_minimal() +
  labs(
    title = "A",
    x = "Distance Category",
    y = "Spearman's Correlation",
    fill = "Distance"
  ) +
  ylim(0, 1) +
  theme(plot.title = element_text(hjust = 0.5))

# Create jitter plot for combined network
pane_b <- ggplot(
  df_tnt, aes(x = factor(distance), y = spearmans, fill = factor(distance))
) +
  geom_jitter(
    width = 0.2, alpha = 0.6, shape = 21, color = "black"
  ) + # Jittered points
  stat_summary(
    fun = mean, geom = "point", color = "black", size = 3
  ) + # Mean point
  scale_fill_brewer(palette = "Greens") +
  theme_minimal() +
  labs(
    title = "B",
    x = "Distance Category",
    y = "Spearman's Correlation",
    fill = "Distance"
  ) +
  ylim(0, 1) +
  theme(plot.title = element_text(hjust = 0.5))

# Combine the two plots
pane_a + pane_b

# Plot Histogram
hist(df_tnt$spearmans,
  breaks = 20,
  col = "lightpink",
  main = "",
  xlab = "Spearman's Correlation",
  ylab = "Frequency",
  xlim = c(0, 1)
)

# LLM On Trophic Network
options(digits = 10)
model <- lmer(spearmans ~ factor(distance) + (1 | year),
  data = df_t
)
summary(model)

# LLM On Trophic/Nontrophic Network
model <- lmer(spearmans ~ factor(distance) + (1 | year),
  data = df_tnt
)
summary(model)

# Restricted View of Trophic Network with Strong Correlations Only
df_t_s <- df_t %>% filter(spearmans > 0.7)
nrow(df_t_s)
pane_a <- ggplot(
  df_t_s, aes(x = factor(distance), y = spearmans, fill = factor(distance))
) +
  geom_jitter(
    width = 0.2, alpha = 0.6, shape = 21, color = "black"
  ) + # Jittered points
  stat_summary(
    fun = mean, geom = "point", color = "black", size = 3
  ) + # Mean point
  scale_fill_brewer(palette = "Blues") +
  theme_minimal() +
  labs(
    title = "A",
    x = "Distance Category",
    y = "Strong Spearman's Correlation (>0.7)",
    fill = "Distance"
  ) +
  theme(plot.title = element_text(hjust = 0.5))

# Restricted View of Trophic-Nontrophic Network with Strong Correlations Only
df_tnt_s <- df_tnt %>% filter(spearmans > 0.7)
nrow(df_tnt_s)
pane_b <- ggplot(
  df_tnt_s, aes(x = factor(distance), y = spearmans, fill = factor(distance))
) +
  geom_jitter(
    width = 0.2, alpha = 0.6, shape = 21, color = "black"
  ) + # Jittered points
  stat_summary(
    fun = mean, geom = "point", color = "black", size = 3
  ) + # Mean point
  scale_fill_brewer(palette = "Greens") +
  theme_minimal() +
  labs(
    title = "B",
    x = "Distance Category",
    y = "Strong Spearman's Correlation (>0.7)",
    fill = "Distance"
  ) +
  theme(plot.title = element_text(hjust = 0.5))

# Combined the plots into one
pane_a + pane_b

# LLM On Restricted Trophic Network
model <- lmer(spearmans ~ factor(distance) + (1 | year),
  data = df_t_s
)
summary(model)

# LLM On Restricted Trophic/Nontrophic Network
model <- lmer(spearmans ~ factor(distance) + (1 | year),
  data = df_tnt_s
)
summary(model)
