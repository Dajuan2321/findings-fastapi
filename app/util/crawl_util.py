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
    netloc = parsed_url.netloc

    # 分离出可能存在的端口号
    if ':' in netloc:
        netloc = netloc.split(':')[0]

    # 将netloc按点分割成列表
    parts = netloc.split('.')

    # 简单的规则：假设最后两个部分是主域名和顶级域名
    # 注意：这并不是一个通用的解决方案，对于复杂的TLD（如 .co.uk ）可能会失败
    if len(parts) > 2:
        # 去除 'www' 子域名
        if parts[0].lower() == 'www':
            parts = parts[1:]
        # 这里假设最后两部分为主域名和顶级域名
        main_domain = '.'.join(parts[-2:])
    else:
        # 对于只有两个部分的情况，直接返回
        main_domain = netloc

    return main_domain