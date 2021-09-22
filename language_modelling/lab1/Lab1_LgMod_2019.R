
##############################################
# Language Modelling 2019
# 
# Computer Lab 1
# Categorical data - TVJ
# 
# Jennifer Spenader & Ana Bosnic
#################################################################

# Clear the memory with the following command
rm(list=ls(all=T))

# You will need certain packages to analyze your data. if it is your first time to open R Studio, you first need to INSTALL packages
# In that case, you need to rund install.packages command. If the command below doesn't work, use Tools and isntall packages one by one

require(ggplot2)
require(foreign)
require(psych)
require(lme4)
require(multcomp)
require(languageR)

install.packages("ggplot2", "foreign", "languageR", "psych", "lme4","multcomp")

# Call the packages with the library command. These are only essential packages but you will probably need more later

library(ggplot2)
library(foreign)
library(languageR)
library(psych)
library(lme4)
library(multcomp)

############################################################################
# Now you have to set the working directory to your own directory
# Alternatively if you have the datafile and this file in the same folder, you can
# use the menu item "Session" and choose "Set working directory"- "to source file location"
######################################################################

#setwd ("C:/")

# OK, now you have your directory set, check the contents

dir()

# Read in the data, either as table or as csv file. We will use csv (change as needed below!)
# Note that sometimes, when you convert to csv, the separation is not always "," (despite the name "comma separated values" but a semi-colon
# (RStudio users, check in the "Global Environment" that you have the correct number of variables. HINT: If the Data is listed as having X obs. of 1 variable, then the separations is not correct!)
# This is not only the command for reading the file, but actually storing it under a new data vector called expdat with the command <-
############################################################################################################################################

expdat<- read.csv(file="Lab1_LgMod_2019.csv", header=TRUE, strip.white = TRUE,sep=";")

# Now we have a new data set called expdat. You can see it in the Environment section on the right. If you click on it, you will see your full data set


# There are series of useful commands in R that can help you get a general overview of the data.
# Check that the data is correctly read by using summary() or str() commands
####################################################################################################
summary(expdat)


# Check what the names of the variables are (from the Heading of the table) using names()
##########################################################################################
names(expdat)


# Symbol $ is used to extract the information of a specified variable, so expdat$Gender gives you information about Gender variable
# You can see, in a table view, information about a single variable called ID (unique code names for the subjects who participated in the test)
# by useing the command table() and extracting info about the subjects. Give it a try below:

################################################################################################################################################
table(expdat$ID)


# length(unique()) gives you information how many people did the experiment. Try using length without the command unique, what do you get?
length(unique(expdat$ID))

 
# Often you will have some participants who did not finish the test and have less responses. This is especially the case if the experiment
# is done online, becasue many people don't finish and/or realize they actually don't want to do this. Regression tolerates missing data so 
# in this data set we will tolerate up to 10% (5 items) of missing data points.
#
# If you see that some participants have more than 5 missing data points, you need to remove them from the data set
# But first let's make the practice dataset easier to use. 

# This practice data set has very complex names for subjects (unnecessarily long and confusing due to the old code we used) 
# but you normally want to code them numerically 
# and that will make things easy to select and remove.
# Here's the code to do it
# create a new column in the dataframe, fill it with something
# expdat$newID <-NA 
# Check that it's there!
# names(expdat)
# Now if you modify the existing ID variable, to make it a factor that is numeric, you'll 
# get a unique number for each subject. Much easier to work with. 
# expdat$newID <- as.numeric(as.factor(expdat$ID))
expdat$newID <-NA 
names(expdat)
expdat$newID <- as.numeric(as.factor(expdat$ID))

# Now we can remove people who didn't complete the experiment (or because we don't like them and believe they 
# have weird ideas about distributivity(* just kidding!))
# To do this, you need to use the command subset, in which you make a subset of your data set and you can store it in the new vector or the same one
# but then you overwrite the old data. The advice is to save to new vector sets, just to be on the safe side.
#
# Before we try the subset command, let's make a copy of our data set. 
# TASK 1: Make a copy in a new vector called "dat"
dat <- expdat
names(expdat)
dat$ID

