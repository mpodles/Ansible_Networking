import re

class FilterModule(object):
    def filters(self):
        return {'cfg2dict': self.cfg2dict,'vlan_to_vni_parser': self.vlan_to_vni_parser}
    
    def cfg2dict(self,text):
        cfg_list = text.split("\n")
        result_dict= {}
        for line in cfg_list:
            var,value = re.split(": *",line)
            result_dict[var] = value
        return result_dict
    
    def vlan_to_vni_parser(self, vlan_list):
        vni_result_list = []
        rt_result_list = []
        for vlan in vlan_list:
            result_vlan = {}
            vlan_id =  vlan.pop('vlan')
            result_vlan['vlan_id'] = vlan_id
            vni = vlan.pop('vni', result_vlan['vlan_id'])
            result_vlan['mapped_vni'] = vni
            result_vlan['enabled'] = 'yes'
            
            vni_result_list.append(result_vlan)

            
            if 'rd' not in vlan:
                rd = 'auto'
            else:
                rd = vlan['rd']

            print(vlan)
            if 'route_targets' not in vlan:
                print("wszedlem")
                result_vlan_rt = {} 
                result_vlan_rt['route_distinguisher'] = rd
                result_vlan_rt['vni'] = vni
                
                result_vlan_rt['route_target_export'] = 'auto'
                result_vlan_rt['route_target_import'] = 'auto'
                rt_result_list.append(result_vlan_rt)
            else:
                for route_target_entry in vlan['route_targets']:
                    rt_result_list.append(self.create_rt_entry(route_target_entry, rd , vni))
        return [vni_result_list, rt_result_list]

    def create_rt_entry(self, route_target_entry, rd, vni):
        result_vlan_rt = {}
        result_vlan_rt['route_distinguisher'] = rd
        result_vlan_rt['vni'] = vni 
        print(route_target_entry)                  
        if 'direction' not in route_target_entry or \
            route_target_entry['direction'] == 'both':
            result_vlan_rt['route_target_export'] = route_target_entry['rt']
            result_vlan_rt['route_target_import'] = route_target_entry['rt']
        elif route_target_entry['direction'] == 'export':
            result_vlan_rt['route_target_export'] = route_target_entry['rt']
        elif route_target_entry['direction'] == 'import':
            result_vlan_rt['route_target_import'] = route_target_entry['rt']
        if 'route_target_export' not in result_vlan_rt:
            result_vlan_rt['route_target_export'] = 'auto'
        if 'route_target_import' not in result_vlan_rt:
            result_vlan_rt['route_target_import'] = 'auto'
        return result_vlan_rt

