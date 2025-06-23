from rpggen import main

def test_main_output(capsys):
    main()
    captured = capsys.readouterr()
    assert "placeholder" in captured.out
