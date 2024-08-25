import sounddevice as sd
import soundfile as sf
import queue
import os
from openai import OpenAI
import requests


client = OpenAI(api_key="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")

pXP420_sites = {
    "SPEI": 427,
    "ECORV": 435,
    "PAER7I": 445,
    "CYC1": 467,  # Only the first value is kept
    "PPUMI": 542,
    "BSRGI": 616,
    "MLUI": 623,
    "ZRAI": 821,
    "AATII": 823,
    "PFOI": 934,
    "BSTAPI": 1073,
    "KASI": 1123,
    "NARI": 1124,
    "SFOI": 1125,
    "PLUTI": 1127,
    "M13/PUC FORWARD": 1252,  # Only the first value is kept
    "M13 FORWARD": 1266,  # Only the first value is kept
    "BFUAI": 1292,
    "SPHI": 1297,
    "SBFI": 1303,
    "SALI": 1305,
    "HINCII": 1307,
    "BAMHI": 1317,
    "BSABI": 1731,
    "MSCI": 1881,
    "BSMI": 1886,
    "AVRII": 1994,
    "SFII": 1998,
    "BSTXI": 2066,
    "BSIWI": 2089,
    "NHEI": 2181,
    "BMTI": 2185,
    "ALEI": 2236,
    "BCLI*": 2225,
    "BSSHII": 2485,
    "ECO53KI": 2584,
    "BANII": 2586,
    "SNABI": 3235,
    "BMGBI": 3673,
    "MFEI": 3885,
    "XCMI": 3884,
    "M13 REV": 3955,
    "M13 REVERSE": 3955,  # Only the first value is kept
    "LAC": 3968,
    "CAP": 3968,
    "BSPQI": 4180,
    "L4440": 4186,  # Only the first value is kept
    "PBR322ORI-F": 4437,  # Only the first value is kept
    "ALWNI": 4712,
    "PSPFI": 4604,
    "BSEYI": 4600,
    "NMEAIII": 5337,
    "BSRFI": 5269,
    "BPMI": 5259,
    "AHDI": 5189,
    "TSOI": 5588,
    "SCAI": 5669,
    "AMP-R": 5739,  # Only the first value is kept
    "BTGZI": 58
}

pET15_sites = {
    "ECORI": 7735,
    "BLPI": 7467,
    "BAMHI": 7414,
    "PAER7I": 7409,
    "SACII": 6971,
    "KPNI": 6953,
    "ACC65I": 6949,
    "SNABI": 6641,
    "BSRGI": 6572,
    "PSII": 6532,
    "STUI*": 6133,
    "NDEI": 5372,
    "6XHIS": 5372,
    "NSII": 5321,
    "XBAI": 5276,
    "LAC": 5230,
    "T7 PROMOTER": 5230,
    "T7": 5230,  # Only the first value is kept
    "BGLII": 5210,
    "SGRAI": 5169,
    "PBRREVBAM": 5127,  # Only the first value is kept
    "SPHI": 5021,
    "ECONI": 4956,
    "LACI-R": 4805,  # Only the first value is kept
    "MLUI": 4488,
    "BCLI*": 4474,
    "BSTEII": 4306,
    "APAI": 4285,
    "PSPOMI": 4281,
    "BSSHII": 4077,
    "PSHAI": 3647,
    "NRUI": 3389,
    "FSPAI": 2907,
    "BSMI": 3006,
    "ALWNI": 1475,
    "PBR322ORI-F": 1729,  # Only the first value is kept
    "L4440": 1982,  # Only the first value is kept
    "BSPQI": 2001,
    "PRS-MARKER": 2082,  # Only the first value is kept
    "PFIFI": 2142,
    "PGEX3'": 2242,  # Only the first value is kept
    "SSPI": 191,
    "AMP-R": 427,  # Only the first value is kept
    "SCAI": 515,
    "PVUI": 627,
    "PSTI": 754,
    "BSAI": 930,
    "AHDI": 996
}


pBABE_sites = {
    "AMPR_PROMOTER": 4975,
    "SSPI": 4975,
    "XMNI": 4770,
    "AMP-R": 4721,  # Start and end positions
    "SCAI": 4651,
    "PVUI": 4541,
    "FSPI": 4393,
    "NOTI": 4050,
    "PBR322ORI-F": 3430,  # Start and end positions
    "DRAI": 3397,
    "AFLIII": 3289,
    "L4440": 3179,  # Start and end positions
    "BSPQI": 3173,
    "BMTI": 2492,
    "NHEI": 2488,
    "DRAIII": 2331,
    "BSPDI": 2414,
    "PURO-F": 2256,  # Start and end positions
    "SACII": 1974,
    "BSIWI": 1816,
    "BSPEI*": 1873,
    "RSRII": 1876,
    "PURO-R": 1760,  # Start and end positions
    "HINDIII": 1751,
    "AVRII": 1735,
    "SFII": 1688,
    "SV40PRO-F": 1663,  # Start and end positions
    "NCOI": 1642,
    "PBABE 3'": 1416,  # Start and end positions
    "HINCII": 1407,
    "ACCI": 1406,
    "SALI": 1405,
    "ECORI": 1387,
    "BSAAI": 1382,
    "BAMHI": 1363,
    "NAEI": 1358,
    "NGOMIV": 1356,
    "PBABE 5'": 1326,  # Start and end positions
    "PLXSN 5'": 1288,  # Start and end positions
    "BSRGI": 1238,
    "AFEI": 879,
    "SPEI": 616,
    "BFUAI": 8
}



