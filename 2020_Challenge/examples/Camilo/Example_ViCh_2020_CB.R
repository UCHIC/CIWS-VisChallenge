# data visualization example. Camilo Bastidas
# 10-13-2020

rm(list=ls()) # delete everything

library(lubridate)
library(tidyverse)

rd = read_csv("Raw_Data.csv", skip = 3) # raw data
ce = read_csv("Classified_Events.csv") # classified events
r = 0.041619 # meter resolution

# classified events
# by end use
ce %>% select(Label, `Volume(gal)`) %>% group_by(Label) %>%
  summarise(total = sum(`Volume(gal)`)) %>%
  ggplot(aes(x="", y=total, fill=Label)) +
  geom_bar(stat="identity", width=1, color="white") +
  coord_polar("y", start=0) + 
  theme_void() + theme(legend.text=element_text(size=12), legend.title=element_text(size=14), plot.title = element_text(size=18)) +
  labs(fill = "End Use") + ggtitle("Distribution of residential water use")

# end uses wihtout irrigation
ce %>% select(Label, `Volume(gal)`) %>% group_by(Label) %>%
  summarise(total = sum(`Volume(gal)`)) %>% filter(Label != 'irrigation') %>%
  mutate(percentage = total*100/sum(total)) %>%
  ggplot(aes(x="", y=percentage, fill=Label)) +
  geom_bar(stat="identity", width=1, color="white") +
  coord_polar("y", start=0) + theme_void() + # remove background, grid, numeric labels
  geom_text(aes(y = c(94,84, 65, 44, 15),
                label = paste0(round(percentage,0),"%")), size=7) + 
  theme(legend.text=element_text(size=12), legend.title=element_text(size=14), plot.title = element_text(size=18)) +
  labs(fill = "End Use")  + ggtitle("Distribution of \"indoor\" water use")


# raw data
# daily use
rd %>% group_by(datetime = floor_date(Time, "1 day")) %>%
  summarise(volume = sum(Pulses) * r) %>%
  ggplot(aes(x= datetime, y=volume/1000)) + ggtitle("Total daily usage") + xlab("Date") +
  geom_bar(stat="identity") + ylab(expression ("Volume ("~10^3~" gallons)"))

# hourly use
rd %>% group_by(datetime = floor_date(Time, "1 hour")) %>%  summarise(volume_h = sum(Pulses) * r) %>%
  group_by(hour = hour(datetime)) %>% summarise(volume = mean(volume_h)) %>%
  ggplot(aes(x= hour, y=volume)) + ggtitle("Hourly water use") +
  geom_bar(stat="identity") + ylab("Volume (gallons)")



