# Set the working directory in R
setwd("")

# Read CSV files with semicolon as the delimiter
control_data <- read.csv("GUI_Control.csv", sep = ";", header = TRUE)
treat_data <- read.csv("GUI_Treat.csv", sep = ";", header = TRUE)

# List of new columns without "GUI" (as it is likely an ID)
columns <- c("A", "B", "C", "D", "E", "F", "G", "H", "I")

# Convert all relevant columns in both datasets to numeric values
for (col in columns) {
  control_data[[col]] <- as.numeric(as.character(control_data[[col]]))
  treat_data[[col]] <- as.numeric(as.character(treat_data[[col]]))
}

# Define the titles for the output
column_titles <- c("Funct Req.", "Nec. Comp.", "Clear & Appr.", "Design Const.", "Visual Desg.", 
                   "Inf. Orga", "Easy Inter.", "Mini. Error", "Overall Sats.")

# Lists to store results
test_results <- list()  # For p-values
test_results_int <- list()  # For confidence intervals
median_control <- list()  # For medians of the control group
median_treat <- list()  # For medians of the treatment group
mean_control <- list()  # For means of the control group
mean_treat <- list()  # For means of the treatment group
cohen_r <- list()  # For Cohen's r (effect size)

# Loop over each column (A to J)
for (i in 1:length(columns)) {
  
  col <- columns[i]
  
  # Ensure there are no NA values
  if (!any(is.na(control_data[[col]])) & !any(is.na(treat_data[[col]]))) {
    
    # Perform Wilcoxon test with confidence interval
    test_result <- wilcox.test(control_data[[col]], treat_data[[col]], 
                               paired = FALSE, conf.int = TRUE, alternative = "two.sided")
    
    # Store p-value and confidence intervals
    test_results[[col]] <- test_result$p.value
    test_results_int[[col]] <- round(test_result$conf.int, 3)  # Round to 3 decimal places
    
    # Calculate and round medians and means for control and treatment groups
    median_control[[col]] <- median(control_data[[col]])
    median_treat[[col]] <- median(treat_data[[col]])
    mean_control[[col]] <- round(mean(control_data[[col]]), 3)
    mean_treat[[col]] <- round(mean(treat_data[[col]]), 3)
    
    # Calculate Cohen's r effect size
    W <- test_result$statistic  # Wilcoxon test statistic
    N <- length(control_data[[col]]) + length(treat_data[[col]])  # Total number of observations
    
    # Calculate the Z-value
    z <- qnorm(test_result$p.value / 2)  # Two-tailed p-value
    
    # Calculate Cohen's r
    r <- abs(z) / sqrt(N)  # Absolute value of the Z-score
    
    # Store Cohen's r
    cohen_r[[col]] <- round(r, 3)
    
  } else {
    test_results[[col]] <- NA
    test_results_int[[col]] <- NA
    median_control[[col]] <- NA
    median_treat[[col]] <- NA
    mean_control[[col]] <- NA
    mean_treat[[col]] <- NA
    cohen_r[[col]] <- NA
    warning(paste("NA values in column", col, "lead to no calculation."))
  }
}

# Print results
cat("Statistical analysis results:\n")

for (i in 1:length(columns)) {
  col <- columns[i]
  
  # Format p-value rounded to 4 decimal places
  p_value_rounded <- formatC(test_results[[col]], format = "e", digits = 4)
  
  # Print the results for each column with the correct titles
  cat("\n-------------------------------------\n")
  cat("Title: ", column_titles[i], "\n")
  cat("Control group median: ", median_control[[col]], "\n")
  cat("Treatment group median: ", median_treat[[col]], "\n")
  cat("Control group mean: ", mean_control[[col]], "\n")
  cat("Treatment group mean: ", mean_treat[[col]], "\n")
  cat("P-value: ", p_value_rounded, "\n")
  cat("Confidence interval: [", test_results_int[[col]][1], ", ", test_results_int[[col]][2], "]\n")
  cat("Cohen's r (effect size): ", cohen_r[[col]], "\n")
}
