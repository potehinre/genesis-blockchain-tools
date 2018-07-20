try:
    import rubenesque
    run_main_part = True
except ImportError as e:
    run_main_part = False

if run_main_part:
    def test_dummy():
        pass
else:
    print("rubenesque backend skipped")
