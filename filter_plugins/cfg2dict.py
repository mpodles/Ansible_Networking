import re

class FilterModule(object):
    def filters(self):
        return {'cfg2dict': self.cfg2dict}
    
    def cfg2dict(self,text):
        cfg_list = text.split("\n")
        result_dict= {}
        for line in cfg_list:
            var,value = re.split(": *",line)
            result_dict[var] = value
        return result_dict