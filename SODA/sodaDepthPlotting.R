## developed by soraya remaili
library(ggplot2)
library(showtext)
library(sf)
library(readxl)
library("rnaturalearth")

font_add("Montserrat", "C:/Users/soray/AppData/Local/Microsoft/Windows/Fonts/Montserrat-Regular.ttf")

showtext.auto()

map <- ne_countries(scale = 110, returnclass = "sf")
world_sf <- st_as_sf(map)

long <- c(74.0868, 73.01238, 67.8053, 69.75, 68.6789, 67.44)*(-1)
lat <- c(38.2268, 40.09925, 40.727667, 43.7, 44.0398, 44.44)
site <- c("DS", "LI", "GB", "S", "IH", "J")
data <- data.frame(long = long, lat = lat, site = site)
filtered <- read_excel("./csv_clean/megaFilter.xlsx")

ggplot() + geom_sf(data = world_sf, size = 0.3,
               fill = "#542047", color = "white") +
  geom_tile(data = filtered,
            aes(x = xt_ocean, y = yt_ocean, fill = st_ocean),
            width = 0.5, height = 0.5) +
  scale_fill_continuous(high = "#003b5c", low = "#b6e4aaff") + 
  geom_point(data = data,
             aes(x = long, y = lat),shape= 21,
             fill= NA, color= "#f5fac7ff",size= 3, stroke= 2) + 
  coord_sf(xlim = c(-76, -64), ylim = c(36, 45)) +
  labs(x = "Longitude", y = "Latitude", fill = "Depth (m)",) +
  scale_x_continuous(breaks = seq(-76, -64, by = 2), 
                     labels = \(x) paste0(abs(x), "\u00B0 W")) +
  scale_y_continuous(breaks = seq(36, 45, by = 1.5),
                     labels = \(x) paste0(abs(x), "\u00B0 N")) +
  theme(axis.text = element_text(family = "Montserrat", 
                                 size = 9,color= "#542047"),
        axis.title.x = element_text(family ="Montserrat",
                                    face = "bold",size = 14, color = "#542047"),
        axis.title.y = element_text(family ="Montserrat",
                                    face = "bold",size = 14, color = "#542047"),
        legend.title = element_text(family ="Montserrat",
                                    face = "bold",size = 14, color = "#542047"),
        legend.text = element_text(family ="Montserrat",
                                    face = "bold",size = 14, color = "#542047"),
        panel.grid.minor = element_blank())