This is a collection of scripts used for the publication *Ectomycorrhizal fungal communities in andean-patagonian Nothofagus forests*.

The general workflow was as follows:
1. get data as fastq files, perform trimming and assembly (merging) of paired-end reads. Sequencing data has been deposited under BioProject ID PRJNA970541.
2. filter short (<150bp) reads and remove potential chimeras
3. get stats (very slow) for each step of the preprocessing pipeline
    `sequence_stats.py`
4. perform taxonomic annotation using the ITS refSeq (PRJNA177353) Database 
    `bash chimera_malt.sh`
5. summarise taxonomic annotations on different labels for each replicate and combined per plot
    `get_tax_level.py`
6. make abundance plot based on the order level
    `make_abundance_plot.py`
7. run FunGuild for ecological annotation on the genus level
    `run_FunGuild.py`
8. calculate diversity indices resp. Hill numbers
    `Diversity_indices.R`
9. perform NMDS
    `NMDS.R`