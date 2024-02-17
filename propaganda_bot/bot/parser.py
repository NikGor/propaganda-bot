from newspaper import Article
import nltk
nltk.download('punkt')


def get_article_header(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.title


def get_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text


def get_article_authors(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.authors


def get_article_publish_date(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.publish_date


def get_article_image(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.top_image


def get_article_summary(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article.summary