# Let's operate now with this new copy and make it cleaner
# TASK 2: Remove the participants who have more than 5 data points missing and store it under the new data set called "data"
#tmpdat <- subset(dat, id %in% )

# check which user got up to 48-5th question
# an alternative solution would be to use table but that's not straightforward because if someone tried the experiment twice up to question 25,
# then they did not answer most of the questions (see dat[dat$newID == 1,])
okusers = unique(dat[(dat$Qnum == 48-5),]$newID)
# number of all users
length(unique(dat$newID))
# number of ok users
length(okusers)
# number of incomplete users
length(unique(dat$newID)) - length(okusers)
# manual check for one user (e.g. 68)
setdiff(unique(dat$newID), okusers)
dat[dat$newID == 68,]

# subset the data
dat = subset(dat, newID %in% okusers)
length(unique(dat$newID))

# There are two ways to subset the data. One is to exclude the values and one is to make a vector with values you want to include. 
# That means that for TASK 2 you can also make a vector listing all the values you want to have in, except the first two. Choose the
# most convenient way to subset your data.
# You can use the following formula:
# dataset <- subset(old.dataset,  id %in% c(name1, name2, name))


# The variable NativeLg is to check who is a native speaker and who is not. In the practice data set, 1 is coded for YES, 2 for NO
# TASK3: Check if there are non-native speakers using the table command and extracting the information about Lang variable
################################################################################################################################
table(unique(dat[c("NativeLg", "newID")])$NativeLg)

#####################################################################
# (Actually almost everyone is non-native. We aren't going to remove them, but in a real experiment we would)
######################################################################

#You can also use the subset command to remove other things, like all fillers, controls, etc
# TASK4: Use the summary() again and check your independent variables (fixed factors).
# Right now they are labeled as letters and there is no way you know what they mean Below you can see the decoded version:
# Condition a is a sentence without each with a collective picture
# Condition b is a sentence with each with a collective picture
# Condition c is a sentence without each with a distributive picture
# Condition d is a sentence with each with a distributive picture
# Condition e is a filler
# Condition f is a control
# You need to remove controls and fillers from the data set because you are not interested in those responses.
# Make a new copy of the data set with cleaner data
# BTW what's the best thing about Switzerland? I think it's the flag. It's a big plus. (Haha! But seriously
# read all the instructions.)
dat = subset(dat, !(Sentence %in% c("e", "f")))
summary(dat)

# Letters used to code the conditions need to be renamed (especially because they are the same in both factors). In other words, levels of the 
# factors need to be changed
# TASK 5: Use the command: levels(DATASET[,"FACTOR1"]) <- list(NAME="a", NAME="b", NAME="c", NAME="d")for both factors
# apply this formula:
# dat <- levels(dat[,"Sentence"]) <- list(No_Each="a", Each="b", No_Each="c", Each="d")
# dat <- levels(dat[,"Picture"]) <- list(Coll="a", Coll="b", Dist="c", Dist="d")
# Check if the change was successful with summary() 
levels(dat[,"Sentence"]) <- list(No_Each="a", Each="b", No_Each="c", Each="d")
levels(dat[,"Picture"]) <- list(Coll="a", Coll="b", Dist="c", Dist="d")
summary(dat)

# This data set is now very neat and tidy, so it is easy to get it ready for the analysis. 
# 
# However, you will usually end up with a set with missing values. 
# That is one of the things you need to check first.
# In R, missing values are represented by the symbol NA (not available) .
# Impossible values (e.g., dividing by zero) are represented by the symbol NaN (not a number). 
# You can use is.na() to test for NA's
# Thankfully we don't have those here (??????)
sum(is.na(dat$NativeLg))
dat[is.na(dat$NativeLg),]

