#klaR Package must be loaded before running this script
vs.method = "stepclass"
lvi.lda <- pvs(xDataset, CLASSIFICATION, prior = priorDistribution,
		method = "lda", vs.method = "stepclass", impr = 0.01, 
		fold = 10, direct = "both", out = FALSE)