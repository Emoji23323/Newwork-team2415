"""YCY：定义 Elasticsearch 文档与索引管理类，负责访问日志和文章索引的创建、删除与重建。"""
import time

import elasticsearch.client
from django.conf import settings
from elasticsearch_dsl import Document, InnerDoc, Date, Integer, Long, Text, Object, GeoPoint, Keyword, Boolean
from elasticsearch_dsl.connections import connections

from blog.models import Article

ELASTICSEARCH_ENABLED = hasattr(settings, 'ELASTICSEARCH_DSL')

if ELASTICSEARCH_ENABLED:
    from elasticsearch import Elasticsearch

    es_config = settings.ELASTICSEARCH_DSL['default']

    # YCY：处理 hosts 配置，确保有 scheme
    hosts = es_config['hosts']
    if isinstance(hosts, str):
        # YCY：如果没有 scheme，自动添加 http://
        if not hosts.startswith(('http://', 'https://')):
            hosts = f'http://{hosts}'
        hosts = [hosts]
    elif isinstance(hosts, list):
        # YCY：处理列表中的每个 host
        processed_hosts = []
        for host in hosts:
            if not host.startswith(('http://', 'https://')):
                host = f'http://{host}'
            processed_hosts.append(host)
        hosts = processed_hosts

    # YCY：ES 连接配置（动态适配认证方式）
    es_params = {
        'hosts': hosts,
        'verify_certs': es_config.get('verify_certs', False),
    }

    # YCY：支持用户名密码认证（ES 8.x 默认启用安全特性）
    if 'username' in es_config and 'password' in es_config:
        es_params['basic_auth'] = (es_config['username'], es_config['password'])

    # YCY：支持 API Key 认证
    if 'api_key' in es_config:
        es_params['api_key'] = es_config['api_key']

    # YCY：支持证书认证
    if 'ca_certs' in es_config:
        es_params['ca_certs'] = es_config['ca_certs']

    # YCY：支持客户端证书
    if 'client_cert' in es_config and 'client_key' in es_config:
        es_params['client_cert'] = es_config['client_cert']
        es_params['client_key'] = es_config['client_key']

    # YCY：创建连接
    es = Elasticsearch(**es_params)
    connections.create_connection(**es_params)

    # YCY：设置 GeoIP pipeline
    try:
        es.ingest.get_pipeline(id='geoip')
    except elasticsearch.exceptions.NotFoundError:
        es.ingest.put_pipeline(id='geoip', body={
            "description": "Add geoip info",
            "processors": [
                {
                    "geoip": {
                        "field": "ip"
                    }
                }
            ]
        })


class GeoIp(InnerDoc):
    continent_name = Keyword()
    country_iso_code = Keyword()
    country_name = Keyword()
    location = GeoPoint()


class UserAgentBrowser(InnerDoc):
    Family = Keyword()
    Version = Keyword()


class UserAgentOS(UserAgentBrowser):
    pass


class UserAgentDevice(InnerDoc):
    Family = Keyword()
    Brand = Keyword()
    Model = Keyword()


class UserAgent(InnerDoc):
    browser = Object(UserAgentBrowser, required=False)
    os = Object(UserAgentOS, required=False)
    device = Object(UserAgentDevice, required=False)
    string = Text()
    is_bot = Boolean()


class ElapsedTimeDocument(Document):
    """YCY：记录页面 URL、耗时、IP 与 User-Agent 的访问日志文档。"""
    url = Keyword()
    time_taken = Long()
    log_datetime = Date()
    ip = Keyword()
    geoip = Object(GeoIp, required=False)
    useragent = Object(UserAgent, required=False)

    class Index:
        name = 'performance'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }


class ElaspedTimeDocumentManager:
    """YCY：封装访问日志索引的建立、删除与批量写入。"""
    @staticmethod
    def build_index():
        from elasticsearch import Elasticsearch
        # YCY：使用已配置好的连接参数
        client = Elasticsearch(**es_params)
        res = client.indices.exists(index="performance")
        if not res:
            ElapsedTimeDocument.init()

    @staticmethod
    def delete_index():
        from elasticsearch import Elasticsearch
        es = Elasticsearch(**es_params)
        try:
            es.indices.delete(index='performance')
        except elasticsearch.exceptions.NotFoundError:
            pass

    @staticmethod
    def create(url, time_taken, log_datetime, useragent, ip):
        ElaspedTimeDocumentManager.build_index()
        ua = UserAgent()
        ua.browser = UserAgentBrowser()
        ua.browser.Family = useragent.browser.family
        ua.browser.Version = useragent.browser.version_string

        ua.os = UserAgentOS()
        ua.os.Family = useragent.os.family
        ua.os.Version = useragent.os.version_string

        ua.device = UserAgentDevice()
        ua.device.Family = useragent.device.family
        ua.device.Brand = useragent.device.brand
        ua.device.Model = useragent.device.model
        ua.string = useragent.ua_string
        ua.is_bot = useragent.is_bot

        doc = ElapsedTimeDocument(
            meta={
                'id': int(
                    round(
                        time.time() *
                        1000))
            },
            url=url,
            time_taken=time_taken,
            log_datetime=log_datetime,
            useragent=ua, ip=ip)
        doc.save(pipeline="geoip")


class ArticleDocument(Document):
    """YCY：文章在 Elasticsearch 中的文档结构，包含标题、正文与标签。"""
    body = Text(analyzer='ik_max_word', search_analyzer='ik_smart')
    title = Text(analyzer='ik_max_word', search_analyzer='ik_smart')
    author = Object(properties={
        'nickname': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'id': Integer()
    })
    category = Object(properties={
        'name': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'id': Integer()
    })
    tags = Object(properties={
        'name': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'id': Integer()
    })

    pub_time = Date()
    status = Text()
    comment_status = Text()
    type = Text()
    views = Integer()
    article_order = Integer()

    class Index:
        name = 'blog'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }


class ArticleDocumentManager():

    """YCY：把 ORM 文章对象转换为索引文档并重建索引。"""
    def __init__(self):
        self.create_index()

    def create_index(self):
        ArticleDocument.init()

    def delete_index(self):
        from elasticsearch import Elasticsearch
        es = Elasticsearch(**es_params)
        try:
            es.indices.delete(index='blog')
        except elasticsearch.exceptions.NotFoundError:
            pass

    def convert_to_doc(self, articles):
        """YCY：把 Article 实例映射为可写入 ES 的文档字典。"""
        return [
            ArticleDocument(
                meta={
                    'id': article.id},
                body=article.body,
                title=article.title,
                author={
                    'nickname': article.author.username,
                    'id': article.author.id},
                category={
                    'name': article.category.name,
                    'id': article.category.id},
                tags=[
                    {
                        'name': t.name,
                        'id': t.id} for t in article.tags.all()],
                pub_time=article.pub_time,
                status=article.status,
                comment_status=article.comment_status,
                type=article.type,
                views=article.views,
                article_order=article.article_order) for article in articles]

    def rebuild(self, articles=None):
        ArticleDocument.init()
        articles = articles if articles else Article.objects.all()
        docs = self.convert_to_doc(articles)
        for doc in docs:
            doc.save()

    def update_docs(self, docs):
        for doc in docs:
            doc.save()