###########################################################################################################################################################
#
# Ok, now we have a nice, clean data set, ready to analyze. 
# First, you should see how many people did the test, what is the mean age and SD and how many female/male participants there are
#
#############################################################################################################

# Check how many people did the experiment (after the clean-up):
length(unique(dat$newID))


# Get the mean age, SD of age etc. for reporting in the Results
# Check if there are NA in Age. You can do this in the following set of commands

agedat <- subset(dat, Age !="NA")
agedat <- unique(dat[,c("newID","Age")])
describe(agedat)


# Gender information
# TASK 6: Using the same formula,make a new vector genderdat (you don't have to check for NA's)
genderdat <- unique(dat[,c("newID","Gender")])

# You can use the following formula to check how many male/female participants did the test

with(genderdat,table(Gender))

# This does the same thing but only gives info for how many male participants

length(which(genderdat$Gender =="m"))


###################################################################
#
# MEAN RATINGS
#
###################################################################
# For each Factor and factor combination see what the rating was. 
# If you type this you'll get the mean and the sd and se for each factor combination.
# with(dat, describeBy(DEP_VAR, list(FACTOR_1, FACTOR_2)))
with(dat, describeBy(Answer, list(Gender, Sentence)))


# SUBJECT DATA FOR RESULTS
############################################

# If you remind yourselves what was the structure of the data set (str) you will see the type of each variable
# Some are labeled as int (=integers), some as Factors. You need to define two types of factors - fixed and random
# Fixed factors are your independent variables and you can add anything as a factor, as long as you think it will have an impact 
# on the results (which is something we will need when finding the models, not here)

# Define the FIXED FACTORS. Sometimes as.factor doesn't work (when you check if something is a factor, it returns FALSE)
# Then you should use a formula that basically stores the newly defined factor under the same variable: dat$FACTOR <- as.factor(dat$FACTOR)

# TASK 7: decide which variables need to be factors in the practice data set and convert them. 
# TIP: Use str() to get the overview what is a factor and what is not. Don't forget to define items and subjects as (random) factors too
# Question: Is age a factor? In other words is there any relationship between `21 years` and `22 years` or is it just catogorical (like colors)?
# I'll give you the answer: it is numeric. Because 21 is less old than 22. This means that Age has to be num: dat$FACTOR <- as.numeric(dat$FACTOR)
dat$Sentence <- as.factor(dat$Sentence)
dat$Picture <- as.factor(dat$Picture)
dat$NativeLg <- as.factor(dat$NativeLg)
dat$Gender <- as.factor(dat$Gender)
dat$Item <- as.factor(dat$Item)
dat$Answer <- as.logical(dat$Answer)
dat$newID <- as.factor(dat$newID)
dat$ID <- as.factor(dat$ID)

dat$Age <- as.numeric(dat$Age)
summary(dat)

# TASK 8: Check if they are factors using is.factor()
is.factor(dat$Sentence)

######################################################################################################
# How many lists are done? use table(). This is just to get an overview of the balance between lists
table(table(dat$newID))

# What are the mean responses for each type?
# TASK 9: Fill in the names of variables and make a new vector with the results 

response.mean <- with(dat,aggregate(list(DEP_VAR=dat$Answer),list(FACTOR1=dat$Sentence, FACTOR2=dat$Gender),mean))

# Let's look at the aggregated results
response.mean

# You can check the means per subject to see if there are some weird participants that you need to exclude
aggregate(dat$Answer, by=list(dat$newID, dat$Sentence, dat$Gender), mean)

# You can see the scores per subject (not means). This can be useful if you have means that are at chance level, so you
# may suspect there are two populations of people, rather than everyone is simply at chance (you don't want that :))

table(dat$Sentence, dat$newID, dat$Gender, dat$Answer)
with(dat,table(dat$Answer, dat$Sentence, dat$Gender))

# DescribeBy is the command from the (psych) package and it gives you the basic statistics (the means, SD and SE) for reporting the results

