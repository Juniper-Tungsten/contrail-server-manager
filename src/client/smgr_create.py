#!/usr/bin/python

# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
   Name : smgr_create.py
   Author : Abhay Joshi
   Description : This program is a simple cli interface to
   create server manager configuration objects.
   Objects can be vns, cluster, server, or image.
"""
import argparse
import pdb
import sys
import pycurl
from StringIO import StringIO
import json
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import ConfigParser
import smgr_client_def

# Below array of dictionary's is used by create_payload
# function to create payload when user choses to input
# object parameter values manually instead of providing a
# json file.
object_dict = {
    "vns" : OrderedDict ([
        ("vns_id", "Specify unique vns_id for this vns cluster"),
        ("email", "Email id for notifications"),
        ("vns_params", OrderedDict ([
             ("router_asn", "Router asn value"),
             ("mask", "Subnet mask"),
             ("gway", "Default gateway for servers in this cluster"),
             ("passwd", "Default password for servers in this cluster"),
             ("domain", "Default domain for servers in this cluster"),
             ("database_dir", "home directory for cassandra"),
             ("db_initial_token", "initial database token"),
             ("openstack_mgmt_ip", "openstack management ip"),
             ("use_certs", "whether to use certificates for auth (True/False)"),
             ("multi_tenancy", "Openstack multitenancy (True/False)"),
             ("service_token", "Service token for openstack access"),
             ("ks_user", "Keystone user name"),
             ("ks_passwd", "keystone password"),
             ("ks_tenant", "keystone tenant name"),
             ("openstack_passwd", "open stack password"),
             ("analytics_data_ttl", "analytics data TTL"),
             ("osd_bootstrap_key", "OSD Bootstrap Key"),
             ("admin_key", "Admin Authentication Key"),
             ("storage_mon_secret", "Storage Monitor Secret Key")]))
    ]),
    "server": OrderedDict ([ 
        ("server_id", "server id value"),
        ("ip", "server ip address"),
        ("mac", "server mac address"),
        ("roles", "comma-separated list of roles for this server"),
        ("server_params", OrderedDict([
            ("ifname", "Ethernet Interface name"),
            ("compute_non_mgmt_ip", "compute node non mgmt ip (default none)"),
            ("compute_non_mgmt_gway", "compute node non mgmt gway (default none)"),
            ("disks", "Storage OSDs")])),
        ("vns_id", "vns id the server belongs to"),
        ("cluster_id", "Physical cluster id the server belongs to"),
        ("pod_id", "pod id the server belongs to"),
        ("rack_id", "rack id the server belongs to"),
        ("cloud_id", "cloud id the server belongs to"),
        ("mask", "subnet mask (default use value from vns table)"),
        ("gway", "gateway (default use value from vns table)"),
        ("domain", "domain name (default use value from vns table)"),
        ("passwd", "root password (default use value from vns table)"),
        ("email", "email id for notifications (default use value from vns table)"),
    ]),
    "image" : OrderedDict ([
        ("image_id", "Specify unique image id for this image"),
        ("image_version", "Specify version for this image"),
        ("image_type", "ubuntu/centos/contrail-ubuntu-repo"),
        ("image_path", "complete path where image file is located on server")
    ]),
    "cluster" : OrderedDict ([
        ("cluster_id", "Specify unique cluster_id for this cluster"),
    ])
}

def parse_arguments(args_str=None):

    # Process the arguments
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            description='''Create a Server Manager object'''
        )
    else:
        parser = argparse.ArgumentParser(
            description='''Create a Server Manager object''',
            prog="server-manager create"
        )
    # end else
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("--ip_port", "-i",
                        help=("ip addr & port of server manager "
                              "<ip-addr>[:<port>] format, default port "
                              " 9001"))
    group1.add_argument("--config_file", "-c",
                        help=("Server manager client config file "
                              " (default - %s)" %(
                              smgr_client_def._DEF_SMGR_CFG_FILE)))
    subparsers = parser.add_subparsers(title='objects',
                                       description='valid objects',
                                       help='help for objects',
                                       dest='object')

    # Subparser for server create
    parser_server = subparsers.add_parser(
        "server",help='Create server')
    parser_server.add_argument(
        "--file_name", "-f",
        help="json file containing server param values")

    # Subparser for vns create
    parser_vns = subparsers.add_parser(
        "vns", help='Create vns')
    parser_vns.add_argument(
        "--file_name", "-f",
        help="json file containing vns param values")

    # Subparser for cluster create
    parser_cluster = subparsers.add_parser(
        "cluster", help='Create cluster')
    parser_cluster.add_argument(
        "--file_name", "-f",
        help="json file containing cluster param values")

    # Subparser for image create
    parser_image = subparsers.add_parser(
        "image", help='Create image')
    parser_image.add_argument(
        "--file_name", "-f",
        help="json file containing image param values")

    args = parser.parse_args(args_str)
    return args
# end def parse_arguments

def send_REST_request(ip, port, object, payload):
    try:
        response = StringIO()
        headers = ["Content-Type:application/json"]
        url = "http://%s:%s/%s" %(
            ip, port, object)
        conn = pycurl.Curl()
        conn.setopt(pycurl.URL, url)
        conn.setopt(pycurl.HTTPHEADER, headers)
        conn.setopt(pycurl.POST, 1)
        conn.setopt(pycurl.POSTFIELDS, '%s'%json.dumps(payload))
        conn.setopt(pycurl.CUSTOMREQUEST, "PUT")
        conn.setopt(pycurl.WRITEFUNCTION, response.write)
        conn.perform()
        return response.getvalue()
    except:
        return None

# Function to accept parameters from user and then build payload to be
# sent with REST API request for creating the object.
def create_payload(object):
    payload = {}
    objects = []
    while True:
        temp_dict = {}
        fields_dict = object_dict[object]
        for key in fields_dict:
            value = fields_dict[key]
            if (key != (object+"_params")):
                msg = key
                if value:
                    msg += " (%s) " %(value)
                msg += ": "
                user_input = raw_input(msg)
                if user_input:
                    # Special case for roles -
                    # store as a list
                    if key == "roles":
                        temp_dict[key] = user_input.strip().split(",")
                    else:
                        temp_dict[key] = user_input
            else:
                param_dict = {}
                for param in value:
                    pvalue = value[param]
                    msg = param
                    if pvalue:
                        msg += " (%s) " %(pvalue)
                    msg += ": "
                    user_input = ""
                    if param == 'disks' and 'storage-compute' in temp_dict["roles"]:
                        disks = raw_input(msg)
                        if disks:
                            disk_list = disks.split(',')
                            user_input = [str(d) for d in disk_list]
                    else:
                        user_input = raw_input(msg)
                    if user_input:
                        param_dict[param] = user_input
                temp_dict[key] = param_dict
            # End if (key != (object+"_params"))
        # End for key, value in fields_dict 
        objects.append(temp_dict)
        choice = raw_input("More %s(s) to input? (y/N)" %(object))
        if ((not choice) or
            (choice.lower() != "y")):
            break
    # End while True
    payload[object] = objects
    return payload
# End create_payload

def create_config(args_str=None):
    args = parse_arguments(args_str)
    if args.ip_port:
        smgr_ip, smgr_port = args.ip_port.split(":")
        if not smgr_port:
            smgr_port = smgr_client_def._DEF_SMGR_PORT
    else:
        if args.config_file:
            config_file = args.config_file
        else:
            config_file = smgr_client_def._DEF_SMGR_CFG_FILE
        # end args.config_file
        try:
            config = ConfigParser.SafeConfigParser()
            config.read([config_file])
            smgr_config = dict(config.items("SERVER-MANAGER"))
            smgr_ip = smgr_config.get("listen_ip_addr", None)
            if not smgr_ip:
                sys.exit(("listen_ip_addr missing in config file"
                          "%s" %config_file))
            smgr_port = smgr_config.get("listen_port", smgr_client_def._DEF_SMGR_PORT)
        except:
            sys.exit("Error reading config file %s" %config_file)
        # end except
    # end else args.ip_port
    object = args.object
    if args.file_name:
        payload = json.load(open(args.file_name))
    else:
        # Accept parameters and construct json.
        payload = create_payload(object)

    resp = send_REST_request(smgr_ip, smgr_port,
                      object, payload)
    print resp
# End of create_config

if __name__ == "__main__":
    import cgitb
    cgitb.enable(format='text')

    create_config(sys.argv[1:])
# End if __name__