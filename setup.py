import cx_Freeze
executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name = "Connect 4",
    options = {"build_exe": {"packages":["pygame"],
                             "include_files":["assets/images/black.png", 
                                              "assets/images/red.png", "treelogic.py", "main.py", "assets/images/board.png", 
                                              "assets/images/empty.png", "assets/audio/click.mp3", "assets/audio/fall.mp3", "assets/audio/win.mp3",
                                              "assets/audio/over.mp3", "assets/audio/menu.mp3", "assets/audio/game.mp3"]}},
    executables = executables

)