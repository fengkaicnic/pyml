#coding:utf8
import textwrap

import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import pdb
reload(sys)
import tornado.web
sys.setdefaultencoding('utf8')
from position import handleposition
from profile import handleprofile
from model import generate_feature
from model import gbdt_model

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


class ProfileHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        body = eval(body)
        profile_json = body['profile']
        company_id = body['pos_id']
        handleprofile.insert_profile(profile_json, company_id)


class PositionHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        body = eval(body)
        position_json = body['company']
        handleposition.insert_company(position_json)


class PositionResumeHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        body = eval(body)
        handleprofile.update_profile(body)


class ModelHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        body = eval(body)
        action = body['action']
        if action == 'train':
            # generate_feature.generate_train()
            gbdt_model.train_model()
        else:
            pos_id = body['pos_id']
            resume_id = body['resume_id']
            score = gbdt_model.predict_data(pos_id, resume_id)
            self.write(score)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/profile", ProfileHandler),
            (r"/position", PositionHandler),
            (r"/pos_resume", PositionResumeHandler),
            (r"/model", ModelHandler)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
