library(RSQLite)
library(scales)
library(ggplot2)
library(dplyr)

# setwd("./R-scripts")
mydb <- dbConnect(RSQLite::SQLite(), "../databases/database.db")
testers_id <- dbGetQuery(mydb, 'SELECT id FROM experiment')

vec_scores <- c()
vec_vmaf <- c()
vmaf_average <- c()

for (tester_id in testers_id[['id']]) {
  sql_request <- paste0('SELECT value, started, timestamp FROM assessment 
                        WHERE video_id == (SELECT id FROM video 
                        WHERE experiment_id == ', tester_id, ')')
  
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

# ggplot(data=vec_vmaf, aes(x=vec_vmaf, y=vec_scores)) +
#   geom_point() + geom_rug()

vec_vmaf %>%
  mutate(vmf_cat = floor(vec_vmaf*20)) %>%
  group_by(vmf_cat) %>%
  summarise(vmf = mean(vec_vmaf), mos = mean(vec_scores)) %>%
  # ggplot(aes(vmf, mos)) + 
  #   geom_point() + 
  #   geom_abline(intercept = 0, slope = 1, color = "red")

# data preparation - 20 different VMAFs, can be changed in the future
data_ag <- vec_vmaf %>%
  mutate(vmf_cat = floor(vec_vmaf*20)) %>%
  group_by(vmf_cat) %>%
  summarise(vmf = mean(vec_vmaf), mos = mean(vec_scores))

# linear model
model_lin <- lm(mos ~ vmf, data_ag)
# plot(model_lin)
summary(model_lin)

# ggplot(data_ag, aes(vmf, mos)) + 
#   geom_point() + 
#   geom_abline(intercept = as.numeric(model_lin$coefficients[1]), 
#               slope = as.numeric(model_lin$coefficients[2]), color = "red")

# power model
data_power <- data_ag %>%
  mutate(vmf = log(vmf)) %>%
  mutate(mos = log(mos))
model_pow <- lm(mos ~ vmf, data_power)
# plot(model_pow)
summary(model_pow)

# ggplot(data_power, aes(vmf, mos)) + 
#   geom_point() + 
#   geom_abline(intercept = as.numeric(model_pow$coefficients[1]), 
#               slope = as.numeric(model_pow$coefficients[2]), color = "red")

# logit model
data_logit <- data_ag %>%
  mutate(mos = log(mos / (1 - mos)))
model_logit <- lm(mos ~ vmf, data_logit)
# plot(model_logit)
summary(model_logit)

# ggplot(data_logit, aes(vmf, mos)) + 
#   geom_point() + 
#   geom_abline(intercept = as.numeric(model_logit$coefficients[1]), 
#               slope = as.numeric(model_logit$coefficients[2]), color = "red")

ggplot(data_ag, aes(vmf, mos)) + 
  geom_point() + 
  geom_function(fun = ~ as.numeric(model_lin$coefficients[1]) + 
                  as.numeric(model_lin$coefficients[2])*(.x), color = "red") +
  geom_function(fun = ~ exp(as.numeric(model_pow$coefficients[1])) *
                (.x)^as.numeric(model_pow$coefficients[2]), color = "green") +
  geom_function(fun = ~ exp(as.numeric(model_logit$coefficients[1]) +  
                  as.numeric(model_logit$coefficients[2]) * (.x)) / 
                    (1 + exp(as.numeric(model_logit$coefficients[1]) +  
                               as.numeric(model_logit$coefficients[2]) * (.x))), 
                color = "blue") +
  ggtitle('Average VMAF to MOS') +
  theme(plot.title = element_text(hjust = 0.5))
  
dbDisconnect(mydb)
