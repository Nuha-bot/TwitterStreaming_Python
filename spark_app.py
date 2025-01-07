import pyspark
import pyspark.streaming


# common setup
def printitems(items):
    for item in items:
        print(item.encode('utf-8'))


def main():
    sc = pyspark.SparkContext(master="local[%i]" % 2)
    sc.setLogLevel("ERROR")
    ssc = pyspark.streaming.StreamingContext(sc, 10)
    socket_stream = ssc.socketTextStream("127.0.0.1", 9892)
    lines = socket_stream.window(10)
    lines.pprint()

    hashtags = lines.flatMap(lambda line: line.split(" ")) \
        .filter(lambda word: word.lower().startswith('#'))
    hashtags.pprint()

    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
