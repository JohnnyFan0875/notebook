# Python: Web Scraping Basics

Web scraping is the workflow of downloading HTML, selecting the parts you care about, and extracting structured data from them.

A practical scraping loop is:

1. Fetch the page.
2. Parse the HTML.
3. Select elements.
4. Extract text or attributes.
5. Follow links if the data spans multiple pages.
6. Save the structured result.

This note focuses on the `scrapy` style of parsing and selection, because it gives a clean mental model for both simple scripts and larger crawlers.

## HTML Structure First

Before writing selectors, you need a rough picture of the HTML tree.

Typical tags:

```html
<html>
  <body>
    <div id="content" class="course-block">
      <a href="/course/python">Python Course</a>
      <p>Hello world</p>
    </div>
  </body>
</html>
```

Useful reminders:

- tags define structure
- attributes add metadata
- text often lives inside nested tags, not directly on the element you first inspect

Common attributes:

- `id`: usually intended to be unique
- `class`: can appear on many elements
- `href`: hyperlink target on `<a>` tags

## What You Usually Extract

In practice, scraping often means one of these:

- visible text
- links from `href`
- identifiers in `id` or `data-*` attributes
- repeated blocks such as cards, rows, or table entries

The real work is usually not downloading the page. It is selecting the right repeated structure reliably.

## Fetch HTML and Turn It into a Selector

You can fetch a page with `requests`, then hand the HTML to Scrapy's `Selector`.

```python
import requests
from scrapy import Selector

url = "https://en.wikipedia.org/wiki/Web_scraping"
html = requests.get(url).content
sel = Selector(text=html)
```

This pattern is useful when:

- you only need one page
- you want Scrapy selectors without building a full spider

## XPath Basics

XPath selects elements by navigating the HTML tree.

Examples:

```python
sel.xpath("/html/body")
sel.xpath("//p")
sel.xpath("/html/body/div/p[2]")
sel.xpath("//table")
sel.xpath('/html/body/div[2]//table')
```

Mental model:

- `/` means direct path from the root
- `//` means search descendants anywhere below
- `[2]` means the second matching sibling

XPath is especially useful when the structure is deeply nested or when you want precise positional selection.

## Selecting by Attributes in XPath

XPath can filter by attributes:

```python
sel.xpath('//p[@class="class-1"]')
sel.xpath('//*[@id="uid"]')
sel.xpath('//div[@id="uid"]/p[2]')
sel.xpath('//*[contains(@class, "class-1")]')
```

Notes:

- `@attr_name` references an attribute
- `contains(...)` is useful when `class` contains multiple tokens
- exact class equality can be brittle if class order changes

## CSS Selectors

CSS selectors are often shorter and easier to read for common cases.

Examples:

```python
sel.css("div > p")
sel.css("div#uid > p.class1")
sel.css(".class1")
sel.css("html > body > div")
sel.css("html > body div > p:nth-of-type(2)")
```

Quick mapping:

- `.class1` selects by class
- `#uid` selects by id
- `>` means direct child
- `nth-of-type(2)` picks a positional child

## XPath vs CSS

Both are good tools. A rough rule of thumb:

- use CSS for common class/id/child selections
- use XPath when you need more structural precision or text/attribute logic

You do not need a philosophical preference here. Use the one that makes the selector easiest to reason about.

## Extracting Attributes

### XPath

```python
sel.xpath('//div[@id="uid"]/a/@href').extract()
```

### CSS

```python
sel.css("div#uid > a::attr(href)").extract()
```

This is one of the most common scraping tasks, because many crawls begin by extracting a list of links to follow.

## Extracting Text

### XPath

```python
sel.xpath('//p[@id="p-example"]/text()').extract()
sel.xpath('//p[@id="p-example"]//text()').extract()
```

Difference:

- `/text()` gets only direct text children
- `//text()` gets text from all descendants

### CSS

```python
sel.css("p#p-example::text").extract()
sel.css("p#p-example ::text").extract()
```

This distinction matters when text is split across nested tags like links or spans.

## `extract()` and `extract_first()`

Selectors are not plain strings yet. You usually need to extract values.

```python
sel.xpath("//p").extract()
sel.xpath("//p").extract_first()
```

Use them like this:

- `extract()` when you expect a list
- `extract_first()` when you want one value

For mental clarity:

- selection step: find elements
- extraction step: convert them to strings

## Working with Repeated Blocks

A common pattern is:

1. select the repeated card / row / block
2. query inside that block

```python
course_divs = response.css("div.course-block")
hrefs = course_divs.xpath("./a/@href")
links = hrefs.extract()
```

Why this is good:

- selectors stay local
- the logic follows the page structure
- you avoid writing one huge brittle selector for everything

## Child Navigation

Sometimes you want the direct children of a selected element.

```python
children = first_div.xpath("./*")
first_child = children[0]
second_child = children[1]
third_child = children[2]
```

This is useful for debugging page structure when the HTML is messy or unfamiliar.

## Scrapy `Response` Object

Inside a Scrapy spider, the `response` object behaves like a selector plus crawl context.

```python
response.xpath('//div/span[@class="bio"]')
response.css("div > span.bio")
response.xpath("//div").css("span.bio").extract()
response.xpath("//div").css("span.bio").extract_first()
```

This makes Scrapy convenient because you can keep narrowing selections step by step.

## Following Links

After collecting links, you often want to crawl the next page.

```python
for link in links:
    yield response.follow(url=link, callback=self.parse_pages)
```

`response.follow()` is better than manually concatenating URLs because it handles relative links cleanly.

## Minimal Spider Skeleton

```python
import scrapy
from scrapy.crawler import CrawlerProcess


class DCSpider(scrapy.Spider):
    name = "dc_spider"

    def start_requests(self):
        urls = ["https://www.example.com"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css("div.course-block > a::attr(href)").extract()
        for link in links:
            yield response.follow(url=link, callback=self.parse_pages)

    def parse_pages(self, response):
        title = response.xpath('//h1[contains(@class, "title")]/text()').extract_first()
        chapters = response.css("h4.chapter__title::text").extract()
        yield {
            "title": title,
            "chapters": chapters,
        }


process = CrawlerProcess()
process.crawl(DCSpider)
process.start()
```

Core spider pieces:

- `name`
- `start_requests()`
- one or more parser callbacks such as `parse()` / `parse_pages()`
- yielded requests or yielded structured results

## Saving Output

The simplest output is often a list of strings or dicts.

For a very small script, you might write to a file directly:

```python
links = response.css("div.course-block > a::attr(href)").extract()

with open("links.txt", "w", encoding="utf-8") as f:
    for link in links:
        f.write(link + "\n")
```

But for most real crawls, yielding dicts from the spider is cleaner than manually writing text line by line.

## Practical Selector Strategy

When scraping a new page:

1. inspect the repeated container first
2. select one block
3. extract one field successfully
4. generalize to all blocks
5. only then add pagination or follow-up requests

This keeps debugging local and reduces selector confusion.

## Common Failure Modes

- selecting direct text when the real text is nested deeper
- matching exact classes when the page uses multiple class names
- using a global selector when the page should be parsed block-by-block
- following relative links incorrectly instead of using `response.follow()`
- extracting raw HTML when you actually wanted text or attributes

## Key Takeaways

- Scraping is mostly about reliable selection, not just downloading pages.
- Learn both XPath and CSS; each is simpler in different situations.
- `extract()` / `extract_first()` are the bridge from selectors to usable data.
- Start from repeated containers, then extract fields inside them.
- In Scrapy, `response.follow()` and small parser callbacks keep multi-page crawls manageable.
