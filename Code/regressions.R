rm(list = ls())

# Load necessary libraries
library(glmnet)
library(caret)
library(stargazer)
library(mice)
library(tidyverse)
library(dplyr)

# Load the data
data <- read.csv('Code & Data/Health Sector/aggregated_dummy_events_added.csv')
data$Date <- NULL
# View(data)

# Load necessary libraries
library(dplyr)
library(glmnet)
library(stargazer)
library(caret)


# Check data dimensions
print(dim(data))

# Prepare the dataset for regression
target <- data$ST.CM

# Select the columns to be scaled (excluding target and event variables)
features_to_scale <- data %>% select(-ST.CM, -DT.DT, -starts_with("EV"))

# Scale the features
preProc <- preProcess(features_to_scale, method = c("center", "scale"))
scaled_features <- predict(preProc, features_to_scale)

# Add event variables back to the scaled features
event_variables <- data %>% select(starts_with("EV"))
scaled_data <- cbind(scaled_features, event_variables)

# Define scenarios
scenario_with_all <- scaled_data  %>% select(-starts_with("ST"))
scenario_without_MA <- scaled_data %>% select(-starts_with("MA"), -starts_with("ST"))
scenario_without_MI <- scaled_data %>% select(-starts_with("MI"), -starts_with("ST"))
scenario_without_MA_MI <- scaled_data %>% select(-starts_with("MA"), -starts_with("MI"), -starts_with("ST"))

# Run OLS regression for each scenario

# Scenario 1: With All Variables
print("Running OLS for scenario: With All Variables")
model_with_all <- lm(target ~ ., data = scenario_with_all)
summary(model_with_all)

# Scenario 2: Without MA Variables
print("Running OLS for scenario: Without MA Variables")
model_without_MA <- lm(target ~ ., data = scenario_without_MA)
summary(model_without_MA)

# Scenario 3: Without MI Variables
print("Running OLS for scenario: Without MI Variables")
model_without_MI <- lm(target ~ ., data = scenario_without_MI)
summary(model_without_MI)

# Scenario 4: Without MA and MI Variables
print("Running OLS for scenario: Without MA and MI Variables")
model_without_MA_MI <- lm(target ~ ., data = scenario_without_MA_MI)
summary(model_without_MA_MI)

# Create a summary table using stargazer
stargazer(
  model_with_all, model_without_MI, model_without_MA,  model_without_MA_MI, 
  type = "latex", 
  title = "OLS Regression Results for Different Scenarios",
  dep.var.labels = c("ST-CM"),
  column.labels = c("With All",  "Without MI", "Without MA", "Without MA and MI"),
  omit.stat = c("f", "ser"),
  no.space = TRUE,
  digits = 2
)




