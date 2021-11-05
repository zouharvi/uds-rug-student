# DONT FORGET TO SET THE DIRECTORY OF THIS FILE AS WORKING DIRECTORY!!!

files <- list.files("./results")
numParticipants <- as.integer(length(files) / 2)


learningDf <- data.frame(read.csv("./results/subject-1.csv", skip = 1))
learningDf$participant <- 1
testingDf <- data.frame(read.csv("./results/subject-1Test.csv"))
learningDf$participant <- 1

for (i in seq(2,numParticipants)) {
  ldf <- data.frame(read.csv(paste("./results/subject-", i, ".csv")))
  tdf <- data.frame(read.csv(paste("./results/subject-", i, "Test.csv")))
}