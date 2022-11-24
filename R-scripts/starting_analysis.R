library(tidyverse)
library(RSQLite)
library(magrittr)



mammals <- DBI::dbConnect(RSQLite::SQLite(), "databases/database.db")
score <- as_tibble(tbl(mammals, 
                       sql("SELECT timestamp, value, video_id, duration FROM assessment")))

score$value <- as.factor(score$value)
score$video_id <- as.factor(score$video_id)
score$timestamp <- strptime(score$timestamp,  format = "%Y-%m-%dT%H:%M:%OS")
summary(score)

score %>%
  ggplot(aes(video_id, fill = value)) + geom_bar() 
score %>%
  ggplot(aes(timestamp, value, color = video_id)) + geom_point()
score %>%
  ggplot(aes(duration)) + geom_histogram()


