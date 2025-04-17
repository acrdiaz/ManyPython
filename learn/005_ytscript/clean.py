def remove_timestamps(input_file, output_file):
    """
    Removes timestamps from the beginning of each line in the input file
    and writes the cleaned lines to the output file.
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Remove the timestamp (assumes format HH:MM:SS.mmm at the start of the line)
            cleaned_line = line.split(' ', 1)[-1] if ' ' in line else line
            outfile.write(cleaned_line)

if __name__ == "__main__":
    input_path = "d:\\_cd\\prj\\github\\ManyPython\\learn\\005_ytscript\\script\\seven_year_software_eng.txt"
    output_path = "d:\\_cd\\prj\\github\\ManyPython\\learn\\005_ytscript\\script\\seven_year_software_eng_cleaned.txt"
    remove_timestamps(input_path, output_path)
    print(f"Timestamps removed. Cleaned file saved to: {output_path}")
