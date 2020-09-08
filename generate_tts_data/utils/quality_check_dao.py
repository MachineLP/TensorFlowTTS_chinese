# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
from conf.config import config
import logging


class QualityCheckDao(object):
    '''
    classdocs
    '''
    def __init__(self, mysql_url):
        self.mysql_url = mysql_url
        self.config_engine = None
        self.metrics_engine = None

        self.init_conn()

    def init_conn(self):
        if self.config_engine is None:
            mysql_conn_config = self.mysql_url
            try:
                self.config_engine = create_engine(
                    mysql_conn_config, pool_size=30, max_overflow=-1, pool_recycle=500, echo=True, pool_pre_ping=True)
                logging.error("[init_conn] config_engine init success !")
            except Exception as e:
                logging.error("init_conn is Error: {}".format(e))

    def get_config_session(self):
        session_factory = sessionmaker(autocommit=True,
                                       autoflush=True,
                                       bind=self.config_engine)
        session = scoped_session(session_factory)
        return session

    def insert(self, sql):
        try:
            session = self.get_config_session()
            result = session.execute(sql)
        except Exception as e:
            logging.error("mysql insert error, error msg: {} , hql : {}".format(e, sql))
        finally:
            if session:
                session.close()

    def query(self, sql):
        result = None
        try:
            session = self.get_config_session()
            res = session.execute(sql)
            result = [self._fmt(o, res) for o in res.fetchall()]
        except Exception as e:
            logging.error("mysql query error, error msg: {} , hql : {}".format(e, sql))
        finally:
            if session:
                session.close()
        return result

    def query_all(self, sql):
        frame = pd.DataFrame()
        try:
            session = self.get_config_session()
            res = session.execute(sql)
            result = [self._fmt(o, res) for o in res.fetchall()]
            frame = pd.DataFrame(result)
        except Exception as e:
            logging.error("mysql query_all error, error msg: {} , hql : {}".format(e, sql))
        finally:
            if session:
                session.close()
        return frame

    def _fmt_i(self, k, v):
        return k, v

    def _fmt(self, o, res):
        r = list(map(self._fmt_i, list(res.keys()), o))
        return {k: v for k, v in r}

