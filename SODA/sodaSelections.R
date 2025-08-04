## developed by soraya remaili
library(readxl)
isotopes <- read_excel("d18Orecords.xlsx")[1:13]
data <- data.frame(years = isotopes[1], oxyiso = isotopes[2])
write.csv(data, file.path("./d18O_data", 
                             "jonesport"), row.names = FALSE)

## nearest available depth
jonesportCSV <- megaCSV %>% filter(between(xt_ocean, 292.5, 293) 
                                   & between(yt_ocean, 44, 44.5) 
                                   & between(st_ocean, 75, 85))
jonesportCSV <- jonesportCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(jonesportCSV, file = "./csv_clean/jonesportCSV.csv",
          row.names = FALSE)

## lowest available depth
jonesportCSV <- megaCSV %>% filter(between(xt_ocean, 292.5, 293) 
                                   & between(yt_ocean, 44, 44.5) 
                                   & between(st_ocean, 180, 190))
jonesportCSV <- jonesportCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(jonesportCSV, file = "./csv_clean/jonesportCSV.csv",
          row.names = FALSE)

isotopes <- read_excel("d18Orecords.xlsx")[1:13]
data <- data.frame(years = isotopes[1], oxyiso = isotopes[10])
write.csv(data, file.path("./d18O_data", 
                             "isleAuHaut"), row.names = FALSE)
## nearest available depth
isleAuHautCSV <- megaCSV %>% filter(between(xt_ocean, 291, 291.5) 
                                   & between(yt_ocean, 44, 44.5) 
                                   & between(st_ocean, 27, 37))

isleAuHautCSV <- isleAuHautCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(isleAuHautCSV, file = "./csv_clean/isleAuHautCSV.csv",
          row.names = FALSE)

## lowest available depth
isleAuHautCSV <- megaCSV %>% filter(between(xt_ocean, 291, 291.5) 
                                   & between(yt_ocean, 44, 44.5) 
                                   & between(st_ocean, 40, 50))
isleAuHautCSV <- isleAuHautCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(isleAuHautCSV, file = "./csv_clean/isleAuHautCSV.csv",
          row.names = FALSE)

isotopes <- read_excel("d18Orecords.xlsx")[1:13]
data <- data.frame(years = isotopes[1], oxyiso = isotopes[4])
write.csv(data, file.path("./d18O_data", 
                             "seguin"), row.names = FALSE)
## nearest available depth and lowest available depth
seguinCSV <- megaCSV %>% filter(between(xt_ocean, 290, 290.5) 
                                   & between(yt_ocean, 43.5, 44) 
                                   & between(st_ocean, 30, 40))
seguinCSV <- seguinCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(seguinCSV, file = "./csv_clean/seguinCSV.csv",
          row.names = FALSE)

isotopes <- read_excel("d18Orecords.xlsx")[1:13]
data <- data.frame(years = isotopes[12], oxyiso = isotopes[13])
names(data)[names(data) == "year_GB"] <- "year"
write.csv(data, file.path("./d18O_data", 
                             "georgesBank"), row.names = FALSE)
## nearest available depth
georgesBankCSV <- megaCSV %>% filter(between(xt_ocean, 292, 292.5) 
                                   & between(yt_ocean, 40.5, 41) 
                                   & between(st_ocean, 68, 78))
georgesBankCSV <- georgesBankCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(georgesBankCSV, file = "./csv_clean/georgesBankCSV.csv",
          row.names = FALSE)

## lowest available depth
georgesBankCSV <- megaCSV %>% filter(between(xt_ocean, 292, 292.5) 
                                   & between(yt_ocean, 40.5, 41) 
                                   & between(st_ocean, 180, 190))
georgesBankCSV <- georgesBankCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(georgesBankCSV, file = "./csv_clean/georgesBankCSV.csv",
          row.names = FALSE)
          
isotopes <- read_excel("d18Orecords.xlsx")[1:13]
data <- data.frame(years = isotopes[1], oxyiso = isotopes[6])
write.csv(data, file.path("./d18O_data", 
                             "longIsland"), row.names = FALSE)
## nearest available depth
longIslandCSV <- megaCSV %>% filter(between(xt_ocean, 287, 287.5) 
                                   & between(yt_ocean, 40, 40.5) 
                                   & between(st_ocean, 44, 54))
longIslandCSV <- longIslandCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(longIslandCSV, file = "./csv_clean/longIslandCSV.csv",
          row.names = FALSE)

## lowest available depth
longIslandCSV <- megaCSV %>% filter(between(xt_ocean, 287, 287.5) 
                                   & between(yt_ocean, 40, 40.5) 
                                   & between(st_ocean, 50, 60))
longIslandCSV <- longIslandCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(longIslandCSV, file = "./csv_clean/longIslandCSV.csv",
          row.names = FALSE)

isotopes <- read_excel("d18Orecords.xlsx")[1:13]
data <- data.frame(years = isotopes[1], oxyiso = isotopes[8])
write.csv(data, file.path("./d18O_data", 
                             "delmarva"), row.names = FALSE)
## nearest available depth
delmarvaCSV <- megaCSV %>% filter(between(xt_ocean, 285.5, 286) 
                                   & between(yt_ocean, 38, 38.5) 
                                   & between(st_ocean, 60, 70))
delmarvaCSV <- delmarvaCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(delmarvaCSV, file = "./csv_clean/delmarvaCSV.csv",
          row.names = FALSE)

## lowest available depth
delmarvaCSV <- megaCSV %>% filter(between(xt_ocean, 285.5, 286) 
                                   & between(yt_ocean, 38, 38.5) 
                                   & between(st_ocean, 105, 115))
delmarvaCSV <- delmarvaCSV %>%
  mutate(time = str_replace(as.character(time), ":60$", ":59"))
write.csv(delmarvaCSV, file = "./csv_clean/delmarvaCSV.csv",
          row.names = FALSE)