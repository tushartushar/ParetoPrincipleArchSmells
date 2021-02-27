data_cs <- read.csv(file="/path/data/results/rq3_cs.csv", header=TRUE, sep=",")
loc <- data_cs[["LOC"]]
sd <- data_cs[["Pareto_category"]]
rq3.cs.corr.test = cor.test(x=as.numeric(sd), y=as.numeric(loc), method="spearman")
print("---------CS ------")
print(rq3.cs.corr.test)

data_java <- read.csv(file="/path/data/results/rq3_java.csv", header=TRUE, sep=",")
loc <- data_java[["LOC"]]
sd <- data_java[["Pareto_category"]]
rq3.java.corr.test = cor.test(x=as.numeric(sd), y=as.numeric(loc), method="spearman")
print("---------Java ------")
print(rq3.java.corr.test)

data <- read.csv(file="/path/data/results/rq3.csv", header=TRUE, sep=",")
str(data)
loc <- data[["LOC"]]
str(as.numeric(loc))
sd <- data[["Pareto_category"]]
rq3.corr.test = cor.test(x=as.numeric(sd), y=as.numeric(loc), method="spearman")
print("---------Combined ------")
print(rq3.corr.test)
pdf("/path/rq3.pdf", width=8, height=6)
plot(sd, loc, xlab="LOC", ylab="Pareto category", col=rgb(4, 62, 108, 50,maxColorValue=255), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
dev.off()
