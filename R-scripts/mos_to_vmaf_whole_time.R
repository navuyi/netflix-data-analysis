library(RSQLite)
library(scales)
library(ggplot2)
library(dplyr)

mydb <- dbConnect(RSQLite::SQLite(), "../databases/database.db")
testers_id <- dbGetQuery(mydb, 'SELECT id FROM experiment')

vec_scores <- c()
vec_vmaf <- c()
vmaf_average <- c()

for (tester_id in testers_id[['id']]) {
  sql_request <- paste0('SELECT value, started, timestamp FROM assessment WHERE video_id == ',
                        tester_id)
  
  assessments <- dbGetQuery(mydb, sql_request)
  vec_scores <- append(vec_scores, rescale(assessments[['value']],
                                           to = c(0, 1), from = range(0.99, 5.01)))
  
  started <- assessments[['started']]
  finished <- assessments[['timestamp']]
  
  sql_request <- paste0("SELECT avg(playback_data.playing_vmaf) ",
                        "AS avg FROM playback_data ",
                        "WHERE playback_data.rendering_state == 'Playing' ",
                        "AND playback_data.timestamp < '", started[1], "'")
  
  sql_response <- dbGetQuery(mydb, sql_request)
  vmaf_average <- append(vmaf_average, round(sql_response['avg']))
  
  for (i in 1:(length(started)-1)){
    sql_request <- paste0("SELECT avg(playback_data.playing_vmaf) ",
                          "AS 'avg' FROM playback_data ",
                          "WHERE playback_data.rendering_state == 'Playing' ",
                          "AND playback_data.timestamp between '",
                          finished[i], "' and '", started[i+1], "'")
    
    sql_response <- dbGetQuery(mydb, sql_request)
    vmaf_average <- c(vmaf_average, round(sql_response[['avg']]))
  }
}

vmaf_average <- data.frame(vmaf_average)

vec_vmaf <- rescale(unlist(vmaf_average), to = c(0, 1), from = range(20, 100))

vec_vmaf <- data.frame(vec_vmaf, vec_scores)

ggplot() +
  geom_point(data=vec_vmaf, aes(x=vec_vmaf, y=vec_scores))

dbDisconnect(mydb)