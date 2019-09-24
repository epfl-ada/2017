import json
import re
from pyspark.sql import *
from pyspark import SparkContext, SQLContext

# context initialization
sc = SparkContext()
sqlContext = SQLContext(sc)

# regex to get one word
word_regex = re.compile(r'(\w+)')

# read the input file line by line
text_file = sc.textFile("frankenstein.txt")


# convert a text line to words vector
def get_line_words(line):
    return word_regex.findall(line.lower())


counts_rdd = text_file.flatMap(get_line_words) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .sortBy(lambda wc: -wc[1])

# convert to dataframe
counts = sqlContext.createDataFrame(counts_rdd.map(lambda wc: Row(word=wc[0], count=wc[1])))

# view the content of the dataframe
counts.show()

# get 3 row for the dataframe
top3 = counts.take(3)
print("Top 3 words:")
for w in top3:
    print(w)

# save to json
counts.write.json("frankenstein_words_count.txt")
