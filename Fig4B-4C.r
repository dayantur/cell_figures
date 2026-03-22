library("tidyverse")
library("ggalluvial")

# Load data from the CSV file
data_file <- "./outputs/Resilience/alluvial_data.csv"
df_alluvial <- read_csv(data_file)

# Load species-color mapping
color_mapping <- read.delim("./outputs/Resilience/species_colors.txt")
species_colors <- setNames(color_mapping$Color, color_mapping$Species)

# Ensure proper ordering and reverse the ranking for visualization
df_alluvial <- df_alluvial %>%
    mutate(
        Species = factor(Species, levels = names(species_colors)),  # Enforce the predefined order
        year = factor(year, levels = unique(year))
    ) %>%
    group_by(year) %>%
    arrange(desc(size), .by_group = TRUE)  # Reverse order of size for each year

# Switch the order of RND and EGM by changing the factor levels
df_alluvial <- df_alluvial %>%
    mutate(attack = factor(attack, levels = c("RND", "EGM")))  # RND on top

# Create the combined plot
alluvial_plot <- ggplot(df_alluvial, aes(
    x = as.factor(year), stratum = Species, alluvium = Species, y = size,
    fill = Species, label = Species
)) +
    geom_alluvium(decreasing = TRUE) +
    geom_stratum(alpha = 1, decreasing = TRUE) +
    scale_fill_manual(values = species_colors) +  # Use predefined species-to-colors mapping
    facet_grid(rows = vars(attack), scales = "free_y", space = "free_y") +  # RND on top, EGM on bottom
    labs(x = NULL, y = NULL) +
    theme_minimal() +
    theme(
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.text.x = element_text(size = 15),  # Adjust size for x-axis labels
        axis.title.x = element_blank(),
        plot.title = element_blank(),
        legend.position = "right",  # Single legend on the right
        legend.title = element_blank(),
        strip.text = element_blank(),  # Remove facet titles
        plot.margin = margin(t = 10, b = 20)  # Adjust bottom margin
    ) +
    scale_x_discrete(labels = function(labels) paste0(labels))  # Keep numeric x-axis labels

# Save or display the plot
ggsave("./generatedfigures/Fig4B-4C.pdf", alluvial_plot, width = 5, height = 7)
print(alluvial_plot)
