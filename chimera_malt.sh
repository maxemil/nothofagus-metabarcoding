

mkdir -p chimera_filtered 
mkdir -p maltout

for f in assembled_reads/*.fastq
do
	sample=$(basename ${f%.fastq})
	# convert to fasta and remove all seqs <150
	seqtk seq -L 150 -A $f > chimera_filtered/"$sample"_150.fasta

# remove chimeric sequences
	/local/two/Software/vsearch-2.15.1/bin/vsearch --uchime_ref chimera_filtered/"$sample"_150.fasta \
        	--db ../Fallopia/fungi.ITS.fna --threads 40 \
        	--nonchimeras chimera_filtered/"$sample"_nochimera.fasta \

	/local/two/Software/malt/malt-run --mode BlastN \
		--alignmentType SemiGlobal \
       		--inFile chimera_filtered/"$sample"_nochimera.fasta \
       		--index ITSREFSEQ \
       		--numThreads 40 \
       		--topPercent 5 -o maltout

	/local/two/Software/megan/tools/rma2info -i maltout/"$sample"_nochimera.rma6  \
        	-c2c Taxonomy \
        	-p > maltout/"$sample"_nochimera.c2c
done
