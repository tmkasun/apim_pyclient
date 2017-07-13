class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val

    __delattr__ = dict.__delitem__


def main():
    endpoint_const = {
        'SECURITY_TYPES': {'BASIC': "basic", 'DIGEST': 'digest'},
        'TYPES': {
            'PRODUCTION': "production",
            'SANDBOX': "sandbox",
            'INLINE': "inline",
        }
    }
    CONST = DotDict(endpoint_const)
    CONST.TYPES = "sadsadsa"
    print(CONST.TYPES)


if __name__ == '__main__':
    main()