def gpt_call(query, string):
    # Grab context from file
    with open(string, 'r') as file:
        context = file.read()

    completion = client.chat.completions.create(
        model="gpt-4-0613",
        temperature=0,  # Change to mess with determinism
        messages=[
            {"role": "system",
             "content": context},
            {"role": "user", "content": query}
        ]
    )
    return completion.choices[0].message.content


def transcribe_audio(filename, client):
    sample_rate = 44100
    channels = 1  # don't change does not work if != 1
    """Record audio until the Enter key is pressed."""
    # delete file from last fxn call
    if os.path.exists(filename):
        os.remove(filename)

    # Setup to record indefinitely until stopped
    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(indata.copy())

    q = queue.Queue()

    # Start the recording
    with sf.SoundFile(filename, mode='x', samplerate=sample_rate, channels=channels, subtype=None) as file:
        with sd.InputStream(samplerate=sample_rate, device=None, channels=channels, callback=callback):
            print("Recording started. Press any key to stop.")
            input()  # wait for key press to stop recording
            print("Recording stopped.")

            # Stop the recording and write data to the file
            while not q.empty():
                data = q.get()
                file.write(data)

    # transcribe into text w/ gpt
    audio_file = open(filename, "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcription


def novelty_check(query):
    # Base URL for Semantic Scholar API
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    # Parameters for the API call
    params = {
        "query": query,
        "fields": "title,abstract,authors,year",
        "limit": 5  # Number of results to return (can be adjusted)
    }

    # Make the request to the API
    response = requests.get(base_url, params=params)

    # Initialize an empty string to store the results
    result_string = ""

    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        if results.get("data"):
            result_string += f"Found {len(results['data'])} papers related to the query '{query}':\n\n"
            for i, paper in enumerate(results['data']):
                result_string += f"{i + 1}. Title: {paper['title']}\n"
                result_string += f"   Authors: {', '.join([author['name'] for author in paper['authors']])}\n"
                result_string += f"   Year: {paper['year']}\n\n"
        else:
            result_string += f"No relevant papers found for the query '{query}'.\n"
    else:
        result_string += f"Failed to fetch data from Semantic Scholar API. Status code: {response.status_code}\n"

    return result_string


def get_sequence_by_accession(accession_number):
    # NCBI efetch URL
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    # Parameters for the request
    params = {
        "db": "nuccore",  # or "protein" if you are retrieving a protein sequence
        "id": accession_number,  # The accession number
        "rettype": "fasta",  # Retrieve in FASTA format
        "retmode": "text"  # Get plain text format
    }

    # Send the request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Unable to fetch data (status code {response.status_code})"


def insert_string_at_index(original_string, index, string_to_insert):
    """
    Inserts a string into another string at a specified index.

    Parameters:
    - original_string: The original string where the insertion will happen.
    - index: The position in the original string where the new string will be inserted.
    - string_to_insert: The string to insert into the original string.

    Returns:
    - A new string with the inserted content.
    """
    if index < 0 or index > len(original_string):
        raise ValueError("Index is out of bounds.")

    # Slice the original string into two parts and insert the new string in between
    new_string = original_string[:index] + string_to_insert + original_string[index:]
    return new_string


def write_string_to_file(file_name, content):
    """
    Writes a given string into a text file.

    Parameters:
    - file_name: The name of the text file to write to (e.g., "output.txt").
    - content: The string content to write into the file.
    """
    with open(file_name, 'w') as file:
        file.write(content)


def read_file_to_string(file_name):
    """
    Reads the content of a text file and returns it as a string.

    Parameters:
    - file_name: The name of the text file to read from (e.g., "input.txt").

    Returns:
    - A string containing the content of the file.
    """
    with open(file_name, 'r') as file:
        content = file.read()
    return content


def string_parser(input_string):

    host, gene, renzyme, promoter = input_string.split(".")


    # Choose map based on target cell type
    if host == "ECOLI":
        map = pET15_sites
        backbone = read_file_to_string("pET15-MHL.txt")
    elif host == "YEAST":
        map = pXP420_sites
        backbone = read_file_to_string("pXP420.txt")
    elif host == "MAMMALIAN":
        map = pBABE_sites
        backbone = read_file_to_string("pBABE-puro.txt")
    else:
        print("error, must target ecoli yeast or mammalian cells")

    # Grab gene from accenssion number
    accession_number = gpt_call(gene, "accession_number.txt")
    print(accession_number)
    insert_seq = get_sequence_by_accession(accession_number)
    print(insert_seq)

    # Grab promoter from ???
    if promoter == "LACUV5":
        promoter_seq = "TTTACACTTTATGCTTCCGGCTCGTATAATG"
    elif promoter == "T7":
        promoter_seq = "TAATACGACTCACTATAGG"
    else:
        print("only T7 and LACUV5 promoters are supported in this demo")

    # Insert sequences at promoter, index grabbed from map
    promoter_seq += insert_seq  # Concatenate the new gene seq and the promoter seq
    plasmid = insert_string_at_index(backbone, map.get(renzyme), promoter_seq)

    return plasmid


query = "design an ecoli strain that glows green"  #transcribe_audio("output.wav", client)
sequence_string = gpt_call(query, "string_assembly.txt")
reasoning = gpt_call(sequence_string, "design_reasoning.txt")
abstract = gpt_call(sequence_string, "experiment_abstract.txt")

# # Reflect 3 times before continuing
# for i in range(3):
#     sequence_string = gpt_call(f"The string is: {sequence_string} and the model reasoning is: {reasoning}",
#                                "reviewer.txt")
#
#     print(sequence_string + str(i))

# Check semantic scholar for relevant papers (room for improvement here, does not currently add much functionality)
ss_results = novelty_check(str(abstract))


write_string_to_file("plasmid.txt", string_parser(sequence_string))

