## Tornado_UA
The tornado application is intended to calculate the number of occurrences of a word on a page and to identify the most frequently used words.

## Online example
[Main page](http://mcs.osinit.com:8080)


[Admin page](http://mcs.osinit.com:8080/admin)

## Local deployment
To run the application on the local machine, use the docker-compose:

`docker-compose build`
`docker-compose up`

## Technical details
The application is written in `python 3` and `tornado`.

`AsyncHTTPClient` is used for retrieving data from a given web page .

`BeautifulSoup`is used for cleaning up the document from HTML and CSS markup and JS scripts and extract text from the document

Then the text goes through custom preprocessing.

Next, `nltk` is used for tokenization, marking parts of speech and counting the frequency of occurrence of words (because the text is already marked, only verbs and nouns are considered).

An asynchronous driver from the package `tormysql` is used for work with the MySQL database.

For encrypting and decrypting we use RSA.