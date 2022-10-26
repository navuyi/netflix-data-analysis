library("lubridate")

csv_files = list.files("../csv")
DATE_FORMAT = "%Y-%m-%dT%H:%M:%OS"

output_assessment <- c()
output_mean_vmaf <- c()

for(file in csv_files){
  data <- read.csv(file.path("../csv", file))
  
  playing_vmaf = data$playing_vmaf
  timestamp = data$timestamp
  assessment_value = na.omit(data$assessment_value)
  assessment_timestamp = data$assessment_timestamp # Removing NAs
  assessment_timestamp <- assessment_timestamp[assessment_timestamp != ""] # Removing empty strings 
  experiment_start <- data$timestamp[1]

  index <- 0
  for(assessment in assessment_value){
    # Increment index
    index <- index + 1
    
    current_timestamp = strptime(assessment_timestamp[index], DATE_FORMAT)
    if(index == 1){
      previous_timestamp = strptime(experiment_start, DATE_FORMAT)
    }
    else{
      previous_timestamp = strptime(assessment_timestamp[index-1], DATE_FORMAT)
    }
    t_delta = current_timestamp - previous_timestamp
    
    vmaf <- c()
    for(i in 1:length(playing_vmaf)){
      vmaf_timestamp = strptime(timestamp[i], DATE_FORMAT)
      if(vmaf_timestamp > previous_timestamp & vmaf_timestamp < current_timestamp){
        vmaf <- c(vmaf, playing_vmaf[i])
      }
    }
    output_assessment <- c(output_assessment, assessment)
    output_mean_vmaf <- c(output_mean_vmaf, mean(vmaf))
  }
}

plot(output_mean_vmaf, output_assessment)





