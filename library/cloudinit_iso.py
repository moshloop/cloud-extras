#!/usr/bin/python
DOCUMENTATION = '''
module: cloudinit_iso
author:
    - "Moshe Immerman"
short_description:  Creates an ISO image containing cloud-init user-data files
description:
    -  Creates systemd services
options:
    dest:
        required: True
        description: ['']
    content:
        required: True
        description: ['']
'''
EXAMPLES = '''
     - cloudinit_iso:
          dest: /tmp/cloudinit.iso
          content: |
            "
'''
import os.path
from subprocess import check_call
from ansible.module_utils.basic import AnsibleModule
import logging

logger = logging.getLogger('cloudinit-iso')
hdlr = logging.FileHandler('/tmp/ansible-cloudinit-iso.log')
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


import os
from tempfile import gettempdir


def main():
    arg_spec = dict(
        dest=dict(required=True),
        content=dict(required=True)
    )
    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=False
    )

    tmp = os.path.join(gettempdir(), '{}'.format(hash(os.times())))
    logger.info("Writing temp user-data.txt: " + tmp)


    os.makedirs(tmp)

    with open(tmp + "/user-data", 'w') as f:
        f.write(module.params['content'])
    with open(tmp + "/meta-data", "w") as f:
        f.write('instance-id: iid-123456')
        f.write('local-hostname: cloudy')

    check_call("genisoimage -output %s -volid cidata -joliet -rock user-data meta-data" % module.params['dest'], shell=True,cwd=tmp)

    module.exit_json(changed=True)


if __name__ == '__main__':
    main()