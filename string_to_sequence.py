"""Converts the plasmid template strings into actual sequences, using library of genetic components. Also checks
for the sequence/cloning idea in literature via semantic scholar API and then predicts transformation effeciency.

- Split backbone into string
- Identify features
- Recompile
- Do not forget to add start/stop codons in processing
"""
import requests


def get_gene_sequence_ncbi(accession):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=fasta&retmode=text"
    response = requests.get(url)
    return response.text

# Example usage
accession_number = "NM_001301717"
sequence = get_gene_sequence_ncbi(accession_number)
print(sequence)
