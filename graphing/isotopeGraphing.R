## developed by soraya remaili
library(ggplot2)
library(mosaic)
library(showtext)
library(readxl)
library(tidyverse)

isotopes <- read_excel("d18Orecords.xlsx")[1:13]

font_add("Montserrat", "C:/Users/soray/AppData/Local/Microsoft/Windows/Fonts/Montserrat-Regular.ttf")

showtext.auto()

years <- 1694:2020
data <- data.frame(years = isotopes[12], oxyiso = isotopes[13])

ggplot() + geom_line(data = data,
             aes(x = year_GB, y = georgesIso), color = "#542047") + 
  labs(x = "Calendar Year C.E.", 
       y = expression(d^{18}*O ~ "(" * "\u2030" ~ VPDB * ")"), 
       color = "#542047") +
  theme(axis.text = element_text(family = "Montserrat", 
                                 size = 9,color= "#542047"),
        axis.title.x = element_text(family ="Montserrat",
                                    face = "bold",size = 14, color = "#542047"),
        axis.title.y = element_text(family ="Montserrat",
                                    face = "bold",size = 14, color = "#542047"),
        panel.grid.minor = element_blank()) +
   scale_y_reverse()