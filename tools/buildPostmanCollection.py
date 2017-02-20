"""Build a Postman v2.0.0 schema collection of SparkPost templates from file"""

import glob
import os.path
import json
import uuid

from utils import mksafename

HOST = 'https://api.sparkpost.com'
TEMPLATES_ENDPOINT = '%s/api/v1/templates' % HOST
TRANSMISSIONS_ENDPOINT = '%s/api/v1/transmissions' % HOST
COLLECTION_FILENAME = 'SparkPost-Templates.postman_collection.json'

def pretty_json(obj): return json.dumps(obj, sort_keys=True, indent=4, separators=(',',':'))

class Template:
    def __init__(self, path):
        def find_first(path, ext):
            found = glob.glob('%s/*.%s' % (path, ext))
            if len(found) == 0: return None
            return found[0]
        def slurp(path, ext):
            foundfile = find_first(path, ext)
            if not foundfile: return None
            return open(foundfile, 'r').read()
        self.name = os.path.basename(path)
        self.tplid = mksafename(self.name)
        self.html = slurp(path, 'html')
        self.text = slurp(path, 'txt')
        self.json = json.loads(slurp(path, 'json'))
        self.subject = self.name
        if 'subject' in self.json:
            self.subject = self.json['subject']
        self.fromaddr = '%s@sparkpostbox.com' % self.tplid

    def to_json(self):
        return pretty_json({'id':self.tplid, 'name':self.name, 'content':self.content()})

    def content(self):
        return {'html':self.html, 'text':self.text, 'subject':self.subject, 'from':self.fromaddr}

    def content_json(self):
        return pretty_json(self.content())

def content_type_json(): return {'key': 'Content-Type', 'value': 'application/json'}

def auth_api_key(): return {'key': 'Authorization', 'value': '{{API_KEY}}'}

def headers(): return [content_type_json(), auth_api_key()]

def build_collection(tplpaths):
    return dict(info=infoblock(), item=items(tplpaths))

def infoblock():
    return dict(name='SparkPost Example Templates',
        _postman_id=str(uuid.uuid1()),
        schema='https://schema.getpostman.com/json/collection/v2.0.0/collection.json')

def items(tplpaths):
    items = []
    for path in tplpaths:
        tpl = Template(path)
        items.append(template_create_req(tpl))
        items.append(transmissions_create_req(tpl))
    return items

def template_create_req(tpl):
    return dict(name='Create template: %s' % tpl.name,
        request=dict(url=TEMPLATES_ENDPOINT, method='POST',
            header=headers(), body=dict(mode='raw', raw=tpl.to_json())))

def transmissions_create_req(tpl):
    return dict(name='Send email with template: %s' % tpl.name,
        request=dict(url=TRANSMISSIONS_ENDPOINT, method='POST',
            header=headers(), body=dict(mode='raw', raw=transmission_json(tpl))))

def transmission_json(tpl):
    trans = dict(description='Send email using template: %s' % tpl.name,
            recipients=[{'address': 'you@example.sinkhole.sparkpostmail.com'}],
        content=tpl.content())
    if 'substitution_data' in tpl.json:
        trans['substitution_data'] = tpl.json['substitution_data']
    return pretty_json(trans)

if __name__ == '__main__':
    # Collect template dirs
    def istemplatedir(path):
        nhtmls = len(glob.glob('%s/*.html' % path))
        ntxts = len(glob.glob('%s/*.txt' % path))
        return nhtmls>0 or ntxts>0
    subdirs = os.listdir('.')
    tplpaths = filter(lambda p: os.path.isdir(p) and not p.startswith('.') and istemplatedir(p), subdirs)
    collection_json = pretty_json(build_collection(tplpaths))
    open(COLLECTION_FILENAME, 'w').write(collection_json)

