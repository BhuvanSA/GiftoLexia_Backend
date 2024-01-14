import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')


words = word_tokenize(
    "beauty beautiful handsome run running ran stand stood standing")

print(words)
