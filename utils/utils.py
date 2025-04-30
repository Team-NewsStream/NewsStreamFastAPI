from utils.mapper import map_to_article_create


def retrieve_news_content(news_data: list[dict], ml_data: list[dict]):
    """
    Retrieves the content of news articles, categorizes them, maps their sources, and
    creates ArticleCreate objects based on the news and ML Inference API data. The function
    matches news articles with corresponding ML Inference API data by their titles and
    processes them accordingly. Articles without a match or title are ignored.

    :param news_data: A list of dictionaries containing news data.
    :param ml_data: A list of dictionaries containing "text" and "category".
    :return: A tuple with three elements:
        - A list of created ArticleCreate objects based on matched news and ML Inference data.
        - A set of categories extracted from the ML Inference.
        - A dictionary mapping source names to their respective logo URLs, if any.
    """
    categories_set = set()
    sources_map = {}
    article_creates = []

    ml_map = {item["text"]: item for item in ml_data}

    for item in news_data:
        title = item.get("title")
        if title is None: continue

        ml_item = ml_map.get(title)
        if ml_item is None: continue

        categories_set.add(ml_item["category"])
        source = item["source"]
        sources_map[source["name"]] = source["logo_url"]
        article = map_to_article_create(news_item=item, ml_data=ml_item)
        article_creates.append(article)

    return article_creates, categories_set, sources_map
