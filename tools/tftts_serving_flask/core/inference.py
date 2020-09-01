# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  TTSInference
   Author :       machinelp
   Date :         2020-08-10
-------------------------------------------------

'''

import os
import sys
import json
from utils.logging import logging
from flask_restful import Resource,Api
from core.models import TTSModel
from flask import Flask,abort, make_response, request, jsonify

tts_model = TTSModel()

class TTSInference(Resource):
    def __init__(self):
        pass

    def post(self):

        if not request.json or 'content' not in request.json :
            res = { "code": "400", "data": {}, "message": "request is not json or content not in json" }
            return jsonify ( res )

        else:
            logging.info( "[TTSInference] [post] request.json:{}".format( request.json ) )
            text = request.json["content"]
            logging.info( "[TTSInference] [post] text:{}".format( text ) )
            mels, alignment_history, audios = tts_model.do_synthesis(text)
            res = { "code": "200", "data": audios.tolist(), "message": "" }
            return jsonify ( res )
