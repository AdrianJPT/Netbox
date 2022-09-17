from pyzabbix import ZabbixAPI

ZABBIX_SERVER = "http://15.228.201.253/zabbix/api_jsonrpc.php"

zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login("Admin", "zabbix")

zabbix_url = 'http://15.228.201.253/zabbix/api_jsonrpc.php'
zabbix_token = '64acb78476350f099de1ea79800e2901ffb5a267f7aef5ac3e7c4d1af167e42a'




def zab_patch_HostGroups(nb_device_name, nb_site_name):
    try:

        zb_hostgroup = zapi.hostgroup.get(output=["groupid", "name"], filter={"name": nb_site_name})

        zb_host_get_1  = zapi.host.get(output=["hostid", "name", "interfaces"], filter={"name": nb_device_name}, selectInterfaces=["interfaceid", "ip", "dns"], selectGroups=["groupid"], selectParentTemplates = ["templateid"])

        zab_hostgroup_id = zb_hostgroup[0]['groupid']

        gid = str(zab_hostgroup_id)

        zb_host_id = zb_host_get_1[0]['hostid']
        json_list = zb_host_get_1[0]['groups']

        variable = {'groupid': gid} in json_list
        #print(variable)

        if variable == True:
            print("Se encontro, no se hara nada")
        else:
            aditional = [{"groupid" : f'{zab_hostgroup_id}'}]
            json_list += aditional
            #print(json_list)

            print("No encontro, UPDATEEEE")
            zapi.host.update(hostid = zb_host_id,
                groups = json_list)

            
    except Exception as e:
        print(f'{e}')
        print(f"ZABBIX | ERROR | Hostgroup and Site ({nb_site_name}) DON'T MATCH")

def zab_patch_Template(zab_host_get, platform_name, NB_DEVICE):
    try: #MATCH PLATFORM Y TEMPLATE

        zab_host_get = zapi.host.get(output=["hostid", "name", "interfaces","template"], filter={"name": NB_DEVICE}, selectInterfaces=["interfaceid", "ip", "dns"], selectGroups=["groupid"], selectParentTemplates = ["templateid"])
        host_id = zab_host_get[0]['hostid']
        zab_template_get = zapi.template.get(output=["name", "templateid"], filter={"name": platform_name})

#        print(zab_host_get)
#        print("")
#        print(zab_template_get)

        platform_template_id = zab_template_get[0]['templateid']

        t_id = str(platform_template_id)
        array_list = zab_host_get[0]['parentTemplates']

        variable = {'templateid': t_id} in array_list    
        
        if variable == True:
            print(f'ZABBIX | WARNING | Template ({platform_name}) already exists')

        else: 
            aditional = [{'templateid': f'{platform_template_id}'}]
            array_list += aditional
            #print(array_list)
            zapi.host.update(hostid = host_id,
            templates = array_list
                )
            print(f"ZABBIX | SUCCESS | template ({platform_name}) updated ")

    except: 
        print(f"ZABBIX | ERROR | PLATFORM ({platform_name}) DONT MATCH with ZABBIX TEMPLATE")
