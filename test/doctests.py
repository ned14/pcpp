        import doctest
        failurecount, testcount = doctest.testmod()
        if failurecount > 0:
            sys.exit(1)