describeBy(dat$Answer, list(dat$Sentence, dat$Gender), mat=TRUE,digits=2)


# You are now ready to make graphs. Scatter plots and histograms are not very informatiive for categorical data, so we will only make barplots for this lab

##############################################################################################################################################
#
# PLOTS and GRAPHS!!!
#
##############################################################################################################################################

# For the purposes of this lab, we will make the plots in Excel and in R, but then you will decide which one you like the most. 
# TASK 10: Make the graphs with standard error in excel first. 


# Alternatively, and more commonly, people plot their data in R (more options). We will try one "official" way of plotting, using the 
# package ggplot2 and one more alternative and fun...

# TASK 11: Make the barplots using ggplot2. Fill in the variables and se values

library(ggplot2)

se = c(´) #fill in the se values, start from the value that is on the first bar (left-most bar)
limits <- aes(ymax = dat$Answer + se, ymin=dat$Answer - se)
dodge <- position_dodge(width=0.9)

ggplot(response.mean, aes(factor(dat$Sentence), dat$Answer, fill = dat$Gender)) + 
  geom_bar(stat="identity", position = "dodge") + geom_errorbar(limits, position=dodge, width=0.25)+
  scale_fill_brewer(palette = "Set3")


# Task 11: A different way to make graphs is to use a fun package called yarrr and make pirate bars!
# You need to install two packages before you start. Later, you can comment those commands out, because you need to 
# install them just that one time. In the future uses, just call them by library commands


install.packages("devtools", "pbapply", "gtools", "yarrr")
library("devtools")
library("yarrr")
require("BayesFactor")


# To be on the safe side, make a copy of your data, call it dat1:


pirateplot(formula = DEP_VAR ~ FACTOR1 + FACTOR2,
           data = DATASET,
           main = "NAME", #give it an appropriate name
           theme = 2,
           pal = "southpark", # changing the color pallette, you can find out about other pallettes if you see it in the Help tab on the right
           xlab = "NAME", #give it an appropriate name
           ylab = "Proportion of YES responses",
           point.pch = 16,
           point.o = .1, #opacity of the points
           hdi.o = .0,
           bar.f.o = .5,#opacity of the bars
           avg.line.o = .5,
           inf.method = "se",
           gl.col = gray(.6), # Gridline specifications
           gl.lty = 0,
           gl.lwd = c(.5, 0))

# Standard error is calculated automatically in pirateplots


#############################################################################################################################################################
#
# MIXED-EFFECT MODELS
#
#############################################################################################################################################################

# There are series of useful commands in R that can help you get a general overview of the data.
# Check that the data is correctly read by using summary or str commands. Choose the cleanest copy of the data set you have for modelling
####################################################################################################


###############################
# MIXED EFFECTS MODELS
###############################

