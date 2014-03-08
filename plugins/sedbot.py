from plugins.categories import ISilentCommand

import regex
import copy
import collections

class Sedbot (ISilentCommand):
    triggers = {
        r'(^s/.*/.*/.*$)': "sed",
        r'(.*)': "log",
    }

    def __init__(self):
        self.backlog = collections.deque(maxlen=100)

    def trigger_log(self, user, channel, match):
        message = match.group(0)
        if not regex.match(r'^s/.*/.*/.*$', message):
            self.backlog.append((user, channel, message))

    def trigger_sed(self, user, channel, match):
        sed_message = match.group(0)
        # No abuse
        if 'James_T' in user:
            return
        for backlog_entry in reversed(self.backlog):
            backlog_user = backlog_entry[0]
            backlog_channel = backlog_entry[1]
            backlog_message = backlog_entry[2]
            if channel != backlog_channel:
                continue
            sed_objects = self.parse(sed_message)
            if not sed_objects:
                continue
            edited_message = backlog_message
            for sed_index, sed_object in enumerate(sed_objects):
                # Set up flags for the regex module
                # TODO: global and offset flag handling
                flags = 0
                if sed_object['flags']['insensitive']:
                    flags |= regex.IGNORECASE
                # If we're on the first expression, use it to also check
                # if the current backlog message is relevant to match
                if sed_index == 0:
                    if sed_object['flags']['meonly']:
                        print backlog_user, user
                        if backlog_user != user:
                            break
                    if not regex.search(
                        sed_object['needle'],
                        edited_message,
                        flags=flags
                    ):
                        break
                # Now let's edit the message
                edited_message = regex.sub(
                    sed_object['needle'],
                    sed_object['replacement'],
                    edited_message,
                    flags=flags
                )
            if edited_message != backlog_message:
                edited_message = edited_message.replace('\n', '')
                self.backlog.append(
                    (backlog_user, backlog_channel, edited_message)
                )
                return "<%s> %s" % (backlog_user.split('!')[0], edited_message)

    @staticmethod
    def parse(expr):
        def error(i, message):
            print 'sed parse error: %d: %s' % (i, message)
        def skeleton():
            return copy.copy({
                'needle': '',
                'replacement': '',
                'flags': {
                    'global': False,
                    'insensitive': False,
                    'meonly': False,
                    'offset': 1
                }
            })
        def skelhits():
            return copy.copy({
                'start': 0,
                'ready': 0,
                'needle': 0,
                'needle_backslash': 0,
                'replacement': 0,
                'replacement_backslash': 0,
                'flags': 0,
                'flags_offset': 0
            })
        state = 'start'
        result = []
        out = skeleton()
        hits = skelhits()
        for i, c in enumerate(expr):
            hits[state] += 1
            if state == 'start':
                if c == 's':
                    state = 'ready'
                else:
                    return error(i, 'expected "s"')
            elif state == 'ready':
                if c == '/':
                    state = 'needle'
                else:
                    return error(i, 'expected "/"')
            elif state == 'needle':
                if c == '/':
                    state = 'replacement'
                elif c == '\\':
                    state = 'needle_backslash'
                else:
                    out['needle'] += c
            elif state == 'needle_backslash':
                if c == '/':
                    out['needle'] += '/'
                else:
                    out['needle'] += '\\' + c
                state = 'needle'
            elif state == 'replacement':
                if c == '/':
                    state = 'flags'
                elif c == '\\':
                    state = 'replacement_backslash'
                else:
                    out['replacement'] += c
            elif state == 'replacement_backslash':
                if c == '/':
                    out['replacement'] += '/'
                else:
                    out['replacement'] += '\\' + c
                state = 'replacement'
            elif state == 'flags':
                f = c.lower()
                if f == 'g':
                    out['flags']['global'] = True
                elif f == 'i':
                    out['flags']['insensitive'] = True
                elif f == 'm':
                    out['flags']['meonly'] = True
                elif f == ';':
                    result.append(out)
                    out = skeleton()
                    hits = skelhits()
                    state = 'start'
                elif f.isdigit():
                    if hits['flags_offset'] == 0:
                        out['flags']['offset'] = int(f)
                        state = 'flags_offset'
                    else:
                        return error(i, 'multiple offset flags not allowed')
                else:
                    return error(i, 'invalid flag')
            elif state == 'flags_offset':
                f = c.lower()
                if f.isdigit():
                    out['flags']['offset'] *= 10
                    out['flags']['offset'] += int(f)
                elif f == 'g':
                    out['flags']['global'] = True
                    state = 'flags'
                elif f == 'i':
                    out['flags']['insensitive'] = True
                    state = 'flags'
                elif f == 'm':
                    out['flags']['meonly'] = True
                    state = 'flags'
                elif f == ';':
                    result.append(out)
                    out = skeleton()
                    hits = skelhits()
                    state = 'start'
                else:
                    return error(i, 'invalid flag')
            else:
                return error(i, 'invalid parser state')
        if state != 'flags' and state != 'flags_offset':
            return error(i, 'invalid parser state at end of expression')
        result.append(out)
        return result
