#!/usr/bin/env python3
import json
import logging, logging.handlers
import argparse

logging.basicConfig(format='%(asctime)s %(levelname)7s %(module)s:%(funcName)s -> %(message)s', level=logging.DEBUG)
logging.debug("Starting up")

# this is for our worker thread pool

parser = argparse.ArgumentParser()

parser.add_argument('-u', required=True, dest='username', help='IDCS Username')
parser.add_argument('-uid', required=True, type=int, dest='posix_uid', help='POSIX UID for user')
parser.add_argument('-gid', required=True, type=int, dest='posix_gid', help='POSIX GID for user')

cmd = parser.parse_args()
from IAMClient import IAMClient
idcs = IAMClient()

userid = idcs.getUserId( cmd.username )

payload = \
    {
      "schemas": [
        "urn:ietf:params:scim:api:messages:2.0:PatchOp"
      ],
      "Operations": [
        {
          "op": "add",
          "path": "urn:ietf:params:scim:schemas:oracle:idcs:extension:posix:User:homeDirectory",
          "value": "/home/" + cmd.username
        },
        {
          "op": "add",
          "path": "urn:ietf:params:scim:schemas:oracle:idcs:extension:posix:User:gecos",
          "value": "gecos 1234"
        },
        {
          "op": "add",
          "path": "urn:ietf:params:scim:schemas:oracle:idcs:extension:posix:User:uidNumber",
          "value": cmd.posix_uid
        },
        {
          "op": "add",
          "path": "urn:ietf:params:scim:schemas:oracle:idcs:extension:posix:User:gidNumber",
          "value": cmd.posix_gid
        },
        {
          "op": "add",
          "path": "urn:ietf:params:scim:schemas:oracle:idcs:extension:posix:User:loginShell",
          "value": "/bin/bash"
        }
      ]
    }

logging.debug("jSON payload is:")
logging.debug( json.dumps( payload, indent=4))

idcs._sendRequest( "PATCH", "/admin/v1/Users/" + userid, payload)
