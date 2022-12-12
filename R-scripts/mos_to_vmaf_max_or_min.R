library(RSQLite)
library(scales)
library(ggplot2)
library(dplyr)

mydb <- dbConnect(RSQLite::SQLite(), "../databases/database.db")
testers_id <- dbGetQuery(mydb, 'SELECT id FROM experiment')

vec_scores <- c()
vec_vmaf_min <- c()
vmaf_min <- c()
vmaf_max <- c()

for (tester_id in testers_id[['id']]) {
  sql_request <- paste0('SELECT value, started, timestamp FROM assessment 
                        WHERE video_id == (SELECT id FROM video 
                        WHERE experiment_id == ', tester_id, ')')
  
  assessments <- dbGetQuery(mydb, sql_request)
  vec_scores <- append(vec_scores, rescale(assessments[['value']],
                                           to = c(0, 1), from = range(0.99, 5.01)))
  
  started <- assessments[['started']]
  finished <- assessments[['timestamp']]
  
  sql_request <- paste0("SELECT max(playback_data.playing_vmaf) AS max, ",
                        "min(playback_data.playing_vmaf)  AS min ",
                        "FROM playback_data ",
                        "WHERE playback_data.rendering_state == 'Playing' ",
                        "AND playback_data.timestamp < '", started[1], "'")
  
  sql_response <- dbGetQuery(mydb, sql_request)
  vmaf_min <- append(vmaf_min, strtoi(sql_response['min']))
  vmaf_max <- append(vmaf_max, strtoi(sql_response['max']))
  
  for (i in 1:(length(started)-1)){
    sql_request <- paste0("SELECT max(playback_data.playing_vmaf) AS max, ",
                          "min(playback_data.playing_vmaf)  AS min ",
                          "FROM playback_data ",
                          "WHERE playback_data.rendering_state == 'Playing' ",
                          "AND playback_data.timestamp between '",
                          finished[i], "' and '", started[i+1], "'")
    
    sql_response <- dbGetQuery(mydb, sql_request)
    vmaf_min <- c(vmaf_min, strtoi(sql_response[['min']]))
    vmaf_max <- c(vmaf_max, strtoi(sql_response[['max']]))
  }
}

vmaf_max <- data.frame(vmaf_max)
vmaf_min <- data.frame(vmaf_min)

vec_vmaf_max <- rescale(unlist(vmaf_max), to = c(0, 1), from = range(20, 100))
vec_vmaf_min <- rescale(unlist(vmaf_min), to = c(0, 1), from = range(20, 100))

vec_vmaf_max <- data.frame(vec_vmaf_max, vec_scores)
vec_vmaf_min <- data.frame(vec_vmaf_min, vec_scores)

# ggplot(data=vec_vmaf_max, aes(x=vec_vmaf_max, y=vec_scores)) + geom_point()
# ggplot(data=vec_vmaf_min, aes(x=vec_vmaf_min, y=vec_scores)) + geom_point()

# data preparation - 20 different VMAFs, can be changed in the future
data_ag_max <- vec_vmaf_max %>%
  mutate(vmf_cat = floor(vec_vmaf_max*20)) %>%
  group_by(vmf_cat) %>%
  summarise(vmf_max = mean(vec_vmaf_max), mos = mean(vec_scores))

data_ag_min <- vec_vmaf_min %>%
  mutate(vmf_cat = floor(vec_vmaf_min*20)) %>%
  group_by(vmf_cat) %>%
  summarise(vmf_min = mean(vec_vmaf_min), mos = mean(vec_scores))


# linear model
model_lin_max <- lm(mos ~ vmf_max, data_ag_max)
model_lin_min <- lm(mos ~ vmf_min, data_ag_min)

# plot(model_lin)
# summary(model_lin)

# ggplot(data_ag, aes(vmf, mos)) + 
#   geom_point() + 
#   geom_abline(intercept = as.numeric(model_lin$coefficients[1]), 
#               slope = as.numeric(model_lin$coefficients[2]), color = "red")

# power model
data_power_max <- data_ag_max %>%
  mutate(vmf_max = log(vmf_max)) %>%
  mutate(mos = log(mos))
model_pow_max <- lm(mos ~ vmf_max, data_power_max)

data_power_min <- data_ag_min %>%
  mutate(vmf_min = log(vmf_min)) %>%
  mutate(mos = log(mos))
model_pow_min <- lm(mos ~ vmf_min, data_power_min)
# plot(model_pow)
# summary(model_pow)

# ggplot(data_power, aes(vmf, mos)) + 
#   geom_point() + 
#   geom_abline(intercept = as.numeric(model_pow$coefficients[1]), 
#               slope = as.numeric(model_pow$coefficients[2]), color = "red")

# logit model
data_logit_max <- data_ag_max %>%
  mutate(mos = log(mos / (1 - mos)))
model_logit_max <- lm(mos ~ vmf_max, data_logit_max)

data_logit_min <- data_ag_min %>%
  mutate(mos = log(mos / (1 - mos)))
model_logit_min <- lm(mos ~ vmf_min, data_logit_min)
# plot(model_logit)
# summary(model_logit)

# ggplot(data_logit, aes(vmf, mos)) + 
#   geom_point() + 
#   geom_abline(intercept = as.numeric(model_logit$coefficients[1]), 
#               slope = as.numeric(model_logit$coefficients[2]), color = "red")

ggplot(data_ag_max, aes(vmf_max, mos)) +
  geom_point() +
  geom_function(fun = ~ as.numeric(model_lin_max$coefficients[1]) +
                  as.numeric(model_lin_max$coefficients[2])*(.x), color = "red") +
  geom_function(fun = ~ exp(as.numeric(model_pow_max$coefficients[1])) *
                  (.x)^as.numeric(model_pow_max$coefficients[2]), color = "green") +
  geom_function(fun = ~ exp(as.numeric(model_logit_max$coefficients[1]) +
                              as.numeric(model_logit_max$coefficients[2]) * (.x)) /
                  (1 + exp(as.numeric(model_logit_max$coefficients[1]) +
                             as.numeric(model_logit_max$coefficients[2]) * (.x))),
                color = "blue") +
  ggtitle('Maximal in period VMAF to MOS') +
  theme(plot.title = element_text(hjust = 0.5))


ggplot(data_ag_min, aes(vmf_min, mos)) +
  geom_point() +
  geom_function(fun = ~ as.numeric(model_lin_min$coefficients[1]) +
                  as.numeric(model_lin_min$coefficients[2])*(.x), color = "red") +
  geom_function(fun = ~ exp(as.numeric(model_pow_min$coefficients[1])) *
                  (.x)^as.numeric(model_pow_min$coefficients[2]), color = "green") +
  geom_function(fun = ~ exp(as.numeric(model_logit_min$coefficients[1]) +
                              as.numeric(model_logit_min$coefficients[2]) * (.x)) /
                  (1 + exp(as.numeric(model_logit_min$coefficients[1]) +
                             as.numeric(model_logit_min$coefficients[2]) * (.x))),
                color = "blue") +
  ggtitle('Minimal in period VMAF to MOS') +
  theme(plot.title = element_text(hjust = 0.5))

dbDisconnect(mydb)