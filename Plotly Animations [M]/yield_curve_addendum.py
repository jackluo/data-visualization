updatemenus = dict(

    # GENERAL
    type = "buttons",
    showactive = False,
    x = 0.1, #x = 1.1
    y = 0, #y = 1
    active = 99,
    bgcolor = "#000000",
    pad = dict(t = 60, r = 10),
    xanchor = "right",
    yanchor = "top",
    direction = "left",

    # BUTTONS
    buttons=[
        dict(
            method = "relayout",
            label = "Slide 1",

            # ARGUMENTS
            args = [
                dict(
                    scene.camera.eye.x = 10,
                    scene.camera.eye.y = 10,
                ),
            ],
        ),
        dict(
            method = "relayout",
            label = "Slide 3",

            # ARGUMENTS
            args = [
                dict(
                    scene.camera.eye.x = 100,
                    scene.camera.eye.y = 100,
                ),
            ],
        ),
    ],

)
