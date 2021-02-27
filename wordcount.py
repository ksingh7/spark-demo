import sys, string
from operator import add

from pyspark.sql import SparkSession


def transform(line):
      line = line.strip()
      line = line.lower()
      line = line.translate(str(line).maketrans("", "", string.punctuation))
      return line

if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: transform(x).split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add).sortByKey(lambda x: x[1])
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))
    counts.saveAsTextFile("cos://wordcountdemo.myocs/results")    

    spark.stop()
