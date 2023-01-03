from youtube_comments_scraper import get_video_comments
from BertCommentClassifier import get_text_class
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import io
import base64
import json
import re


STOPWORDS = stopwords.words("russian")

# Расширяет список стоп-слов словами из файла.
with open("stop_words_addition.txt", 'r') as f:
    words = f.readline()

    for word in words:
        STOPWORDS.append(word)


# Возвращает положительные и негативные комментарии.
def get_comments_by_tone(comments):
    positive_comments = []
    negative_comments = []

    for comment in comments:
        if get_text_class(comment) == 1:
            positive_comments.append(comment)
        else:
            negative_comments.append(comment)

    return positive_comments, negative_comments


# Строит облако слов и возвращает base64 изображение.
def get_comments_wordcloud(comments, name):
    text = " ".join(comments)
    text = text.replace("&quot;", "")

    # Определяем параметр stopwords при создании объекта облака слов
    cloud = WordCloud(width=1000, height=500, stopwords=set(STOPWORDS)).generate(text)

    plt.figure(figsize=(20, 10))

    plt.imshow(cloud)
    plt.axis('off')
    plt.savefig("output/" + name + '.png')

    string_io_bytes = io.BytesIO()
    plt.savefig(string_io_bytes, format='jpg')
    string_io_bytes.seek(0)
    plt_base64_image = base64.b64encode(string_io_bytes.read())

    return plt_base64_image


def get_words_frequency(text, name):
    text = " ".join(text)
    word_freq = {}
    text_char_list = text.split()

    unique_words = set(text_char_list)

    filtered_unique_words = [w for w in unique_words if not w.lower() in STOPWORDS]

    for words in filtered_unique_words:
        word_freq[words] = text_char_list.count(words)

    sorted_word_freq = dict(sorted(word_freq.items(), key=lambda item: item[1]))

    with open("output/" + name + '.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_word_freq, f, ensure_ascii=False, indent=4)

    return sorted_word_freq


def get_analysis(url):
    comments = get_video_comments(url)
    positive_comments, negative_comments = get_comments_by_tone(comments)

    positive_wordcloud = get_comments_wordcloud(positive_comments, "positive_cloud")
    negative_wordcloud = get_comments_wordcloud(negative_comments, "negative_cloud")

    positive_word_frequency = get_words_frequency(positive_comments, "positive_frequencies")
    negative_word_frequency = get_words_frequency(negative_comments, "negative_frequencies")

    output = {
        "positive_wordcloud": str(positive_wordcloud),
        "negative_wordcloud": str(negative_wordcloud),
        "positive_word_frequency": str(positive_word_frequency),
        "negative_word_frequency": str(negative_word_frequency)
    }

    return output

# print(get_analysis("lYWx3WK8oO8"))
