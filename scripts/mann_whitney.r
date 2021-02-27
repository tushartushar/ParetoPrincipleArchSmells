library(rcompanion)
library(effsize)

mann_whitney <- function(sample1, sample2, sample1_name, sample2_name) {
    cat("mann_whitney", sample1_name, sample2_name, "\n")
    test = wilcox.test(sample1, sample2)
    print(test)
    d=cohen.d(sample1, sample2, hedges.correction=TRUE)
    print(d)
    return(d)
}

data_cs = read.csv("/data/results/pareto_cs.csv")
data_java = read.csv("/data/results/pareto_java.csv")

mann_whitney(data_cs[["Pareto_category"]], data_java[["Pareto_category"]], "CS", "Java")
