DOCUMENTATION = """
    name: ip_range
    author: Emil Harvey
    version_added: "2.13.4"
    short_description: Returns a range of IPs
    description:
        - This lookup returns a list of IPs between (and including) the first and second parameter
    options:
      _terms:
        description: Start IP(s)
        required: True
      end:
        description: End IP
        type: str
        required: True
"""

EXAMPLES = """
- ansible.builtin.debug:
    msg: "IP range is {{ generated_ip_range }}"
  vars:
    start: 192.168.0.0
    end: 192.168.0.10
    generated_ip_range: "{{lookup('ip_range', start, end) }}"
    EXPECTED:
      - 192.168.0.0
      - 192.168.0.1
      - 192.168.0.2
      - 192.168.0.3
      - 192.168.0.4
      - 192.168.0.5
      - 192.168.0.6
      - 192.168.0.7
      - 192.168.0.8
      - 192.168.0.9
      - 192.168.0.10
  failed_when: generated_ip_range != EXPECTED
"""

RETURN = """
  _raw:
    description:
      - List(s) representing IP ranges
    type: list
    elements: str
"""

from typing import List
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_text
from ansible.utils.display import Display
import socket, struct # For ips()

display = Display()

# I copied-pasted this function by @User on 2022-09-28
# https://stackoverflow.com/questions/17641492/how-can-i-generate-all-possible-ips-from-a-list-of-ip-ranges-in-python
def ips(start, end) -> List:
    start = struct.unpack('>I', socket.inet_aton(start))[0]
    end = struct.unpack('>I', socket.inet_aton(end))[0]
    return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end)]


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        ret = []
        self.set_options(var_options=variables, direct=kwargs)
        

        for start in terms:
            display.debug("Start address %s" % start)

            end = self.get_option('end')
            display.debug("End address %s" % end)
            
            ret.append(ips(start, end))

        return ret