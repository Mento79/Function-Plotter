from Main import MyApp, validate_function, validate_limits


def test_add_function(qtbot):
    app = MyApp()
    qtbot.addWidget(app)
    app.button_add[0].click()

    assert len(app.input_function) == 2
    assert len(app.color_label) == 2
    assert len(app.input_start) == 2
    assert len(app.input_end) == 2
    assert len(app.button_add) == 2
    assert len(app.button_remove) == 2
    assert len(app.spacing) == 2


def test_remove_function(qtbot):
    app = MyApp()
    qtbot.addWidget(app)
    app.button_add[0].click()
    app.button_remove[1].click()

    assert len(app.input_function) == 1
    assert len(app.color_label) == 1
    assert len(app.input_start) == 1
    assert len(app.input_end) == 1
    assert len(app.button_add) == 1
    assert len(app.button_remove) == 1
    assert len(app.spacing) == 1


def test_points_maker(qtbot):
    start = 1
    end = 2
    function = 'x'
    index = 0
    app = MyApp()
    qtbot.addWidget(app)
    x, y = app.points_maker(start, end, function, index)

    assert x == [1.000, 1.100, 1.200, 1.300, 1.400, 1.500, 1.600, 1.700, 1.800, 1.900, 2.000]
    assert y == [1.000, 1.100, 1.200, 1.300, 1.400, 1.500, 1.600, 1.700, 1.800, 1.900, 2.000]


def test_validate_no_start(qtbot):
    start = ''
    end = '2'
    function = 'x'
    index = 0
    app = MyApp()
    qtbot.addWidget(app)
    result = app.validate(start, end, function, index, False)

    assert result == False


def test_validate_no_end(qtbot):
    start = '2'
    end = ''
    function = 'x'
    index = 0
    app = MyApp()
    qtbot.addWidget(app)
    result = app.validate(start, end, function, index, False)

    assert result == False


def test_validate_start_more_than_end(qtbot):
    start = '5'
    end = '2'
    function = 'x'
    index = 0
    app = MyApp()
    qtbot.addWidget(app)
    result = app.validate(start, end, function, index, False)

    assert result == False


def test_validate_start_not_a_number(qtbot):
    start = 's'
    end = '2'
    function = 'x'
    index = 0
    app = MyApp()
    qtbot.addWidget(app)
    result = app.validate(start, end, function, index, False)

    assert result == False


def test_validate_end_not_a_number(qtbot):
    start = '2'
    end = 's'
    function = 'x'
    index = 0
    app = MyApp()
    qtbot.addWidget(app)
    result = app.validate(start, end, function, index, False)

    assert result == False


def test_validate_not_valid_function(qtbot):
    start = '2'
    end = '5'
    function = 'x++'
    index = 0
    app = MyApp()
    qtbot.addWidget(app)
    result = app.validate(start, end, function, index, False)

    assert result == False


def test_validate_valid_function(qtbot):
    start = '2'
    end = '5'
    function = 'x+2'
    index = 0
    app = MyApp()
    qtbot.addWidget(app)
    result = app.validate(start, end, function, index, False)

    assert result


def test_plot_axes(qtbot):
    app = MyApp()
    qtbot.addWidget(app)
    app.plot_axes()
    assert app.axes


def test_validate_function_not_valid():
    inp='x++'
    assert validate_function(inp)==False

def test_validate_function_valid():
    inp='x+2'
    assert validate_function(inp)


def test_validate_limits_not_valid():
    inp='2x'
    assert validate_limits(inp)==False

def test_validate_limits_valid():
    inp='-2'
    assert validate_limits(inp)
