import datetime
from inverted_index import InvertedIndex
from tf_idf import TfIdf
import pandas as pd

custom_separator = "###"

if __name__ == '__main__':
    df=pd.read_csv('../data/stories.csv', sep=',',header=None)
    df_head = pd.read_csv('../data/db_books.csv', sep=',')
    
    array_content = df.values
    # array_segment = array_content[0:3]
    
    # INVERTED INDEX
    print("Init INVERTED INDEX")
    begin_time = datetime.datetime.now()
    invindex = InvertedIndex(array_content)
    invindex.process()
    print(datetime.datetime.now() - begin_time)   
    invindex.saveIndexInDisc()
    
    # TF IDF
    print("Init TF IDF")
    begin_time = datetime.datetime.now()
    tf_idf = TfIdf(array_content)
    tf_idf.process()
    print(datetime.datetime.now() - begin_time)   
    tf_idf.saveIndexInDisc()