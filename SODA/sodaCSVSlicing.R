## developed by soraya remaili
library(tidyverse)

## getting rid of rows with missing temp and salt values
files <- list.files(path = "./psmreu2025/csv", full.names = TRUE)
for (file in files) {
  print(paste("Processing file:", file))
  data <- read.csv(file)
  clean <- data %>% filter(!is.na(temp) & !is.na(salt)) 
  write.csv(clean, file.path("./psmreu2025/csv_clean", 
                             basename(file)), row.names = FALSE)
}

## combining the csv files into one dataset
files <- list.files(path = "./psmreu2025/csv_clean", 
                        pattern = "\\.csv$", full.names = TRUE)
megaCSV <- do.call(rbind, lapply(files, read.csv))
write.csv(megaCSV, file = "./psmreu2025/csv_clean/megaCSV.csv", row.names = FALSE)