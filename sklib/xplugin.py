# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

import imp  
import os  
from .config import getPaths,Prefs


class PluginAdapter():
    """
    Class implementing the Plugin Manager.
    """
    
    __instance =  None
    @staticmethod
    def new():
        """
        static instance method .
        """
        if not PluginAdapter.__instance:
            PluginAdapter.__instance = PluginAdapter()
        return PluginAdapter.__instance
    
    
    __plugins = []
    
    def getPlugins(self):
        return self.__plugins
    
    def __init__(self,pluginpath="plugins"):
        """
        init the pluginHelper
        """
        #sys.path.append(os.path.join(os.path.dirname(sys.argv[0]),pluginpath))
        
        for directory in getPaths("pluginsDir",""):
            # read plugins from core,ext,.seeking dir

            module_names = list(split_pair[0]  for split_pair  \
                               in map(self.__validPluginName,os.listdir(directory)) \
                               if split_pair is not None)
            module_names.sort()
            # load modules
            for module_name in module_names:
                #just find 
                rv = imp.find_module(module_name,[directory])  
                #really load
                
                if rv is not None:
                    try:
                        mod = imp.load_module(module_name,*rv)
                        #avoid muti load
                        if not mod.name in set(mod.name for mod in self.__plugins):
                            if  hasattr(mod,"activate") \
                            and hasattr(mod,"deactivate")\
                            and hasattr(mod,"author") \
                            and hasattr(mod,"version")\
                            and hasattr(mod,"packageName"):
                                self.__plugins.append(mod)
                    except  Exception as e:
                        raise e
                        print ('loadd error :  %s' % str(e))
                        
        
            
    def __validPluginName(self,name):
        """
        Public methode to check, if a file name is a valid plugin name.
        """
        suffix=".py"
        if name.endswith(suffix) and name.startswith("plugin"):
            return (name[:-len(suffix)],suffix)  
        return None
    def getPluginByName(self,name):
        """
        get the plugin by name
        """
        for mod in self.__plugins:
            if mod.__name__== name:
                return mod
        return None
    
    def readInfos(self):
        """
        Read module infos
        """
        rs = []
        for mod in self.__plugins:
            rs.append([mod.__name__,mod.name,mod.author,mod.version,\
                       Prefs.new().getPluginState(mod.__name__).toBool(),mod.description])
        return rs
    def finalizeActivate(self):
        for module in self.__plugins:
            if hasattr(module, "activate"):
                if Prefs.new().getPluginState(module.__name__).toBool():
                    module.activate()
                
