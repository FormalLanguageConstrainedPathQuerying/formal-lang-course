def print_csr_matrix(matrix):
    # Convert to dense format for better readability
    dense_matrix = matrix.toarray()

    # Calculate the maximum width for formatting
    max_width = max(len(str(item)) for row in dense_matrix for item in row)

    for row in dense_matrix:
        formatted_row = " | ".join(f"{str(item):>{max_width}}" for item in row)
        print(f"| {formatted_row} |")
