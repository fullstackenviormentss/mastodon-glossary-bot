import json
import re
import os
import subprocess

import pandas as pd
from mastodon import Mastodon


def load_acronyms():
    if not os.path.isdir('RCAUAF'):
        print('Acronyms not found, cloning...')
        subprocess.run(['git', 'clone', 'https://github.com/michelbl/RCAUAF.git'])
    else:
        subprocess.run(['git', '-C', 'RCAUAF', 'pull', 'origin', 'master'])

    RCAUAF_filename = 'RCAUAF/RCAUAF.csv'
    RCAUAF = pd.read_csv(RCAUAF_filename)
    RCAUAF['key'] = RCAUAF.term.apply(str.upper)
    RCAUAF
    RCAUAF_keys = set(RCAUAF.key)

    print('Loading of acronyms is done !')

    return RCAUAF, RCAUAF_keys

RCAUAF, RCAUAF_keys = load_acronyms()


mastodon = Mastodon(
    client_id='clientcred.txt',
    access_token='usercred.txt',
    api_base_url='https://mastodon.etalab.gouv.fr',
)



def process_update(content):
    print('Update : ' + json.dumps(content))

def process_notification(content):
    print('Notification : ' + json.dumps(content))
    if content['type'] == 'mention':
        texte_html = content['status']['content']
        texte = re.sub(r'<[^>]*>', '', texte_html)
        words = sorted(set(texte.upper().split(' ')))
        acronyms = [w for w in words if w in RCAUAF_keys]
        
        toot = '@{}\n\n'.format(content['account']['username'])
        if acronyms:
            for a in acronyms:
                rows = RCAUAF[RCAUAF.key == a]
                definitions = list(rows.definition)
                for index, row in rows.iterrows():
                    toot += '{} = {}\n\n'.format(row['term'], row['definition'].encode('latin-1').decode('unicode_escape'))
        else:
            toot += "Je n'ai rien trouvé :("
        toot = toot[:499]
        
        mastodon.status_post(
            toot,
            in_reply_to_id=content['status']['id'],
            media_ids=None,
            sensitive=False,
            visibility=content['status']['visibility'],
            spoiler_text=None,
        )

def process_delete(content):
    print('Delete : ' + json.dumps(content))


class StreamListener():
    def handle_stream(self, stream):
        event = None
        
        for l_b in stream:
            l_unicode = l_b.decode('utf-8')
            if not l_unicode:
                continue
            semicolon_index = l_unicode.index(':')
            message_type = l_unicode[:semicolon_index]
            content = l_unicode[semicolon_index+2:]
            
            if message_type == 'event':
                assert content in {'update', 'notification', 'delete'}
                assert event is None
                event = content
            elif message_type == 'data':
                assert event is not None
                content_parsed = json.loads(content)
                
                if event == 'update':
                    process_update(content_parsed)
                elif event == 'notification':
                    process_notification(content_parsed)
                elif event == 'delete':
                    process_delete(content_parsed)
                
                event = None                
            else:
                assert message_type == ''

stream_listener = StreamListener()


mastodon.user_stream(listener=stream_listener)
