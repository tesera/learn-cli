#Run MANOVA
a = (cbind(B1_MEAN,B3_MEAN,LVI_CENTX,LVI_CENTY,LVI_NDVI45M))
MV <- manova(a  ~ CLASSIFICATION, data=xDataset)
MV.lm <- lm(CLASSIFICATION~, data=xDataset)