################################################################################
# The meaning of some symbols in the formulas for models
#       '+' = ADDITIVE MODEL
#       '*'= LOOK FOR AN INTERACTION
#       'a ~ b'= TRY TO EXPLAIN THE VARIATION IN a BY THE FEATURES GIVEN IN b / a PREDICTED BY b
#       '(1| name) = (random intercept for subject) USE DIFFERENT INTERCEPTS FOR EACH PERSON, E.G. EACH SUBJECT WILL HAVE A DIFFERENT BASELINE REACTION TIME SPEED
#       '(1| item) = (random intercept for item) EXPECT ITEMS TO ALSO HAVE DIFFERENT BASELINE READING SPEEDS, 
#        TAKE THAT INTO ACCOUNT BY LETTING THEM EACH HAVE A DIFFERENT INTERCEPT 
#        
###############################################################################
# You need to use the package lme4
# 
# lmer formula is for continuous variables (and Likert scale ratings) 
# glmer formula is for categorical variables (+ you need to specify family=binomial to indicate binary data)
# 
# In your model formula you include both fixed and random effects. You can start from a full intercept model and then add factors and random slopes,
# or you can start from the most complex model and delete factors in a stepwise manner. I suggest the first strategy.
# 
# You should also do the additive model before you move on to interactions
#
# ADDITIVE MODEL: In other words, the effect of Fixed factor 1 (FF1) on the response (dependent variable) does not depend on the value of Fixed factor 2 (FF2), 
# and the effect of FF2 on dependent variable does not depend on the value of FF1
#
# INTERACTION MODEL:  In other words, the effect of FF1 on dependent variable depends on the value of FF2, or the effect of FF2 
# on dependent variable depends on the value of FF1
#
# When you run a model, you can summarize it with the summary command and see the output
# You compare the model with the anova command (anova command is not the same as ANOVA, which is a statistical test for variance)
#
# WARNING: when the model fails to converge and you get some warning messages, try using different optimizers. bobyqa usually works
# If the model is too complex, model will probably fail to converge despite the optimizers 
#
# Let's start with the model that doesn't have any fixed effects. You, of course, suspects that that model will be bad because
# you didn't specify any factors except random factors, so you basically asked: can I explain my data with subjects and items only:
################################################################################

model_0 <- glmer(Answer ~ (1|id) + (1|Item), data=dat, family = binomial)
summary(model_0)

# You didn't find anything from model_0, let's start adding factors. Maybe our data can be explained with Picture factor only. This means that types of pictures
# can influence the data alone. 

model_1 <- glmer(Answer ~ Picture + (1|id) + (1|Item), data=dat, family=binomial)
summary(model_1)

# Estimate and z values are important for the results.
# Estimates are the values how different one variable is from the other (in logistic regression these values are logs so it is 
# at first hard to interpret them, but there are formulas that transform this into meaningful values for interpreting). For continuous values
# these values are actual measurements (ms for RT data, etc).

# Z value is the regression coefficient divided by its standard error.
# If the z-value is too big in magnitude (i.e., either too positive or too negative),
# it indicates that the corresponding true regression coefficient is not 0 and the corresponding X-variable matters. 
# A good rule of thumb is to use a cut-off value of 2 which approximately corresponds to a two-sided hypothesis test with a significance level of \alpha=0.05. 
# So, for the Picture variable, what is the z-value? What does this mean?

# However, we only started. By looking at graphs, you also see that results change when SType changes, so let's add this variable to our model. 

model_2 <-

# We see an effect of SType too. OK, let's compare the models now
anova(model_1, model_2)

# When assessing the better model, you should look at the AIC score (this is what is generally advised, the math behind this coefficient is a bit complex)
# You choose the model with the lowest AIC, because this means it is closer to explaining your data accurately. If the difference between two AIC scores is less or equal to 2
# it is understood there there are no real differences between the models and you can choose either. However, in that case, you choose the one that is simpler (less Df (degrees
# of freedom))
# For us, the better model is model_2

# Let's see the interaction model. Do you expect an interaction of picture and sentence? Use * for interactions

model_3 <- 
summary()

# Compare the previous best model with the interaction model
anova()

# Take the new best model and run it witout items (we generally make sure that items are similar enough so there wouldn't be an effect). Then compare

model_4 <- 
  


# Check if Age is a predictor. Add it to your new best model

model_5 <- 

############ If you get convergence failures, first try possible optimizers:
# Add this to your formula: control = glmerControl(optimizer="bobyqa")
# If bobyqa fails, try "Nelder_Mead"
# If that one fails, check it with the following formulas.
# Model fit check:

# source(system.file("utils", "allFit.R", package="lme4"))
# mod.all <- allFit(YOUR_MODEL)
# ss <- summary(mod.all)
# ss$ fixef               ## extract fixed effects
# ss$ llik                ## log-likelihoods
# ss$ sdcor               ## SDs and correlations
# ss$ theta               ## Cholesky factors
# ss$ which.OK            ## which fits worked
##############

