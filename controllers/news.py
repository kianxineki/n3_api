from bottle import get, post, request, redirect
from modules.oauth2 import auth
from models.news import M_news


class News:

    @get('/api/news')
    @get('/api/other_news/<page>')
    def other_news(page=0):
        news = M_news.news(int(page))
        for new in news['result']:
            new['_id'] = str(new['_id'])
            new['date'] = new['date'].strftime("%Y-%m-%d %H:%M:%S")
            new['comments'] = len(new['comments'])  # TODO
        return {'news': news}

    @get('/api/search/page/<page>/tags/<tags:path>')
    def view_tags(page, tags):
        tags_parse = tags.split('/')
        news = M_news.tags(tags_parse, int(page))
        for new in news['result']:
            new['_id'] = str(new['_id'])
            new['date'] = new['date'].strftime("%Y-%m-%d %H:%M:%S")
            new['comments'] = len(new['comments'])  # TODO
        return {'news': news,
                'tags': tags_parse,
                'search': True}

    @get('/api/comments/<id_post>')
    def comments(id_post):
        new = M_news.new_detailed(id_post)
        new['_id'] = str(new['_id'])
        new['date'] = new['date'].strftime("%Y-%m-%d %H:%M:%S")
        for comment in new['comments']:
            comment['date'] = comment['date'].strftime("%Y-%m-%d %H:%M:%S")
        return new

    @post('/api/new_comment/<id_post>')
    @auth(0)
    def new_comment(id_post, auth_user):
        M_news.new_comment(id_post, request.forms.get('texto').decode(
            'utf-8'), request.environ.get('REMOTE_ADDR'), auth_user)
        # TODO
        redirect('/comments/%s' % id_post)
        # return {"result": True}
