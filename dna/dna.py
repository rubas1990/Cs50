
import csv
import sys


def main():
    # Verifica si se han proporcionado los argumentos correctos
    if len(sys.argv) != 3:
        print("Error: se requieren dos argumentos (archivo CSV y archivo de texto)")
        sys.exit(1)

    # Lee el archivo CSV
    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        str_counts = {}
        for row in reader:
            str_counts[row['name']] = row

    # Lee la secuencia de ADN
    with open(sys.argv[2], 'r') as dnafile:
        dna = dnafile.read()

    # Busca la coincidencia
    for name, str_count in str_counts.items():
        match = True
        for str, count in str_count.items():
            if str != 'name':
                if longest_match(dna, str) != int(count):
                    match = False
                    break
        if match:
            print(name)
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


if __name__ == '__main__':
    main()
		