###############################################
# Add Random slopes for individuals and questions, because you should expect the variations with subjects. If you excluded items above (that is, if you found the models
# don't differ with or without items) then you should just continue without items for random slopes too.
# Try writing the formula for random slopes alone. Copy the best model you found so far and then in places for random effects (1|id) and (1|Item) (if you have items), add the 
# fixed factors. Basically, you are asking the model if there are differences with the subjects if they see Factor1, Factor2 or both.
# So, if you suspect people behave differently when they see different Pictures, you should put (1 + Picture |id), etc. Use optimizers if the model doesn't converge
# Check all possible combinations and compare them with anova. 
# Discover what is the best final random slope model.
##############################################


# Extract the fixed effect output for reporting in the results:
summary(BEST_RS_MODEL)$coef 

###############################################################
# POST-HOC tests 

# If you had the interactions, here is how you check where the interaction is present (which levels interact)
# With the glmer you only get the relationships between the intercept and other variables, and the intercept is actually just automatically assigned 
# (based on the first letter in alphabet). In case you are interested in only one level of the variable and you want that to be your reference point, you can relevel 
# and run the model again, making your desired level your reference point.
#
# dat$SType <- relevel(dat$SType, "3-each-2")
# dat$Picture <- relevel(dat$Picture, "dist")
# 
# This formula will make the level 3-each-2 and the level dist (or whatever you named them), your reference points, and the intercept will be that
#
# If you are, on the other hand, interested in multiple level comparisons, you can use multcomp or lsmeans to get this statistical test done
#################################################################################################################

# Add the interaction variable you want to check (it will appear as a new variable in your data set)

dat$FF1_FF2 <- interaction(dat$FF1, dat$FF2)

# Make a model with the interaction variable (use the best random slope model you found)

# the_best_model <- glmer(Answer ~ FF1_FF2 + .....

# Several ways to get the comparisons

library(multcomp)

summary(glht(the_best_model, mcp(FF1_FF2="Tukey")))

sign_contrast <- glht(the_best_model, linfct=mcp(Picture_SType="Tukey")) 
summary(sign_contrast)

library(lsmeans)

lsmeans(BEST_RS_MODEL, pairwise~FF1*FF2, adjust="tukey")
summary(glht(BEST_RS_MODEL, linfct = lsm(pairwise ~ FF1*FF2)))

pairs(lsmeans(the_best_model, ~ FF1_FF2, adjust = "mvt"))


# Remember how Estimates for logistic regression are logs of the values? Well, you can use plogis command to interpret logit coefficients.
# You can type 1 if you want that level of a factor to be "switched on" and 0 if they want to exclude the levels from the calculations

plogis(fixef(BEST_RS_MODEL)["(Intercept)"] + 1*fixef(BEST_RS_MODEL)[""] + 1*fixef(BEST_RS_MODEL)[""])


# Use round() to round up the coefficients
round(summary()$coef,3)


# For the lab report: Find the best model, report the output and make sure that the names of the variables make sense, don't leave SType3-2 (or whatever name you gave)
# because that is uninterpretable to the reader. 
# Explain the results using the information from the model. Say explictly what is significant, report the main effects and interactions (if there are any)
# Here is the example from another experiment:
#
# We used a logistic mixed effects model and a stepwise variable deletion procedure, starting with the complete interaction model, and including random slopes. 
# The best fitting model had Verb Type (NP1 or NP2)as a predictor, and the interaction between VerbtType and Pronoun Type (Stressed vs. Unstressed),
# as well as Random Slopes for VerbType. NP2 verbs were significantly more likely to have object continuations than NP1 verbs (p < 0.000). 
# The effect of Pronoun Type was not significant (p = 0.06).
# The model retaining the interaction between Verb Type and Pronoun Type was a better first, but pairwise comparisons showed no relevant, significant interaction effects. 
# The model is given in Appendix A.

# Then you should make a table in the Appendix and copy your output.
