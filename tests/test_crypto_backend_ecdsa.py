try:
    import ecdsa
    run_main_part = True
except ImportError as e:
    run_main_part = False

if run_main_part:
    pass
else:
    print("cryptography backend skipped")
