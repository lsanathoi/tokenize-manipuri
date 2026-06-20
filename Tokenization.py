from pathlib import Path
import re
import csv
import unicodedata
import os


# =====================================================
# CONFIG
# =====================================================

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")


# =====================================================
# TEXT NORMALIZATION
# =====================================================

def normalize_text(text):
    """
    Normalize Unicode text for stable Meitei Mayek processing.
    """

    text = unicodedata.normalize("NFC", text)

    text = text.replace("\ufeff", "")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Join broken lines into spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# SENTENCE SPLITTING
# =====================================================

def split_sentences(text):
    """
    Split Manipuri text sentence by sentence.

    It splits only after Meitei Mayek sentence mark: ꯫
    It does NOT split after English full stop.
    """

    text = normalize_text(text)

    # Find sentences ending with ꯫
    sentences = re.findall(r"[^꯫]+꯫", text)

    clean_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            clean_sentences.append(sentence)

    return clean_sentences


# =====================================================
# CSV OUTPUT
# =====================================================

def write_csv(sentences, csv_output_file):
    """
    Write sentence_no and sentence to CSV.
    """

    with open(
        csv_output_file,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "sentence_no",
            "sentence"
        ])

        for sentence_no, sentence in enumerate(sentences, start=1):
            writer.writerow([
                sentence_no,
                sentence
            ])

    print("CSV saved:", csv_output_file)


# =====================================================
# TXT OUTPUT
# =====================================================

def write_txt(sentences, txt_output_file):
    """
    Write sentence_no and sentence to TXT.
    """

    with open(
        txt_output_file,
        "w",
        encoding="utf-8"
    ) as f:

        for sentence_no, sentence in enumerate(sentences, start=1):
            f.write(f"{sentence_no}. {sentence}\n")

    print("TXT saved:", txt_output_file)


# =====================================================
# PROCESS ONE FILE
# =====================================================

def process_file(txt_file):
    """
    Process one txt file and save tokenized output
    using the same file name.
    """

    print("\nProcessing:", txt_file.name)

    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        print("Skipped empty file:", txt_file.name)
        return

    sentences = split_sentences(text)

    if not sentences:
        print("No sentences found in:", txt_file.name)
        return

    output_name = txt_file.stem + "_tokenized"

    csv_output_file = OUTPUT_DIR / f"{output_name}.csv"
    txt_output_file = OUTPUT_DIR / f"{output_name}.txt"

    write_csv(sentences, csv_output_file)
    write_txt(sentences, txt_output_file)

    print("Total sentences:", len(sentences))


# =====================================================
# MAIN
# =====================================================

def main():

    print("Current folder:", os.getcwd())

    if not DATA_DIR.exists():
        raise FileNotFoundError(
            "\nData folder not found.\n"
            "Create a folder named data and put your .txt files inside it."
        )

    OUTPUT_DIR.mkdir(exist_ok=True)

    txt_files = list(DATA_DIR.glob("*.txt"))

    if not txt_files:
        raise FileNotFoundError(
            "\nNo .txt files found inside data folder.\n"
            "Put your text files like this:\n"
            "data/file1.txt"
        )

    print("Text files found:", len(txt_files))

    for txt_file in txt_files:
        process_file(txt_file)

    print("\nDone. All files processed.")


if __name__ == "__main__":
    main()