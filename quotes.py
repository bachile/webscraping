from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = f'http://quotes.toscrape.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
page = urlopen(url)			
soup = BeautifulSoup(page, 'html.parser')
title = soup.title
print("\n" + title.text)
quotes = soup.findAll('div', class_ = "quote")
print()

quote_count = 0

longest_quote = '0'

shortest_quote = '0'*10000

all_quotes_length = 0

author_dict = {}

total_tag_count = 0

tag_dict = {}

for page in range(0,11):

    url = f'http://quotes.toscrape.com/page/{page}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    page = urlopen(url)			

    soup = BeautifulSoup(page, 'html.parser')

    quotes = soup.findAll('div', class_ = "quote")

    for quote in quotes[:10]:

        text = quote.find('span', class_ = "text").text
        quote_count += 1
        all_quotes_length += len(text)
        if len(text) > len(longest_quote):
            longest_quote = text
        if len(text) < len(shortest_quote):
            shortest_quote = text

        author = quote.find('small', class_ = "author").text
        try:
            author_dict[author].append(text) 
        except:
            author_dict[author] = [text]

        tags = quote.find('div', class_ = 'tags')
        for entry in tags.findAll('a'):
            tag = entry.text
            total_tag_count += 1
            try:
                tag_dict[tag] += 1
            except:
                tag_dict[tag] = 1

author_num_quote_dict = {}
for key in author_dict:
    author_num_quote_dict[key] = len(author_dict[key])

highest_quotes = 0
lowest_quotes = 100

from operator import itemgetter

top_ten_tag_dict = dict(sorted(tag_dict.items(), key=itemgetter(1), reverse=True)[:10])
top_ten_tags = [i for i in top_ten_tag_dict]
top_ten_tags_count = [top_ten_tag_dict[i] for i in top_ten_tag_dict]

top_ten_author_dict = dict(sorted(author_num_quote_dict.items(), key=itemgetter(1), reverse=True)[:10])
top_ten_authors = [i for i in top_ten_author_dict]
top_ten_authors_count = [top_ten_author_dict[i] for i in top_ten_author_dict]

from plotly.graph_objs import bar
from plotly import offline

data = [
    {
        "type":'bar',
        "x": top_ten_tags,
        "y": top_ten_tags_count,
        "marker":{
            "color":"rgb(60, 100, 150)",
            "line":{"width":1.5, "color": "rgb(25,25,25)"},
        },
        "opacity":0.6,
    }
]

my_layout = {
    "title": "Most popular tags by Authors",
    "xaxis":{"title":"Tags"},
    "yaxis":{"title":"Count"}
}

data2 = [
    {
        "type":'bar',
        "x": top_ten_authors,
        "y": top_ten_authors_count,
        "marker":{
            "color":"rgb(60, 100, 150)",
            "line":{"width":1.5, "color": "rgb(25,25,25)"},
        },
        "opacity":0.6,
    }
]

my_layout2 = {
    "title": "Quotes by Authors",
    "xaxis":{"title":"Authors"},
    "yaxis":{"title":"Number of Quotes"}
}

fig = {"data":data, "layout":my_layout}
fig2 = {"data":data2, "layout":my_layout2}

offline.plot(fig, filename="popular_tags.html")
offline.plot(fig2, filename="popular_authors.html")

for key in author_num_quote_dict:
    if author_num_quote_dict[key] > highest_quotes:
        highest_quotes = author_num_quote_dict[key]
        highest_author = key
    if author_num_quote_dict[key] < lowest_quotes:
        lowest_quotes = author_num_quote_dict[key]
        lowest_author = key
    print(f'Author: {key}, Number of Quotes: {author_num_quote_dict[key]}')

print()

print(f'Author with the most quotes: {highest_author}')
print(f'Author with the least quotes: {lowest_author}')

print()

print(f'Average length of quotes: {all_quotes_length/quote_count} characters')
print(f'The longest quote is {len(longest_quote)} characters long')
print(f'The shortest quote is {len(shortest_quote)} characters long')

print()

print(f'The most popular tag is {top_ten_tags[0]}')
print(f'The total amounts of tags that were used across all quotes is {total_tag_count}')

print()
