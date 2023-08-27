import difflib


class StringComparator:
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual

    def levenshtein_distance(self):
        m = len(self.expected)
        n = len(self.actual)

        # Create a matrix to store the distances
        matrix = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize the first row and column of the matrix
        for i in range(m + 1):
            matrix[i][0] = i
        for j in range(n + 1):
            matrix[0][j] = j

        # Calculate the minimum edit distance
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.expected[i - 1] == self.actual[j - 1]:
                    matrix[i][j] = matrix[i - 1][j - 1]
                else:
                    matrix[i][j] = min(
                        matrix[i - 1][j] + 1,  # Deletion
                        matrix[i][j - 1] + 1,  # Insertion
                        matrix[i - 1][j - 1] + 1,  # Substitution
                    )

        return matrix[m][n]

    def calculate_error_rate(self):
        distance = self.levenshtein_distance()
        error_rate = (distance / max(len(self.expected), len(self.actual))) * 100
        return error_rate

    def find_misspelled_words(self):
        expected_words = self.expected.split()
        actual_words = self.actual.split()

        # Find the differing words using difflib
        diff = difflib.ndiff(expected_words, actual_words)
        differing_words = [word for word in diff if word.startswith("-")]

        # Remove the '-' character from differing words
        misspelled_words = [word[2:] for word in differing_words]

        return misspelled_words
