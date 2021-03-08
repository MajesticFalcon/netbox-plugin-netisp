from extras.plugins import PluginConfig


class NetISP(PluginConfig):
    name = "netbox_netisp"
    verbose_name = "net isp"
    description = "Manages isp connections"
    version = "0.1"
    author = "sutley"
    author_email = "sutley5.com"
    base_url = ""
    required_settings = []
    default_settings = {}


config = NetISP
