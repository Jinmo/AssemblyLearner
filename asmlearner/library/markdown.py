import markdown as markdown_


def markdown(content):
    return markdown_.markdown(content, extensions=['markdown.extensions.fenced_code'])
