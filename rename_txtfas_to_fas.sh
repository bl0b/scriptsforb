#!/bin/bash
for TXTFASTA in *.txt.fas; do
    # %% removes the right part from the value
    # of the variable in the left part.
    FASTA="${TXTFASTA%%.txt.fas}.fas"
    mv $TXTFASTA $FASTA
done
