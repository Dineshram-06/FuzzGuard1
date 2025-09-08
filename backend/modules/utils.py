import logging

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

def load_wordlist():
    # Hardcoded common wordlist for demo
    return [
        '/admin', '/admin/login', '/backup', '/backup.zip', '/config', '/config.json',
        '/db', '/db.sqlite', '/.git', '/.env', '/robots.txt', '/sitemap.xml',
        '/wp-admin', '/phpmyadmin', '/test', '/debug'
    ]