<<lookup-header>>

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        paramvals = self.get_options()
        cmd = '/usr/local/etc/ansible/facts.d/pot.fact'
        potfact = <<py_shell()>>
        potfact = json.loads(potfact.stdout)
        potname = paramvals['pot']

        if 'active' in paramvals:
            return potfact['jails'][potname]['active']

        attr = paramvals['attribute']
        return potfact['jails'][potname]['config'][attr]
