from playwright.async_api import async_playwright
from gne import GeneralNewsExtractor
import newspaper
from urllib.parse import urlparse

async def get_article_detail(
        url,
        mode: str = "gne",
        wait: bool = False,
        with_body_html: bool = False,
        language: str = "en",
):
    html_text = await get_response_playwright(url, wait)
    if html_text:
        if "newspaper" == mode:
            return await get_article_detail_newspaper(url, html_text, language)
        else:
            return await get_article_detail_gne(html_text, with_body_html)

async def get_article_detail_newspaper(
        url,
        html_text,
        language: str = "en"
):
    article = newspaper.article(url=url, input_html=html_text, language=language)
    if article:
        article.nlp()
        result = {
            'title': article.title,
            'author': ' '.join(article.authors),
            'publish_date': article.publish_date,
            'content': article.text,
            'meta': {
                'keywords': ' '.join(article.keywords),
                'description': article.summary
            },
            'body_html': ''
        }
        return result

async def get_article_detail_gne(
        html_text,
        with_body_html
):
    extractor = GeneralNewsExtractor()
    return extractor.extract(html_text, with_body_html=with_body_html)

async def get_response_playwright(
        url,
        wait: bool = False
):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        if wait:
            await page.wait_for_timeout(3000)
        html_text = await page.content()
        await browser.close()

    return html_text

def extract_base_url(url):
    # 解析URL
    parsed_url = urlparse(url)

    # 组合scheme和netloc以获取基础URL
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    return base_url

def get_main_domain(url):
    # 解析URL并获取netloc部分
    parsed_url = urlparse(url)
    # 输出 www.example.com
    return parsed_url.netloc