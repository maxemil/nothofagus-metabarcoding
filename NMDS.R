library(vegan)
library(dplyr)
set.seed(2)

samples = read.csv('Nothofagus_plots_counts_genus.csv', sep='\t',
    header=TRUE,row.names=1)

# transpose and make to relative abundance
tsamples = t(samples)
reltsamples = decostand(tsamples, method = "total")

# transpose again and convert to tibble
ttib = as_tibble(t(as.data.frame(reltsamples)), rownames=NA)

# filter by minimum relative abundance in at least one plot (0.1%)
fttib = ttib %>% filter_all(any_vars(. > 0.001))
fil_rel_abundance = t(as.data.frame(fttib))

# distmat = vegdist(fil_rel_abundance, method='bray')

variables = read.csv('Sample_variables.csv', sep='\t',
    header=TRUE, row.names=1)
# pca of numerical variables 
#pca =rda(variables[,-c(1,2,22)])

my_NMDS=metaMDS(fil_rel_abundance, k=5, trymax=100, distance='bray')
# drop 'site'
variables = variables[-c(3)]
# fit all variables
ef <- envfit(my_NMDS, variables, permu = 999)
# fit only some variables
ef <- envfit(my_NMDS, variables[,c(3,5,10,17)], permu = 999)

pdf('Nothofagus_NMDS.pdf')
  pl = ordiplot(my_NMDS,type="none")
  points(pl, "species", pch=20, cex=0.3, col="chocolate1")
  orditorp(my_NMDS,display="sites",cex=0.7,air=0.1)
  ordispider(my_NMDS,groups=variables$tree.species)
  ordiellipse(my_NMDS,groups=variables$tree.species,draw="polygon",label=T, cex=.5)
  plot(ef, p.max=0.01)
dev.off()

pdf('nmds_contour.pdf')
pl = ordiplot(my_NMDS,display="species",type="points")
ordisurf(my_NMDS,elevation,main="",col="forestgreen", add=T)
orditorp(my_NMDS,display="sites",cex=1.25,air=0.01)
plot(ef, p.max = 0.05)
dev.off()

pdf('nmds_ellipse_contour.pdf')
  ordiplot(my_NMDS,display="species",type="points")
  orditorp(my_NMDS,display="sites",cex=1.25,air=0.01)
  ordiellipse(my_NMDS,groups=groups,draw="polygon",label=T)
  ordisurf(my_NMDS,elevation,main="",col="forestgreen", add=T)
dev.off()

pdf('Nothofagus_NMDS.pdf')
  plot(my_NMDS, 'sites')
  orditorp(my_NMDS, 'sites')
dev.off()


my.rda <- rda(fil_rel_abundance)
pdf('Nothofagus_PCA.pdf')
  biplot(my.rda, display = c("sites", 
                   "species"),
       type = c("text",
                "points"))
  ordihull(my.rda,
         group = variables$age,
         col = c(1,2,3))
  legend("topright",
       col = c(1,2,3), 
       lty = 1,
       legend = levels(variables$age))
dev.off()
