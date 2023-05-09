library(vegan)

samples = read.csv('Nothofagus_plots_counts_genus.csv', sep='\t',
    header=TRUE,row.names=1)

tsamples = t(samples)
reltsamples = decostand(tsamples, method = "total")


    
shannon = diversity(reltsamples, index='shannon')
rn = renyi(reltsamples, hill=TRUE)

pdf('diversity.pdf',height=10,width=15)
    plot(rn, layout=c(4, 4),xlab='order of diversity')
dev.off()

pdf('specaccum.pdf',height=10,width=10)
    plot(specaccum(reltsamples,method='random'), ci.col="red",
		ylab='Number of species', xlim=c(1,18), xaxp=c(0,18,3), cex.lab=1.4, cex.axis=1.4)
dev.off()

# write.csv(rn, 'Hill_diversity.csv')
########## diversity in one plot #############
library(ggplot2)
library(reshape2)

rn = as.data.frame(rn)

variables = read.csv('Sample_variables.csv', sep='\t',
    header=TRUE, row.names=1)
    
rn$site = paste0('site',variables$site)
rn$plot = rownames(rn)

y = melt(rn)
pdf('diversity_in_one.pdf',height=7,width=10)
	ggplot(y, aes(x=variable,y=value,group=plot,col=site)) +
		geom_point() +
		geom_line(linetype="dotted") +
		scale_y_continuous() +
		labs(y='Diversity',x='Order of diversity') +
		theme_bw() +
		theme(panel.grid.major = element_blank(), legend.position = c(0.90, 0.80),legend.key = element_blank())
dev.off()
#		scale_color_manual(values=c("#cc3399", "#e60000", "#ff9900", "#53ff1a", "#66ccff", "#1a1aff"),name='Site') +
