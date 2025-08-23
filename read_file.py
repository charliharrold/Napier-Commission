import PyPDF2
import re
import nltk
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')

nltk.download('words')

english_vocab = set(words.words())
lemmatizer = WordNetLemmatizer()

def is_valid_word(word):
    base = lemmatizer.lemmatize(word.lower())
    return base in english_vocab

common_replacements = {"laudlord": "landlord", "chairynan": "Chairman"}

def read_file():
    for i in range(1, 6):
        filename = './napier-commission-vol-' + str(i) + '.pdf'
        fileout = './napier-commission-vol-' + str(i) + '.txt'
        
        with open(filename,'rb') as pdf_file: #opens pdf in relative path
            reader = PyPDF2.PdfReader(pdf_file) #build reader object and pass in pdf file data
            num_pages = len(reader.pages) #collect number of pages
            with open(fileout, "a", encoding="utf-8") as outfile: #open out.txt file in append mode
                for i in range(0, num_pages): #loop over pages in pdf
                    page = reader.pages[i] #gather page data for each page
                    text = page.extract_text() #convert page to text
                    outfile.writelines(text) #write page to file and repeat  
    return

def manual_clean(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        raw_text = infile.read()

    cleaned_words = []
    lines = raw_text.splitlines()

    for line in lines:
        line_words = line.split()
        new_line = []

        for word in line_words:
            stripped = word.strip("—.,!?;:\"()[]{}").lower()
            if stripped in common_replacements:
                fixed = word.replace(stripped, common_replacements[stripped])
                new_line.append(fixed)
            elif "?—" in stripped:
                fixed = ""
                split_words = word.split("?—")
                for i in range(len(split_words)):
                    original_words = split_words[:]
                    split_words[i] = split_words[i].lower()
                    
                    if split_words[i] in english_vocab:
                        fixed += original_words[i]
                    else:
                        print(f"\nUnrecognized word: '{split_words[i]}'")
                        print(f"Line: {line}")
                        correction = input("Enter correction (or press Enter to keep as-is): ")
                        fixed += (correction if correction else original_words[i])
                        
                    if i != len(split_words) - 1:
                        fixed += "?—"
                        
                new_line.append(fixed)
            elif is_valid_word(stripped) or stripped == "" or re.search(r"[0-9]+\.", word) != None:
                new_line.append(word)
            else:  
                print(f"\nUnrecognized word: '{word}'")
                print(f"Line: {line}")
                correction = input("Enter correction (or press Enter to keep as-is): ")
                new_line.append(correction if correction else word)

        cleaned_words.append(" ".join(new_line))

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(cleaned_words))

if __name__ == "__main__":
    # read_file()
    manual_clean('test.txt', 'out.txt')
